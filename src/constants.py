# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from src.enums.campaign import CampaignMethod


class AppConstants(object):
    CampaignMethodList = [
        CampaignMethod.KOL_WALLET,
        CampaignMethod.RINZ_WALLET
    ]

    EditReleasedCampaignFields = [
        "name",
        "hightlight_text",
        "website_domain",
        "social_link",
        "image_url"
    ]

    EditNonReleasedCampaignFields = [

    ]

    HotCampaignCategories = ["", "up_coming", "on_going", "completed"]
    pass
