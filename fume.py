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

def collect_loop(lock, problems):
    collector = collect.Collect(lock, problems, conf.get('zabbix', 'api'),
            conf.get('zabbix', 'user'), conf.get('zabbix', 'password'))
    while True:
        collector.poll_triggers([conf.get('zabbix', 'hostgroups')])
        time.sleep(4)

def dispatch_loop(lock, problems):
    dispatcher = dispatch.Dispatch(lock, problems)

if __name__ == '__main__':
    lock = mp.Lock()
    problems = dict()
    c = mp.Process(target=collect_loop, args=(lock, problems))
    d = mp.Process(target=dispatch_loop, args=(lock, problems))
    c.start()
    d.start()
    d.join()
    c.join()
