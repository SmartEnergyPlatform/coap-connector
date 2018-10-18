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

from coapthon.server.coap import CoAP
from coap_server.resources import WKResource,RDResource,UpdateResource,LookupResource
import threading

class CoAPMulticastServer(CoAP,threading.Thread):
    """
    Server class, where the API endpoints gets appended
    Multicast:
    coap://224.0.1.187:5683/rd
    coap://224.0.1.187:5683/rd-lookup/ep
    Unicast:
    coap://127.0.0.1:5683/rd
    """
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port), multicast=True)
        threading.Thread.__init__(self)
        self.add_resource('.well-known/core/', WKResource.WKResource())
        self.add_resource('rd/', RDResource.RDResource())
        self.add_resource('rd-lookup/ep/', LookupResource.LookupResource("endpoints"))
        self.add_resource('rd-lookup/res/', LookupResource.LookupResource("resources"))

    def run(self):
        while True:
            self.listen(10)



