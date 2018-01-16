#!/usr/local/bin/python2.7
import json
from collections import OrderedDict

# Open json file
def open_json(directory, filename):
	json_data = []
	try:
		with open(directory+filename) as data_file:
			json_data = json.load(data_file, object_pairs_hook=OrderedDict)
	except ValueError:
		print "No JSON object could be decoded."
		exit()
	return json_data