# WinWizard add-on for NVDA
#This file is covered by the GNU General Public License.
#See the file COPYING.txt for more details.
#Copyright (C) 2020 Oriol Gomez <ogomez.s92@gmail.com>
from builtins import str
from builtins import range
import ui
import controlTypes
from tones import beep
lastHidden=0
stack=0
import re
import pickle
hidden={}
from ctypes import *
import appModuleHandler
import winKernel
import winUser
from logHandler import log
import os
impPath = os.path.abspath(os.path.dirname(__file__))
import globalPluginHandler
from sys import path
path.append(impPath)
import threading
import addonHandler
import api
from speech import cancelSpeech
import config
from configobj import *
import scriptHandler
addonHandler.initTranslation()
_basePath = os.path.dirname(os.path.abspath(__file__))
_configFile = os.path.join(_basePath,"settings.ini")
_savePath = os.path.join(_basePath, "settings")
psapi = windll.psapi
if not os.path.isfile(_configFile):
	config = ConfigObj()
	config.filename = _configFile
	config ["status"]="enabled"
	config.write()
def getFilePath():
	global hidden,stack
	file = standarFileName("hiddenwindows")
	file = file+".dat"
	path = os.path.join(_basePath, file)
	abspath=os.path.abspath(path)
	return open(abspath,"rb")
def getFileLoad():
	global hidden,stack
	file = standarFileName("hiddenwindows")
	file = file+".dat"
	path = os.path.join(_basePath, file)
	abspath=os.path.abspath(path)
	return abspath

def getFileWrite():
	global hidden,stack
	file = standarFileName("hiddenwindows")
	file = file+".dat"
	path = os.path.join(_basePath, file)
	abspath=os.path.abspath(path)
	return open(abspath,"wb")

def standarFileName(fileName):
	global hidden,stack
	notAllowed = re.compile("\?|:|\*|\t|<|>|\"|\/|\\||") # Invalid characters
	allowed = re.sub(notAllowed, "", str(fileName))
	return allowed
def savelist():
	global hidden,stack
	f = getFileWrite()
	pickle.dump(hidden,f)
	f.close()
def hidewindow(num):
	global hidden,lastHidden,stack
	num=num+(stack*10)
	try:
		#is it a window what we want to show, or has it disappeared? nUtils runs a forever running while loop for this, but we don't want to waste resources. so we just check here.
		if hidden[num][0]==api.getForegroundObject().windowHandle:
			hidden.pop(num)
			hidewindow(num)
		elif winUser.isWindow(hidden[num][0])==1:
			value=hidden[num][0]
			beep(180,80)
			winUser.user32.ShowWindowAsync(value,3)
			winUser.user32.SetFocus(value)
			hidden.pop(num)
			lastHidden=0
			return
		else:
			hidden.pop(num)
			hidewindow(num)
		return
	except KeyError:
		current=api.getForegroundObject()
		appName=appModuleHandler.getAppNameFromProcessID(current.processID,True)
		title=current.name
		current=current.windowHandle
		if (title==None):
			beep(300,80)
			return

		if title=="Program Manager" or title=="Taskbar":
			beep(300,80)
			return
		winUser.user32.ShowWindowAsync(current,0)
		temp=[]
		temp.append(current)
		temp.append(title)
		temp.append(appName)
		temp.append(num)
		hidden[num]=temp
		beep(80,80)
	savelist()
def clickWindow(object):
	object.setFocus()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		global hidden,stack
		globalPluginHandler.GlobalPlugin.__init__(self)
		for n in range(1,10):
			self.bindGesture("kb:shift+windows+%s" % n, "window")
		self.bindGesture("kb:shift+windows+0", "window")
		self.bindGesture("kb:shift+windows+leftArrow", "stackdown")
		self.bindGesture("kb:shift+windows+rightArrow", "stackup")

		try:
			hidden=pickle.load(getFilePath())
		except:
			hidden={}
	def script_hideFirstAvailable(self,gesture):
		global hidden,lastHidden,stack

		curnum=1
		try:
			while (hidden[curnum]!=None):
				curnum=curnum+1
		except:
			pass
		lastHidden=curnum
		hidewindow(curnum)
	def script_unhideLastWindow(self,gesture):
		global lastHidden,hidden
		if lastHidden==0:
			ui.message(_("There is no window recorded as last hidden window"))
			return
		hidewindow(lastHidden)

	def script_killProcess(self,gesture):
		focus=api.getFocusObject()
		appName=appModuleHandler.getAppNameFromProcessID(focus.processID,True)
		kernel32=winKernel.kernel32
		pid=focus.processID
		handle = kernel32.OpenProcess(1, 0, pid)
		beep(90,80)
		return (0 != kernel32.TerminateProcess(handle, 0))


	def script_window(self,gesture):
		num=int(gesture.mainKeyName[-1])
		hidewindow(num)
	def script_stackdown(self,gesture):
		global stack
		stack-=1
		if stack<0: stack=0
		ui.message(_("stack {0}").format(stack))
	def script_stackup(self,gesture):
		global stack
		stack+=1
		if stack>10: stack=10
		ui.message(_("stack {0}").format(stack))
	def script_cycleWindows(self,gesture):
		nwp=0
		nwn=0
		try:
			fg=api.getForegroundObject().parent
			fgp=fg.appModule
		except:
			ui.message(_("Can't retrieve window information for this object."))
		try:
			if not fg.simplePrevious.appModule==fgp:
				if fg.simpleNext.appModule==fgp:
					nwn=fg.simpleNext
			if not fg.simpleNext.appModule==fgp:
				if fg.simplePrevious.appModule==fgp:
					nwp=fg.simplePrevious
		except AttributeError:
			ui.message(_("This is not a valid window. You are probably on the desktop or the start button."))
		if nwn==0 and nwp==0:
			ui.message(_("This window has no top level windows to cycle to."))
		elif not nwn==0 and not nwp==0:
			ui.message(_("Multiple top level windows detected."))
		elif not nwn==0:
			clickWindow(nwn)
		elif not nwp==0:
			clickWindow(nwp)
	__gestures = {
"kb:windows+tab":"cycleWindows",
"kb:shift+windows+h": "hideFirstAvailable",
"kb:NVDA+windows+h": "unhideLastWindow",
"kb:windows+F4": "killProcess",
}