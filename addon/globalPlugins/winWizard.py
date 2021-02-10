# -*- coding: UTF-8 -*-

# WinWizard add-on for NVDA
# This file is covered by the GNU General Public License.
# See the file COPYING.txt for more details.
# Copyright (C) 2020 Oriol Gomez <ogomez.s92@gmail.com>
# Currently maintained by Łukasz Golonka <lukasz.golonka@mailbox.org>

import collections
from dataclasses import dataclass, field
import pickle
import os
import globalPluginHandler
import appModuleHandler
import addonHandler
import ui
import scriptHandler
import api
from globalCommands import SCRCAT_FOCUS
import winKernel
import winUser
import tones
import wx
import gui
import globalVars
addonHandler.initTranslation()


@dataclass(frozen=True, order=True)
class Priority:
	constant: int = field(repr=False)
	name: str = field(default="", compare=False)

	def __str__(self):
		return self.name


class stack:

	def __init__(self, stackNumber, hiddenInStack):
		self.stackNumber = stackNumber
		self.hiddenInStack = hiddenInStack

	def __str__(self):
		# Translators: Name of the stack shown in the dialog - for example Stack 1.
		return _("Stack {}").format(self.stackNumber)

	@property
	def numbers(self):
		for window in self.hiddenInStack:
			yield from window.numbers


class hiddenWindow:

	def __init__(self, slotNumber, textualRepresentation):
		self.slotNumber = slotNumber
		self.textualRepresentation = textualRepresentation
		self.presentationalNumber = self.slotNumber
		if self.presentationalNumber % 10 == 0:
			# Slots are internally numbered from 0
			# Renumber them for showing in the GUI
			self.presentationalNumber += 10

	def __str__(self):
		# Translators: Text of the  entry for the hidden window in the hidden windows tree.
		return _("{}: {}").format(self.presentationalNumber, self.textualRepresentation)

	@property
	def numbers(self):
		yield self.slotNumber


class baseSingletonDialog(wx.Dialog):

	title = ""
	_instance = None

	def __new__(cls, *args, **kwargs):
		if cls._instance is None:
			return super().__new__(cls, *args, **kwargs)
		return cls._instance

	def __init__(self, *args, **kwargs):
		if self.__class__._instance is not None:
			return
		self.__class__._instance = self
		super().__init__(parent=gui.mainFrame, title=self.title)

	def onClose(self, evt):
		self.Destroy()
		self.__class__._instance = None

	def __del__(self):
		self.__class__._instance = None

	@classmethod
	def run(cls, *args, **kwargs):
		gui.mainFrame.prePopup()
		d = cls(*args, **kwargs)
		if d:
			d.Show()
		gui.mainFrame.postPopup()


