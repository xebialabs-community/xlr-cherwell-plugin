#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import json
from cherwell.HttpClient import HttpClient
import logging
import time
import sys


logger = logging.getLogger(__name__)

class CherwellClient(object):
    def __init__(self, http_connection, username=None, password=None):
        self.http_request = HttpClient(http_connection, username, password)

    def get_teams(self):
        cherwell_api_url = '/api/V1/getteams'
        cherwell_response = self.http_request.get_request(
            cherwell_api_url, additional_headers={"Accept": "application/json"})
        cherwell_response.raise_for_status()
        data = cherwell_response.json()
        return data

    def create_business_object(self, businessObjectJson):
        return self.save_business_object(businessObjectJson)

    def save_business_object(self, bus_obj_json):
        foundError = False
        cherwell_api_url = "/api/V1/savebusinessobject"
        cherwell_response = self.http_request.post_request(cherwell_api_url, content=bus_obj_json,
            additional_headers={"Content-Type": "application/json", "Accept": "application/json"})
        self.http_request.logResponseAndRequest(cherwell_response)
        cherwell_response.raise_for_status()
        data = cherwell_response.json()
        logger.debug("Data from save_business_object call: %s" % data)
        if data['hasError']:
            foundError = True
            print("Received error code %s" % data['errorCode'])
            print("Received error message %s" % data['errorMessage'])
        for validation_error in data['fieldValidationErrors']:
            foundError = True
            print("Field id: [%s]" % validation_error['fieldId'])
            print("Error: [%s]" % validation_error['error'])
            print("Error code: [%s]" % validation_error['errorCode'])
        if foundError:
            sys.exit(1)
        return data

    def get_business_object(self, business_object_id, business_identifier, usePublicId):
        url_record = "/api/V1/getbusinessobject/busobid/%s/busobrecid/%s" % (business_object_id, business_identifier)
        url_public = "/api/V1/getbusinessobject/busobid/%s/publicid/%s" % (business_object_id, business_identifier)
        cherwell_api_url = url_public if usePublicId else url_record
        cherwell_response = self.http_request.get_request(
            cherwell_api_url, additional_headers={"Accept": "application/json"})
        cherwell_response.raise_for_status()
        data = cherwell_response.json()
        logger.debug("Data from get_business_object call: %s" % data)
        if data['hasError']:
            print("Received error code %s" % data['errorCode'])
            print("Received error message %s" % data['errorMessage']) 
            sys.exit(1)      
        return data

    def get_business_objects(self, dataRequest):
        endpoint = "/api/V1/getsearchresults"
        cherwell_response = self.http_request.post_request(
            endpoint,
            content=dataRequest,
            additional_headers={"Content-Type": "application/json", "Accept": "application/json"}
        )
        cherwell_response.raise_for_status()
        data = cherwell_response.json()
        logger.debug("Data from get_business_object call: %s" % data)
        if data['hasError']:
            print("Received error code %s" % data['errorCode'])
            print("Received error message %s" % data['errorMessage'])
            sys.exit(1)
        return data

    def update_business_object_record(self, business_object_id, business_object_record_id, fields):
        data = self.get_business_object(business_object_id, business_object_record_id, False)
        fields_data = data['fields']
        for item in fields_data:
            logger.debug("Name = %s, Value = %s" % (item['name'], item['value'])) 
            testField = fields.get(item['name'])
            if testField:
                item['value'] = fields[item['name']]
                item['dirty'] = True
                logger.debug("New value has been set for field %s, dirty has been set to %s" % (item['name'], item['dirty']))
        bus_obj_json = json.dumps(data)
        logger.debug("Updated business object about to be saved: %s" % bus_obj_json)
        return self.save_business_object(bus_obj_json)

    def poll_status(self, bus_ob_id, bus_ob_public_id, status_field_name, expected_status_list, poll_interval, poll_timeout_count):
        logger.debug("In poll_status")
        pollingCount = 0
        statusValue = "Error - Field named %s was not found." % status_field_name
        foundExpectedValue = False

        while pollingCount < poll_timeout_count and not foundExpectedValue:
            pollingInterval = int(poll_interval)
            time.sleep(pollingInterval)
            data = self.get_business_object(bus_ob_id, bus_ob_public_id, True)
            fields_data = data['fields']
            for item in fields_data:
                logger.debug("Name = %s, Value = %s" % (item['name'], item['value'])) 
                if item['name'] == status_field_name:
                    statusValue = item["value"]
                    if statusValue in expected_status_list:
                        foundExpectedValue = True
            pollingCount += 1
        if pollingCount >= poll_timeout_count and not foundExpectedValue:
            print("Polling count exceeded configured limit of %s. Last status retrieved - %s" % (poll_timeout_count, statusValue))
            sys.exit(1)
        return statusValue 