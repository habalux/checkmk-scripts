#!/usr/bin/python
#
# Agent side plugin for checking apache virtualhosts
#
# The plugin gets virtualhosts from apache and lists them for
# the server component to check (not yet done!)
#
# Copyright (c) 2013, Teemu Haapoja <teemu.haapoja@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY
# OF SUCH DAMAGE.

import commands
import re
import sys

def test_https(host,port):
	if host == "*":
		host = "127.0.0.1"
	import urllib2
	try:
		urllib2.urlopen("https://%s:%s"%(host,port))
	except urllib2.URLError:
		return False
	return True

s,o = commands.getstatusoutput("apachectl -S")

if s != 0:
	# Not found, just exit.
	sys.exit(0)

print "<<<apache>>>"
for l in o.split('\n'):
	m = re.match(r'^(?P<hostname>\*|[0-9\.:]+):(?P<port>[0-9]+).*$',l)
	if m:
		attrs = m.groupdict()
		attrs['ssl'] = test_https(attrs['hostname'], attrs['port'])
		print "VIRTUALHOST %s"%( " ".join( ["%s=%s"%(k,v) for k,v in attrs.items()] ) )
