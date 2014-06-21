#!/usr/bin/env python
#-*- coding: utf-8 -*-

import wx

class Form(wx.Dialog):
	def __init__(self, parent, id, title):
		wx.Dialog.__init__(self, parent, id, title)
		vbox = wx.BoxSizer(wx.VERTICAL)


		stline = wx.StaticText(self, 2, 'Discipline ist Macht.')
		vbox.Add(stline, 1, wx.ALIGN_CENTER|wx.TOP, 45)
		sizer =  self.CreateButtonSizer(wx.NO|wx.YES|wx.HELP)
		vbox.Add(sizer, 0, wx.ALIGN_CENTER)
		self.SetSizer(vbox)
		self.Bind(wx.EVT_BUTTON, self.OnYes, id=wx.ID_YES)

	def OnYes(self, event):
		self.Close()
