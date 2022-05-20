from src.task import worker
from src.helpers.campaign import check_campaign_subdoamin_valid


@worker.task(name='worker.deploy_smc', rate_limit='10/s')
def deploy_smc():
    try:
        return 'Deploy smc successfully !'
    except Exception as e:
        print(e)
        return None


@worker.task(name='worker.create_domain', rate_limit='10/s')
def create_domain(subdomain: str) -> str:
    try:
        _status_code, _resp = check_campaign_subdoamin_valid(subdomain=subdomain)
        if _status_code != 200:
            return 'Create subdomain successfully !'
    except Exception as e:
        print(e)
        return "Create submodumain failed !"
