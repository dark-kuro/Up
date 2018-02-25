from oauth2client import tools
from argparse import ArgumentParser
import os
import urllib3.fields

from oauth2client import (client, tools)
from oauth2client.file import Storage

from google.auth.transport.requests import AuthorizedSession
from google.oauth2.credentials import Credentials

import json
from os import path
import sys

class UploadWithProgress(object):
    def __init__(self, filename, chunksize=1 << 13):
        self.filename = filename
        self.name = os.path.basename(filename)

        self.chunksize = chunksize
        self.totalsize = os.path.getsize(filename)
        self.readsofar = 0

    def __iter__(self):
        with open(self.filename, 'rb') as file:
            while True:
                data = file.read(self.chunksize)
                if not data:
                    sys.stderr.write("\n")
                    break
                self.readsofar += len(data)
                percent = self.readsofar * 1e2 / self.totalsize
                sys.stderr.write('\r{percent:3.0f}%'.format(percent=percent), flush=True)
                yield data

    def __len__(self):
        return self.totalsize

class BaseApi(object):
    DIR = path.dirname(path.abspath(__file__))

    def join(self, *args):
        return path.join(self.DIR, *args)

    @staticmethod
    def args():
        parser = ArgumentParser(description='Upload photos to Google Photos', parents=[ tools.argparser ])
        parser.add_argument('path', 
            metavar='PATH',
            help='Folder containing media files',
            nargs='?',
            default='.')
        return parser

    @staticmethod
    def walk(directory='.', media=('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')):
        for (dirpath, dirnames, filenames) in os.walk(directory):
            for filename in filenames:
                if not filename.endswith(media):
                    continue
                filename = os.path.join(dirpath, filename)
                yield filename

    @staticmethod
    def data(name):
        it = UploadWithProgress(name)
        return {
            'headers':{'Content-Type':urllib3.fields.guess_content_type(name), 'Slug':it.name},
            'data':it,
            'params':{'fields':'media:group'}
        }

    PHOTOS = 'https://picasaweb.google.com/data/'

    def auth(self, client_info, scope=[PHOTOS], flags=None):
        self.store = Storage(self.join('.user_auth.json'))
        credentials = self.store.get()
        if not credentials:
            credentials = tools.run_flow(
                client.flow_from_clientsecrets(client_info, scope=scope), 
                self.store, 
                flags)

        credentials = json.loads(credentials.to_json()) # hack, TODO find better way

        self.credentials = Credentials.from_authorized_user_info(credentials)

        return AuthorizedSession(self.credentials)

    def __init__(self, client_info=None, flags=None):
        api = self.auth(self.join('client_info.json') if not client_info else client_info, flags=flags)
        api.headers['GData-Version'] = '3'
        api.params['alt'] = 'json'
        api._refresh_status_codes += (403, )

        self.get = api.get
        self.api = api
