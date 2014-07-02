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
from Progressbar import Run_Unzip, Run_Download


ID_ONE = 1
ID_TWO = 2
ID_THREE = 3

import socket, struct
url = "http://23.239.29.14:8080"
#url = "http://localhost:8000"
class Authentication(wx.Dialog):
	
	def __init__(self, parent, id=-1, title="Authentication Window"):
		wx.Dialog.__init__(self, parent, id, title, size=(-1, -1), style= wx.STAY_ON_TOP)
		
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
		self.form_data = dict()
                
		w = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X)
                h = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)
                #wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.MINIMIZE_BOX
                wx.Frame.__init__(self, None, 1, size=(400,500), pos=(w/2, h/3), style=wx.DEFAULT|wx.STAY_ON_TOP|wx.FRAME_FLOAT_ON_PARENT)

                self.pnl = wx.Panel(self)

                topsizer = wx.BoxSizer(wx.VERTICAL)


                gridSizer = wx.GridSizer(rows=6, cols=2, hgap=5, vgap=8)
                titleSizer = wx.BoxSizer(wx.HORIZONTAL)


                title = wx.StaticText(self, label="""This is the user form to be filled to register to play Modules selected, 
                Please ensure to fill the module and email id correctly""",)
                titleSizer.Add(title, 0, wx.ALL, 5)



                gridSizer.Add(wx.StaticText(self.pnl, label='First Name'), wx.ALIGN_RIGHT)
                gridSizer.Add(wx.TextCtrl(self.pnl, size= (200, 30), name="first_name"), 0, wx.EXPAND)


                gridSizer.Add(wx.StaticText(self.pnl, label='Last Name'), wx.ALIGN_RIGHT)
                gridSizer.Add(wx.TextCtrl(self.pnl, size= (200, 30), name="second_name"), 0, wx.EXPAND)

                gridSizer.Add(wx.StaticText(self.pnl, label='Email Id'), wx.ALIGN_RIGHT)
                gridSizer.Add(wx.TextCtrl(self.pnl, size= (200, 30), name="email_id"), 0, wx.EXPAND)


                gridSizer.Add(wx.StaticText(self.pnl, label='Country'), wx.ALIGN_RIGHT)
                gridSizer.Add(wx.TextCtrl(self.pnl, size= (200, 30), name="country"), 0, wx.EXPAND)


		choose_button = wx.Button(self.pnl, label='Payment jpeg', id=wx.ID_ANY) 
		self.Bind(wx.EVT_BUTTON,  self.OnOpen, id=choose_button.GetId())
		gridSizer.Add(choose_button, wx.ALIGN_RIGHT)
		self.control=wx.TextCtrl(self.pnl, size= (200, 30), name="jpeg image")
		gridSizer.Add(self.control, 0, wx.EXPAND)




                courses = ["English", "Economics", "Accounts", "Geography", "Business Studies", "Life Sciences"]
                gridSizer.Add(wx.StaticText(self.pnl, label='Modules'), wx.ALIGN_RIGHT)
                gridSizer.Add(wx.ComboBox(self.pnl, size= (200, 30), choices=courses, name="modules", style= wx.CB_DROPDOWN|wx.CB_READONLY),0, wx.EXPAND)



                self.pnl.SetSizer(gridSizer)

                button_box = wx.BoxSizer(wx.HORIZONTAL)
                submitButton = wx.Button(self, label='Submit', id=wx.ID_ANY)
                self.Bind(wx.EVT_BUTTON,  self.OnSubmit, id=submitButton.GetId())

                closeButton = wx.Button(self, label='Close', id=wx.ID_ANY)
                self.Bind(wx.EVT_BUTTON,  self.OnClose, id=closeButton.GetId())
                button_box.Add(submitButton)
                button_box.Add(closeButton, flag=wx.LEFT, border=5)
                topsizer.Add(titleSizer, 0, wx.CENTER, 5)
                topsizer.Add(wx.StaticLine(self), 0, wx.ALL|wx.EXPAND, 5)
                topsizer.Add((10, 20))
                topsizer.Add(self.pnl, proportion=1, flag=wx.ALL|wx.EXPAND, border=5)
                topsizer.Add(button_box, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)



                self.SetSizerAndFit(topsizer)

	def OnSubmit(self, event):
		wait = wx.BusyCursor() 
		for child in self.pnl.GetChildren():
			if isinstance(child, wx.TextCtrl): 
				if not bool(child.GetValue()):
					dlg = wx.MessageDialog(self, "%s cannot be left empty"%child.GetName(), "Warning", wx.OK | wx.ICON_WARNING)
					dlg.ShowModal()
					dlg.Destroy()
				if child.GetName() == "jpeg image":
					try:
						open(child.GetValue())
					except Exception:
						dlg = wx.MessageDialog(self, "Please enter a valid file", "Warning", wx.OK | wx.ICON_WARNING)
						dlg.ShowModal()
						dlg.Destroy()
						self.Enable()
						return
					

				self.form_data[child.GetName()] = child.GetValue()
			if isinstance(child, wx.ComboBox): 
				if not bool(child.GetValue()):
					dlg = wx.MessageDialog(self, "%s cannot be left empty"%child.GetName(), "Warning", wx.OK | wx.ICON_WARNING)
					dlg.ShowModal()
					dlg.Destroy()
					return


				combobox_value = "".join(child.GetValue().split(" "))
				self.form_data[child.GetName()] = combobox_value
				
		self.form_data["platform"] = sys.platform
		self.form_data["mac_id"] = getHwAddr()
		
		
	
		self.form_data["payment_receipt_image"] = self.payment_receipt_image
		
		try:
			response = requests.post("%s/v1/register_user"%url, data=self.form_data)
			messege = response.json().get("messege")
		except requests.ConnectionError:
			messege = "some how the request cannot be completed, Please check your internet connection"

		dlg = wx.MessageDialog(self, messege, "Notification", wx.OK | wx.ICON_WARNING)
		if dlg.ShowModal() == wx.ID_OK:
			dlg.ShowModal()
			dlg.Destroy()
			self.Destroy()
		del wait
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
			try:
				f = open(os.path.join(self.dirname, self.filename), 'rb')
				self.control.SetValue(os.path.join(self.dirname, self.filename))
				self.payment_receipt_image = base64.encodestring(f.read())
				f.close()

			except IOError as e:
				dlg = wx.MessageDialog(self, "Please enetr a valid file", "Warning", wx.OK | wx.ICON_WARNING)
				dlg.ShowModal()
				dlg.Destroy()
				return
		dlg.Destroy()


