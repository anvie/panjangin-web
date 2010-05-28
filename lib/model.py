
from google.appengine.ext import db



	
class PjSession(db.Model):
	
	ip_address = db.StringProperty()
	agent = db.StringProperty()
	# urls = relation from UrlRecord
	
	
class UrlRecord(db.Model):
	
	orig_url = db.StringProperty()
	gen_url = db.StringProperty()
	code = db.StringProperty()
	mbr = db.StringProperty(multiline=True)
	_session = db.ReferenceProperty(PjSession,collection_name="urls")
	
	@property
	def hits_count(self):
		return self.hits.count()
		
	@property
	def hits_str(self):
		if self.hits_count > 0:
			return "%d hits" % self.hits_count
		elif self.hits_count == 1:
			return "%d hit" % self.hits_count
		return ""
	
class HitCounter(db.Model):
	
	url_referer = db.StringProperty(default="direct")
	agent = db.StringProperty(default="unknown")
	_url_record = db.ReferenceProperty(UrlRecord,collection_name="hits")
	