class changeProcessPriorityDialog(baseSingletonDialog):

	# Translators: title of the dialog.
	title = _("Change process priority")

	def __init__(self, currentProcess):
		self.currentProcess = currentProcess
		super().__init__()
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		sHelper = gui.guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)
		self.priorities = sHelper.addItem(
			wx.RadioBox(
				self,
				# Translators: Label for the group of radio buttons for choosing a process priority.
				label=_("Choose priority"),
				choices=[str(priority) for priority in process.PRIORITIES],
				style=wx.RA_SPECIFY_ROWS
			)
		)
		currentPriorityIndex = process.PRIORITIES.index(Priority(self.currentProcess.getProcessPriority()))
		self.priorities.SetSelection(currentPriorityIndex)
		buttons = gui.guiHelper.ButtonHelper(wx.HORIZONTAL)
		okAction = buttons.addButton(
			self,
			# Translators: Label of the button which sets priority in the dialog.
			label=_("Change")
		)
		okAction.Bind(wx.EVT_BUTTON, self.onChange)
		self.AffirmativeId = okAction.Id
		okAction.SetDefault()
		cancelAction = buttons.addButton(
			self,
			wx.ID_CLOSE,
			# Translators: Label for the button which  dismiss the dialog.
			label=_("Cancel")
		)
		cancelAction.Bind(wx.EVT_BUTTON, self.onClose)
		sHelper.addDialogDismissButtons(buttons)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.EscapeId = wx.ID_CLOSE
		mainSizer.Add(sHelper.sizer, border=gui.guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
		mainSizer.Fit(self)
		self.Sizer = mainSizer
		self.CentreOnScreen()

	def onChange(self, evt):
		priorityToSet = self.priorities.GetSelection()
		self.currentProcess.setProcessPriorityByIndex(priorityToSet)
		self.Destroy()
		self.__class__._instance = None


class unhideWindowDialog(baseSingletonDialog):

	# Translators: Title of the dialog.
	title = _("Hidden windows")

	def __init__(self, hiddenWindowsList):
		self.hiddenWindowsList = hiddenWindowsList
		super().__init__()
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		sHelper = gui.guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)
		self.windowsTree = sHelper.addItem(
			wx.TreeCtrl(
				self,
				size=wx.Size(600, 400),
				style=wx.TR_HAS_BUTTONS | wx.TR_HIDE_ROOT | wx.TR_LINES_AT_ROOT | wx.TR_SINGLE
			)
		)
		self.windowsTree.Bind(wx.EVT_CHAR, self.onTreeChar)
		self.treeRoot = self.windowsTree.AddRoot("root")
		try:
			self.lastHidden = self.hiddenWindowsList.history[-1]
		except IndexError:
			self.lastHidden = None
		self.populateTree()
		buttons = gui.guiHelper.ButtonHelper(wx.HORIZONTAL)
		okAction = buttons.addButton(
			self,
			# Translators: Label for the button which shows currently selected hidden window.
			label=_("Unhide")
		)
		okAction.Bind(wx.EVT_BUTTON, self.onUnhide)
		self.AffirmativeId = okAction.Id
		okAction.SetDefault()
		cancelAction = buttons.addButton(
			self,
			wx.ID_CLOSE,
			# Translators: Label for the button which closes the dialog.
			label=_("Close")
		)
		cancelAction.Bind(wx.EVT_BUTTON, self.onClose)
		sHelper.addDialogDismissButtons(buttons)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.EscapeId = wx.ID_CLOSE
		mainSizer.Add(sHelper.sizer, border=gui.guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
		mainSizer.Fit(self)
		self.Sizer = mainSizer
		self.CentreOnScreen()

	def onTreeChar(self, evt):
		if evt.KeyCode in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
			evt = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, wx.ID_ANY)
			button = self.FindWindowById(self.AffirmativeId)
			button.ProcessEvent(evt)
		else:
			evt.Skip()

	def populateTree(self):
		for stack in self.hiddenWindowsList.splitToStacks():
			stackInTree = self.windowsTree.AppendItem(self.treeRoot, str(stack))
			self.windowsTree.SetItemData(stackInTree, stack)
			for slotNumber in stack.hiddenInStack:
				slotInTree = self.windowsTree.AppendItem(stackInTree, str(slotNumber))
				self.windowsTree.SetItemData(slotInTree, slotNumber)
				if self.lastHidden is not None and self.lastHidden == slotNumber.slotNumber:
					self.lastHidden = None  # No point in checkiing further
					self.windowsTree.SelectItem(slotInTree)

	def onUnhide(self, evt):
		treeSelection = self.windowsTree.Selection
		selectedItem = self.windowsTree.GetItemData(treeSelection)
		for slotNumber in selectedItem.numbers:
			toShow = self.hiddenWindowsList.pop(slotNumber)
			toShow.show()
		self.hiddenWindowsList.save()
		self.Destroy()
		self.__class__._instance = None


