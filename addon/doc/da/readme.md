# Win Wizard #

* Forfatter: Oriol Gómez, vedligeholdes i øjeblikket af Łukasz Golonka
* NVDA-kompatibilitet: 2019.3 og derefter
* Download [stabil version][1]

This add-on allows you to perform some operations on the focused window or
the process associated with it.  When killing a process, or showing / hiding
a window a confirmation beep is played when the action succeeds.  If you
find this annoying you can disable these beeps in the Win Wizard's settings
panel available from NVDA's settings dialog.

## Tastaturkommandoer
Alle tilhørende kommandoer kan ændres fra dialogboksen "Håndter kommandoer"
under kategorien "Win Wizard".
### Skjul og vis skjulte vinduer
* NVDA+Windows+numre fra 1 til 0 - skjuler det aktuelt fokuserede vindue for
  tallet svarende til det trykte nummer
* NVDA+Windows+venstre pil - flytter til den forrige stak af skjulte vinduer
* NVDA+Windows+højre pil - flytter til den næste stak af skjulte vinduer
* Windows+Shift+h - skjuler det aktuelt fokuserede vindue på den første
  tilgængelige plads
* NVDA+Windows+h - viser det sidste skjulte vindue
* Windows+Shift+l - viser listen over alle skjulte vinduer grupperet efter
  deres tilhørende stakken (bemærk, at det sidste skjulte vindue som
  standard er valgt)

### Styring af processer
* Windows+F4 - afslutter processen, der er knyttet til det aktuelt
  fokuserede vindue
* NVDA+Windows+p - åbner dialog, der giver dig mulighed for at indstille
  prioritet for den proces, der er knyttet til det aktuelt fokuserede vindue

### Diverse kommandoer
* NVDA+Windows+TAB - switches between top level windows of the current
  program (useful in foobar2000, Back4Sure etc.)
* CTRL+ALT+T - giver dig mulighed for at ændre titlen på det aktuelt
  fokuserede program

## Ændringer

### Changes for 5.0.4:

* Compatibility with NVDA 2022.1
* It is now possible to disable confirmation beeps in the add-ons settings
  panel
* Update translations

### Ændringer i 5.0.3:

* Kompatibilitet med NVDA 2021.1

### Ændringer i 5.0.2:

* First release available from the add-ons website

[[!tag dev stable]]

[1]: https://addons.nvda-project.org/files/get.php?file=winwizard
