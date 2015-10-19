#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals

import os, re, sys

TAB_WIDTH = 4
FILE_SUFFIXES = '.h', '.hpp', '.cpp'
TAB_SPLIT = re.compile('\t').split

def edit_file(fname, function):
    changed = False
    outfile = fname + '.untab.'
    with open(fname) as f_in, open(outfile, 'w') as f_out:
        for line in f_in:
            new_line = function(line)
            f_out.write(new_line)
            changed = changed or (line != new_line)
    os.remove(fname)
    os.rename(outfile, fname)
    return changed

def edit_files(root, suffixes, function):
    for dirpath, dirnames, filenames in os.walk(root):
        for f in filenames:
            for s in suffixes:
                if f.endswith(s):
                    fname = os.path.join(dirpath, f)
                    if edit_file(fname, function):
                        print('Changed file', fname)

def to_field(s):
    return s + (TAB_WIDTH - len(s) % TAB_WIDTH) * ' '

def fix_tab(s):
    split = TAB_SPLIT(s)
    return ''.join(to_field(i) for i in split).rstrip() + '\n'

if __name__ == '__main__':
    root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    edit_files(root, FILE_SUFFIXES, fix_tab)
