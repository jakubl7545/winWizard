# Ikkunavelho #

* Tekijä: Oriol Gómez, nykyinen ylläpitäjä Łukasz Golonka
* Yhteensopivuus: NVDA 2019.3 tai uudempi
* Lataa [vakaa versio][1]

This add-on allows you to perform some operations on the focused window or
the process associated with it.  When killing a process, or showing / hiding
a window a confirmation beep is played when the action succeeds.  If you
find this annoying you can disable these beeps in the Win Wizard's settings
panel available from NVDA's settings dialog.

## Näppäinkomennot:
Näitä komentoja voidaan muuttaa Näppäinkomennot-valintaikkunan
Ikkunavelho-kategoriasta.
### Ikkunoiden piilottaminen ja piilotettujen ikkunoiden näyttäminen:
* NVDA+Win+numerot 1-0: Piilottaa aktiivisen ikkunan painettua numeroa
  vastaavaan paikkaan.
* NVDA+Win+Vasen nuoli: Siirtää edelliseen piilotettujen ikkunoiden pinoon.
* NVDA+Win+Oikea nuoli: Siirtää seuraavaan piilotettujen ikkunoiden pinoon.
* Win+Vaihto+H: Piilottaa aktiivisen ikkunan ensimmäiseen käytettävissä
  olevaan paikkaan.
* NVDA+Win+H: Näyttää viimeksi piilotetun ikkunan.
* Win+Vaihto+L: Näyttää luettelon kaikista piilotetuista ikkunoista pinojen
  mukaan ryhmiteltyinä (viimeksi piilotettu ikkuna on oletusarvoisesti
  valittuna).

### Prosessien hallinta:
* Win+F4: Lopettaa aktiiviseen ikkunaan liittyvän prosessin.
* NVDA+Win+P: Avaa valintaikkunan, jossa voit asettaa aktiiviseen ikkunaan
  liittyvän prosessin prioriteetin.

### Sekalaiset komennot:
* NVDA+Windows+TAB - switches between top level windows of the current
  program (useful in foobar2000, Back4Sure etc.)
* Ctrl+Alt+T: Mahdollistaa aktiivisen ohjelman ikkunan nimen muuttamisen.

## Muutokset:

### Changes for 5.0.4:

* Compatibility with NVDA 2022.1
* It is now possible to disable confirmation beeps in the add-ons settings
  panel
* Update translations

### Muutokset versiossa 5.0.3:

* Yhteensopiva NVDA 2021.1:n kanssa

### Muutokset versiossa 5.0.2:

* First release available from the add-ons website

[[!tag dev stable]]

[1]: https://addons.nvda-project.org/files/get.php?file=winwizard
