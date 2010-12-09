# Python imports
from subprocess import Popen, PIPE
import ConfigParser
import json
import optparse
import os
import re
import sys
import urllib2
import webbrowser

config = ConfigParser.ConfigParser({'url':'http://localhost:8080'})
config.read(os.path.expanduser('~/.pubdiffrc'))

AFTER = 'after'
BEFORE = 'before'
CONTENTS = 'contents'
NAME = 'name'
URL = config.get('core', 'url') + '/api/upload'
VERSION = '0.0.1.dev'

class SourceFile(dict):
    def __init__(self, name=None, contents=None):
        self[NAME] = name
        self[CONTENTS] = contents

class Diff(dict):
    def __init__(self, before, after):
        self[BEFORE] = before
        self[AFTER] = after

class DiffParser(object):
    def __init__(self, stdin):
        self.cwd = os.getcwd()
        self.diff = stdin.split('\n')

    def diffs(self):
        raise NotImplementedError('fetch_diffs() must be implementd')

    def shell(self, cmd):
        output = Popen(cmd, cwd=self.cwd, shell=True, stdout=PIPE, stderr=PIPE)
        return output.communicate()

class GitParser(DiffParser):
    RE_FILE_NAMES = re.compile(r'a/(?P<before>.*) b/(?P<after>.*)')
    RE_PATTERN = re.compile(r'^diff --git')
    RE_BLOBS = re.compile(r'index '
                          r'(?P<before>[a-z0-9]{7,})\.\.'
                          r'(?P<after>[a-z0-9]{7,}) '
                          r'(?P<perms>[0-9]{6})')

    def source(self, name, blob):
        cmd = 'git show %s -- %s' % (blob, name)
        stdout, stderr = self.shell(cmd)

        # If the index hash specified in the diff doesn't exist, this
        # might be a unstaged/cached change.  We can validate by
        # comparing the hash in the diff, with the hash of the file on
        # disk, if the same... use that file exactly as is.  Once they
        # add the change to the index, git show will be able to fetch
        # the contents by the hash (avoiding this lookup).
        if 'bad revision' in stderr:
            cmd = 'git hash-object %s' % name
            stdout, stderr_inner = self.shell(cmd)
            if stdout.startswith(blob):
                stdout = open(name).read()
            else:
                print('Error when running:', cmd)
                print(stderr)

        return SourceFile(name, stdout)

    def fetch_source_files(self, names, blobs):
        before = self.source(names.group('before'), blobs.group('before'))
        after = self.source(names.group('after'), blobs.group('after'))
        return Diff(before, after)

    def fetch_diffs(self):
        diffs = []

        for i, line in enumerate(self.diff):
            blobs = GitParser.RE_BLOBS.match(line)
            if blobs:
                names = GitParser.RE_FILE_NAMES.search(self.diff[i - 1])
                diffs.append(self.fetch_source_files(names, blobs))

        return diffs

class Client(object):
    def __init__(self):
        self.stdin = sys.stdin.read()
        self.parser = self.fetch_parser(self.stdin)

    def fetch_parser(self, diff):
        for cls in [GitParser]:
            if cls.RE_PATTERN.match(diff):
                return cls(self.stdin)

        msg = 'Your diff appears to be unsupported'
        raise UnsupportedClientError(msg)

    def main(self):
        # Parse command line options
        (options, args) = self.getopts()

        diffs = self.parser.fetch_diffs()
        if diffs:
            if os.environ.get('debug'):
                for diff in diffs:
                    print('Before:')
                    print(diff['before']['contents'][:100])
                    print('After:')
                    print(diff['after']['contents'][:100])

            request = urllib2.Request(URL, json.dumps(diffs))
            response = urllib2.urlopen(request)
            payload = json.loads(response.read())
            if payload['success']:
                url = payload['data']['url']

                if options.browser:
                    webbrowser.open(url)

                print(url)
            else:
                print(payload['exception'])


    def getopts(self):
        p = optparse.OptionParser('Usage: %prog [options]')
        p.add_option('-b', '--browser', dest='browser', action='store_true')
        p.set_defaults(browser=False)

        return p.parse_args()

class UnsupportedClientError(Exception):
    pass

def main():
    client = Client()
    client.main()

if __name__ == '__main__':
    main()
