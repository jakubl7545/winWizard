# Win Wizard (Майстер вікон) #

* Автор: Oriol Gómez, поточне обслуговування Łukasz Golonka
* Сумісність з NVDA: 2019.3 та новіші
* Завантажити [стабільну версію][1]

This add-on allows you to perform some operations on the focused window or
the process associated with it.  When killing a process, or showing / hiding
a window a confirmation beep is played when the action succeeds.  If you
find this annoying you can disable these beeps in the Win Wizard's settings
panel available from NVDA's settings dialog.

## Комбінації клавіш:
Всі ці команди можна перепризначити у діалозі жестів вводу в категорії Win
Wizard.
### Приховування й відображення прихованих вікон:
* NVDA+Windows+числа від 1 до 0- приховує поточне вибране вікно в слоті,
  який відповідає натиснутому номеру
* NVDA+Windows+стрілка вліво - переходить до попередньої полиці прихованих
  вікон.
* NVDA+Windows+стрілка вправо - переходить до наступної полиці прихованих
  вікон.
* NVDA+Windows+left arrow - приховує поточне виділене вікно в першому
  доступному слоті
* NVDA+Windows+h -  відображає останнє приховане вікно
* Windows+Shift+l -  відображає список всіх прихованих вікон згрупованих за
  полицями (будь ласка, зауважте, що початково вибрано останнє приховане
  вікно)

### Керування процесами:
* Windows+F4 - завершує процес пов'язаний з поточним вибраним вікном
* NVDA+Windows+p -  відкриває діалог, що дозволяє встановити пріоритет
  процесу, пов'язаного з поточним вибраним вікном

### Різні команди:
* NVDA+Windows+TAB - switches between top level windows of the current
  program (useful in foobar2000, Back4Sure etc.)
* CTRL+ALT+T -  дозволяє змінити назву поточної програми у фокусі

## Зміни:

### Changes for 5.0.4:

* Compatibility with NVDA 2022.1
* It is now possible to disable confirmation beeps in the add-ons settings
  panel
* Update translations

### Зміни у версії 5.0.3:

* Сумісність з NVDA 2021.1

### Зміни у версії 5.0.2:

* First release available from the add-ons website

[[!tag dev stable]]

[1]: https://addons.nvda-project.org/files/get.php?file=winwizard
