from src.task import worker
from src.helpers.campaign import check_campaign_subdomain_valid, create_new_subdomain


@worker.task(name='worker.deploy_smc', rate_limit='10/s')
def deploy_smc():
    try:
        return 'Deploy smc successfully !'
    except Exception as e:
        print(e)
        return None


@worker.task(name='worker.create_domain', rate_limit='10/s')
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
