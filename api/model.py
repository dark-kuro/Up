class Base(object):
    def __repr__(self):
        return pformat(vars(self))

class Entry(Base):
    def __init__(self, json):
        self.json = json
        self.title = self.pop('title')
        self.num = self.pop('gphoto$numphotos')
        self.aid = self.pop('gphoto$id')

    def pop(self, key):
        value = self.json.pop(key, {})
        value = value.pop('$t', value)
        return value

class Feed(Base):
    def __init__(self, req):
        if not req.ok:
            print('ERROR:', req, req)
            print('ERROR TEXT:', req.text)
            return
        json = req.json()
        self.json = json = json.pop('feed', json)
        self.entry = json.pop('entry', json)
        self.entry = [Entry(i) for i in self.entry]

class Doc(object):
    def __init__(self, name):
        self.name = name

    def doc(self, typ):
        return open(self.name, typ, encoding='utf-8')

    def write(self, string):
        with self.doc('w') as w:
            w.write(string)

    def read(self):
        with self.doc('r') as r:
            read = r.read()
        return read.strip()
