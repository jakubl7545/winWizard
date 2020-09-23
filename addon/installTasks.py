# -*- coding: UTF-8 -*-
# Install tasks for Win Wizard add-on
# Released under GPL 2

import addonHandler


def onInstall():
	for addon in addonHandler.getAvailableAddons(filterFunc=lambda addon: not addon.isPendingInstall):
		if addon.name == "winWizard":
			oldVersionPath = addon.path
			import os
			for (basedir, dirs, files) in os.walk(oldVersionPath):
				for file in files:
					if file == "hiddenwindows.dat":
						import shutil
						shutil.copy(
							os.path.abspath(os.path.join(basedir, file)),
							os.path.abspath(os.path.join(os.path.dirname(__file__), "globalPlugins"))
						)
