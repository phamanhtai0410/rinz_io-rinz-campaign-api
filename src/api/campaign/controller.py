# -*- coding: utf-8 -*-

""""
    Copyright (C) 2022 ESOL LABS - All Rights Reserved.

    You may use, distribute and modify this code under the
    terms of the XYZ license, which unfortunately won't be
    written for another century.

    You should have received a copy of the XYZ license with
    this file. If not, please write to: , or visit :
"""

# File: controller.py
# Created at May 17th, 2022
# Author: taipa

"""
   Description:
        -
        -
"""
import lib
from lib.logger import Logger
from schemas.campaign import *
from src.api import campaign
from src.services.campaign import CampaignService


@lib.handle_res(req_schema=FormCreateNewCampaign, res_schema=CreateNewCampaignResp, login=True)
def create_new_campaign(wallet, body, *args, **kwargs):
    # Load data
    _user_id = wallet.user
    _campaign_info = {
        'user': _user_id,
        'contract': '',
        'is_released': False,
        'name': body.name, 
        'image_url': body.image_url,
        'hightlight_text': body.hightlight_text,
        'max_allocation': body.max_allocation,
        'allocation_symbol': body.allocation_symbol,
        'chain_name': body.chain_name,
        'chain_currency': body.chain_currency,
        'total_supply': body.total_supply,
        'total_raise': body.total_raise,
        'start_time': body.start_time,
        'end_time': body.end_time,
        'website_domain': body.website_domain,
        'social_link': body.social_link, 
        'campaign_method': body.campaign_method, 
        'random_nft': body.random_nft, 
        'nft_list': body.nft_list
    }
    
    # Call service process api
    name, is_released = CampaignService.create_campaign(_campaign_info)
    
    return {
        'name': name,
        'is_released': is_released
    }



@lib.handle_res(req_schema=FormNonReleasedCampaignEditor, res_schema=CampaignEditorResp)
def edit_non_released_campaign(wallet, body, *args, **kwargs):
    _user_id = wallet.user
    _campaign_id = body._id
    _edit_infos = body.__dict__
    del _edit_infos["_id"]

    _id, _result = CampaignService.edit_non_release_campaign(_user_id, _campaign_id, _edit_infos)

    return {
        "_id": _id,
        "edit_result": _result
    }



@lib.handle_res(req_schema=FormCreateNewCampaign, res_schema=CampaignEditorResp)
def edit_released_campaign(wallet, body, *args, **kwargs):
    _user_id = wallet.user
    _campaign_id = body._id
    _edit_infos = body.__dict__
    del _edit_infos["_id"]
    
    _id, _result = CampaignService.edit_release_campaign(_user_id, _campaign_id, _edit_infos)

    return {
        "_id": _id,
        "edit_result": _result
    }




@lib.handle_res(param_schema=GetListCampaignParams,res_schema=GetListCampaignsResp)
def list_campaigns(wallet, *args, **kwargs):

    _user_id = wallet.user
    _total, _page, _campaigns = CampaignService.get_list_campaigns(_user_id)

    return {
        "total": _total,
        "page": _page,
        "campaigns": _campaigns
    }



@lib.handle_res(param_schema=ReleaseCampaignParams, res_schema=ReleaseCampaignResp)
def release_campaign(wallet, params, *args, **kwargs):
    _campaign_id = params.campaign_id
    _user_id = wallet.user
    _id, _is_released = CampaignService.release_campaign(_campaign_id, _user_id)

    return {
        "_id": _id,
        "is_released": _is_released
    }

