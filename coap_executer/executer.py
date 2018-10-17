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

from coapthon.client.helperclient import HelperClient
import threading
from connector_client.client import Client
from helper_functions import core_link_format_helper,request_helper
import logging
logger = logging.getLogger("log")

class Executer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            task = Client.receive()
            self.execute_task(task)

    def execute_task(self,task):
        coap_client = HelperClient("127.0.0.1", 5683)
        response = coap_client.get("/rd-lookup/ep?id={id}".format(id=task))
        links = core_link_format_helper.parse_links(response)
        device = links[0]
        uri = request_helper.parse_url(device.get("path"))
        coap_client = HelperClient((uri.hostname, uri.port))

        try:
            logger.info("EXECUTER: Send command to {host}:{port} with id: {id}".format(host=uri.hostname,port=uri.port,id=id))
            config = task.get("metadata")
            service = task.get("data")
            if config == "GET":
                coap_client.get(device.get("path") + service)
            elif config == "POST":
                coap_client.post(device.get("path") + service, task)
            elif config == "PUT":
                coap_client.put(device.get("path") + service, task)
            elif config == "DELETE":
                coap_client.delete(device.get("path") + service)

            logger.info("EXECUTER: Send command was sucsessful")
        except Exception as e:
            logger.error("EXECUTER: Send command was not successful")

        try:
            logger.info("EXECUTER: Send response to platform")
            Client.response(task, task)
        except Exception as e:
            logger.error("OBSERVER: Send response to platform was not successful")

