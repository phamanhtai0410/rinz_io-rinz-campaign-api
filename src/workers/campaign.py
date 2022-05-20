from src.task import worker



@worker.task(name='worker.deploy_smc', rate_limit='10/s')
def deploy_smc():
    try:
        return 'Deploy smc successfully !'
    except Exception as e:
        print(e)
        return None


@worker.task(name='worker.create_domain', rate_limit='10/s')
def create_domain():
    try:
        return 'Create subdomain successfully !'
    except Exception as e:
        print(e)
        return None
