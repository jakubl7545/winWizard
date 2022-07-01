# Win čarobnjak (Win Wizard) #

* Autor: Oriol Gómez, dodatak trenutačno održava Łukasz Golonka
* NVDA kompatibilnost: 2019.3 i novije verzije
* Preuzmi [stablnu verziju][1]

This add-on allows you to perform some operations on the focused window or
the process associated with it.  When killing a process, or showing / hiding
a window a confirmation beep is played when the action succeeds.  If you
find this annoying you can disable these beeps in the Win Wizard's settings
panel available from NVDA's settings dialog.

## Tipkovne naredbe:
Sve ove naredbe mogu se ponovo odrediti u dijaloškom okviru ulaznih gesta u
kategoriji Win čarobnjak.
### Prikazivanje i skrivanje skrivenih prozora:
* NVDA+Windows+brojke od 1 do 0 – skriva trenutačno fokusirani prozor na
  položaj koji odgovara pritisnutoj brojki
* NVDA+Windows+strelica lijevo – premješta prethodni skup skrivenih prozora.
* NVDA+Windows+strelica desno – premješta sljedeći skup skrivenih prozora.
* Windows+šift+h – skriva trenutačno fokusirani prozor u prvom dostupnom
  položaju
* NVDA+Windows+h – prikazuje zadnji skriveni prozor
* Windows+šift+l – prikazuje popis svih skrivenih prozora grupiranih u
  skupovima (standardno se bira zadnji skriveni prozor)

### Upravljanje procesima:
* Windows+F4 – prekida proces koji je povezan s trenutačno fokusiranim
  prozorom
* NVDA+Windows+p – otvara dijaloški okvir za prioriziranje procesa koji je
  povezan s trenutačno fokusiranim prozorom

### Razne naredbe:
* NVDA+Windows+TAB - switches between top level windows of the current
  program (useful in foobar2000, Back4Sure etc.)
* CTRL+ALT+T – omogućuje mijenjanje naslova trenutačno fokusiranog programa

## Promjene:

### Changes for 5.0.4:

* Compatibility with NVDA 2022.1
* It is now possible to disable confirmation beeps in the add-ons settings
  panel
* Update translations

### Promjene u 5.0.3:

* Kompatibilnost s NVDA 2021.1

### Promjene u 5.0.2:

* First release available from the add-ons website

[[!tag dev stable]]

[1]: https://addons.nvda-project.org/files/get.php?file=winwizard
