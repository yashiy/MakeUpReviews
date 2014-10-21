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
import os

from google.appengine.ext import ndb
import jinja2
import webapp2
import logging

from models import MakeUpPics


jinja_env = jinja2.Environment(
                               loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                               autoescape=True)

# Generic Key to serve as parent
PARENT_KEY = ndb.Key("Entity", "weatherpics_root")

class MakeUpPicsPage(webapp2.RequestHandler):
    def get(self):
        makeup_query = MakeUpPics.query(ancestor=PARENT_KEY).order(-MakeUpPics.last_touch_date_time)
        
        template = jinja_env.get_template("templates/mainpage.html")
        self.response.write(template.render({"makeup_query": makeup_query}))
        
class InsertPicAction(webapp2.RequestHandler):
    def post(self):
        if(self.request.get("entity_key")):
            logging.info(self.request.get("entity_key"))
            weatherPic = ndb.Key(urlsafe=self.request.get("entity_key"))
        else:
            new_pic = MakeUpPics(parent = PARENT_KEY,
                                  image_url = self.request.get("image_url"),
                                  caption = self.request.get("caption"),
                                  brand = self.request.get("brand"),
                                  category = self.request.get("category"))
            new_pic.put()
        self.redirect(self.request.referer)

app = webapp2.WSGIApplication([
    ("/", MakeUpPicsPage),
    ("/insertpic", InsertPicAction)
], debug=True)
