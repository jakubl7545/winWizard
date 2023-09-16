# Win Wizard #

* Autor: Oriol Gómez, mantenido actualmente por Łukasz Golonka
* Compatibilidad con NVDA: 2019.3 y versiones posteriores
* Descargar [versión estable][1]

Este complemento permite realizar algunas operaciones en la ventana con el
foco o el proceso asociado a ella. Al matar un proceso, o mostrar/ocultar
una ventana, se reproduce un pitido de confirmación si la acción tiene
éxito. Si encuentras esto molesto, puedes desactivar los pitidos en el panel
de opciones de WinWizard, disponible en el diálogo de opciones de NVDA.

## Atajos de teclado:
Todas estas órdenes se pueden reasignar desde el diálogo Gestos de entrada,
en la categoría Win Wizard.
### Ocultar y mostrar ventanas ocultas:
* NVDA+windows+números del 1 al 0 - Oculta la ventana que tiene el foco en
  la ranura correspondiente al número pulsado
* NVDA+windows+flecha izquierda - Se mueve a la pila anterior de ventanas
  ocultas.
* NVDA+windows+flecha derecha - Se mueve a la siguiente pila de ventanas
  ocultas.
* Windows+shift+h - Oculta la ventana que tiene el foco actualmente en la
  primera ranura disponible
* NVDA+windows+h - Muestra la última ventana oculta
* Windows+shift+l - Muestra la lista de todas las ventanas ocultas agrupadas
  en pilas (ten en cuenta que se selecciona la última ventana oculta)

### Gestión de procesos:
* Windows+f4 - Termina el proceso asociado con la ventana que tiene
  actualmente el foco
* NVDA+windows+p - Abre un diálogo que permite establecer la prioridad del
  proceso asociado a la ventana con el foco

### Órdenes varias:
* NVDA+windows+tab - Alterna entre las ventanas de alto nivel del programa
  actual (útil en foobar2000, Back4Sure, etc.)
* Ctrl+alt+t - Permite cambiar el título del programa que tiene el foco

## Cambios:

### Cambios para 5.0.4:

* Compatibilidad con NVDA 2022.1
* Ahora es posible deshabilitar los pitidos de confirmación desde el panel
  de opciones del complemento
* Traducciones actualizadas

### Cambios para 5.0.3:

* Compatibilidad con NVDA 2021.1

### Cambios para 5.0.2:

* Primera versión disponible en el sitio web de complementos

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=winwizard
