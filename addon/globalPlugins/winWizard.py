# -*- coding: UTF-8 -*-

# WinWizard add-on for NVDA
# This file is covered by the GNU General Public License.
# See the file COPYING.txt for more details.
# Copyright (C) 2020-2022 Oriol Gomez <ogomez.s92@gmail.com>
# Currently maintained by Łukasz Golonka <lukasz.golonka@mailbox.org>

from __future__ import annotations

import collections
import contextlib
import dataclasses
import enum
import os
import pickle
import weakref
from typing import (
	TYPE_CHECKING,
	ClassVar,
	Iterable,
	Iterator,
	Generator,
	List,
	Optional,
	Type,
)

import globalPluginHandler
import appModuleHandler
import addonHandler
import config
import ui
import scriptHandler
import api
import winKernel
import winUser
import tones
import wx
import gui
import gui.guiHelper
import gui.settingsDialogs as gsd
import globalVars

if TYPE_CHECKING:
	# While these imports are harmless, and can be done at runtime,
	# they're used only for type annotations, and we use stringified from of type hints anyway.
	import inputCore

addonHandler.initTranslation()


def playTonesIfEnabled(*args, **kwargs) -> None:
	if config.conf["winWizard"]["playConfirmationBeeps"]:
		tones.beep(*args, **kwargs)


class WinWizardSettingsPanel(gsd.SettingsPanel):

	title = _("winWizard")

	def makeSettings(self, settingsSizer):
		sHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		# Translators: Label of a checkbox which can be used to enable or disable sounds.
		self.enableBeepsChk = sHelper.addItem(wx.CheckBox(self, label=_("&Confirm actions with sounds")))
		self.enableBeepsChk.SetValue(config.conf["winWizard"]["playConfirmationBeeps"])

	def postInit(self):
		self.enableBeepsChk.SetFocus()

	def onSave(self):
		config.conf["winWizard"]["playConfirmationBeeps"] = self.enableBeepsChk.GetValue()


class Win32FunctionError(Exception):
	"""Raised when a Win32 function (such as the one for killing processes) fails."""


class PRIORITIES(enum.IntEnum):

	"""Enumerates all possible process priorities.

	The full list with the more detailed description can be found at:
	https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-setpriorityclass#parameters
	"""

	IDLE = 64
	BELOW_NORMAL = 16384
	NORMAL = 32
	ABOVE_NORMAL = 32768
	HIGH = 128
	REAL_TIME = 256

	def __str__(self) -> str:
		"""Return the descriptio nof the given priority, used when displaying in the GUI."""
		return {
			# Translators: Name of the process priority
			PRIORITIES.IDLE: _("Idle"),
			# Translators: Name of the process priority
			PRIORITIES.BELOW_NORMAL: _("Below Normal"),
			# Translators: Name of the process priority
			PRIORITIES.NORMAL: _("Normal"),
			# Translators: Name of the process priority
			PRIORITIES.ABOVE_NORMAL: _("Above normal"),
			# Translators: Name of the process priority
			PRIORITIES.HIGH: _("High"),
			# Translators: Name of the process priority
			PRIORITIES.REAL_TIME: _("Real time"),
		}[self]


@dataclasses.dataclass
class Stack:

	"""Representation of a single stack of hidden windows, used when displaying them in the GUI."""

	stackNumber: int
	hiddenInStack: Iterable[HiddenWindow]

	def __str__(self) -> str:
		# Translators: Name of the stack shown in the dialog - for example Stack 1.
		return _("Stack {}").format(self.stackNumber)

	@property
	def numbers(self) -> Iterator[int]:
		for window in self.hiddenInStack:
			yield from window.numbers


@dataclasses.dataclass
class HiddenWindow:

	"""Stores data about a single hidden window. This is used only in the GUI."""

	slotNumber: int
	textualRepresentation: str
	presentationalNumber: int = dataclasses.field(init=False)

	def __post_init__(self) -> None:
		self.presentationalNumber = self.slotNumber
		if self.presentationalNumber % 10 == 0:
			# Slots are internally numbered from 0
			# Renumber them for showing in the GUI
			self.presentationalNumber += 10

	def __str__(self) -> str:
		# Translators: Text of the  entry for the hidden window in the hidden windows tree.
		return _("{}: {}").format(self.presentationalNumber, self.textualRepresentation)

	@property
	def numbers(self) -> Iterator[int]:
		yield self.slotNumber


