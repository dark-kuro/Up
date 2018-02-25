from .api import BaseApi
from .model import 

try:
	from urllib.parse import urljoin
except ImportError:
	from urlparse import urljoin

class Api(BaseApi):
	PHOTOS = 'https://picasaweb.google.com/data/'
	def api_join(self, *args):
		return urljoin(self.PHOTOS, *args)
