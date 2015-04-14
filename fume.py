#!/usr/bin/env python

import time
import logging
import ConfigParser
import multiprocessing as mp
from threading import Lock
from Fume import collect
from Fume import dispatch

# Config
conf = ConfigParser.SafeConfigParser()
conf.read('./fume.conf')
dispatcher = dispatch.Dispatch(
        redis_use_socket=conf.get('redis', 'use_socket'),
        redis_socket=conf.get('redis', 'socket'))
collector = collect.Collect(dispatcher, conf.get('zabbix', 'api'),
        conf.get('zabbix', 'user'), conf.get('zabbix', 'password'),
        hostgroups=[conf.get('zabbix', 'hostgroups')], interval=3)

