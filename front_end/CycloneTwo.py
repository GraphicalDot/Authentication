#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import wx
import requests
import time
import subprocess
import os
import wx
import re
import sys
import time
import itertools
import hashlib
import tempfile
import zipfile
import shutil
import base64
from uuid import getnode as get_mac


ID_ONE = 1
ID_TWO = 2
ID_THREE = 3

import socket, struct
url = "http://23.239.29.14:8080"
#url = "http://localhost:8000"
class Authentication(wx.Dialog):
	
	def __init__(self, parent, id=-1, title="Authentication Window"):
		wx.Dialog.__init__(self, parent, id, title, size=(-1, -1))
		
		self.mainSizer = wx.BoxSizer(wx.VERTICAL)
		self.buttonSizer = wx.BoxSizer(wx.HORIZONTAL)

		self.label = wx.StaticText(self, label="Enter Key:")
		self.field = wx.TextCtrl(self, value="", size=(300, 30))
		self.okbutton = wx.Button(self, label="Ok", id=wx.ID_OK)
		self.cancelbutton = wx.Button(self, label="Cancel", id=wx.ID_OK)

		self.mainSizer.Add(self.label, 0, wx.ALL, 8 )
		self.mainSizer.Add(self.field, 0, wx.ALL, 8 )

		self.buttonSizer.Add(self.okbutton, 0, wx.ALL, 8 )
		self.buttonSizer.Add(self.cancelbutton, 0, wx.ALL, 8 )

		self.mainSizer.Add(self.buttonSizer, 0, wx.ALL, 0)

		self.Bind(wx.EVT_BUTTON, self.onOK, id=wx.ID_OK)
		self.Bind(wx.EVT_TEXT_ENTER, self.onOK)

		self.SetSizerAndFit(self.mainSizer)
		self.result = None

	def onOK(self, event):
		self.result = self.field.GetValue()
		self.Destroy()

	def onCancel(self, event):
		self.result = None
		self.Destroy()




def getHwAddr():
	return get_mac()

