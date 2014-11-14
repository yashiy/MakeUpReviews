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
import urllib

from google.appengine.api import images
from google.appengine.ext import blobstore
from google.appengine.ext import db
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers
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
        #makeup_query = MakeUpPics.query(ancestor=PARENT_KEY).order(-MakeUpPics.last_touch_date_time)
        print(self.request.get("sortby"))
        upload_url = blobstore.create_upload_url('/insertpic')
        if(self.request.get("sortby") == "pop"):
            
            makeup_query = MakeUpPics.query(ancestor=PARENT_KEY)
            makeup_list = makeup_query.fetch()
            images_list = []
            makeup_list = sorted(makeup_list, key=lambda makeup: -makeup.agree-makeup.disagree)
            for item in makeup_list:
                if item.image_url == "":
                    logging.warning(item.image_url_local)
                    images_list.append(images.get_serving_url(item.image_url_local))
                else:
                    images_list.append(item.image_url)
        else:
            images_list = []
            makeup_query = MakeUpPics.query(ancestor=PARENT_KEY).order(-MakeUpPics.last_touch_date_time)
            for item in makeup_query:
                if item.image_url == "":
                    images_list.append(images.get_serving_url(item.image_url_local))
                else:
                    images_list.append(item.image_url)
            makeup_list = makeup_query.fetch()
        template = jinja_env.get_template("templates/mainpage.html")
        
        self.response.write(template.render({"makeup_query": makeup_list, "upload_url": upload_url, "images_list":images_list}))
        
class InsertPicAction(blobstore_handlers.BlobstoreUploadHandler):
    print("at insert picture")
    def post(self):
        if(self.request.get("entity_key")):
            logging.info(self.request.get("entity_key"))
            
            weatherPic = ndb.Key(urlsafe=self.request.get("entity_key"))
            print("at insert picture, get key")

        else:
            print("at insert picture, inserting")
            upload_files = self.get_uploads("image_url_local")
            if (upload_files != []):
                blob_info = upload_files[0]
                blob_info = blob_info.key()
                image_url_2 = ""
            else:
                blob_info = None
                image_url_2 = self.request.get("image_url")
            new_pic = MakeUpPics(parent = PARENT_KEY,
                                  image_url = image_url_2,
                                  image_url_local = blob_info,
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
        upload_url = blobstore.create_upload_url('/insertpic')
        print(MakeUpPics)
        if(self.request.get("sortby") == "pop"):      
            facemakeup = MakeUpPics.query(MakeUpPics.category == "Face Make Up")
            facemakeup_list = facemakeup.fetch()
            facemakeup_query = sorted(facemakeup_list, key=lambda makeup: -makeup.agree-makeup.disagree) 
        else:
            facemakeup_query = MakeUpPics.query(MakeUpPics.category == "Face Make Up").order(-MakeUpPics.last_touch_date_time)

        images_list = []
        for item in facemakeup_query:
            
            if item.image_url == "":
                images_list.append(images.get_serving_url(item.image_url_local))
            else:
                images_list.append(item.image_url)
        template = jinja_env.get_template("templates/mainpage.html")
        self.response.write(template.render({"makeup_query": facemakeup_query, "images_list": images_list, "upload_url": upload_url   }))
        

class EyeMakeUpPage(webapp2.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/insertpic')
        if(self.request.get("sortby") == "pop"):
            eyemakeup = MakeUpPics.query(MakeUpPics.category == "Eye Make Up")
            eyemakeup_list = eyemakeup.fetch()
            eyemakeup_query = sorted(eyemakeup_list, key=lambda makeup: -makeup.agree-makeup.disagree) 
        else:
            eyemakeup_query = MakeUpPics.query(MakeUpPics.category == "Eye Make Up").order(-MakeUpPics.last_touch_date_time)
        images_list = []
        for item in eyemakeup_query:
            
            if item.image_url == "":
                images_list.append(images.get_serving_url(item.image_url_local))
            else:
                images_list.append(item.image_url)
        template = jinja_env.get_template("templates/mainpage.html")
        self.response.write(template.render({"makeup_query": eyemakeup_query, "upload_url": upload_url, "images_list": images_list}))
        
class LipsPage(webapp2.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/insertpic')
        if(self.request.get("sortby") == "pop"):
            lips = MakeUpPics.query(MakeUpPics.category == "Lips")
            lipsmakeup_list = lips.fetch()
            lips_query = sorted(lipsmakeup_list, key=lambda makeup: -makeup.agree-makeup.disagree) 
        else:
            lips_query = MakeUpPics.query(MakeUpPics.category == "Lips").order(-MakeUpPics.last_touch_date_time)
        images_list = []
        for item in lips_query:
            
            if item.image_url == "":
                images_list.append(images.get_serving_url(item.image_url_local))
            else:
                images_list.append(item.image_url)
        template = jinja_env.get_template("templates/mainpage.html")
        self.response.write(template.render({"makeup_query": lips_query, "upload_url": upload_url, "images_list": images_list}))
        
class NailsPage(webapp2.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/insertpic')
        if(self.request.get("sortby") == "pop"):
            nails = MakeUpPics.query(MakeUpPics.category == "Nails")
            nailsmakeup_list = nails.fetch()
            nails_query = sorted(nailsmakeup_list, key=lambda makeup: -makeup.agree-makeup.disagree) 
        else:
            nails_query = MakeUpPics.query(MakeUpPics.category == "Nails").order(-MakeUpPics.last_touch_date_time)
        images_list = []
        for item in nails_query:
            
            if item.image_url == "":
                images_list.append(images.get_serving_url(item.image_url_local))
            else:
                images_list.append(item.image_url)
        template = jinja_env.get_template("templates/mainpage.html")
        self.response.write(template.render({"makeup_query": nails_query, "upload_url": upload_url, "images_list": images_list}))

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
