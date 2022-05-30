from src.task import worker
from src.helpers.campaign import check_campaign_subdomain_valid, create_new_subdomain
import requests
from src.config import DefaultConfig
from src.models.campaign import CampaignModel
from bson import ObjectId
from lib.decorators.exception import handle_exception
from datetime import timezone


@worker.task(name='worker.create_domain', rate_limit='1000/s')
@handle_exception()
def create_domain(subdomain: str, campaign_id: str):
    try:
        _status_code, _resp = check_campaign_subdomain_valid(subdomain=subdomain)
        if _status_code != 200:
            return "Can't verify subdomain !"
        
        if not _resp["data"]["result"]:
            return "subdomain not valid !"
        
        _code_create_new_domain, _resp_create_new_domain = create_new_subdomain(
            subdomain=subdomain,
            campaign_id=campaign_id
        )

        if _code_create_new_domain != 200:
            return False, f"Create subdomain failed ! {_code_create_new_domain}"

        if _resp_create_new_domain['data'] == {}:
            return False, \
                   f"Create subdomain failed ! {_resp_create_new_domain['error_code']} {_resp_create_new_domain['msg']}"

        return _resp_create_new_domain['data']['result'], "Create subdomain successfully !"

    except Exception as e:
        print(e)
        return False


@worker.task(name="worker.create_campaign_smc", rate_limit="1000/s")
@handle_exception()
def create_campaign_smc(_campaign_dict, _campaign_id, *args, **kwargs):
    """
        Call to Wallet-IAPI to create new campaign contract
    """
    print('worker - campaign id : ', _campaign_id)
    _payload = {
        "_id": _campaign_id,
        "start_time": _campaign_dict["start_time"],
        "end_time": _campaign_dict["end_time"],
        "symbol": _campaign_dict["allocation_symbol"],
        "market_address": DefaultConfig.RINZ_MARKET_ADDRESS,
        "factory_address": DefaultConfig.RINZ_CAMPAIGN_FACTORY_ADDRESS,
        "token_address": DefaultConfig.RINZ_COIN_TOKEN_ADDRESS,
        "is_fixed_token": _campaign_dict["is_fixed_token"] if _campaign_dict["is_fixed_token"] else False,
        "name": _campaign_dict["name"]
    }

    print("worker : ", _payload)
    resp = requests.post(
        f"{DefaultConfig.WALLET_IAPI}/deploy/campaign",
        json=_payload,
        verify=False,
        timeout=10
    )
    return "success"
