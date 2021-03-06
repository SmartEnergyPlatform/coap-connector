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

from coapthon.client.helperclient import HelperClient
import threading
import time
from helper_functions import core_link_format_helper
from database import DB
from connector_client.client import Client

class CoAPDiscovery(HelperClient, threading.Thread):
    def __init__(self, host="224.0.1.187", port = 5683):
        HelperClient.__init__(self,server=(host, port))
        threading.Thread.__init__(self)
        # discover things by sening multicast request to the .well-known/core endpoint
        # returns the API of the device CoAP Server
        self.db = DB.DB()

    def handle_mutlicast_responses(self, response):
        print(response.pretty_print())

        if not DB.DB.host_exists(response.source[0]):  # todo check ip change
            informations = {
                "host": response.source[0],
                "port": response.source[1],
                "query_parameters": {
                    "ep": "Unknown Name"
                },
                "links": core_link_format_helper.parse_links(response.payload),
            }

            id = DB.DB.create(informations)
            device = DB.DB.get(id)
            Client.add(device)

    def run(self):
        while True:
            time.sleep(30)
            self.discover(self.handle_mutlicast_responses)