class baseSingletonDialog(wx.Dialog):

	title: ClassVar[str] = ""
	_instance: ClassVar[Optional[weakref.ReferenceType[baseSingletonDialog]]] = None

	def __new__(cls, *args, **kwargs):
		if not cls._instance or not cls._instance():
			# Either dialog has never been opened, so the class variable is `None`,
			# or there is no live reference.
			# We can continue constructing the object.
			return super().__new__(cls, *args, **kwargs)

	def __init__(self, *args, **kwargs):
		self.__class__._instance = weakref.ref(self)
		super().__init__(parent=gui.mainFrame, title=self.title)

	def onClose(self, evt):
		self.Destroy()

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

	def __init__(self, currentProcess: Process) -> None:
		self.currentProcess = currentProcess
		super().__init__()
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		sHelper = gui.guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)
		self.priorities = sHelper.addItem(
			wx.RadioBox(
				self,
				# Translators: Label for the group of radio buttons for choosing a process priority.
				label=_("Choose priority"),
				choices=[str(priority) for priority in PRIORITIES],
				style=wx.RA_SPECIFY_ROWS
			)
		)
		self.priorities_to_indexes = {prio: index for index, prio in enumerate(PRIORITIES)}
		currentPriorityIndex = self.priorities_to_indexes[currentProcess.getProcessPriority()]
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
		self.currentProcess.setProcessPriority({k: v for v, k in self.priorities_to_indexes.items()}[priorityToSet])
		self.Destroy()


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

	def populateTree(self) -> None:
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


class hiddenWindowsList (collections.UserDict):

	SAVE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "hiddenwindows.dat")
	"""Path to the file storing hidden windows.

	Hidden windows are preserved between NVDA restarts, and even between add-on updates
	(see the installTasks module for the function which migrates them during update).
	Name of the file, and its location are kept for historical reasons,
	so that people who have hidden windows using version of winWizard maintained by Oriol,
	can update without unhiding all their windows beforehand.
	The file is expected to be placed in the `globalPlugins` folder - that is why winWizard is not a package,
	so that we can easily calculate path relative to winWizard's Python file.
	"""

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.currentStack: int = 0
		self.history: List[int] = list()
		# Load hidden windows from a saved file, if it exists.
		# If it does not, jjust ignore the error.
		# The format of the hidden windows list is documented in the docstring of `save` method.
		with contextlib.suppress(FileNotFoundError):
			with open(self.SAVE_PATH, "rb") as f:
				for value in pickle.load(f).values():
					handle, windowTitle, appName, number = value
					try:
						self[number] = Window(handle=handle, windowTitle=windowTitle, appName=appName)
					except ValueError:
						continue
		self.history.clear()  # Inserting windows from the file didn't preserve order, so there is no history.
		self.save()

	def __setitem__(self, key, value):
		self.history.append(key)
		super().__setitem__(key, value)

	def __delitem__(self, key):
		with contextlib.suppress(ValueError):  # Occurs when unhiding window from save file, hence no history entry.
			self.history.remove(key)
		super().__delitem__(key)

	def save(self) -> None:
		"""Dumps hidden windows to a file.

		Format of the dump is the same as in Oriol's version, to ease migration.
		The data is dumped as a dictionary, in which key is the slot in which the window was hidden,
		and the value is a list which contains in order:
		handle of the window, window's title, name of the application in which the window exists
		and once again a slot number (the redundancy is to keep compatible with the old format).
		Note that only valid windows are saved,
		and when this method is called on an empty list save file is removed.
		"""
		fileContent = dict()
		for slot in list(self.keys()):
			if self[slot].isAlive:
				fileContent[slot] = [self[slot].handle, self[slot].windowTitle, self[slot].appName, slot]
			else:
				del self[slot]
		if len(self) == 0:
			try:
				os.remove(self.SAVE_PATH)
			except FileNotFoundError:
				return
		else:
			with open(self.SAVE_PATH, "wb") as f:
				pickle.dump(fileContent, f)

	def previousStack(self) -> int:
		self.currentStack -= 1
		if self.currentStack < 0:
			self.currentStack = 0
		return self.currentStack

	def nextStack(self) -> int:
		self.currentStack += 1
		return self.currentStack

	def firstEmptySlot(self) -> int:
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
						HiddenWindow(
							windowNumber,
							str(self[windowNumber])
						)
					)
				yield Stack(stackNumber, sorted(hiddenInCurrentStack, key=lambda slot: slot.presentationalNumber))


