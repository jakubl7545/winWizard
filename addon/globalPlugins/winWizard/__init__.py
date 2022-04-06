import globalVars
import globalPluginHandler


if globalVars.appArgs.secure:
	GlobalPlugin = globalPluginHandler.GlobalPlugin
else:
	from . import winWizard
	GlobalPlugin = winWizard.GlobalPlugin
