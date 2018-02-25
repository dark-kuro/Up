#!/usr/bin/env python
from api import Api
from pprint import pprint
from os import path


def main():
	parse = Api.args()
	args = parse.parse_args()
	if not path.isdir(args.path):raise
	pprint(args)
	api = Api()
	pprint(api)



if __name__ == '__main__':
	main()