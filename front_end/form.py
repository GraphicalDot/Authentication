#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import wx
import requests
import time
from helpers import getHwAddr
url = "http://localhost:8989/v1"

class Form(wx.Frame):
	def __init__(self):
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

		self.SetSizer(vbox)
        
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
		self.form_data["mac_id"] = getHwAddr("eth0")

		response = requests.post("%s/register_user"%url, data=self.form_data)
		dlg = wx.MessageDialog(self, response.json().get("messege"), "Notification", wx.OK | wx.ICON_WARNING)
		dlg.ShowModal()
		dlg.Destroy()
		print response.text
		print self.form_data
		
		
		self.Destroy()
		return

        def OnClose(self, e):
        	self.Destroy()
        
