#!/usr/bin/env python
#-*- coding: utf-8 -*-
import requests
import sys
import wx

link = "http://localhost:8000/v1/fake"
file_name = "/home/k/Desktop/fake.zip"
with open(file_name, "wb") as f:
	print "Downloading %s" % file_name
	response = requests.get(link, stream=True)
	total_length = response.headers.get('content-length')

	if total_length is None: # no content length header
		f.write(response.content)
	else:
		dl = 0
		total_length = int(total_length)
		wait = wx.BusyCursor()
		for data in response.iter_content():
			dl += len(data)
			f.write(data)
			done = int(50 * dl / total_length)
			print done
			sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
			sys.stdout.flush()
		del wait