#This list has all the colors available in wx python


class CanvasPanel(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, -1, size=(510,300), pos=((wx.DisplaySize()[0])/2,(wx.DisplaySize()[1])/2), style=wx.CLOSE_BOX)

		self.hbox = wx.BoxSizer(wx.VERTICAL)
		self.panel = wx.Panel(self, 3, style=wx.RAISED_BORDER)

		font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
		font.SetPointSize(8)
		text = """    Welcome to METC 
		
				If have authentication code, prese yes
				or press no to make a new registration.
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
		self.Enable(False)
		dia = Form()
		dia.Show(True)	
		self.Enable(True)
		return

	def close_window(self, event):
		self.Close()
	

	def disable_buttons(self, flag):
		for button in self.button_panel.GetChildren():
			if not flag:
				button.Enable()
			else:
				button.Disable()

	def yes_authentication_code(self, event):
		self.Enable(False)
		#frame = wx.TextEntryDialog(self, "Enter the authentication code", "", style=wx.OK|wx.CANCEL)
		frame = Authentication(self)
		frame.ShowModal()
		mac_id = getHwAddr()
		
		if not frame.result:
			return

		response = requests.get("%s/v1/download?mac_id=%s&key=%s&path=%s&check_module=%s"%(url, mac_id, frame.result, False, True))
			
		
		if response.json().get("error"):
			dlg = wx.MessageDialog(self, response.json().get("messege"), "Warning", wx.OK | wx.ICON_WARNING)
			dlg.ShowModal()
			dlg.Destroy()
			self.Enable(True)
			return
		
		module_name = response.json()["module_name"]
		hashkey = response.json()["hash"]
		user_os = sys.platform[:3]
		working_dir = os.path.abspath(os.path.dirname("__file__"))
		#This creates a new working directory with parent directory in which this .exe is running by the name of the data
		
		
		path = "%s/%s_%s.zip"%(working_dir, user_os[:3], module_name)

		print path
		try:
				
			#SEcond time user
			if os.path.exists(path):
				self.already_registered_user(response, path, hashkey, module_name, user_os)
		
			else:
				self.new_user(response, path, frame.result, module_name, user_os, mac_id)

		except requests.ConnectionError:
			raise StandardError("Your internet connection is not working")	
		
		return


	def already_registered_user(self, response, path, hashkey, module_name, user_os):

		dirpath = tempfile.mkdtemp()
		with  cd(dirpath):
				zip_file = zipfile.ZipFile(path) 
				zipfile.ZipFile.extractall(zip_file, pwd=hashkey)
				
				Run_Unzip("%s_%s.zip"%(user_os[:3], module_name), dirpath, None, "Extracting files....")
				#zip_file = zipfile.ZipFile("%s_%s.zip"%(user_os[:3], module_name))
				#zipfile.ZipFile.extractall(zip_file)
				
				if user_os == "win":
					subprocess.call(["Play me.exe"])
				elif user_os == "lin":
					subprocess.call(["ls"])
					subprocess.call(["wine", "Play me.exe"])
				
				else:
					subprocess.call(["wine", "Play me.exe"])
		
		shutil.rmtree(dirpath)

		return


	def new_user(self, response, path, key, module_name, user_os, mac_id):
		#r = requests.get("%s/v1/download?mac_id=%s&key=%s&path=%s"%(url, mac_id, key, False))

		link = "%s/v1/download?mac_id=%s&key=%s&path=%s"%(url, mac_id, key, False)
		"""
		if r.headers.get("content-length"):
			dlg = wx.MessageDialog(self, r.json().get("messege"), "Warning", wx.OK | wx.ICON_WARNING)
			dlg.ShowModal()
			dlg.Destroy()
			return
		"""

		Run_Download(path, link, "Please wait while the file is being downloaded")
		#zf = zipfile.ZipFile(path, mode='w')
		#zf.fp.write(r.content)
		#zf.fp.close()


		#if path doesnt exists the response will have the zip file and this writes that encrypted zip file into the path
		#Now the Data Folder do have WholeZip.zip and now the path exists

		dirpath = tempfile.mkdtemp()
				
		response = requests.get("%s/v1/download?mac_id=%s&key=%s&path=%s"%(url, mac_id, key, True))
		
		with  cd(dirpath):
				zip_file = zipfile.ZipFile(path) 
				zipfile.ZipFile.extractall(zip_file, pwd=response.json().get("hash"))
				
				
				Run_Unzip("%s_%s.zip"%(user_os[:3], module_name), dirpath, None, "Extracting files....")
				#zip_file = zipfile.ZipFile("%s_%s.zip"%(user_os[:3], module_name)) 
				#zipfile.ZipFile.extractall(zip_file)
				
				if user_os == "win":

					subprocess.call(["Play me.exe"])
				elif user_os == "lin":
					subprocess.call(["ls"])
					subprocess.call(["wine", "Play me.exe"])
				
				else:
					print "user os cannot be determined"
	
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
