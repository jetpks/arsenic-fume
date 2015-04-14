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
import copy
import logging
from fume_exceptions import FumeIsBroken
from zabbix.api import ZabbixAPI

# Base Config
#logging.basicConfig(level = logging.ERROR)
#logger = logging.getLogger(__name__)

# Class Defs
class Collect:
    def __init__(self, dispatcher, api, user, password, debug=False):
        self.target = api
        self.user = user
        self.password = password
        self.dispatcher = dispatcher
        if debug:
            logging.basicConfig(level = logging.DEBUG)
        else:
            logging.basicConfig(level = logging.ERROR)
        if not self.connect():
            raise FumeIsBroken("Problem with connection or credentials: %s"
                                    % self.target)

    def connect(self):
        self.z = ZabbixAPI(url=self.target, user=self.user,
                            password=self.password)
        return self.conn_okay()

    def conn_okay(self):
        if re.search('^2\.\d', self.z.apiinfo.version()):
            return True
        return False

    def poll_triggers(self, groupids, min_sev=1):
        self.dispatcher.screen(self.z.trigger.get(groupids=groupids, min_severity=min_sev,
                                    only_true=True,
                                    output="extend",
                                    expandData=True,
                                    expandComment=True,
                                    expandDescription=True,
                                    expandExpression=True))
