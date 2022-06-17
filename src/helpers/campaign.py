# -*- coding: utf-8 -*-
"""
    Utils has nothing to do with models and views.
"""
import json
import traceback
import requests
from src.config import DefaultConfig
import re
from marshmallow import ValidationError


def log_any(x, *args, **kwargs):
    """
        Log any message to json format.
    """
    msg = {
        'msg': x,
    }

    print()
    if args:
        msg['args'] = json.dumps(args)
    if kwargs:
        msg['kwargs'] = json.dumps(kwargs)
    print(msg)
    return json.dumps(msg)


"""
    Function: Call IAPI service to check if the submitted subdomain for campaign is valid or not
    @params: subdomain <string>
    @params: campaign_id <string>
    @return: True if sub_domain is valid 
"""


def check_campaign_subdomain_valid(subdomain, campaign_id=None):
    try:
        _payload = {
            "domain": subdomain
        }

        if campaign_id:
            _payload["campaign_id"] = campaign_id

        resp = requests.post('{}/domain/check'.format(DefaultConfig.IAPI_URL),
                             json=_payload,
                             verify=False,
                             timeout=5)
        log_any(f'Call IAPI service check domain {subdomain}: {resp.status_code}  {resp.text}')
        return resp.status_code, resp.json()
    except Exception as e:
        print(e)
        return 400, {}


"""
    Function: Call IAPI service to delete the submitted subdomain for campaign is valid or not
    @params: subdomain <string>
    @params: campaign_id <string>
    @return: API return
"""


def delete_subdomain(subdomain):
    try:
        _payload = {
            "domain": subdomain
        }

        resp = requests.delete('{}/domain'.format(DefaultConfig.IAPI_URL),
                               json=_payload,
                               verify=False,
                               timeout=5)
        log_any(f'Call IAPI service delete domain {subdomain}: {resp.status_code}  {resp.text}')
        return resp.status_code, resp.json()
    except Exception as e:
        print(e)
        return 400, {}


"""
    Function: Call IAPI service to create new subdomain
    @params: 
    @return: True or False
"""


def create_new_subdomain(subdomain, campaign_id):
    try:
        _payload = {
            "domain": subdomain,
            "campaign_id": campaign_id
        }

        resp = requests.post(
            '{}/domain'.format(DefaultConfig.IAPI_URL),
            json=_payload,
            verify=False,
            timeout=5
        )

        log_any(f'Call IAPI service create domain {subdomain}: {resp.status_code}  {resp.text}')
        return resp.status_code, resp.json()
    except Exception as e:
        print(e)
        return 400, {}


"""
    Validator function for input data
"""


def is_valid_number(_number) -> bool:
    if _number < 0:
        raise ValidationError("Number in this field cannot be negative !")
    if _number > 2 ** 63 - 1:
        raise ValidationError("Number in this field is out of range !")
    return True


def is_valid_subdomain(_subdomain: str) -> bool:
    pattern = "[A-Za-z0-9](?:[A-Za-z0-9\-]{0,61}[A-Za-z0-9])"
    return bool(re.match(pattern, _subdomain))
