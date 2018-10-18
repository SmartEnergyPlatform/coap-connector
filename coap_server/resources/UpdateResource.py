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

from helper_functions import device_translator
from helper_functions import core_link_format_helper,request_helper
from connector_client.device import Device
from connector_client.client import Client
from database import DB
from coapthon.resources.resource import Resource


class UpdateResource(Resource):
    def __init__(self, name="UpdateResource", coap_server=None):
        super(UpdateResource, self).__init__(name, coap_server, visible=True,
                                            observable=True, allow_children=True)
        self.db = DB.DB()

    def render_POST(self, request):
        res = UpdateResource()
        print("POST to /rd/[id] from {host}:{port}".format(host=request.source[0], port=request.source[1]))
        informations = {
            'query_parameters':  request_helper.get_query_parameter(request),
            'links': core_link_format_helper.parse_links(request.payload.decode('utf-8')),
        }
        id = request.uri_path.split("/")[-1]
        device = self.db.get(id)
        Client.update(device)
        return res


