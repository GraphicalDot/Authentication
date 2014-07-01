#!/usr/bin/env python
import wx.lib.newevent
import thread
import exceptions
import time
import zipfile
import os
import shutil

(RunEvent, EVT_RUN) = wx.lib.newevent.NewEvent()
(CancelEvent, EVT_CANCEL) = wx.lib.newevent.NewEvent()
(DoneEvent, EVT_DONE) = wx.lib.newevent.NewEvent()
(ProgressStartEvent, EVT_PROGRESS_START) = wx.lib.newevent.NewEvent()
(ProgressEvent, EVT_PROGRESS) = wx.lib.newevent.NewEvent()

class InterruptedException(exceptions.Exception):
    def __init__(self, args = None):
        self.args = args

class ThreadedJob:
	def __init__(self):
		# tell them ten seconds at first
		self.secondsRemaining = 10.0
		self.lastTick = 0

		# not running yet
		self.isPaused = False
		self.isRunning = False
		self.keepGoing = True
#		self.secondsPerTick = 0
	def Start(self):
		self.keepGoing = self.isRunning = True
		thread.start_new_thread(self.Run, ())
		self.isPaused = False

	def Stop(self):
		self.keepGoing = False

	def WaitUntilStopped(self):
		while self.isRunning:
			time.sleep(0.1)
		wx.SafeYield()

	def IsRunning(self):
		return self.isRunning

	def Run(self):
		# this is overridden by the
		# concrete ThreadedJob
		print "Run was not overloaded"
		self.JobFinished()
		pass

	def Pause(self):
		self.isPaused = True
		pass

	def Continue(self):
		self.isPaused = False
		pass

	def PossibleStoppingPoint(self):
		if not self.keepGoing:
			raise InterruptedException("process interrupted.")
		wx.SafeYield()

		# allow cancel while paused
		while self.isPaused:
			if not self.keepGoing:
				raise InterruptedException("process interrupted.")

		# don't hog the CPU
		time.sleep(0.1)

	def SetProgressMessageWindow(self, win):
		self.win = win


	def JobBeginning(self, totalTicks):
		self.lastIterationTime = time.time()
		self.totalTicks = totalTicks

		if hasattr(self, "win") and self.win:
			wx.PostEvent(self.win, ProgressStartEvent(total=totalTicks))

	def JobProgress(self, currentTick):
		dt = time.time() - self.lastIterationTime
		self.lastIterationTime = time.time()
		dtick = currentTick - self.lastTick
		self.lastTick = currentTick

		alpha = 0.92
		if currentTick > 1:
			self.secondsPerTick = dt * (1.0 - alpha) + (self.secondsPerTick * alpha)
		else:
			self.secondsPerTick = dt

		if dtick > 0:
			self.secondsPerTick /= dtick

			self.secondsRemaining = self.secondsPerTick * (self.totalTicks - 1 - currentTick) + 1

		if hasattr(self, "win") and self.win:
			wx.PostEvent(self.win, ProgressEvent(count=currentTick))

	def SecondsRemaining(self):
		return self.secondsRemaining


	def TimeRemaining(self):

		if 1: #self.secondsRemaining > 3:
			minutes = self.secondsRemaining // 60
			seconds = int(self.secondsRemaining % 60.0)
			return "%i:%02i" % (minutes, seconds)

		else:
			return "a few"

	def JobFinished(self):
		if hasattr(self, "win") and self.win:
			wx.PostEvent(self.win, DoneEvent())

		self.isRunning = False

class EggTimerJob(ThreadedJob):
	""" A sample Job that demonstrates the mechanisms and features of the Threaded Job"""
	def __init__(self, src, dist):
		self.src = src
		self.dist = dist
		ThreadedJob.__init__(self)



	def Run(self):
		try:
			self.sudo_run()
		except Exception as e:
			print e


	def sudo_run(self):
		self.time0 = time.clock()
		try:
			zf = zipfile.ZipFile(self.src)

			uncompressed_size = sum((file_name.file_size for file_name in zf.infolist()))
			print uncompressed_size

			self.JobBeginning((len(zf.infolist())))
			extracted_size = 0
            		count = 0
			for file_name, count in zip(zf.infolist(), range(len(zf.infolist()))):
				time.sleep(0.1)
				print count
				print file_name.filename
				zf.extract(file_name, path = self.dist)
				extracted_size += file_name.file_size
				self.JobProgress(count)
				count += 1
				self.PossibleStoppingPoint()

		except InterruptedException:
			# clean up if user stops the Job early
			# unlink / delete the file that is partially copied
			shutil.rmtree(self.dist)
			print "canceled, dest deleted!"

		# always signal the end of the job
		self.JobFinished()

	def __str__(self):
		""" The job progress dialog expects the job to describe its current state."""
		response = []
		if self.isPaused:
			response.append("Paused Counting")
		elif not self.isRunning:
			response.append("Will Count the seconds")
		else:
			response.append("Now Extracting...")
			
		return " ".join(response)

