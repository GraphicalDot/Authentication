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
		dia = Form()
		dia.Show()	
		return

	def close_window(self, event):
		self.Close()
	
	
	def yes_authentication_code(self, event):
		frame = wx.TextEntryDialog(self, "Enter the authentication code", "", style=wx.OK|wx.CANCEL)
		mac_id = getHwAddr("eth0")
		
		if frame.ShowModal() == wx.ID_OK:
			form_data={"mac_id": mac_id, "key": frame.GetValue(), "check_module": True, "path": False}
			response = requests.get("http://localhost:8989/v1/download",data= form_data)
			
			if response.json().get("error"):
				dlg = wx.MessageDialog(self, response.json().get("messege"), "Warning", wx.OK | wx.ICON_WARNING)
				dlg.ShowModal()
				dlg.Destroy()
				return
		
		module_name = response.json()["module_name"]
		hashkey = response.json()["hash"]
		user_os = sys.platform[:3]

		working_dir = os.path.abspath(os.path.dirname(__file__))
		#This creates a new working directory with aprent directory in which this .exe is running by the name of the data
		if not os.path.exists("%s/Data"%working_dir):
			os.mkdir("%s/Data"%working_dir)
			if not os.path.exists("%s/Data/%s"%(working_dir, module_name)):
				with cd("%s/Data"%working_dir):
					os.mkdir(module_name)
		
		
		path = "%s/Data/%s/%s_%s.zip"%(working_dir, module_name, user_os[:3], module_name)
		print path


		try:
				
			#SEcond time user
			if os.path.exists(path):
				self.already_registered_user(response, path, hashkey, module_name, user_os)
			
			else:
				form_data={"mac_id": mac_id, "key": frame.GetValue(), "path": False}
				response = requests.get("http://localhost:8989/v1/download",data= form_data)
				self.new_user(response, path, hashkey, module_name, user_os)

		except requests.ConnectionError:
			raise StandardError("Your internet connection is not working")	
		return

	def already_registered_user(self, response, path, hashkey, module_name, user_os):

		dirpath = tempfile.mkdtemp()
		print dirpath
		with  cd(dirpath):
				zip_file = zipfile.ZipFile(path) 
				zipfile.ZipFile.extractall(zip_file, pwd=hashkey)
				
				zip_file = zipfile.ZipFile("%s_%s.zip"%(user_os[:3], module_name))
				zipfile.ZipFile.extractall(zip_file)
				
				subprocess.call(["ls"])
				subprocess.call(["wine", "Play me.exe"])
		
		shutil.rmtree(dirpath)
		return


	def new_user(self, response, path, hashkey, module_name, user_os):
		#if path doesnt exists the response will have the zip file and this writes that encrypted zip file into the path
		file_name = open(path, "w")
		file_name.write(response.content)
		file_name.close()
		#Now the Data Folder do have WholeZip.zip and now the path exists

		dirpath = tempfile.mkdtemp()
		print dirpath
				
		form_data={"mac_id": getHwAddr("eth0"), "key": key, "path": True}
		response = requests.get("http://localhost:8989/v1/download", data= form_data)
		
		with  cd(dirpath):
				zip_file = zipfile.ZipFile(path) 
				zipfile.ZipFile.extractall(zip_file, pwd=response.json().get("hash"))
				
				zip_file = zipfile.ZipFile("Whole.zip")
				zipfile.ZipFile.extractall(zip_file)
				
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
