#!/usr/bin/env python
import time
import wx
import zipfile
from threading import Thread

from wx.lib.pubsub import Publisher

########################################################################
class TestThread(Thread):
    """Test Worker Thread Class."""

    #----------------------------------------------------------------------
    def __init__(self):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self.start()    # start the thread
	self.count = 0
    #----------------------------------------------------------------------
    def run(self):
		"""Run Worker Thread."""
		# This is the code executing in the new thread.
		zf = zipfile.ZipFile('/home/k/Downloads/Data/Economics/win_Economics.zip')

                uncompress_size = sum((file.file_size for file in zf.infolist()))
                extracted_size = 0
                print uncompress_size

                for file in zf.infolist():
                        extracted_size += file.file_size

                        zf.extract(file, path = "/home/k/Destop/junk/")
                        messege = "Completion %s %%" % (extracted_size * 100/uncompress_size)
                        print messege
                        wx.CallAfter(Publisher().sendMessage, "update", "")

                        self.count += 1
                        if self.count == len(zf.infolist()):
                                self.timer.Stop()
                                wx.Bell()
				
		return
########################################################################
class MyProgressDialog(wx.Dialog):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Dialog.__init__(self, None, title="Progress")
        self.count = 0

        self.progress = wx.Gauge(self, range=20)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.progress, 0, wx.EXPAND)
        self.SetSizer(sizer)

        # create a pubsub receiver
        Publisher().subscribe(self.updateProgress, "update")

    #----------------------------------------------------------------------
    def updateProgress(self, msg):
        """"""
        self.count += 1

        if self.count >= 20:
            self.Destroy()

        self.progress.SetValue(self.count)


########################################################################
class MyForm(wx.Frame):

    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Tutorial")

        # Add a panel so it looks the correct on all platforms
        panel = wx.Panel(self, wx.ID_ANY)
        self.btn = btn = wx.Button(panel, label="Start Thread")
        btn.Bind(wx.EVT_BUTTON, self.onButton)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(btn, 0, wx.ALL|wx.CENTER, 5)
        panel.SetSizer(sizer)

    #----------------------------------------------------------------------
    def onButton(self, event):
        """
        Runs the thread
        """
        btn = event.GetEventObject()
        btn.Disable()

        TestThread()
        dlg = MyProgressDialog()
        dlg.ShowModal()

        btn.Enable()


#----------------------------------------------------------------------
# Run the program
if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = MyForm().Show()
    app.MainLoop()
