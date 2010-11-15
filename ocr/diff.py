from subprocess import Popen, PIPE
import sys

NEWLINE = '\n'

class SourceFile(object):
    def __init__(self, path):
        with open(path) as fh:
            self.lines = fh.read().split(NEWLINE)
            self.name = fh.name

    @property
    def cols(self):
        longest = 0
        for line in self.lines:
            length = len(line)
            if length > longest:
                longest = length
        
        return longest

class Diff(object):
    def __init__(self, before, after):
        self._before = SourceFile(before)
        self._after = SourceFile(after)
        self.mid_point = self._before.cols
        self.lines = self.process()

    def __str__(self):
        text = NEWLINE.join([''.join(line) for line in self.lines])
        return text

    def _analyze(self, stdout):
        lines = []
        for line in stdout.split(NEWLINE):
            lines.append(self.parse(line))

        return lines

    @property
    def after(self):
        return NEWLINE.join(part[-1] for part in self.lines)

    @property
    def before(self):
        return NEWLINE.join(part[0] for part in self.lines)
        
    def calculate_delta(self, delta):
        mapping = {'>':'Added',
                   '|':'Modified',
                   ' ':'Same',
                   '<':'Removed'}

        return mapping[delta]

    def parse(self, line):
        zb_mid_point = self.mid_point - 1
        zb_mid_width = 3
        if line:
            before =  line[:zb_mid_point]
            after = line[zb_mid_point + zb_mid_width:]
            delta = line[zb_mid_point:zb_mid_point + zb_mid_width]
        else:
            before, after, delta = [''] * 3

        parts = [before, delta, after]
        return parts

    def pretty_print(self):
        print(self)

    def process(self):
        width = self._before.cols + self._after.cols
        cmd = 'diff --expand-tabs --width %s --side-by-side %s %s'
        cmd = cmd % (width, self._before.name, self._after.name)

        # Execute the command and capture output
        output = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = output.communicate()
        
        return self._analyze(stdout)

def main():
    diff1 = Diff('/tmp/couch.py.old', '/tmp/couch.py')
    diff2 = Diff('/tmp/env.py.old', '/tmp/env.py')
    #diff1.pretty_print()
    #print(diff1.before)
    #print(diff1.after)

if __name__ == '__main__':
    main()
