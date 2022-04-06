# -*- coding: UTF-8 -*-

# WinWizard add-on for NVDA
# This file is covered by the GNU General Public License.
# See the file COPYING.txt for more details.
# Copyright (C) 2020-2022 Oriol Gomez <ogomez.s92@gmail.com>
# Currently maintained by Łukasz Golonka <lukasz.golonka@mailbox.org>

import globalVars
import globalPluginHandler


if globalVars.appArgs.secure:
	GlobalPlugin = globalPluginHandler.GlobalPlugin
else:
	from . import winWizard
	GlobalPlugin = winWizard.GlobalPlugin
