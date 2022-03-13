#!/usr/bin/python3

import json
import glob
import sys
import os

objects = {}

def add(verb, key):
	if not verb in objects:
		objects[verb] = []
	objects[verb].append(key)

def analyze_file(json_file):
	with open(json_file, 'r') as file:
		data = json.load(file)
		for record in data['Records']:
			if record['eventSource'] != 's3.amazonaws.com':
				continue
			
			if record['managementEvent']:
				continue
			
			eventName = record['eventName']
			params = record['requestParameters']
			
			if eventName == 'ListObjects':
				add(eventName, params['prefix'])
			elif eventName == 'HeadBucket' or eventName == 'DeleteObjects' or eventName == 'ListObjectVersions':
				continue
			else:
				add(eventName, '{}\t{}\t{}'.format(record['eventTime'], record['sourceIPAddress'], params['key']))

def print_summary():
	for verb in objects:
		print('{} - {}'.format(verb, len(objects[verb])))

def write_result_files():
	for verb in objects:
		with open('{}-list.txt'.format(verb), 'w') as file:
			files = objects[verb]
			files.sort()
			for obj in files:
				file.write('{}\n'.format(obj))

for log_file in glob.glob(sys.argv[1] + '/**/*.json', recursive=True):
	print('Analyzing {}'.format(log_file))
	analyze_file(log_file)

print_summary()
write_result_files()
