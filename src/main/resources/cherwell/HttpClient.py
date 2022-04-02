#
# Copyright 2022 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import requests
import logging
import time


logger = logging.getLogger(__name__)


class HttpClient(object):
    def __init__(self, http_connection, username=None, password=None):
        self.http_connection = http_connection
        self.url = http_connection['url']
        self.username = username if username else http_connection['username']
        self.password = password if password else http_connection['password']
        self.proxy = None
        self.auth_mode = http_connection['authMode']
        self.api_key = http_connection['apiKey']
        self.currentAccessToken = ""
        self.tokenExpiresTime = 0
        if http_connection['proxyHost']:
            self.proxy = {'http': '%s:%s' % (
                http_connection['proxyHost'], http_connection['proxyPort'])}
        self.verify_ssl = http_connection['enableSslVerification']

    def get_request(self, context_root, additional_headers={}):
        additional_headers["Authorization"] = "Bearer %s" % self.get_access_token()
        request_url = self.url + context_root
        return requests.get(request_url, headers=additional_headers,
                            proxies = self.proxy, verify = self.verify_ssl)

    def post_request(self, context_root, content, additional_headers = {}):
        additional_headers["Authorization"]="Bearer %s" % self.get_access_token()
        request_url=self.url + context_root+("?api_key=%s" % self.api_key)
        return requests.post(request_url, headers = additional_headers,
                             proxies = self.proxy, verify = self.verify_ssl, data = content)

    def put_request(self, context_root, content, additional_headers = {}):
        additional_headers["Authorization"]="Bearer %s" % self.get_access_token()
        request_url=self.url + context_root
        return requests.put(request_url, headers = additional_headers,
                            proxies = self.proxy, verify = self.verify_ssl, data = content)

    def delete_request(self, context_root, additional_headers = {}):
        additional_headers["Authorization"]="Bearer %s" % self.get_access_token()
        request_url=self.url + context_root
        return requests.delete(request_url, headers = additional_headers,
                               proxies = self.proxy, verify = self.verify_ssl)

    def get_access_token(self):
    
        if not self.is_current_token_valid():
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            content="grant_type=password&client_id=%s&username=%s&password=%s" % (self.api_key, self.username, self.password)
            result=requests.post("%s/token?auth_mode=%s&api_key=%s" % (self.url, self.auth_mode,
                                                                    self.api_key), proxies = self.proxy,
                                                                    verify = self.verify_ssl,
                                                                    headers=headers,
                                                                    data = content)
            self.logResponseAndRequest(result)
            if result.status_code != requests.codes.ok :
                print("ERROR getting access token %s" % str(result.status_code))
                result.raise_for_status()
            logger.debug("get_access_token response = %s" % result.json())
            self.currentAccessToken = result.json()['access_token']
            try:
                # Set token to expire 5 seconds before actual exipration
                self.tokenExpiresTime = (int(result.json()['expires_in'])) + int(round(time.time())) - (5)
                logger.debug("Just set tokenExpiresTime to %s" % str(self.tokenExpiresTime))
            except:
                self.tokenExpiresTime = 0
        logger.debug("About to return the currentAccessToken - %s" % self.currentAccessToken)
        return self.currentAccessToken

    def is_current_token_valid(self):
        is_valid = False

        if len(str(self.currentAccessToken)) > 0 and self.tokenExpiresTime > 0:
            currentTime = int(round(time.time()))
            logger.debug("Current Time is %s " % str(currentTime))
            if self.tokenExpiresTime > currentTime:
                logger.debug("Token has NOT expired. currentTime = %s, tokenExpiresTime = %s" % (str(currentTime), str(self.tokenExpiresTime)))
                is_valid = True
            else:
                logger.debug("Token has expired. currentTime = %s, tokenExpiresTime = %s" % (str(currentTime), str(self.tokenExpiresTime)))
        logger.debug("is_current_token_valid = %s, currentToken = %s" % (str(is_valid), str(self.currentAccessToken)))
        return is_valid

    def logResponseAndRequest(self, theResponse):
        logger.debug("***************")
        logger.debug("the response code is %s" % str(theResponse.status_code))
        logger.debug("We have the response. The following is more info about the original request")
        logger.debug("response.request.headers['Authorization']: %s" % theResponse.request.headers.get('Authorization', "No Authorization Header Found"))
        logger.debug("response.request.headers['Content-Type']: %s" % theResponse.request.headers.get('Content-Type', "No Content-Type Header Found"))
        logger.debug("response.request.headers['Accept']: %s" % theResponse.request.headers.get('Accept', "No Accept Header Found"))
        logger.debug("response.request.url: %s" % theResponse.request.url)
        logger.debug("response.request.body: %s" % theResponse.request.body)
        logger.debug("***************")
