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

rest_campaign.add_url_rule('delete', methods=['POST'], view_func=delete_campaign)

"""
        API for KOL Marketplace (Admin Site):
        + Get information of campaign for page details: by subdomain in headers
        API for Launchpad Page:
        + Get information for page detail of campaign: by campaign_id in query
"""

rest_campaign.add_url_rule('details', methods=['GET'], view_func=get_campaign_details)

"""
        API for Market Details:
        Information of campaign by contract_address
"""

rest_campaign.add_url_rule('nft_details', methods=['POST'], view_func=get_nft_details)

"""
    API for campaign details of admin page for Edit page
    query by campaign_id
"""

rest_campaign.add_url_rule('admin/details/<campaign_id>', methods=['GET'], view_func=get_campaign_details_admin)


"""
    API for homepage
    Get list hot campaigns
"""

rest_campaign.add_url_rule('hot', methods=['GET'], view_func=get_hot_campaigns)

