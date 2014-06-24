#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx

from wx.lib.pubsub import Publisher
TASK_RANGE = 50

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

		self.gauge = wx.Gauge(pnl, range=TASK_RANGE, size=(250, 25))
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
		self.SetTitle('wx.Gauge')
		self.Centre()
		self.Show(True)     
		
#	def OnOk(self, e):
 #       
#		if self.count >= TASK_RANGE:
#			return
#		
#		self.timer.Start(100)
#		self.text.SetLabel('Task in Progress')

	def OnStop(self, e):
        
		if self.count == 0 or self.count >= TASK_RANGE or not self.timer.IsRunning():
			return

		self.timer.Stop()
		self.text.SetLabel('Task Interrupted')
        
	def OnOk(self, e):
        

		import zipfile
		zf = zipfile.ZipFile('/home/k/Downloads/Data/Economics/win_Economics.zip')

		uncompress_size = sum((file.file_size for file in zf.infolist()))
		extracted_size = 0
		import time
		for file in zf.infolist():
			time.sleep(1)
			self.count += 1
			extracted_size += file.file_size
			print file.filename
			zf.extract(file, path = "/home/k/Destop/junk")
			self.text.SetLabel("Completion %s %%" % (extracted_size * 100/uncompress_size))
			self.gauge.SetValue(self.count)
        
		if self.count == len(zf.infolist()):
			self.timer.Stop()
			self.text.SetLabel('File extracted')
                     

def main():
    
	ex = wx.App()
	Example(None)
	ex.MainLoop()    

if __name__ == '__main__':
	main()                 

