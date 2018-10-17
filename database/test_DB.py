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

import DB
import unittest

class TestRegistrationAPI(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.db = DB.DB()
        self.informations = {
            "host": "host",
            "port": 1,
            "query_parameters": {
                "ep": "name",
                "et": "type"
            },
            "links": [
                {
                    "path": "/path",
                    "title": "titel"
                }
            ]
        }

    def test_create_endpoint_1(self):
        self.db.create_endpoint(self.informations)
        result = self.db.execute("""
                        SELECT * FROM endpoints
                        """)
        self.assertNotEqual(len(result), 0)

    def test_create_endpoint_2(self):
        self.db.create_endpoint(self.informations)
        result = self.db.execute("""
                        SELECT * FROM endpoints
                        WHERE ep LIKE '{ep}'
                        """.format(ep=self.informations["query_parameters"]["ep"]))
        self.assertEqual(result[0]["et"], self.informations["query_parameters"]["et"])

if __name__ == '__main__':
    unittest.main()