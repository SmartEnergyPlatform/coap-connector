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

from zeroconf import ServiceBrowser, Zeroconf
import threading
from coapthon.client.helperclient import HelperClient

# discover things by using mDNs

class MdnsDiscovery(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.zeroconf = Zeroconf()
        self.listener = MyListener()

    def run(self):
        browser = ServiceBrowser(self.zeroconf, "_coap._udp.local.", self.listener)


class MyListener:
    def remove_service(self, zeroconf, type, name):
        print("Service %s removed" % (name,))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        print("Service %s added, service info: %s" % (name, info))
        coap_client = HelperClient((ip,port))
        response = coap_client.discover()
        # todo register 
        # if not exists 



