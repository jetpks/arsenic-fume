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
import logging
from fume_exceptions import FumeIsBroken
from flask import Flask
from flask.ext import restful
from flask.ext.restful import Resource, Api, reqparse

# Base Config
logging.basicConfig(level = logging.DEBUG)
logger = logging.getLogger(__name__)
api_prefix = '/api/v0.1'

resources = dict()
# main
class Dispatch:
    def __init__(self, lock, problems, bind='127.0.0.1', port=9001, debug=True):
        self.lock = lock
        self.problems = problems
        self.app = Flask(__name__)
        self.api = restful.api
        for res in self.resources: # Dict iteration
            self.api.add_resource(self.resources[res], api_prefix + res)

        self.app.run(debug=True)

# Flask Routing

""" Flask Resources
"""
class Slash(Resource):
    def get(self):
        return {'battlecruiser': 'operational'}
resources['/'] = Slash # Add us to the default load list with endpoint

class Ack(Resource):
    def get(self):
        pass

class Problem(Resource):
    def get(self):
        pass # TODO define
resources['/problems'] = Problem


""" Flask Req Parsers
"""
problem_parser = reqparse.RequestParser()
problem_parser.add_argument('hostgroup', type=str, action='append')
problem_parser.add_argument('box', type=str, action='append')
problem_parser.add_argument('active', type=int)
problem_parser.add_argument('since', type=int)
problem_parser.add_argument('before', type=int)
problem_parser.add_argument('limit', type=int)
problem_parser.add_argument('last',  type=int)
problem_parser.add_argument('region', type=int)
problem_parser.add_argument('min_severity', type=int)
problem_parser.add_argument('max_severity', type=int)
problem_parser.add_argument('acked', type=int)
