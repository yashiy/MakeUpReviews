from google.appengine.ext import ndb


class MakeUpPics(ndb.Model):
    image_url = ndb.StringProperty()
    caption = ndb.StringProperty()
    brand = ndb.StringProperty()
    category = ndb.StringProperty()
    last_touch_date_time = ndb.DateTimeProperty(auto_now=True)