# -*- coding: utf-8 -*-

""""
    Copyright (C) 2022 ESOL LABS - All Rights Reserved.

    You may use, distribute and modify this code under the
    terms of the XYZ license, which unfortunately won't be
    written for another century.

    You should have received a copy of the XYZ license with
    this file. If not, please write to: , or visit :
"""

# File: __init__.py
# Created at May 17th, 2022
# Author: taipa

"""
   Description:
        -
        -
"""

from marshmallow import EXCLUDE, INCLUDE, fields, Schema, validate
from lib.schema.req import ResDatetimeField, ObjectIdField
from src.enums.campaign import CampaignGetList
from src.helpers.campaign import is_valid_number, is_valid_subdomain


"""
    Campaign Creation
"""


class FormNftOfCampaign(Schema):
    class Meta:
        unknown = INCLUDE
        ordered = True
    
    name = fields.Str(required=True)
    image_uri = fields.Str(required=True)
    supply = fields.Int(required=True, validate=is_valid_number)
    price = fields.Float(allow_none=True, validate=is_valid_number)
    type = fields.Str(required=True)
    percent = fields.Float(allow_none=True)
    description = fields.Str(allow_none=True)


class CampaignDescription(Schema):
    title = fields.Str(required=True)
    html_content = fields.Str(required=True)
    image_uri = fields.Str(allow_none=True, missing='')


class FormCreateNewCampaign(Schema):
    class Meta:
        unknown = INCLUDE
        ordered = True

    name = fields.Str(required=True)
    description = fields.List(fields.Nested(CampaignDescription()), allow_none=True, missing=[])
    about_kol = fields.Str(allow_none=True)
    kol_image_url = fields.Str(allow_none=True)
    image_url = fields.Str(required=True)
    highlight_text = fields.Str(allow_none=True)
    max_allocation = fields.Int(allow_none=True, validate=is_valid_number)
    allocation_symbol = fields.Str(allow_none=True)
    chain_name = fields.Str(required=True, default='')
    chain_currency = fields.Str(required=True)
    total_supply = fields.Int(required=True, validate=is_valid_number)
    total_raise = fields.Float(required=True, validate=is_valid_number)
    start_time = ResDatetimeField(required=True)
    end_time = ResDatetimeField(required=True)
    website_domain = fields.Str(required=True, validate=is_valid_subdomain)
    social_link = fields.Dict(allow_none=True)
    campaign_method = fields.Int(required=True)
    random_nft = fields.Bool(required=True)
    nft_list = fields.List(fields.Nested(FormNftOfCampaign()))


