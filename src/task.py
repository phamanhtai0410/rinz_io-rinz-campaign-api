# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from pymodm import connect

from lib.worker import create_worker
from src.config import DefaultConfig

connect(DefaultConfig.DB_DAPP, connect=False)
worker = create_worker(DefaultConfig)
