# Python imports
import json
import os
import sys
import urllib2

URL = 'http://localhost:8080/api/upload'

def consume_source(path):
    source = {}
    with open(path) as fh:
        source['contents'] = fh.read()
        source['name'] = fh.name

    return source

def package_source(before, after):
    package = {}
    package['before'] = consume_source(before)
    package['after'] = consume_source(after)

    return package

def main():
    diffs = []
    diffs.append(package_source('/tmp/couch.py.old', '/tmp/couch.py'))
    diffs.append(package_source('/tmp/env.py.old', '/tmp/env.py'))

    request = urllib2.Request(URL, json.dumps(diffs))
    response = urllib2.urlopen(request)
    print response.read()

if __name__ == '__main__':
    main()