class Form(wx.Frame):
	def __init__(self):

		self.payment_receipt_image = None
		self.form_data = dict()
		w = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X)
		h = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)
		#wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.MINIMIZE_BOX
           	wx.Frame.__init__(self, None, 1, size=(400,500), pos=(w/2, h/3), style=wx.DEFAULT)          
		
		self.pnl = wx.Panel(self)
		vbox = wx.BoxSizer(wx.VERTICAL)

		sb = wx.StaticBox(self.pnl, label='user form')
		sbs = wx.StaticBoxSizer(sb, orient=wx.VERTICAL)        
        
		vbox1 = wx.BoxSizer(wx.VERTICAL)       

		vbox1.Add((0,30))
		hbox1 = wx.BoxSizer(wx.HORIZONTAL)
		hbox1.Add(wx.StaticText(self.pnl, label='First Name'))
		hbox1.Add(wx.TextCtrl(self.pnl, size= (200, 30), name="first_name"), flag=wx.LEFT, border=50)
		vbox1.Add(hbox1)
		vbox1.Add((0,15))


		hbox1 = wx.BoxSizer(wx.HORIZONTAL)
		hbox1.Add(wx.StaticText(self.pnl, label='Last Name'))
		hbox1.Add(wx.TextCtrl(self.pnl, size= (200, 30), name="second_name"), flag=wx.LEFT, border=50)
		vbox1.Add(hbox1)
		vbox1.Add((0,15))
		
		
		hbox1 = wx.BoxSizer(wx.HORIZONTAL)
		hbox1.Add(wx.StaticText(self.pnl, label='Email Id'))
		hbox1.Add(wx.TextCtrl(self.pnl, size= (200, 30), name="email_id"), flag=wx.LEFT, border=70)
		vbox1.Add(hbox1)
		vbox1.Add((0,15))
		
		hbox1 = wx.BoxSizer(wx.HORIZONTAL)
		hbox1.Add(wx.StaticText(self.pnl, label='Country'))
		hbox1.Add(wx.TextCtrl(self.pnl, size= (200, 30), name="country"), flag=wx.LEFT, border=71)
		vbox1.Add(hbox1)
		vbox1.Add((0,15))
		

		hbox1 = wx.BoxSizer(wx.HORIZONTAL)
		choose_button = wx.Button(self.pnl, label='Payment jpeg', id=wx.ID_ANY) 
		self.Bind(wx.EVT_BUTTON,  self.OnOpen, id=choose_button.GetId())
		hbox1.Add(choose_button, flag=wx.LEFT, border=5)
		self.control = wx.TextCtrl(self.pnl, size= (200, 30), name="jpeg image", style=wx.TE_MULTILINE)
		hbox1.Add(self.control, flag=wx.LEFT, border = 66)
		vbox1.Add(hbox1)
		vbox1.Add((0,15))
		
		
		courses = ["Accounting", "Economics", "Finance", "Philosophy"]
		hbox1 = wx.BoxSizer(wx.HORIZONTAL)
		hbox1.Add(wx.StaticText(self.pnl, label='Modules'))
		hbox1.Add(wx.ComboBox(self.pnl, size= (200, 30), choices=courses, name="modules", style= wx.CB_DROPDOWN|wx.CB_READONLY), flag=wx.LEFT, border=66)
		vbox1.Add(hbox1)
		vbox1.Add((0,15))
		
		


		sbs.Add(vbox1)
        
		self.pnl.SetSizer(sbs)
       
		button_box = wx.BoxSizer(wx.HORIZONTAL)
		submitButton = wx.Button(self, label='Submit', id=wx.ID_ANY)
		self.Bind(wx.EVT_BUTTON,  self.OnSubmit, id=submitButton.GetId())
		
		closeButton = wx.Button(self, label='Close', id=wx.ID_ANY)
		self.Bind(wx.EVT_BUTTON,  self.OnClose, id=closeButton.GetId())
		button_box.Add(submitButton)
		button_box.Add(closeButton, flag=wx.LEFT, border=5)

		vbox.Add(self.pnl, proportion=1, flag=wx.ALL|wx.EXPAND, border=5)
		vbox.Add(button_box, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

		self.SetSizerAndFit(vbox)
        
	def OnSubmit(self, event):
		print "Onsubmit has been clicked"
		for child in self.pnl.GetChildren():
			if isinstance(child, wx.TextCtrl): 
				if not bool(child.GetValue()):
					dlg = wx.MessageDialog(self, "%s cannot be left empty"%child.GetName(), "Warning", wx.OK | wx.ICON_WARNING)
					dlg.ShowModal()
					dlg.Destroy()
					return

				self.form_data[child.GetName()] = child.GetValue()
			if isinstance(child, wx.ComboBox): 
				if not bool(child.GetValue()):
					dlg = wx.MessageDialog(self, "%s cannot be left empty"%child.GetName(), "Warning", wx.OK | wx.ICON_WARNING)
					dlg.ShowModal()
					dlg.Destroy()
					return
				self.form_data[child.GetName()] = child.GetValue()
		
		self.form_data["platform"] = sys.platform
		self.form_data["mac_id"] = getHwAddr()
		self.form_data["payment_receipt_image"] = self.payment_receipt_image
		response = requests.post("%s/v1/register_user"%url, data=self.form_data)
		dlg = wx.MessageDialog(self, response.json().get("messege"), "Notification", wx.OK | wx.ICON_WARNING)
		dlg.ShowModal()
		dlg.Destroy()
		print response.text
		print self.form_data
		
		
		self.Destroy()
		return

        def OnClose(self, e):
        	self.Destroy()
        

	def OnOpen(self,e):
		""" Open a file"""
		self.dirname = ''
		dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
		if dlg.ShowModal() == wx.ID_OK:
			self.filename = dlg.GetFilename()
			self.dirname = dlg.GetDirectory()
			f = open(os.path.join(self.dirname, self.filename), 'rb')
			self.control.SetValue(os.path.join(self.dirname, self.filename))
			self.payment_receipt_image = base64.encodestring(f.read())
			print self.payment_receipt_image
			f.close()
		dlg.Destroy()


#This list has all the colors available in wx python


class CanvasPanel(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, -1, size=(510,300), pos=((wx.DisplaySize()[0])/2,(wx.DisplaySize()[1])/2), style=wx.CLOSE_BOX)

		self.hbox = wx.BoxSizer(wx.VERTICAL)
		self.panel = wx.Panel(self, 3, style=wx.RAISED_BORDER)

		font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
		font.SetPointSize(8)
		text = """    Welcome to Cyclone2  
		
				If you have your own personal authentication code, 
				Please press yes Otherwise, press no to make a new registration.
		"""   

		self.text = wx.StaticText(self.panel, label=text)
		self.text.SetFont(font)

		self.button_box = wx.BoxSizer(wx.HORIZONTAL)
		self.button_panel = wx.Panel(self, 1, style=wx.RAISED_BORDER)
		self.button_one = wx.Button(self.button_panel, ID_ONE, label='Yes', size=(160, 30))
		self.button_two = wx.Button(self.button_panel, ID_TWO, label='No', size=(160, 30))
		self.button_three = wx.Button(self.button_panel, ID_THREE, label='Close', size=(160, 30))

		self.Bind(wx.EVT_BUTTON, self.yes_authentication_code, id=ID_ONE)
		self.Bind(wx.EVT_BUTTON, self.no_authentication_code, id=ID_TWO)
		self.Bind(wx.EVT_BUTTON, self.close_window, id=ID_THREE)

		self.button_box.Add(self.button_one, wx.ALIGN_LEFT|wx.EXPAND)
		self.button_box.Add(self.button_two, wx.ALIGN_CENTER|wx.EXPAND)
		self.button_box.Add(self.button_three, wx.ALIGN_RIGHT|wx.EXPAND)

		self.button_panel.SetSizer(self.button_box)
		self.hbox.Add(self.panel, 2, wx.EXPAND | wx.ALL, 3)
		self.hbox.Add(self.button_panel, 1, wx.EXPAND | wx.ALL, 3)
		self.SetSizerAndFit(self.hbox)
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
		#frame = wx.TextEntryDialog(self, "Enter the authentication code", "", style=wx.OK|wx.CANCEL)
		frame = Authentication(self)
		frame.ShowModal()
		mac_id = getHwAddr()
		
		if not frame.result:
			return

		form_data={"mac_id": mac_id, "key": frame.result, "check_module": True, "path": False}
		response = requests.get("%s/v1/download"%url,data= form_data)
			
		print response.json()	
		
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
		
		
		path = "%s/Data/%s/%s_%s.zip"%(working_dir, module_name, user_os[:3], module_name)
		print path

		try:
				
			#SEcond time user
			if os.path.exists(path):
				self.already_registered_user(response, path, hashkey, module_name, user_os)
			
			else:
				if not os.path.exists("%s/Data"%working_dir):
					os.mkdir("%s/Data"%working_dir)
					if not os.path.exists("%s/Data/%s"%(working_dir, module_name)):
						with cd("%s/Data"%working_dir):
							os.mkdir(module_name)
				print "Path dowsnt exixts on this user machine"
				form_data={"mac_id": mac_id, "key": frame.result, "path": False}
				response = requests.get("%s/v1/download"%url, data= form_data)
				self.new_user(response, path, frame.result, module_name, user_os)

		except requests.ConnectionError:
			raise StandardError("Your internet connection is not working")	
		return
	def already_registered_user(self, response, path, hashkey, module_name, user_os):

		dirpath = tempfile.mkdtemp()
		print dirpath
		print path
		with  cd(dirpath):
				zip_file = zipfile.ZipFile(path) 
				print "path file is corrupted or not %s"%zip_file.testzip()
				zipfile.ZipFile.extractall(zip_file, pwd=hashkey)
				
				zip_file = zipfile.ZipFile("%s_%s.zip"%(user_os[:3], module_name))
				print "path file is corrupted or not %s"%zip_file.testzip()
				zipfile.ZipFile.extractall(zip_file)
				
				if user_os == "win":

					subprocess.call(["ls"])
					subprocess.call(["wine", "Play me.exe"])
				elif user_os == "lin":
					subprocess.call(["ls"])
					subprocess.call(["wine", "Play me.exe"])
				
				else:
					print "user os cannot be determined"
		
		shutil.rmtree(dirpath)
		return


	def new_user(self, response, path, key, module_name, user_os):
		#if path doesnt exists the response will have the zip file and this writes that encrypted zip file into the path
		zf = zipfile.ZipFile(path, mode='w')
		zf.write(response.content)
		zf.close()
		#Now the Data Folder do have WholeZip.zip and now the path exists

		dirpath = tempfile.mkdtemp()
		print "This is the dir path %s"%dirpath
				
		form_data={"mac_id": getHwAddr(), "key": key, "path": True}
		response = requests.get("%s/v1/download"%url, data= form_data)
		
		print 
		with  cd(dirpath):
				zip_file = zipfile.ZipFile(path) 
				print "path file is corrupted or not %s"%zip_file.testzip()
				zipfile.ZipFile.extractall(zip_file, pwd=response.json().get("hash"))
				
				zip_file = zipfile.ZipFile("%s_%s.zip"%(user_os[:3], module_name)) 
				print "path file is corrupted or not %s"%zip_file.testzip()
				zipfile.ZipFile.extractall(zip_file)
				
				if user_os == "win":

					subprocess.call(["ls"])
					subprocess.call(["wine", "Play me.exe"])
				elif user_os == "lin":
					subprocess.call(["ls"])
					subprocess.call(["wine", "Play me.exe"])
				
				else:
					print "user os cannot be determined"
	
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
	app = wx.App(False)
	app.frame = CanvasPanel()
	app.frame.Show(True)
	app.frame.Center()
	app.MainLoop()



if __name__ == "__main__":

	run_app()
