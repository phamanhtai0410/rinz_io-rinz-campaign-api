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
from src.schemas.campaign import *
from src.api import campaign
from src.services.campaign import CampaignService


@lib.handle_res(req_schema=FormCreateNewCampaign, res_schema=CreateNewCampaignResp, login=True)
def create_new_campaign(wallet, body, *args, **kwargs):
    # Load data
    _user_id = wallet.user
    # _user_id = 'test_user_id'
    _campaign_info = {
        'user': _user_id,
        'contract': '',
        'is_released': False,
        **body.__dict__
    }

    print("*** Campaign Information for create : ", _campaign_info)
    
    # Call service process api
    name, is_released = CampaignService.create_campaign(_campaign_info)
    
    return {
        'name': name,
        'is_released': is_released
    }


@lib.handle_res(req_schema=FormNonReleasedCampaignEditor, res_schema=CampaignEditorResp, login=True)
def edit_non_released_campaign(wallet, body, *args, **kwargs):
    _user_id = wallet.user
    # _user_id = '62767fa500f8f9069bef877d'
    _campaign_id = body._id
    _edit_infos = body.__dict__
    del _edit_infos["_id"]

    _id, _result = CampaignService.edit_non_release_campaign(_user_id, _campaign_id, _edit_infos)

    return {
        "_id": _id,
        "edit_result": _result
    }


@lib.handle_res(req_schema=FormReleasedCampaignEditor, res_schema=CampaignEditorResp)
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


@lib.handle_res(param_schema=GetListCampaignParams, res_schema=GetListCampaignsResp)
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
    _id, _result, _msg = CampaignService.release_campaign(_campaign_id, _user_id)

    return {
        "_id": _id,
        "result": _result,
        "messages": _msg
    }


@lib.handle_res(req_schema=DeleteCampaignReq, res_schema=DeleteCampaignRes)
def delete_campaign(wallet, body, *args, **kwargs):
    _user_id = wallet.user
    return {
        "result": CampaignService.delete_campaign(body.campaign_id, _user_id)
    }


@lib.handle_res(param_schema=GetCampaignDetailsByIdParams, res_schema=SingleCampaign, login=False)
def get_campaign_details(subdomain, params, *args, **kwargs):
    if subdomain:
        _details = CampaignService.get_campaign_details_by_subdomain(subdomain)
    else:
        _details = CampaignService.get_campaign_details_by_id(params.campaign_id)
    return _details or {}


@lib.handle_res(req_schema=GetCampaignDetailsByContractReq, res_schema=GetCampaignDetailsByContractRes, login=False)
def get_nft_details(body, *args, **kwargs):

    _details = CampaignService.get_nft_type_details(body.contract_address, body.index_type)
    return _details or {}


@lib.handle_res(res_schema=SingleCampaign)
def get_campaign_details_admin(campaign_id, *args, **kwargs):
    _details = CampaignService.get_campaign_details_by_id(campaign_id)
    return _details or {}


@lib.handle_res(param_schema=GetHotCampaignsParams, res_schema=GetHotCampaignsList, login=False)
def get_hot_campaigns(params, *args, **kwargs):
    _details = CampaignService.get_hot_campaigns(params.category)
    return _details or {}