class hiddenWindowsList (collections.UserDict):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.savePath = os.path.join(os.path.abspath(os.path.dirname(__file__)), "hiddenwindows.dat")
		self.currentStack = 0
		self.history = list()
		try:
			with open(self.savePath, "rb") as f:
				for value in pickle.load(f).values():
					handle, windowTitle, appName, number = value
					try:
						self[number] = windowWithHandle(handle=handle, windowTitle=windowTitle, appName=appName)
					except ValueError:
						continue
		except FileNotFoundError:
			pass
		self.history.clear()
		self.save()

	def __setitem__(self, key, value):
		self.history.append(key)
		super().__setitem__(key, value)

	def __delitem__(self, key):
		try:
			self.history.remove(key)
		except ValueError:
			pass
		super().__delitem__(key)

	def save(self):
		fileContent = dict()
		for slot in list(self.keys()):
			if self[slot].isAlive:
				fileContent[slot] = [self[slot].handle, self[slot].windowTitle, self[slot].appName, slot]
			else:
				del self[slot]
		if len(self) == 0:
			try:
				os.remove(self.savePath)
			except FileNotFoundError:
				return
		else:
			with open(self.savePath, "wb") as f:
				pickle.dump(fileContent, f)

	def previousStack(self):
		self.currentStack -= 1
		if self.currentStack < 0:
			self.currentStack = 0
		return self.currentStack

	def nextStack(self):
		self.currentStack += 1
		return self.currentStack

	def firstEmptySlot(self):
		if len(self) == 0:
			return 0
		takenSlots = set(self.keys())
		lastSlot = max(takenSlots)
		allSlots = set(range(0, (lastSlot + 2)))
		freeSlots = allSlots - takenSlots
		return min(freeSlots)

	def splitToStacks(self):
		takenSlots = list(self.keys())
		if len(takenSlots) == 0:
			# In theory this should never happen as this method is invoked only on non-empty instances
			raise RuntimeError("Cannot divide empty list into stacks")
		else:
			slotsToStacks = [int(str(slotNumber + 10)[:-1]) for slotNumber in takenSlots]
			for stackNumber in sorted(set(slotsToStacks)):
				numbersInCurrentStack = [
					slotNumber for slotNumber in takenSlots if int(str(slotNumber + 10)[:-1]) == stackNumber
				]
				hiddenInCurrentStack = []
				for windowNumber in numbersInCurrentStack:
					hiddenInCurrentStack.append(
						hiddenWindow(
							windowNumber,
							str(self[windowNumber])
						)
					)
				yield stack(stackNumber, sorted(hiddenInCurrentStack, key=lambda slot: slot.presentationalNumber))


class windowWithHandle:

	def __init__(self, handle=None, windowTitle=None, appName=None):
		if handle:
			if winUser.isWindow(handle) == 0:
				raise ValueError("Cannot create object for non existing window")
			else:
				self.handle = handle
				self.windowTitle = windowTitle
				self.appName = appName
		else:
			self.handle = api.getForegroundObject().windowHandle
			self.windowTitle = api.getForegroundObject().name
			self.appName = appModuleHandler.getAppNameFromProcessID(api.getForegroundObject().processID, True)

	@property
	def isAlive(self):
		return bool(winUser.isWindow(self.handle))

	@property
	def windowText(self):
		return winUser.getWindowText(self.handle)

	def __str__(self):
		# Translators: Text describing hidden window. For example: "Untitled -  notepad from process notepad.exe"
		return _("{} from process {}").format(self.windowTitle, self.appName)

	def setWindowText(self, text):
		res = winUser.user32.SetWindowTextW(self.handle, text)
		return res

	def canBeHidden(self):
		if self.windowText == "Start":
			return False
		elif winUser.getClassName(self.handle) in (
			"WorkerW",
			"Progman",
			"Shell_TrayWnd",
			"DV2ControlHost",
			"Windows.UI.Core.CoreWindow"
		):
			return False
		else:
			return True

	def hide(self):
		if self.canBeHidden():
			winUser.user32.ShowWindowAsync(self.handle, winUser.SW_HIDE)
		else:
			raise RuntimeError("This window cannot be hidden")

	def show(self, setFocus=False):
		SW_SHOW = 5
		winUser.user32.ShowWindowAsync(self.handle, SW_SHOW)
		if setFocus:
			winUser.user32.SetFocus(self.handle)


