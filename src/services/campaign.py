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
from src.api import campaign
from src.models.campaign import CampaignModel
from src.exceptions.campaign import ExCampaign
from src.constants import AppConstants
from src.enums.campaign import CampaignGetList



class CampaignService(object):

    @classmethod
    def create_campaign(cls, campaign_dict):
        _list_nft = campaign_dict['nft_list']
        
        _sum_percent = sum([nft['percent'] for nft in _list_nft])
        _sum_supply = sum([nft['supply'] for nft in _list_nft])
        
        if _sum_percent != 100:
            raise ExCampaign('Invalid Nft List: total percent not valid !')
        
        if _sum_supply != campaign_dict['total_supply']:
            raise ExCampaign('Invalid Nft List: total suplly not valid !')

        if campaign_dict['campaign_method'] not in AppConstants.CampaignMethodList:
            raise ExCampaign('Invalid campaign method !')

        CampaignModel.insert(campaign_dict)

        return campaign_dict['name'], campaign_dict['is_released']

    
    @classmethod
    def edit_non_release_campaign(cls, user_id, campaign_id, edit_infos):
        
        _campaign = CampaignModel.get_item(oid=campaign_id).to_dict()
        
        if _campaign['user'] != user_id:
            raise ExCampaign("Not have permission to update this campaign !")

        if _campaign['is_released']:
            raise ExCampaign("This campaign's already released !")

        CampaignModel.update(
            oid=campaign_id,
            obj=edit_infos
        )
        
        return campaign_id, 'success'

    @classmethod
    def edit_release_campaign(cls, user_id, campaign_id, edit_infos):
        
        _campaign = CampaignModel.get_item(oid=campaign_id).to_dict()
        
        if _campaign['user'] != user_id:
            raise ExCampaign("Not have permission to update this campaign !")

        if not _campaign['is_realeased']:
            raise ExCampaign("This campaign's not a released one !")

        CampaignModel.update(
            oid=campaign_id,
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
        _campaign = CampaignModel.get_item(oid=campaign_id).to_dict()

        if _campaign['is_released']:
            raise ExCampaign("This campaign 's already released !")
        
        if _campaign['user'] != user_id:
            raise ExCampaign("Not have permissions to release this campagn !")
        
        CampaignModel.update(
            oid=campaign_id,
            obj={
                "is_released": True
            }
        )

        return campaign_id, True

    @classmethod
    def get_campaign_details_by_subdomain(cls, subdoamin):
        # hard code for client build UI
        return CampaignModel.get_item(oid="6285fc1a8e445aaef2c2d7ec")