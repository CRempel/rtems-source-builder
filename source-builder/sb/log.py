#
# RTEMS Tools Project (http://www.rtems.org/)
# Copyright 2010-2012 Chris Johns (chrisj@rtems.org)
# All rights reserved.
#
# This file is part of the RTEMS Tools package in 'rtems-testing'.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

#
# Log output to stdout and/or a file.
#

import os
import sys

import error

#
# A global log.
#
default = None

def set_default_once(log):
    if default is None:
        default = log

def output(text = os.linesep, log = None):
    """Output the text to a log if provided else send it to stdout."""
    if text is None:
        text = os.linesep
    if type(text) is list:
        _text = ''
        for l in text:
            _text += l + os.linesep
        text = _text
    if log:
        log.output(text)
    elif default is not None:
        default.output(text)
    else:
        for l in text.replace(chr(13), '').splitlines():
            print l

def flush(log = None):
    if log:
        log.flush()
    elif default is not None:
        default.flush()

class log:
    """Log output to stdout or a file."""
    def __init__(self, streams = None):
        self.fhs = [None, None]
        if streams:
            for s in streams:
                if s == 'stdout':
                    self.fhs[0] = sys.stdout
                elif s == 'stderr':
                    self.fhs[1] = sys.stderr
                else:
                    try:
                        self.fhs.append(file(s, 'w'))
                    except IOError, ioe:
                         raise error.general("creating log file '" + s + \
                                             "': " + str(ioe))

    def __del__(self):
        for f in range(2, len(self.fhs)):
            self.fhs[f].close()

    def has_stdout(self):
        return self.fhs[0] is not None

    def has_stderr(self):
        return self.fhs[1] is not None

    def output(self, text):
        """Output the text message to all the logs."""
        # Reformat the text to have local line types.
        out = ''
        for l in text.replace(chr(13), '').splitlines():
            out += l + os.linesep
        for f in range(0, len(self.fhs)):
            if self.fhs[f] is not None:
                self.fhs[f].write(out)

    def flush(self):
        """Flush the output."""
        for f in range(0, len(self.fhs)):
            if self.fhs[f] is not None:
                self.fhs[f].flush()

if __name__ == "__main__":
    l = log(['stdout', 'log.txt'])
    for i in range(0, 10):
        l.output('hello world: %d\n' % (i))
    l.output('hello world CRLF\r\n')
    l.output('hello world NONE')
    l.flush()
    del l