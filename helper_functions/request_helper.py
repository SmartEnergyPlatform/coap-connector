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

import urllib
def get_query_parameter(request):
    # use python shortcut to create list
    query_parameters = {}
    parsed_query = urllib.parse.parse_qs(request.uri_query)
    for parameter in parsed_query:
        query_parameters[parameter] = parsed_query[parameter][0]
    return query_parameters

def parse_url(url):
    return urllib.parse.urlparse(url)


def generate_uri(ip, paths, parameters={}):
    """
    Generates an URI based on the protocol, the ip/hostname, multiple paths and parameters
    """

    uri = 'coap://' + ip
    for path in paths:
        uri += path
    #todo if parameters set ? only
    return uri + '?' + urllib.urlencode(parameters)


