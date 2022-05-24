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
def create_domain(subdomain: str, campaign_id: str) -> str:
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
            return f"Create subdomain failed ! {_code_create_new_domain}"

        return _resp_create_new_domain['data']['result']

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
        "start_time": _campaign_dict["start_time"].replace(tzinfo=timezone.utc).timestamp(),
        "end_time": _campaign_dict["end_time"].replace(tzinfo=timezone.utc).timestamp(),
        "symbol": _campaign_dict["chain_currency"],
        "market_address": DefaultConfig.RINZ_MARKET_ADDRESS,
        "factory_address": DefaultConfig.RINZ_CAMPAIGN_FACTORY_ADDRESS,
        "token_address": DefaultConfig.RINZ_COIN_TOKEN_ADDRESS,
        "is_fixed_token": _campaign_dict["is_fixed_token"] if _campaign_dict["is_fixed_token"] else False
    }

    print("worker : ", _payload)
    resp = requests.post(
        f"{DefaultConfig.IAPI_URL}/deploy/campaign",
        json=_payload,
        verify=False,
        timeout=10
    )
    return "success"
