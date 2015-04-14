#!/usr/bin/env python
"""
8888                                     
8www 8   8 8d8b.d8b. .d88b   88b. Yb  dP 
8    8b d8 8P Y8P Y8 8.dP'   8  8  YbdP  
8    `Y8P8 8   8   8 `Y88P w 88P'   dP   
                             8     dP    
"""
import re
import time
import redis
import logging
from fume_exceptions import FumeIsBroken

class Dispatch:
    def __init__(self, redis_srv='127.0.0.1', redis_port=6379,
            redis_db=0, redis_use_socket=False, redis_socket='/tmp/redis.sock',
            redis_ch_alerts='alerts', redis_ch_acks='acks', debug=False):
        # Lumberjack
        if debug:
            logging.basicConfig(level = logging.DEBUG)
        else:
            logging.basicConfig(level = logging.ERROR)

        # Redis connect
        if redis_use_socket:
            self.r = redis.StrictRedis(unix_socket_path=redis_socket, db=redis_db)
        else:
            self.r = redis.StrictRedis(host=redis_srv, port=redis_port, db=redis_db)
        self.r.flushall() # Remove any stale data
        self.ch_alerts = redis_ch_alerts
        self.ch_acks = redis_ch_acks

    """For shipping alerts to moxxy"""
    def publish(self, host, triggerid):
        self.r.publish(self.ch_alerts, host + 'A' + triggerid)

    """For ACKs and junk"""
    def subscribe(self, handler):
        pass

    """ return boolean based on whether or not we've seen $alert
    before"""
    def seen(self, alert):
        key = alert['host'] + 'A' + alert['triggerid']
        # Have we stored this trigger?
        if not self.r.exists(key):
            logging.debug('never seen this alert for this host before')
            return False
        # Has this trigger been updated since we stored it?
        if int(alert['lastchange']) != int(self.r.hget(key, 'lastchange')):
            logging.debug('the alert we have is stale. %s != %s' % (alert['lastchange'], self.r.hget(key, 'lastchange')))
            return False
        return True

    def store(self, alert):
        """ This is an example of an alert:
                {
            "status": "0",
            "hostname": "dc-6642c37-000",
            "description": "image.uploaded.success",
            "state": "0",
            "url": "",
            "type": "1",
            "templateid": "0",
            "value_flags": "0",
            "lastchange": "1428605426",
            "value": "1",
            "priority": "1",
            "triggerid": "184099",
            "hostid": "12757",
            "flags": "0",
            "comments": "\"description\": \"cb44829f-a803-472e-9...\", \"event_type\": \"image.uploaded\", \"status\": \"success\"\n",
            "groups": [
                {
                    "groupid": "19"
                }
            ],
            "error": "",
            "host": "dc-6642c37-000",
            "expression": "{dc-6642c37-000:image.uploaded.success.regexp(\\w+)}=1",
            "groupid": "19"
        }"""
        # Get rid of the pesky groups array
        alert.pop('groups')
        # We're using a composite key for a lot of reasons. If you have a
        # better idea, implement it and submit a pull request.
        # Reasons:
        # 0. redis doesn't support complex data structures
        # 0. we want r.hexists calls to be fast.
        # 0. pickle, while neat, is kind of gross.
        # 0. So much json (de/en)coding
        self.r.hmset(alert['host'] + 'A' + alert['triggerid'], alert)

    def screen(self, trigs):
        for trig in trigs:
            if not self.seen(trig):
                self.store(trig)
                self.publish(trig['host'], trig['triggerid'])
