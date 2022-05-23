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

"""
   Description:
        -
        -
"""

from src.models.campaign import CampaignModel
from src.exceptions.campaign import ExCampaign
from src.constants import AppConstants
from src.enums.campaign import CampaignGetList
from src.helpers.campaign import check_campaign_subdomain_valid
import src.workers.campaign as campaign_worker
from bson import ObjectId


class CampaignService(object):

    @classmethod
    def create_campaign(cls, campaign_dict):
        _list_nft = campaign_dict['nft_list']
        
        if campaign_dict["random_nft"]:
            _sum_percent = sum([nft['percent'] for nft in _list_nft])
            if _sum_percent != 100:
                raise ExCampaign('Invalid Nft List: total percent not valid !')
        else:
            _sum_supply = sum([nft['supply'] for nft in _list_nft])  
            if _sum_supply != campaign_dict['total_supply']:
                raise ExCampaign('Invalid Nft List: total suplly not valid !')

        if campaign_dict['campaign_method'] not in AppConstants.CampaignMethodList:
            raise ExCampaign('Invalid campaign method !')

        _check_domain_status_code, _check_subdomain_resp = check_campaign_subdomain_valid(campaign_dict['website_domain'])
        if _check_domain_status_code != 200:
            raise ExCampaign(f"Submitted subdomain error: {_check_subdomain_resp['msg']}")
        
        if _check_domain_status_code == 200 and not _check_subdomain_resp['data']['result']:
            raise ExCampaign(f"Submitted subdomain is invalid ! Already existed !")
        
        if not campaign_dict["random_nft"]:
            _typeIndex = 1
            for _nft in campaign_dict["nft_list"]:
                _nft["index_type"] = _typeIndex
                _typeIndex += 1
        
        CampaignModel.insert(campaign_dict)

        return campaign_dict['name'], campaign_dict['is_released']

    @classmethod
    def edit_non_release_campaign(cls, user_id, campaign_id, edit_infos):
        
        _campaign = CampaignModel.get_item(oid=campaign_id)
        
        if _campaign['user'] != user_id:
            raise ExCampaign("Not have permission to update this campaign !")

        if _campaign['is_released']:
            raise ExCampaign("This campaign's already released !")

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

        CampaignModel.update_one(
            filter={
                "_id": ObjectId(campaign_id)
            },
            obj=edit_infos
        )

        return campaign_id, 'success'

    @classmethod
    def get_list_campaigns(cls, _user_id, page=CampaignGetList.DEFAULT_PAGE, page_size=CampaignGetList.DEFAULT_PAGE_SIZE):
        _filter = {
            "user": _user_id
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
        
        #    Create subdomain for campaign
        #       @params: subdomain need to be created
        #       @return: result of creation: True or False and created subdomain 

        _creation_result = campaign_worker.create_domain(
            campaign_id=campaign_id,
            subdomain=_campaign["website_domain"]
        )
        print("*** Subdomain Creation Result : ", _creation_result)

        #       Update released status in db record
        #       @params: None
        #       @return: update field: "is_released": True
        if _creation_result:
            CampaignModel.update_one(
                filter={
                    "_id": ObjectId(campaign_id)
                },
                obj={
                    "is_released": True
                }
            )

            #       Call to CampaignFactory to deploy new campaign contract
            #       params: infors of campaigns
            #       return: created campaign contract's address
            # _campaign_address =

            return campaign_id, True

        return campaign_id, False

    @classmethod
    def get_campaign_details_by_subdomain(cls, subdomain):
        # hard code for client build UI
        # return CampaignModel.get_item(oid="6285fc1a8e445aaef2c2d7ec")
        return CampaignModel.get_item_with(filter={
            "website_domain": subdomain
        })
