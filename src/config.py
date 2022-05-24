# -*- coding: utf-8 -*-

import os
import json
from dotenv import load_dotenv

load_dotenv()


class BaseConfig(object):
    PROJECT = "rinz-io-campaign"

    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    DEBUG = False
    TESTING = False

    # http://flask.pocoo.org/docs/quickstart/#sessions
    SECRET_KEY = os.getenv("SECRET_KEY")


class DefaultConfig(BaseConfig):
    DEBUG = True

    # Flask-babel: http://pythonhosted.org/Flask-Babel/
    ACCEPT_LANGUAGES = ['vi']
    BABEL_DEFAULT_LOCALE = 'en'

    DB_DAPP = os.getenv('DB_DAPP')

    REDIS_CLUSTER = json.loads(os.getenv('REDIS_CLUSTER'))

    SENTRY_DSN = os.getenv('SENTRY_DSN')
    # Blockchain RPC
    RPC_URI = os.getenv('RPC_URI')
    # Token
    TOKEN_EXP_TIME = int(os.getenv('TOKEN_EXP_TIME', default='864000'))

    # Worker config
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
    CELERY_TASK_RESULT_EXPIRES = os.getenv('CELERY_TASK_RESULT_EXPIRES')
    CELERY_TASK_RESULT_EXPIRES = int(CELERY_TASK_RESULT_EXPIRES) if CELERY_TASK_RESULT_EXPIRES else 600
    CELERY_DEFAULT_QUEUE = 'campaign-queue'

    CELERY_ROUTES = {
        'worker.deploy_smc': {'queue': 'campaign-queue'},
        'worker.create_domain': {'queue': 'campaign-queue'},
        'worker.create_campaign_smc': {'queue': 'campaign-queue'}
    }

    CELERY_TRACK_STARTED = "True"

    CELERY_ENABLE_UTC = True

    # IAPI server
    IAPI_URL = os.getenv('IAPI_URL')
    WALLET_IAPI = os.getenv('WALLET_IAPI')

    # CONTRACT ADDRESS
    RINZ_CAMPAIGN_FACTORY_ADDRESS = os.getenv("RINZ_CAMPAIGN_FACTORY_ADDRESS")
    RINZ_MARKET_ADDRESS = os.getenv("RINZ_MARKET_ADDRESS")
    RINZ_COIN_TOKEN_ADDRESS = os.getenv("RINZ_COIN_TOKEN_ADDRESS")


