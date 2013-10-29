#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import logging
import webapp2
from rauth import OAuth2Service

REDIRECT_URL = 'http://bconsumer2.appspot.com/callback'

client = OAuth2Service(
    client_id='3MVG99qusVZJwhskkJlhLYtkoCKFDj3Q9Hk__aKoxuzzrYVRZqKVCGSW9ISArceeNTJ0XPnjRw.nnvZtgXd_B',
    client_secret='7998019891987789331',
    name='Connector',
    authorize_url='https://login.salesforce.com/services/oauth2/authorize',
    access_token_url='https://login.salesforce.com/services/oauth2/token',
    base_url='https://eu2.salesforce.com/services/data/v20.0/')


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

        params = {
            'response_type': 'code',
            'redirect_uri': REDIRECT_URL}

        url = client.get_authorize_url(**params)

        self.redirect(url)


class CallbackHandler(webapp2.RequestHandler):
    def get(self):
        code = self.request.params
        if 'code' in self.request.params:
            logging.info("Code=" + self.request.params['code'])
            session = client.get_auth_session(data={
                'grant_type': 'authorization_code', 'code': self.request.params['code'],
                'redirect_uri': REDIRECT_URL, 'format': 'urlencoded'})
            result = session.get('query?q=' + 'SELECT name, title FROM Contact LIMIT 100').json()
            self.response.write(result)


app = webapp2.WSGIApplication([
                                  ('/', MainHandler), ('/callback', CallbackHandler)
                              ], debug=True)