class FileCopyJob(ThreadedJob):
	""" A common file copy Job. """

	def __init__(self, orig_filename, copy_filename):

		self.src = orig_filename
		self.dest = copy_filename
		ThreadedJob.__init__(self)

	def Run(self):
		""" This can either be run directly for synchronous use of the job, or started as a thread when ThreadedJob.Start() is called.
		It is responsible for calling JobBeginning, JobProgress, and JobFinished. And as often as possible, calling PossibleStoppingPoint() 
		which will sleep if the user pauses, and raise an exception if the user cancels.
		"""

		self.time0 = time.clock()
		

		try:
			source = open(self.src, 'rb')

           
	   		import os
			(st_mode, st_ino, st_dev, st_nlink, st_uid, st_gid, st_size, st_atime, st_mtime, st_ctime) = os.stat(self.src)
			num_blocks = st_size / self.block_size
			current_block = 0
		
			zf = zipfile.ZipFile(self.src)

	                uncompress_size = sum((file_name.file_size for file_name in zf.infolist()))
        	        extracted_size = 0

			self.JobBeginning(num_blocks)

			#dest = open(self.dest, 'wb')

			for file_name in zf.infolist():
				zf.extract(file_name, path = self.dest)
				extracted_size += file_name.file_size
				current_block += 1
				self.JobProgress(current_block)
				self.PossibleStoppingPoint()
				#else:
				#	break

			#source.close()
			#dest.close()

		except InterruptedException:
			# clean up if user stops the Job early
			dest.close()
			# unlink / delete the file that is partially copied
			os.unlink(self.dest)
			print "canceled, dest deleted!"

		# always signal the end of the job
		self.JobFinished()

	def __str__(self):
		""" The job progress dialog expects the job to describe its current state."""
		response = []
		if self.isPaused:
			response.append("Paused Copy")
		elif not self.isRunning:
			response.append("Will Copy a file")
		else:
			response.append("Copying")
		
		return " ".join(response)

class JobProgress(wx.Dialog):
	""" This dialog shows the progress of any ThreadedJob.
	It can be shown Modally if the main application needs to suspend 
	operation, or it can be shown Modelessly for background progressreporting.
	app = wx.PySimpleApp()
    
    	job = EggTimerJob(duration = 10)
	dlg = JobProgress(None, job)
	job.SetProgressMessageWindow(dlg)
	job.Start()
	dlg.ShowModal()

	"""
	def __init__(self, parent, job):
		self.job = job

		wx.Dialog.__init__(self, parent, -1, "Extracting files", size=(350,200))

		# vertical box sizer
		sizeAll = wx.BoxSizer(wx.VERTICAL)

		# Job status text
		self.JobStatusText = wx.StaticText(self, -1, "Starting...")
		sizeAll.Add(self.JobStatusText, 0, wx.EXPAND|wx.ALL, 8)

		# wxGague
		self.ProgressBar = wx.Gauge(self, -1, 10, wx.DefaultPosition, (250, 15))
		sizeAll.Add(self.ProgressBar, 0, wx.EXPAND|wx.ALL, 8)

		# horiz box sizer, and spacer to right-justify
		sizeRemaining = wx.BoxSizer(wx.HORIZONTAL)
		sizeRemaining.Add((2,2), 1, wx.EXPAND)

		# time remaining read-only edit
		# putting wide default text gets a reasonable initial layout.
		
		self.remainingText = wx.StaticText(self, -1, "???:??")
		sizeRemaining.Add(self.remainingText, 0, wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 8)

		# static text: remaining
		self.remainingLabel = wx.StaticText(self, -1, "remaining")
		sizeRemaining.Add(self.remainingLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 8)


		#add that row to the mix
		sizeAll.Add(sizeRemaining, 1, wx.EXPAND)

		# horiz box sizer & spacer
		sizeButtons = wx.BoxSizer(wx.HORIZONTAL)
		sizeButtons.Add((2,2), 1, wx.EXPAND|wx.ADJUST_MINSIZE)

		# Pause Button
		#self.PauseButton = wx.Button(self, -1, "Pause")
		#sizeButtons.Add(self.PauseButton, 0, wx.ALL, 4)
		#self.Bind(wx.EVT_BUTTON, self.OnPauseButton, self.PauseButton)

		# Cancel button
		#self.CancelButton = wx.Button(self, wx.ID_CANCEL, "Cancel")
		#sizeButtons.Add(self.CancelButton, 0, wx.ALL, 4)
		#self.Bind(wx.EVT_BUTTON, self.OnCancel, self.CancelButton)


		# Add all the buttons on the bottom row to the dialog
		sizeAll.Add(sizeButtons, 0, wx.EXPAND|wx.ALL, 4)

		self.SetSizerAndFit(sizeAll)
		sizeAll.SetSizeHints(self)

		# jobs tell us how they are doing
		self.Bind(EVT_PROGRESS_START, self.OnProgressStart)
		self.Bind(EVT_PROGRESS, self.OnProgress)
		self.Bind(EVT_DONE, self.OnDone)
		self.SetBackgroundColour("light blue")
		self.Layout()

	def OnPauseButton(self, event):
		if self.job.isPaused:
			self.job.Continue()
			self.PauseButton.SetLabel("Pause")
			self.Layout()
		else:
			self.job.Pause()
			self.PauseButton.SetLabel("Resume")
			self.Layout()

	def OnCancel(self, event):
		self.job.Stop()


	def OnProgressStart(self, event):
		self.ProgressBar.SetRange(event.total)
		self.statusUpdateTime = time.clock()

	def OnProgress(self, event):
		# update the progress bar
		self.ProgressBar.SetValue(event.count)
		self.remainingText.SetLabel(self.job.TimeRemaining())

		# update the text a max of 20 times a second
		if time.clock() - self.statusUpdateTime > 0.05:
			self.JobStatusText.SetLabel(str(self.job))
			self.statusUpdateTime = time.clock()
			self.Layout()

	def OnDone(self, event):
		self.ProgressBar.SetValue(0)
		self.JobStatusText.SetLabel("Finished")
		self.Destroy()

	
def Run_Job(src, dest):
	app = wx.PySimpleApp()
	job = EggTimerJob(src, dest)
	dlg = JobProgress(None, job)
	job.SetProgressMessageWindow(dlg)
	job.Start()
	dlg.ShowModal()


if __name__ == "__main__":
	Run_Job("/home/k/Desktop/LIFE SCIENCES_Course.zip", "/home/k/Desktop/junk")