class Window:

	"""Stores data about a single window in the operating system.

	The data can be either loaded from a file which stores list of all windows hidden by the user,
	or the instance can be created based on the currently focused window.
	When trying to create instance  for a window  whose handle is no longer valid,
	``ValueError`` is raised.
	If you want to avoid this check (usefull when you're creating an object from a focused window),
	`verify_handle_valid` can be set to `False` in the initializer.
	"""

	def __init__(self, handle: int, windowTitle: str, appName: str, verify_handle_valid: bool = True) -> None:
		if verify_handle_valid:
			if not self._handle_valid(handle):
				raise ValueError("Cannot create object for non existing window")
		self.handle = handle
		self.windowTitle = windowTitle
		self.appName = appName

	@classmethod
	def from_focused_window(cls: Type[Window]) -> Window:  # cls annotated, to avoid VS Code bug
		return cls(
			handle=api.getForegroundObject().windowHandle,
			windowTitle=api.getForegroundObject().name,
			appName=appModuleHandler.getAppNameFromProcessID(api.getForegroundObject().processID, True),
			verify_handle_valid=False
		)

	@property
	def isAlive(self) -> bool:
		return self._handle_valid(self.handle)

	def _handle_valid(self, handle: int) -> bool:
		return bool(winUser.isWindow(handle))

	@property
	def windowText(self) -> str:
		return winUser.getWindowText(self.handle)

	def __str__(self) -> str:
		# Translators: Text describing hidden window. For example: "Untitled -  notepad from process notepad.exe"
		return _("{} from process {}").format(self.windowTitle, self.appName)

	def setWindowText(self, text: str) -> None:
		if winUser.user32.SetWindowTextW(self.handle, text) == 0:
			raise Win32FunctionError

	def canBeHidden(self) -> bool:
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

	def hide(self) -> None:
		if self.canBeHidden():
			winUser.user32.ShowWindowAsync(self.handle, winUser.SW_HIDE)
		else:
			raise RuntimeError("This window cannot be hidden")

	def show(self, setFocus: bool = False) -> None:
		SW_SHOW = 5
		winUser.user32.ShowWindowAsync(self.handle, SW_SHOW)
		if setFocus:
			winUser.user32.SetFocus(self.handle)


class PROCESS_ACCESS_RIGHTS(enum.IntEnum):

	"""Incomplete, limited only to these we're actually using, list of process access rights.

	Full list is available at:
	https://learn.microsoft.com/en-us/windows/win32/procthread/process-security-and-access-rights
	"""

	PROCESS_TERMINATE = 1
	PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
	PROCESS_SET_INFORMATION = 0x0200


