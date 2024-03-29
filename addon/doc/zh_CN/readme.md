# Win Wizard-窗口管理 #

* Author: Oriol Gómez, Łukasz Golonka, current maintenance by Jakub Lukowicz
* NVDA兼容性： 2019.3及以上
* 下载 [稳定版][1]

This add-on allows you to perform some operations on the focused window or
the process associated with it.  When killing a process, or showing / hiding
a window a confirmation beep is played when the action succeeds.  If you
find this annoying you can disable these beeps in the Win Wizard's settings
panel available from NVDA's settings dialog.

## 快捷键：
以下快捷键都可以在“输入手势”下的“窗口管理”类别下重新设置。
### 隐显窗口：
* NVDA + Windows + 从1到0的数字——在与所按数字相对应的位置隐藏当前所聚焦的窗口（再次按下则显示）。
* NVDA + Windows + 左光标——移至上一个隐藏窗口分组。
* NVDA + Windows + 右光镖——移至下一个隐藏窗口分组。
* Windows + Shift + H——隐藏当前窗口至第一个可用位置。
* NVDA + Windows + H——显示最后一个被隐藏的窗口。
* Windows + Shift + L——打开一个对话框，将被隐藏的窗口按分组显示在列表内（默认选中最后一个隐藏的窗口）。

### 进程管理
* Windows + F4——结束与当前所聚焦窗口关联的进程。
* NVDA + Windows + P——打开一个对话框来设置与当前所聚焦窗口关联的进程优先级。

### 其他命令：
* NVDA+Windows+TAB - switches between top level windows of the current
  program (useful in foobar2000, Back4Sure etc.)
* CTRL + ALT + T——打开更改当前窗口标题的对话框。

## 更新：

### Changes for 5.0.6:

* Compatibility with NVDA 2024.1
* Update translations

### Changes for 5.0.5:

* Compatibility with NVDA 2023.2
* Update translations

### Changes for 5.0.4:

* Compatibility with NVDA 2022.1
* It is now possible to disable confirmation beeps in the add-ons settings
  panel
* Update translations

### 5.0.3 的更新：

* 兼容 NVDA 2021.1

### 5.0.2 的更新：

* First release available from the add-ons website

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=winwizard
