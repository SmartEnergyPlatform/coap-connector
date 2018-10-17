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


"""
This script runs as a client connector in a local network.
It exposes an API to get registration data of new devices from the resource directory via CoAP and
sends them to the platform connector via a web socket connection.
Furthermore it gets commands from the platform and executes them by discovering the device in the resource directory
and performing a CoAP request to the IP address of the device.
"""
import os, sys, inspect
import_path = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0],"connector-client")))
if import_path not in sys.path:
    sys.path.insert(0, import_path)
    
from connector_client.client import Client
from coap_observer import observer
from database import DB
import logging

logger = logging.getLogger("log")
logger.setLevel(logging.INFO)
fn = logging.handlers.RotatingFileHandler('log.log', mode='a', maxBytes=5*1024*1024, 
                                 backupCount=2, encoding=None, delay=0)
fn.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(fn)
from coap_server import server
from pinger import pinger
from coap_executer import executer
#from discovery import mdns_discovery
#from discovery import coap_discovery

if __name__ == '__main__':
    # initiation phase nicht notwenidg, da alles was connected ist, schon mit connected status in db sthet
    # hochstens bei start das nochmal uberprufen, aber passiet eh weiter unten
    # devices method liefert eh nur connected devices
    # nochmal chekcen vorher ?! synchron aber damit erst danach client connecion aufbaut

    # Start Web Socket connection and synchronize connected devices
    connector_client = Client(DB.DB())

    # CoAP server listens on multicast and gets registration requests from devices
    # CoAP Server with registration und discovery endpoints
    coap_server = server.CoAPMulticastServer("0.0.0.0", 5683)
    coap_server.start()

    # CoAP Client for pining devices to update device manager
    coap_pinger = pinger.Pinger()
    coap_pinger.start()

    # Executer - Receive command and respond
    coap_executer = executer.Executer()
    coap_executer.start()

    # Observer - Gets data from connected devices and pushes them to the platform
    #coap_observer = observer.Observer()
    #coap_observer.start()
 
    # Discover things IP address by listening for mDNS Queries
    #mdns_discoverer = mdns_discovery.MdnsDiscovery()
    #mdns_discoverer.start()

    # Discovering things by using multicast CoAP Requests
    #coap_discoverer = coap_discovery.CoAPDiscovery()
    #coap_discoverer.start()
