# WinWizard #

* Author: Oriol Gómez, Łukasz Golonka, current maintenance by Jakub Lukowicz
* NVDA-kompatibilitet: 2019.3 og derefter
* Download [stabil version][1]

Denne tilføjelse giver dig mulighed for at udføre nogle handlinger på det
fokuserede vindue eller den proces, der er forbundet med det. Når du dræber
en proces, eller viser/skjuler et vindue, afspilles et bekræftelsesbip, når
handlingen lykkes. Hvis du finder dette irriterende, kan du deaktivere disse
bip i WinWizards indstillingspanel, der er tilgængeligt fra NVDAs
indstillingsdialog.

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
* NVDA+Windows+TAB - skifter mellem vinduer på øverste niveau i det aktuelle
  program (nyttigt i foobar2000, Back4Sure osv.) Da denne kommando flytter
  systemfokus, kan den findes i kategorien Systemfokus i dialogboksen
  "Håndter kommandoer"
* CTRL+ALT+T - giver dig mulighed for at ændre titlen på det aktuelt
  fokuserede program

## Ændringer

### Changes for 5.0.5:

* Compatibility with NVDA 2023.2
* Opdateret oversættelser

### Ændringer for 5.0.4:

* Kompatibilitet med NVDA 2022.1.
* Det er nu muligt at deaktivere bekræftelsesbip i indstillingspanelet for
  tilføjelsen.
* Opdateret oversættelser

### Ændringer i 5.0.3:

* Kompatibilitet med NVDA 2021.1

### Ændringer i 5.0.2:

* - Første frigivelse tilgængelig fra tilføjelseswebstedet.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=winwizard
