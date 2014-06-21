#!/usr/bin/env python
#-*- coding:utf-8 -*-
import subprocess
import wx
import re
import sys
import time
import itertools
import hashlib
from helpers import getHwAddr
from form import Form
import requests
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

		self.Bind(wx.EVT_BUTTON, self.no_authentication_code, id=ID_ONE)
		self.Bind(wx.EVT_BUTTON, self.yes_authentication_code, id=ID_TWO)
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
		from helpers import TokenDialog
		frame = wx.TextEntryDialog(self, "Enter the authentication code", "", style=wx.OK|wx.CANCEL)
		if frame.ShowModal() == wx.ID_OK:
			print frame.GetValue()
			mac_id = getHwAddr("eth0")
			r = requests.post("http://localhost:8989/v1/register_user", data={"mac_id": mac_id, "access_token": "43242"})
			print r.content
		return

def run_app():
	app = wx.PySimpleApp()
	app.frame = CanvasPanel()
	app.frame.Show(True)
	app.frame.Center()
	app.MainLoop()



if __name__ == "__main__":

	run_app()
