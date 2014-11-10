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
import json
import logging
import os

from google.appengine.ext import ndb
import jinja2
import webapp2

from models import MakeUpPics


jinja_env = jinja2.Environment(
                               loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                               autoescape=True)

# Generic Key to serve as parent
PARENT_KEY = ndb.Key("Entity", "weatherpics_root")

class MakeUpPicsPage(webapp2.RequestHandler):
    def get(self):
        makeup_query = MakeUpPics.query(ancestor=PARENT_KEY).order(-MakeUpPics.last_touch_date_time)
        print(self.request.get("sortby"))
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
                                  category = self.request.get("category"),
                                  star_rating = int(self.request.get("star_rating")),
                                  agree = 0,
                                  disagree = 0)
            
            new_pic.put()
        self.redirect(self.request.referer)


class FaceMakeUpPage(webapp2.RequestHandler):
    def get(self):
        print(MakeUpPics)
        facemakeup_query = MakeUpPics.query(MakeUpPics.category == "Face Make Up").order(-MakeUpPics.last_touch_date_time)
        print(facemakeup_query)
        print(ndb.ModelAttribute())
        
        template = jinja_env.get_template("templates/mainpage.html")
        self.response.write(template.render({"makeup_query": facemakeup_query}))
        

class EyeMakeUpPage(webapp2.RequestHandler):
    def get(self):
        eyemakeup_query = MakeUpPics.query(MakeUpPics.category == "Eye Make Up").order(-MakeUpPics.last_touch_date_time)

        template = jinja_env.get_template("templates/mainpage.html")
        self.response.write(template.render({"makeup_query": eyemakeup_query}))
        
class LipsPage(webapp2.RequestHandler):
    def get(self):
        lips_query = MakeUpPics.query(MakeUpPics.category == "Lips").order(-MakeUpPics.last_touch_date_time)

        template = jinja_env.get_template("templates/mainpage.html")
        self.response.write(template.render({"makeup_query": lips_query}))
        
class NailsPage(webapp2.RequestHandler):
    def get(self):
        nails_query = MakeUpPics.query(MakeUpPics.category == "Nails").order(-MakeUpPics.last_touch_date_time)

        template = jinja_env.get_template("templates/mainpage.html")
        self.response.write(template.render({"makeup_query": nails_query}))

class UpdateLikes(webapp2.RequestHandler):
    def post(self):
        """ Receives the updated round scores from a player after they complete a round. """
        print("Makeup_key" + self.request.get('makeup_key'))
        pin = ndb.Key(urlsafe=self.request.get('makeup_key')).get()
        agree = self.request.get("agree")
        if(agree == "true"):
            pin.agree = pin.agree+1
        else:
            pin.disagree = pin.disagree + 1
        pin.put()
        self.response.out.write(json.dumps({"agree": pin.agree, "disagree": pin.disagree}))
        
    
        
app = webapp2.WSGIApplication([
    ("/", MakeUpPicsPage),
    ("/insertpic", InsertPicAction),
    ("/facemakeup", FaceMakeUpPage),
    ("/eyemakeup", EyeMakeUpPage),
    ("/lips", LipsPage),
    ("/nails", NailsPage),
    ("/likesupdate", UpdateLikes)
], debug=True)
