#!/usr/bin/env python
from api import Api
from pprint import pprint
from os import path

from requests import Request

print(Request)

exit()

def main():
	parse = Api.args()
	args = parse.parse_args()
	args = parse.parse_args(['..', '--noauth_local_webserver'])
	if not path.isdir(args.path):raise

	api = Api(flags=args)
	# for i in Api.walk(args.path):
		# print(i)
	print(api.dropbox())



if __name__ == '__main__':
	main()