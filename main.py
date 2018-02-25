#!/usr/bin/env python
from api import Api
from pprint import pprint
from os import path

def main():
	parse = Api.args()
	args = parse.parse_args()
	# args = parse.parse_args(['..', '--noauth_local_webserver'])
	if not path.isdir(args.path):raise

	api = Api(flags=args)
	foo = api.foo()
	for i in Api.walk(args.path):
		print(i)
		# a = Api.ul(foo, i)
		a = api.up(i)
		print(a)
		pprint(a.json())
		# break
	# print(api.dropbox())



if __name__ == '__main__':
	main()