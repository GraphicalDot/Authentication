#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
class ProgressDialog(wx.Dialog):
	"""
	Shows a Progres Gauge while an operation is taking place. May be cancellable
	which is possible when converting pdf/ps
	"""
	def __init__(self, gui, title, to_add=1, cancellable=False):
		"""Defines a gauge and a timer which updates the gauge."""
	    	wx.Dialog.__init__(self, gui, title=title,
		style=wx.CAPTION)
		self.gui = gui
		self.count = 0
		self.to_add = to_add
		self.timer = wx.Timer(self)
		self.gauge = wx.Gauge(self, range=100, size=(180, 30))
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.gauge, 0, wx.ALL, 10)
    
		if cancellable:
			cancel = wx.Button(self, wx.ID_CANCEL, _("&Cancel"))
			cancel.SetDefault()
			cancel.Bind(wx.EVT_BUTTON, self.on_cancel)
			btnSizer = wx.StdDialogButtonSizer()
			btnSizer.AddButton(cancel)
			btnSizer.Realize()
			sizer.Add(btnSizer, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)
    

		self.SetSizer(sizer)
		sizer.Fit(self)
		self.SetFocus()
		self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
		self.timer.Start(30)
	
	def on_timer(self, event):
		"""Increases the gauge's progress."""
		self.count += self.to_add
		self.gauge.SetValue(self.count)
		if self.count > 100:
			self.count = 0
    
	def on_cancel(self, event):
		"""Cancels the conversion process"""
		pass
if __name__ == "__main__":
	dl = ProgressDialog()
	dl.ShowModal()
