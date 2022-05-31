# Win Wizard

* Author: Oriol Gómez, current maintenance by Łukasz Golonka
* NVDA compatibility: 2019.3 and beyond

This add-on allows you to perform some operations on the focused window or the process associated with it.
When killing a process, or showing / hiding a window a confirmation beep is played when the action succeeds.
If you find this annoying you can disable these beeps in the Win Wizard's settings panel available from NVDA's settings dialog.

## Keyboard commands:
All these commands can be remapped from the Input gestures dialog in the Win Wizard category.
### Hiding and showing hidden windows:
* NVDA+Windows+numbers from 1 to 0 - hides  currently focused window in the slot corresponding to the pressed number
* NVDA+Windows+left arrow - moves to the previous stack of hidden windows.
* NVDA+Windows+right arrow - moves to the next stack of hidden windows.
* Windows+Shift+h - hides the currently focused window in the first available slot
* NVDA+Windows+h - shows the last hidden window
* Windows+Shift+l - shows the list of all hidden windows grouped by the stacks (please note that by default last hidden window is selected)

### Managing processes:
* Windows+F4 - kills the process associated with the currently focused window
* NVDA+Windows+p - opens dialog allowing you to set priority of the process associated with the currently focused window

### Miscellaneous  commands:
* NVDA+Windows+TAB - switches between top level windows of the current program (useful in foobar2000, Back4Sure etc.)
* CTRL+ALT+T - allows you to change title of the currently focused program

## Changes:

### Changes for 5.0.4:

* Compatibility with NVDA 2022.1
* It is now possible to disable confirmation beeps in the add-ons settings panel
* Update translations

### Changes for 5.0.3:

* Compatibility with NVDA 2021.1

### Changes for 5.0.2:

* First release available from the add-ons website
