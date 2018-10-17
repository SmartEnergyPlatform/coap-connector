"""
   Copyright 2018 SEPL Team

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from helper_functions import request_helper
from helper_functions import core_link_format_helper

from database import DB
from coapthon.resources.resource import Resource
import logging
logger = logging.getLogger("log")


class LookupResource(Resource):
    """
    Lookup resource, which is accessbile via:
     - /rd-lookup/ep for device discovery
     - /rd-lookup/res for service discovery
    """
    def __init__(self, lookup_table, name="LookupResource", coap_server=None):
        super(LookupResource, self).__init__(name, coap_server, visible=True,
                                             observable=True, allow_children=True)
        self.lookup_table = lookup_table

    def render_GET(self, request):
        if request.source[0] != "127.0.0.1":
            logger.info("CoAP RD: GET to /rd-lookup from {host}:{port}".format(host=request.source[0], port=request.source[1]))
        res = LookupResource(self.lookup_table)
        query_parameters = request_helper.get_query_parameter(request)
        if len(query_parameters) == 0:
            res.payload = DB.DB.lookup_all(self.lookup_table)
        else:
            res.payload = DB.DB.lookup_with_parameter(self.lookup_table, query_parameters)
        return res