class process:

	PRIORITIES = (
		Priority(
			64,
			# Translators: Name of the process priority
			name=_("Idle")
		),
		Priority(
			16384,
			# Translators: Name of the process priority
			name=_("Below Normal")
		),
		Priority(
			32,
			# Translators: Name of the process priority
			name=_("Normal")
		),
		Priority(
			32768,
			# Translators: Name of the process priority
			name=_("Above normal")
		),
		Priority(
			128,
			# Translators: Name of the process priority
			name=_("High")
		),
		Priority(
			256,
			# Translators: Name of the process priority
			name=_("Real time")
		),
	)

	def __init__(self, PID=None):
		if PID:
			self.pid = PID
		else:
			self.pid = api.getFocusObject().processID

	def kill(self):
		PROCESS_TERMINATE = 1
		handle = winKernel.kernel32.OpenProcess(PROCESS_TERMINATE, 0, self.pid)
		res = winKernel.kernel32.TerminateProcess(handle, 0)
		winKernel.kernel32.CloseHandle(handle)
		return res

	def getProcessPriority(self):
		PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
		handle = winKernel.kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, 0, self.pid)
		res = winKernel.kernel32.GetPriorityClass(handle)
		winKernel.kernel32.CloseHandle(handle)
		return res

	def setProcessPriorityByIndex(self, index):
		PROCESS_SET_INFORMATION = 0x0200
		handle = winKernel.kernel32.OpenProcess(PROCESS_SET_INFORMATION, 0, self.pid)
		res = winKernel.kernel32.SetPriorityClass(handle, process.PRIORITIES[index].constant)
		winKernel.kernel32.CloseHandle(handle)
		return res


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	scriptCategory = _("Win Wizard")

	def __init__(self):
		super().__init__()
		if globalVars.appArgs.secure:
			return
		self.hiddenWindowsList = hiddenWindowsList()

	def terminate(self):
		super().terminate()
		self.hiddenWindowsList.save()
		del self.hiddenWindowsList

	@scriptHandler.script(
		description=_(
			# Translators: Description of the keyboard command
			# allowing to jump between top-level windows of the current application.
			"Jumps between top-level windows of the current application."
		),
		gesture="kb:NVDA+windows+Tab",
		category=SCRCAT_FOCUS,
	)
	def script_cycleWindows(self, gesture):
		if(
			api.getForegroundObject()
			and api.getForegroundObject().parent
			and hasattr(api.getForegroundObject().parent, "appModule")
		):
			topWindow = api.getForegroundObject().parent
			topWindowAppModule = api.getForegroundObject().parent.appModule
			if topWindowAppModule.appName == "explorer":
				# Translators: Information given when user tries to move to top-level window in Windows  Explorer
				ui.message(_("Not supported here."))
				return
			nextTopWin = prevTopWin = None
			if topWindow.simplePrevious and topWindow.simplePrevious.appModule == topWindowAppModule:
				prevTopWin = topWindow.simplePrevious
			if topWindow.simpleNext and topWindow.simpleNext.appModule == topWindowAppModule:
				nextTopWin = topWindow.simpleNext
			if not prevTopWin and not nextTopWin:
				# Translators: Announced when the current application has no top-level windows.
				ui.message(_("This window has no top level windows to cycle to."))
				return
			elif prevTopWin and not nextTopWin:
				prevTopWin.setFocus()
			elif not prevTopWin and nextTopWin:
				nextTopWin.setFocus()
			else:
				# Translators: Announced when current program has multiple top-level windows.
				ui.message(_("Multiple top level windows detected."))
		else:
			# Translators: Reported when informations for the current window cannot be retrieved.
			ui.message(_("Can't retrieve window information for this object."))
			return

	@scriptHandler.script(
		# Translators: Description of the keyboard command that kills currently focused process.
		description=_("Kills currently focused process."),
		gesture="kb:windows+f4",
	)
	def script_killProcess(self, gesture):
		p = process()
		res = p.kill()
		if res == 0:
			# Translators: Announced when current process cannot be killed.
			ui.message(_("Cannot kill the current process"))
			return
		else:
			tones.beep(90, 80)

	@scriptHandler.script(
		# Translators: Description of the keyboard command used to change title of the curently focused window.
		description=_("Opens a dialog allowing to change title of the current window"),
		gesture="kb:control+alt+t",
	)
	def script_changeTitle(self, gesture):
		w = windowWithHandle()
		changeTitleDialog = wx.TextEntryDialog(
			gui.mainFrame,
			# Translators: Message in the dialog used to change title of the curently focused window.
			_("Enter the new title for this window:"),
			# Translators: Title of the dialog.
			_("Change window title"),
			w.windowText
		)

		def callback(result):
			if result == wx.ID_OK:
				newTitle = changeTitleDialog.GetValue()
				res = w.setWindowText(newTitle)
				if res == 0:
					wx.CallAfter(
						gui.messageBox,
						# Translators: Shown when changing of the current window title failed.
						_("Failed to change window title!"),
						# Translators: Title of the error dialog
						_("Error"),
						wx.OK | wx.ICON_ERROR
					)
					return
		gui.runScriptModalDialog(changeTitleDialog, callback)

	@scriptHandler.script(
		description=_(
			# Translators: Description of the keyboard command
			# that opens dialog allowing to change priority of the currently focused program.
			"Opens dialog used to change priority of the process of currently focused program."
		),
		gesture="kb:windows+nvda+p",
	)
	def script_changeProcessPriority(self, gesture):
		currentProcess = process()
		wx.CallAfter(changeProcessPriorityDialog.run, currentProcess)

	def _hideInSlot(self, slotNumber):
		focusedWindow = windowWithHandle()
		try:
			focusedWindow.hide()
			tones.beep(80, 80)
			self.hiddenWindowsList[slotNumber] = focusedWindow
		except RuntimeError:
			# Translators: Message informing user that the current window cannot be hidden.
			ui.message(_("Cannot hide this window!"))
			return
		self.hiddenWindowsList.save()

	def _showFromSlot(self, slotNumber):
		windowToShow = self.hiddenWindowsList.pop(slotNumber)
		self.hiddenWindowsList.save()
		if windowToShow.isAlive:
			windowToShow.show()
			tones.beep(180, 80)
		else:
			raise RuntimeError("This window no longer exists!")

	@scriptHandler.script(
		# Translators: Description of the keyboard command that shows or hides window at the current slot.
		description=_("Shows or hides window in the current slot."),
		gestures=[f"kb:windows+NVDA+{i}" for i in range(0, 10)],
	)
	def script_hideShowWindow(self, gesture):
		winNumber = int(gesture.mainKeyName) + (self.hiddenWindowsList.currentStack * 10)
		try:
			self._showFromSlot(winNumber)
		except (RuntimeError, KeyError):
			self._hideInSlot(winNumber)

	@scriptHandler.script(
		# Translators: Description of the keyboard command.
		description=_("Goes to the previous stack"),
		gesture="kb:windows+NVDA+leftArrow",
	)
	def script_previousStack(self, gesture):
		# Translators: Message announced when user switches to another stack.
		ui.message(_("Stack {}").format(self.hiddenWindowsList.previousStack() + 1))

	@scriptHandler.script(
		# Translators: Description of the keyboard command.
		description=_("Goes to the next stack"),
		gesture="kb:windows+NVDA+rightArrow",
	)
	def script_nextStack(self, gesture):
		# Translators: Announced when user switches to  another stack.
		ui.message(_("Stack {}").format(self.hiddenWindowsList.nextStack() + 1))

	@scriptHandler.script(
		# Translators: Description of the keyboard command.
		description=_("Hides  current window in the first available slot"),
		gesture="kb:windows+Shift+h",
	)
	def script_hideFirstAvailable(self, gesture):
		self._hideInSlot(self.hiddenWindowsList.firstEmptySlot())

	@scriptHandler.script(
		# Translators: Description of the keyboard command.
		description=_("Shows last hidden window"),
		gesture="kb:windows+NVDA+h",
	)
	def script_showLastHidden(self, gesture):
		try:
			self._showFromSlot(self.hiddenWindowsList.history[-1])
		except IndexError:
			# Translators: Announced when user attempts to show last hidden window but history is empty.
			ui.message(_("There is no window recorded as last hidden!"))
			return
		except RuntimeError:
			# Translators: Announced when user attempts to show last hidden window but it no loger exists.
			ui.message(_("Window recorded as last hidden no longer exists!"))
			return

	@scriptHandler.script(
		description=_(
			# Translators: Description of the keyboard command
			# that opens dialog allowing to unhide currently hidden windows.
			"Opens dialog for unhiding currently hidden windows."
		),
		gesture="kb:windows+Shift+l",
	)
	def script_unhideHiddenWindows(self, gesture):
		self.hiddenWindowsList.save()  # To remove dead windows from the list
		if len(self.hiddenWindowsList) > 0:
			wx.CallAfter(unhideWindowDialog.run, self.hiddenWindowsList)
		else:
			# Translators: Announced when user tries to display list of hidden windows but there are none hidden.
			ui.message(_("There are no windows currently hidden."))
			return
