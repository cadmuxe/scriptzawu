"""TODO(koonwah): DO NOT SUBMIT without one-line documentation for paser_hey_output.

TODO(koonwah): DO NOT SUBMIT without a detailed description of paser_hey_output.
"""
from __future__ import print_function

import re
import sys

p = re.compile("((Fri|Sat|Sun|Mon) \d* Jun 2019 \d{2}:\d{2}:\d{2} (PM|AM) PDT)")
ps = re.compile("(\[(\d*)\]\W*(\d*) responses)")
f = open("hey_log.ig.txt", "r")
lines = f.readlines()

for line in lines:
  result = p.search(line)
  if result:
    print("\n %s" % result.group(), end='')

  result = ps.search(line)
  if result:
    print("\t%s" % result.group(), end='')


