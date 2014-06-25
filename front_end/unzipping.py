#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import threading
from wx.lib.pubsub import Publisher
from wx.lib.delayedresult import startWorker
import time
import zipfile
from wx.lib.pubsub import Publisher

class Example(wx.Frame):
           
	def __init__(self, *args, **kw):
		super(Example, self).__init__(*args, **kw) 
        
		self.InitUI()
        
	def InitUI(self):   
        
		self.count = 0
#		self.timer = wx.Timer(self, 1)
#		self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
		
		pnl = wx.Panel(self)
		vbox = wx.BoxSizer(wx.VERTICAL)
		hbox1 = wx.BoxSizer(wx.HORIZONTAL)
		hbox2 = wx.BoxSizer(wx.HORIZONTAL)
		hbox3 = wx.BoxSizer(wx.HORIZONTAL)

		self.gauge = wx.Gauge(pnl, size=(250, 25))
		self.gauge.SetBezelFace(3)
		self.gauge.SetShadowWidth(3)
		
		self.btn1 = wx.Button(pnl, wx.ID_OK)
		self.text = wx.StaticText(pnl, label='Press ok to start unzipping')

		self.Bind(wx.EVT_BUTTON, self.OnOk, self.btn1)

		hbox1.Add(self.gauge, proportion=1, flag=wx.ALIGN_CENTRE)
		hbox2.Add(self.btn1, proportion=1, flag=wx.RIGHT, border=10)
		hbox3.Add(self.text, proportion=1)
		vbox.Add((0, 30))
		vbox.Add(hbox1, flag=wx.ALIGN_CENTRE)
		vbox.Add((0, 20))
		vbox.Add(hbox2, proportion=1, flag=wx.ALIGN_CENTRE)
		vbox.Add(hbox3, proportion=1, flag=wx.ALIGN_CENTRE)
		
		pnl.SetSizer(vbox)
        
		self.SetSize((300, 200))
		self.Centre()
		self.Show(True)     
		

        
#	def OnOk(self, e):
#		self.timer.Start(100)
#		self.text.SetLabel("You pressed ok button")
#		return 

		
		
	def OnOk(self, event):	
		zf = zipfile.ZipFile('/home/k/Downloads/Data/Economics/win_Economics.zip')

		uncompress_size = sum((file_name.file_size for file_name in zf.infolist()))
		extracted_size = 0
		print uncompress_size

		for file_name in zf.infolist():
			extracted_size += file_name.file_size
			"""
			thread = threading.Thread(self.extract, args=(zf, file_name))
			thread.start()
			"""
			messege = "Completion %s %%" % (extracted_size * 100/uncompress_size)
			
			print messege
			self.text.SetLabel(str(file_name.file_size))
			wx.CallAfter(self.gauge.SetValue, extracted_size)
			
			self.count += 1
			if self.count == len(zf.infolist()):
				self.text.SetLabel('File extracted')
				wx.Bell()
				return 
		return

	def extract(self, zf, file_name):
		zf.extract(file_name, path = "/home/k/Destop/junk/")
		return

def main():
    
	ex = wx.App(False)
	Example(None)
	ex.MainLoop()    

if __name__ == '__main__':
	main()                 

