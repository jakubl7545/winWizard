# Win Wizard #

* Autor: Oriol Gómez, mantido actualmente por Łukasz Golonka
* Compatibilidade co NVDA: 2019.3 en diante
* Descargar [versión estable][1]

This add-on allows you to perform some operations on the focused window or
the process associated with it.  When killing a process, or showing / hiding
a window a confirmation beep is played when the action succeeds.  If you
find this annoying you can disable these beeps in the Win Wizard's settings
panel available from NVDA's settings dialog.

## Ordes de teclas:
Todos estes comandos pódense reasignar dende o diálogo Xestos de entrada na
categoría Win Wizard.
### Ocultando e amosando ventás ocultas:
* NVDA+Windows+números do 1 ó 0 - oculta a ventá actualmente co foco na
  posición correspondente ó número premido
* NVDA+Windows+frecha esquerda - móvese á pía anterior de ventás ocultas.
* NVDA+Windows+frecha dereita - móvese á seguinte pía de ventás ocultas.
* Windows+Shift+h - oculta a ventá actualmente co foco na primeira posición
  dispoñible
* NVDA+Windows+h - amosa a última ventá ocultada
* Windows+Shift+l - amosa a lista de todas as ventás ocultas agrupadas por
  pía (ten en conta que se selecciona a última ventá ocultada)

### Administrando procesos:
* Windows+F4 - mata o proceso asociado coa ventá actualmente co foco
* NVDA+Windows+p - abre un diálogo que che permite establecer a prioridade
  do proceso asociado coa ventá actualmente co foco

### Ordes misceláneas:
* NVDA+Windows+TAB - switches between top level windows of the current
  program (useful in foobar2000, Back4Sure etc.)
* CTRL+ALT+T - permíteche cambiar o título do programa actualmente co foco

## Trocos:

### Changes for 5.0.4:

* Compatibility with NVDA 2022.1
* It is now possible to disable confirmation beeps in the add-ons settings
  panel
* Update translations

### Trocos para 5.0.3:

* Compatibilidade con NVDA 2021.1

### Trocos para 5.0.2:

* First release available from the add-ons website

[[!tag dev stable]]

[1]: https://addons.nvda-project.org/files/get.php?file=winwizard