@dataclasses.dataclass
class Process:

	"""Represents a single process in the operating system.

	It can be either initialized by passing PID of an exisiting process to the initializer,
	or by using factory method which creates it from the process of the currenty focused window.
	"""

	pid: int

	@classmethod
	def from_Focused_process(cls) -> Process:
		return cls(api.getFocusObject().processID)

	@staticmethod
	@contextlib.contextmanager
	def open_handle_with_access_rights(
			process: Process,
			access_right: PROCESS_ACCESS_RIGHTS
	) -> Generator[int, None, None]:
		handle = winKernel.kernel32.OpenProcess(access_right.value, 0, process.pid)
		try:
			yield handle
		finally:
			winKernel.kernel32.CloseHandle(handle)

	def kill(self) -> None:
		with self.open_handle_with_access_rights(self, PROCESS_ACCESS_RIGHTS.PROCESS_TERMINATE) as handle:
			if winKernel.kernel32.TerminateProcess(handle, 0) == 0:
				raise Win32FunctionError("Failed to kill the process.")

	def getProcessPriority(self) -> PRIORITIES:
		with self.open_handle_with_access_rights(
			self, PROCESS_ACCESS_RIGHTS.PROCESS_QUERY_LIMITED_INFORMATION
		) as handle:
			return PRIORITIES(winKernel.kernel32.GetPriorityClass(handle))

	def setProcessPriority(self, priority_to_set: PRIORITIES) -> None:
		with self.open_handle_with_access_rights(self, PROCESS_ACCESS_RIGHTS.PROCESS_SET_INFORMATION) as handle:
			winKernel.kernel32.SetPriorityClass(handle, priority_to_set.value)


def disableInSecureMode(decoratedCls):
	if globalVars.appArgs.secure:
		return globalPluginHandler.GlobalPlugin
	return decoratedCls


@disableInSecureMode
class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	scriptCategory = _("Win Wizard")

	def __init__(self):
		super().__init__()
		confSpec = {"playConfirmationBeeps": "boolean(default=True)"}
		config.conf.spec["winWizard"] = confSpec
		self.hiddenWindowsList: hiddenWindowsList = hiddenWindowsList()
		gsd.NVDASettingsDialog.categoryClasses.append(WinWizardSettingsPanel)

	def terminate(self):
		super().terminate()
		self.hiddenWindowsList.save()
		del self.hiddenWindowsList
		gsd.NVDASettingsDialog.categoryClasses.remove(WinWizardSettingsPanel)

	@scriptHandler.script(
		description=_(
			# Translators: Description of the keyboard command
			# allowing to jump between top-level windows of the current application.
			"Jumps between top-level windows of the current application."
		),
		gesture="kb:NVDA+windows+Tab",
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

	@scriptHandler.script(
		# Translators: Description of the keyboard command that kills currently focused process.
		description=_("Kills currently focused process."),
		gesture="kb:windows+f4",
	)
	def script_killProcess(self, gesture: inputCore.InputGesture) -> None:
		try:
			Process.from_Focused_process().kill()
		except Win32FunctionError:
			# Translators: Announced when current process cannot be killed.
			ui.message(_("Cannot kill the current process"))
		else:
			playTonesIfEnabled(90, 80)

	@scriptHandler.script(
		# Translators: Description of the keyboard command used to change title of the curently focused window.
		description=_("Opens a dialog allowing to change title of the current window"),
		gesture="kb:control+alt+t",
	)
	def script_changeTitle(self, gesture: inputCore.InputGesture) -> None:
		w = Window.from_focused_window()
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
				try:
					w.setWindowText(newTitle)
				except Win32FunctionError:
					wx.CallAfter(
						gui.messageBox,
						# Translators: Shown when changing of the current window title failed.
						_("Failed to change window title!"),
						# Translators: Title of the error dialog
						_("Error"),
						wx.OK | wx.ICON_ERROR
					)
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
		currentProcess = Process.from_Focused_process()
		wx.CallAfter(changeProcessPriorityDialog.run, currentProcess)

	def _hideInSlot(self, slotNumber: int) -> None:
		focusedWindow = Window.from_focused_window()
		try:
			focusedWindow.hide()
			playTonesIfEnabled(80, 80)
			self.hiddenWindowsList[slotNumber] = focusedWindow
			self.hiddenWindowsList.save()
		except RuntimeError:
			# Translators: Message informing user that the current window cannot be hidden.
			ui.message(_("Cannot hide this window!"))

	def _showFromSlot(self, slotNumber: int) -> None:
		windowToShow = self.hiddenWindowsList.pop(slotNumber)
		self.hiddenWindowsList.save()
		if windowToShow.isAlive:
			windowToShow.show()
			playTonesIfEnabled(180, 80)
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
		except RuntimeError:
			# Translators: Announced when user attempts to show last hidden window but it no longer exists.
			ui.message(_("Window recorded as last hidden no longer exists!"))

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
