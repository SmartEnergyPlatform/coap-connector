"""
   Copyright 2018 InfAI (CC SES)

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

from coapthon.resources.resource import Resource
from helper_functions import request_helper, core_link_format_helper
import logging
logger = logging.getLogger("log")

class WKResource(Resource):
    def __init__(self, name="WKResource", coap_server=None):
        super(WKResource, self).__init__(name, coap_server, visible=True,
                                            observable=True, allow_children=True)
        self.resources = {
            'core.rd': {
                'path': "/rd",
                'parameters': {
                    'rt': 'core.rd'
                }
            },
            'core.rd-lookup-res': {
                'path': "/rd-lookup/res",
                'parameters': {
                    'rt': 'core.rd-lookup-res'
                }
            },
            'core.rd-lookup-group': {
                'path': "/rd-lookup/group",
                'parameters': {
                    'rt': 'core.rd-lookup-group'
                }
            },
            'core.rd-lookup-d': {
                'path': "/rd-lookup/d",
                'parameters': {
                    'rt': 'core.rd-lookup-d'
                }
            },
            'core.rd-lookup-ep': {
                'path': "/rd-lookup/ep",
                'parameters': {
                    'rt': 'core.rd-lookup-ep'
                }
            }
        }

    def render_GET(self, request):
        res = WKResource()
        logger.info("GET to /.well-known/core from {host}:{port}".format(host=request.source[0], port=request.source[1]))
        query_parameters = request_helper.get_query_parameter(request)
        resource_type = query_parameters.get('rt')

        if resource_type == 'core.rd*' or not resource_type:
            # todo more pythonic
            all_resources = []
            for resource in self.resources:
                all_resources.append(self.resources[resource])
            res.payload = core_link_format_helper.generate_link(all_resources)

        else:
            res.payload = core_link_format_helper.generate_link([self.resources[resource_type]])

        return res