class CreateNewCampaignResp(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    name = fields.Str(required=True)
    is_released = fields.Bool(required=True)


"""
    Campaign Editor
"""


class FormNonReleasedCampaignEditor(Schema):
    class Meta:
        unknown = INCLUDE
        ordered = True
    
    _id = fields.Str(required=True)
    name = fields.Str(allow_none=True)
    description = fields.List(fields.Nested(CampaignDescription()), allow_none=True)
    about_kol = fields.Str(allow_none=True)
    kol_image_url = fields.Str(allow_none=True)
    image_url = fields.Str(required=True)
    highlight_text = fields.Str(allow_none=True)
    max_allocation = fields.Int(allow_none=True)
    allocation_symbol = fields.Str(allow_none=True)
    chain_name = fields.Str(allow_none=True, default='BSC')
    chain_currency = fields.Str(allow_none=True)
    total_supply = fields.Int(allow_none=True) 
    total_raise = fields.Int(allow_none=True)
    start_time = ResDatetimeField(allow_none=True)
    end_time = ResDatetimeField(allow_none=True)
    website_domain = fields.Str(allow_none=True)
    social_link = fields.Dict(allow_none=True)
    campaign_method = fields.Int(allow_none=True)
    random_nft = fields.Bool(allow_none=True)
    nft_list = fields.List(fields.Nested(FormNftOfCampaign()))


class FormReleasedCampaignEditor(Schema):
    class Meta:
        unknown = INCLUDE
        ordered = True
    
    _id = fields.Str(required=True)
    name = fields.Str(allow_none=True)
    highlight_text = fields.Str(allow_none=True)
    description = fields.List(fields.Nested(CampaignDescription()), allow_none=True)
    about_kol = fields.Str(allow_none=True)
    kol_image_url = fields.Str(allow_none=True)
    image_url = fields.Str(allow_none=True)
    social_link = fields.Dict(allow_none=True)


class CampaignEditorResp(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True
    
    _id = fields.Str(required=True)
    edit_result = fields.Str(required=True)


"""
    Campaign Get List
"""


class GetListCampaignParams(Schema):

    class Meta:
        unknown = INCLUDE
        ordered = True

    page = fields.Int(allow_none=True, default=CampaignGetList.DEFAULT_PAGE)
    page_size = fields.Int(allow_none=True, default=CampaignGetList.DEFAULT_PAGE_SIZE)


class NftOfCampaignResp(Schema):
    class Meta:
        unknown = INCLUDE
        ordered = True
    
    name = fields.Str(required=True)
    image_uri = fields.Str(required=True)
    supply = fields.Int(allow_none=True)
    price = fields.Float(required=True)
    type = fields.Str(required=True)
    percent = fields.Float(allow_none=True)
    description = fields.Str(allow_none=True)

    current_sell = fields.Int(allow_none=True, missing=0)
    index_type = fields.Int(allow_none=True, missing='')


class SingleCampaign(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    _id = ObjectIdField(required=True)
    name = fields.Str(required=True)
    image_url = fields.Str(required=True)
    highlight_text = fields.Str(allow_none=True)
    max_allocation = fields.Int(allow_none=True)
    allocation_symbol = fields.Str(required=True)
    chain_name = fields.Str(required=True, default='BSC')
    chain_currency = fields.Str(required=True)
    total_supply = fields.Int(required=True) 
    current_sell = fields.Int(allow_none=True, missing=0)
    total_raise = fields.Int(required=True)
    start_time = ResDatetimeField(required=True)
    end_time = ResDatetimeField(required=True)
    website_domain = fields.Str(required=True)
    social_link = fields.Dict(allow_none=True)
    campaign_method = fields.Int(required=True)
    random_nft = fields.Bool(required=True)
    nft_list = fields.List(fields.Nested(NftOfCampaignResp()))

    contract = fields.Str(required=True)
    is_released = fields.Bool(required=True)
    description = fields.List(fields.Nested(CampaignDescription()), missing=[])
    about_kol = fields.Str(missing='')
    kol_image_url = fields.Str(missing='')

    is_hot = fields.Bool(allow_none=True, missing=False)


class GetListCampaignsResp(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True
    
    total = fields.Int(required=True)
    page = fields.Int(required=True)
    campaigns = fields.List(fields.Nested(SingleCampaign()))


"""
    Campaign Release
"""


class ReleaseCampaignParams(Schema):
    class Meta:
        unknown = INCLUDE
        ordered = True

    campaign_id = fields.Str(required=True)


class ReleaseCampaignResp(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True
    
    _id = fields.Str(required=True)
    result = fields.Bool(required=True)
    messages = fields.Str(required=True)


"""
    Delete Campaign
"""


class DeleteCampaignReq(Schema):
    class Meta:
        unknown = INCLUDE
        ordered = True

    campaign_id = fields.Str(required=True)


class DeleteCampaignRes(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    result = fields.Bool(required=True)


"""
    Get campaign details by campaign_id
"""


class GetCampaignDetailsByIdParams(Schema):
    class Meta:
        unknown = INCLUDE
        ordered = True
        
    campaign_id = fields.Str(allow_none=True, default='')


"""
    Get campaign details by contract
"""


class GetCampaignDetailsByContractReq(Schema):
    class Meta:
        unknown = INCLUDE
        ordered = True

    contract_address = fields.Str(required=True)
    index_type = fields.Int(required=True)


class GetCampaignDetailsByContractRes(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    name = fields.Str(required=True)
    image_url = fields.Str(required=True)
    total_supply = fields.Int(required=True)
    current_sell = fields.Int(allow_none=True, missing=0)
    start_time = ResDatetimeField(required=True)
    end_time = ResDatetimeField(required=True)
    social_link = fields.Dict(allow_none=True)
    random_nft = fields.Bool(required=True)
    contract = fields.Str(required=True)
    is_released = fields.Bool(required=True)
    description = fields.List(fields.Nested(CampaignDescription()), missing=[])
    user_infos = fields.Dict(required=True, default={})
    nft_infos = fields.Dict(required=True, default={})


"""
    Get hot campaign list
"""


class GetHotCampaignsParams(Schema):
    class Meta:
        unknown = INCLUDE
        ordered = True

    category = fields.Str(allow_none=True, default="")


class GetHotCampaignsList(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    campaigns = fields.List(fields.Nested(SingleCampaign()))







