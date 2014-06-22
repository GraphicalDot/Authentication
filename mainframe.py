#!/usr/bin/env python
#-*- coding:utf-8 -*-
import subprocess
import os
import wx
import re
import sys
import time
import itertools
import hashlib
from helpers import getHwAddr
from form import Form
import requests
import tempfile
import zipfile
import shutil
ID_ONE = 1
ID_TWO = 2
ID_THREE = 3

#This list has all the colors available in wx python


class CanvasPanel(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, -1, size=(310,300), pos=((wx.DisplaySize()[0])/2,(wx.DisplaySize()[1])/2), style=wx.CLOSE_BOX)

		self.hbox = wx.BoxSizer(wx.VERTICAL)
		self.panel = wx.Panel(self, 3, style=wx.RAISED_BORDER)

		font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
		font.SetPointSize(11)
		self.text = wx.StaticText(self.panel, label='Enter yoour personal authentication code')
		self.text.SetFont(font)

		self.button_box = wx.BoxSizer(wx.HORIZONTAL)
		self.button_panel = wx.Panel(self, 1, style=wx.RAISED_BORDER)
		self.button_one = wx.Button(self.button_panel, ID_ONE, label='Yes', size=(100, 30))
		self.button_two = wx.Button(self.button_panel, ID_TWO, label='No', size=(100, 30))
		self.button_three = wx.Button(self.button_panel, ID_THREE, label='Close', size=(100, 30))

		self.Bind(wx.EVT_BUTTON, self.yes_authentication_code, id=ID_ONE)
		self.Bind(wx.EVT_BUTTON, self.no_authentication_code, id=ID_TWO)
		self.Bind(wx.EVT_BUTTON, self.close_window, id=ID_THREE)

		self.button_box.Add(self.button_one)
		self.button_box.Add(self.button_two)
		self.button_box.Add(self.button_three)

		self.button_panel.SetSizer(self.button_box)
		self.hbox.Add(self.panel, 1, wx.EXPAND | wx.ALL, 3)
		self.hbox.Add(self.button_panel, 1, wx.EXPAND | wx.ALL, 3)
		self.SetSizer(self.hbox)
		self.SetBackgroundColour("light blue")
		self.Centre()
		self.Show()


	def no_authentication_code(self, event):
		dia = Form(self, -1, '')
		val = dia.ShowModal()
		dia.Destroy()
		return

	def close_window(self, event):
		self.Close()
	
	
	def yes_authentication_code(self, event):
		frame = wx.TextEntryDialog(self, "Enter the authentication code", "", style=wx.OK|wx.CANCEL)
		auth_token = frame.GetValue()
		
		working_dir = os.path.abspath(os.path.dirname(__file__))
		#This creates a new working directory with aprent directory in which this .exe is running by the name of the data
		if not os.path.exists("%s/Data"%working_dir):
			os.mkdir("%s/Data"%working_dir)

		path = "%s/Data/WholeZip.zip"%working_dir
		if frame.ShowModal() == wx.ID_OK:
			mac_id = getHwAddr("eth0")
			try:
				pdata={"mac_id": mac_id, "auth_token": frame.GetValue(), "path": os.path.exists(path)}
				response = requests.get("http://localhost:8989/v1/download",data= pdata)

				print response
			except requests.ConnectionError:
				raise StandardError("Your internet connection is not working")	
			
			self.handle_response(response, frame.GetValue())
		return

	def handle_response(self, response, key):
		working_dir = os.path.abspath(os.path.dirname(__file__))
		path = "%s/Data/WholeZip.zip"%working_dir
		encrypted_file_path = "%s/Data/file.zip"%working_dir
		try:
			response.json().get("error")
			print "Wrong auth token"
			return 
		except:
			pass

		if response.ok:
			if not os.path.exists(path):
				file_name = open(path, "w")
				file_name.write(response.content)
				file_name.close()
			
			if not os.path.exists(encrypted_file_path):
				with  cd("%s/Data/"%working_dir):
					print path
					zip_file = zipfile.ZipFile(path) 
					zipfile.ZipFile.extractall(zip_file)
				
			dirpath = tempfile.mkdtemp()
			print dirpath
			with  cd(dirpath):
				zip_file = zipfile.ZipFile(encrypted_file_path) 
				zipfile.ZipFile.extractall(zip_file, pwd=key)
				
				src = "%s/Data/"%working_dir
				import glob
				for filename in glob.glob(os.path.join(src, '*.*')):
					shutil.copy(filename, dirpath)

				subprocess.call(["ls"])
				subprocess.call(["wine", "Play me.exe"])
		
			print dirpath
			shutil.rmtree(dirpath)
		return


class cd:
	"""Context manager for changing the current working directory"""
	def __init__(self, newPath):
		self.newPath = newPath

	def __enter__(self):
		self.savedPath = os.getcwd()
		os.chdir(self.newPath)

	def __exit__(self, etype, value, traceback):
		os.chdir(self.savedPath)


def run_app():
	app = wx.PySimpleApp()
	app.frame = CanvasPanel()
	app.frame.Show(True)
	app.frame.Center()
	app.MainLoop()



if __name__ == "__main__":

	run_app()
