# -*- coding: utf-8 -*-

""""
    Copyright (C) 2022 ESOL LABS - All Rights Reserved.

    You may use, distribute and modify this code under the
    terms of the XYZ license, which unfortunately won't be
    written for another century.

    You should have received a copy of the XYZ license with
    this file. If not, please write to: , or visit :
"""

# File: campaign.py
# Created at May 17th, 2022
# Author: taipa
from pydash import get

"""
   Description:
        -
        -
"""
import json
from src.models.campaign import CampaignModel
from src.models.nft_supply import SupplyNFTModel
from src.models.user import UserModel
from src.exceptions.campaign import ExCampaign
from src.constants import AppConstants
from src.enums.campaign import CampaignGetList
from src.helpers.campaign import check_campaign_subdomain_valid, delete_subdomain
import src.workers.campaign as campaign_worker
from bson import ObjectId
from lib.logger import Logger
from datetime import datetime, timezone
from lib.util import dt_utcnow
from src.constants import AppConstants


class CampaignService(object):

    @classmethod
    def create_campaign(cls, campaign_dict):
        _list_nft = campaign_dict['nft_list']

        if campaign_dict["random_nft"]:

            _sum_percent = sum([nft['percent'] if 'percent' in nft else 0 for nft in _list_nft])

            if _sum_percent != 100:
                raise ExCampaign('Invalid Nft List: total percent not valid !')
        else:
            _sum_supply = sum([nft['supply'] for nft in _list_nft])
            _sum_raise = sum([nft['supply'] * nft['price'] for nft in _list_nft])

            if _sum_supply != campaign_dict['total_supply']:
                raise ExCampaign('Invalid Nft List: total supply not valid !')

            if _sum_raise != campaign_dict["total_raise"]:
                raise ExCampaign('Invalid Nft List: total raise not valid !')

        if campaign_dict['campaign_method'] not in AppConstants.CampaignMethodList:
            raise ExCampaign('Invalid campaign method !')

        # Check if subdomain
        _check_domain_status_code, _check_subdomain_resp = check_campaign_subdomain_valid(
            campaign_dict['website_domain'])

        if _check_domain_status_code != 200:
            raise ExCampaign(f"Submitted subdomain error: {_check_subdomain_resp['msg']}")

        if _check_domain_status_code == 200 and not _check_subdomain_resp['data']['result']:
            raise ExCampaign(f"Submitted subdomain is invalid ! Already existed !")

        Logger.debug("*** Campaign dict : ", campaign_dict)
        Logger.debug("*** Campaign dict - nft list: ", _list_nft)

        campaign_dict["nft_list"] = [{**x, 'index_type': idx + 1} for idx, x in enumerate(_list_nft)]

        Logger.debug("Campaign dict have index_type 2: ", campaign_dict)

        CampaignModel.insert(campaign_dict)

        return campaign_dict['name'], campaign_dict['is_released']

    @classmethod
    def edit_non_release_campaign(cls, user_id, campaign_id, edit_infos):

        _campaign = CampaignModel.get_item(oid=campaign_id)
        # if 'nft_list' in edit_infos:
        _list_nft = edit_infos['nft_list']

        if _campaign["deleted"]:
            raise ExCampaign("This campaign's already been deleted !")

        if edit_infos["random_nft"]:
            _sum_percent = sum([nft['percent'] for nft in _list_nft])
            if _sum_percent != 100:
                raise ExCampaign('Invalid Nft List: total percent not valid !')
        else:
            _sum_supply = sum([nft['supply'] for nft in _list_nft])
            _sum_raise = sum([nft['supply'] * nft['price'] for nft in _list_nft])
            print('sum raise = ', _sum_raise)
            if _sum_supply != edit_infos['total_supply']:
                raise ExCampaign('Invalid Nft List: total supply not valid !')
            if _sum_raise != edit_infos["total_raise"]:
                raise ExCampaign('Invalid Nft List: total raise not valid !')

        if _campaign['user'] != user_id:
            raise ExCampaign("Not have permission to update this campaign !")

        if _campaign['is_released']:
            raise ExCampaign("This campaign's already released !")

        if 'nft_list' in edit_infos:
            edit_infos["nft_list"] = [{**x, 'index_type': get(x, 'index_type', idx + 1)} for idx, x in
                                      enumerate(edit_infos['nft_list'])]

        CampaignModel.update_one(
            filter={
                "_id": ObjectId(campaign_id)
            },
            obj=edit_infos
        )

        return campaign_id, 'success'

    @classmethod
    def edit_release_campaign(cls, user_id, campaign_id, edit_infos):

        _campaign = CampaignModel.get_item(oid=campaign_id)

        if _campaign['user'] != user_id:
            raise ExCampaign("Not have permission to update this campaign !")

        if not _campaign['is_released']:
            raise ExCampaign("This campaign's not a released one !")
        if 'nft_list' in edit_infos:
            edit_infos["nft_list"] = [{**x, 'index_type': get(x, 'index_type', idx + 1)} for idx, x in
                                      enumerate(edit_infos['nft_list'])]

        CampaignModel.update_one(
            filter={
                "_id": ObjectId(campaign_id)
            },
            obj=edit_infos
        )

        return campaign_id, 'success'

    @classmethod
    def get_list_campaigns(cls, _user_id, page=CampaignGetList.DEFAULT_PAGE,
                           page_size=CampaignGetList.DEFAULT_PAGE_SIZE):
        _filter = {
            "user": _user_id,
            "deleted": False
        }

        _total = CampaignModel.get_count(
            filter=_filter
        )
        _campaigns = CampaignModel.get_list(
            filter=_filter,
            page=page,
            page_size=page_size
        )
        return _total, page, _campaigns

    @classmethod
    def release_campaign(cls, campaign_id, user_id):
        _campaign = CampaignModel.get_item(oid=campaign_id)

        if _campaign['is_released']:
            raise ExCampaign("This campaign 's already released !")

        if _campaign['user'] != user_id:
            raise ExCampaign("Not have permissions to release this campaign !")

        if _campaign["deleted"]:
            raise ExCampaign("This campaign's already been deleted !")
        #    Create subdomain for campaign
        #       @params: subdomain need to be created
        #       @return: result of creation: True or False and created subdomain 

        _creation_result, _msg = campaign_worker.create_domain(
            campaign_id=campaign_id,
            subdomain=_campaign["website_domain"]
        )
        print("*** Subdomain Creation Result : ", _creation_result)

        if _creation_result:
            #       Call to CampaignFactory to deploy new campaign contract
            #       params: infors of campaigns
            #       return: created campaign contract's address
            print('_campaign_dict : ', _campaign, type(_campaign))
            print('_campaign_id : ', campaign_id, type(campaign_id))

            for _key, _value in _campaign.items():
                if isinstance(_value, ObjectId):
                    _campaign[_key] = str(_value)
                if isinstance(_value, datetime):
                    _campaign[_key] = _value.replace(tzinfo=timezone.utc).timestamp()

            print('_campaign_dict after encode: ', _campaign, type(_campaign))

            campaign_worker.create_campaign_smc.delay(
                _campaign_dict=dict(_campaign),
                _campaign_id=campaign_id
            )

        return campaign_id, _creation_result, _msg

    @classmethod
    def delete_campaign(cls, campaign_id, user_id):

        _campaign = CampaignModel.get_item(oid=campaign_id)

        if not _campaign:
            raise ExCampaign("Campaign's not exist !")

        if _campaign["deleted"]:
            raise ExCampaign("This campaign's already been deleted !")

        if _campaign["user"] != user_id:
            raise ExCampaign("Not have permissions to delete this campaign !")

        delete_subdomain(subdomain=_campaign["website_domain"])

        CampaignModel.update_one(
            filter={
                "_id": ObjectId(campaign_id)
            },
            obj={
                "deleted": True,
                "deleted_time": dt_utcnow()
            }
        )
        return True

    @classmethod
    def get_campaign_details_by_subdomain(cls, subdomain):
        # hard code for client build UI

        _campaign = CampaignModel.get_item_with(filter={
            "website_domain": subdomain,
            "deleted": False
        })

        if _campaign["is_released"]:
            _supplies = SupplyNFTModel.get_list(
                filter={
                    "contract": _campaign["contract"]
                }
            )

            _current_sells = [{
                "index_type": _s["type"],
                "current_sell": _s["total_supply"]
            } for _s in _supplies]

            if not _current_sells:
                return _campaign

            _nft_list = []
            for x in _campaign["nft_list"]:
                is_match = False
                for y in _current_sells:
                    if x['index_type'] == y['index_type']:
                        is_match = True
                        _nft_list.append({**x, **y})
                if not is_match:
                    _nft_list.append({**x, "current_sell": 0})

            _campaign["nft_list"] = _nft_list

            print('nft_list : ', [_c["current_sell"] or 0 for _c in _campaign["nft_list"]])

            _campaign["current_sell"] = sum([_c["current_sell"] for _c in _nft_list])

        return _campaign

    @classmethod
    def get_campaign_details_by_id(cls, campaign_id):
        _campaign = CampaignModel.get_item(oid=campaign_id)

        if _campaign:
            _user = UserModel.get_item(oid=_campaign["user"])
            del _campaign["user"]
            _campaign = {
                **_campaign,
                "user_infos": {
                    "username": _user["username"],
                    "avatar": _user["avatar"],
                    "public_address": _user["public_address"]
                }
            }
        return _campaign

    @classmethod
    def get_nft_type_details(cls, contract_address, index_type):
        _campaign = CampaignModel.get_item_with(filter={
            "contract": contract_address
        })

        _user = UserModel.get_item(oid=_campaign["user"])

        del _campaign["user"]

        _nft_infos = [_nft for _nft in _campaign["nft_list"] if _nft["index_type"] == index_type][0]

        _resp = {
            **_campaign,
            "user_infos": {
                "username": _user["username"],
                "avatar": _user["avatar"],
                "public_address": _user["public_address"]
            },
            "nft_infos": _nft_infos
        }

        return _resp

    @classmethod
    def get_hot_campaigns(cls, category, page=CampaignGetList.DEFAULT_HOT_PAGE,
                          page_size=CampaignGetList.DEFAULT_HOT_PAGE_SIZE):

        if category not in AppConstants.HotCampaignCategories:
            raise ExCampaign("Invalid category of hot campaign !")

        _filter = [
            {
                "is_hot": True,
                "deleted": False,
            }, {
                "is_hot": True,
                "deleted": False,
                "start_time": {
                    "$gt": datetime.now()
                }
            }, {
                "is_hot": True,
                "deleted": False,
                "start_time": {
                    "$lt": datetime.now()
                },
                "end_time": {
                    "$gt": datetime.now()
                }
            }, {
                "is_hot": True,
                "deleted": False,
                "end_time": {
                    "$lt": datetime.now()
                }
            }
        ]

        _campaigns = CampaignModel.get_list(
            filter=_filter[AppConstants.HotCampaignCategories.index(category)],
            page_size=page_size,
            page=page
        )

        return {
            "campaigns": _campaigns
        }

