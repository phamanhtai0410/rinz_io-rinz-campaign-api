# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask import Blueprint

from .controller import *

rest_campaign = Blueprint('rest_campaign', __name__, url_prefix='')

"""
        API for Admin page (form origin api url):
        + Create campaign
        + Edit Campaign
        + Release Campaign
        + Get List Campaign
"""

rest_campaign.add_url_rule('create_new', methods=['POST'], view_func=create_new_campaign)

rest_campaign.add_url_rule('get_list', methods=['GET'], view_func=list_campaigns)

rest_campaign.add_url_rule('edit_non_released', methods=['POST'], view_func=edit_non_released_campaign)

rest_campaign.add_url_rule('edit_released', methods=['POST'], view_func=edit_released_campaign)

rest_campaign.add_url_rule('release', methods=['GET'], view_func=release_campaign)



"""
        API for KOL Marketplace:
        + Get information of campaign for page details:
"""

rest_campaign.add_url_rule('get_details', methods=['GET'], view_func=get_campaign_details)