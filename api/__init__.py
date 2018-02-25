from .api import BaseApi
from .model import (Feed, Doc)

from .requests_futures.sessions import FuturesSession



try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

class Api(BaseApi):
    def api_join(self, *args):
        return urljoin(self.PHOTOS, *args)

    def default(self, **params):# Note: it results on albums page and num of photos
        json = self.get(self.api_join('feed/api/user/default/'), params=params)
        return Feed(json)

    def dropbox_album_id(self):
        feed = self.default(fields='entry(title,gphoto:numphotos,gphoto:id)')
        aid = None
        for i in feed.entry:
            if i.title == 'Drop Box':
                aid = i.aid
                break
        return aid

    def get_dropbox(self, params={'fields':'entry(title),gphoto:numphotos', 'kind':'photo', 'max-results': '999999999'}):
        doc = Doc(self.join('.dropbox'))
        try:
            aid = doc.read()
            if not aid:raise
        except:
            aid = self.dropbox_album_id()
            if not aid:
                print("Album Id Empty")
                return []
            doc.write(aid)
        url = self.api_join('feed/api/user/default/albumid/{}'.format(aid))
        req = self.get(url, params=params)
        if not req.ok:
            print("Perhaps Drop Box Album is not found", req)
            doc.write('')
            return None
        return req

    def _dropbox(self):
        req = self.get_dropbox()
        if not req:
            return []

        feed = Feed(req)
        return [i.title for i in feed.entry]

    def get_dropbox_size(self):
        json = self.get_dropbox({'fields':'gphoto:numphotos'}).json()
        json = json.get('feed', json)
        json = json.get('gphoto$numphotos', {})
        json = json.get('$t', '')
        return json

    def dropbox(self):
        try:
            return self.up_media
        except:
            self.up_media = self._dropbox()
            return self.dropbox()

    def default_album(self):
        return self.api_join('feed/api/user/default/albumid/default')

    @classmethod
    def ul(self, api, name):
        return api.post(api.prefix, **self.data(name))

    def up(self, name):
        self.api.prefix = self.default_album()
        return self.ul(self.api, name)

    def foo(self, num=5):
        f = FuturesSession(max_workers=num, session=self.api)
        f.prefix = self.default_album()
        return f