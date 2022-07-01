# WinWizard #

* Autor: Oriol Gómez, aktuelle Wartung durch Łukasz Golonka
* NVDA-Kompatibilität: 2019.3 und neuer
* [Stabile Version herunterladen][1]

Mit dieser Erweiterung können Sie einige Operationen an dem fokussierten
Fenster oder dem damit verbundenen Prozess durchführen. Beim Beenden eines
Prozesses oder beim Ein- und Ausblenden eines Fensters ertönt ein Signalton
zur Bestätigung, wenn die Aktion erfolgreich war. Wenn Sie dies als störend
empfinden, können Sie diese Signaltöne in den Einstellungen der Erweiterung
deaktivieren, die Sie über den NVDA-Einstellungen aufrufen können.

## Tastaturbefehle:
Alle diese Befehle können im Dialogfeld für Tastenebefehle in der Kategorie
"WinWizard" neu zugeordnet werden.
### Versteckte Fenster ein- und ausblenden:
* NVDA+Windows+Zahlenreihe - Blendet das aktuell fokussierte Fenster in dem
  Slot aus, der der gedrückten Zahl entspricht
* NVDA+Windows+Pfeiltaste nach links - Wechselt zum vorherigen Stapel
  ausgeblendeter Fenster.
* NVDA+Windows+Pfeiltaste nach rechts - Wechselt zum nächsten Stapel
  ausgeblendeter Fenster.
* Windows+Umschalt+H - Blendet das aktuell fokussierte Fenster im ersten
  verfügbaren Slot aus
* NVDA+Windows+H - Zeigt das letzte ausgeblendete Fenster an
* Windows+Umschalt+L - Zeigt die Liste aller versteckten Fenster gruppiert
  nach den Stapeln an (bitte beachten Sie, dass standardmäßig das letzte
  versteckte Fenster ausgewählt ist)

### Prozesse verwalten:
* Windows+F4 - Beendet den Prozess des aktuell fokussierten Fensters
* NVDA+Windows+P - Öffnet ein Dialogfeld, in dem Sie die Priorität des
  Prozesses für das aktuell fokussierte Fenster festlegen können

### Verschiedene Befehle:
* NVDA+Windows+TAB - Schaltet zwischen den Fenstern der obersten Ebene des
  aktuellen Programms um (nützlich in Foobar2000, Back4Sure, etc.)
* Strg+Alt+T - Damit können Sie den Titel des aktuell fokussierten Programms
  ändern

## Änderungen:

### Änderungen in 5.0.4:

* Kompatibel mit NVDA 2022.1
* Sie können nun die Signaltöne zur Bestätigung in den Einstellungen der
  Erweiterung deaktivieren
* Übersetzungen aktualisiert

### Änderungen in 5.0.3:

* Kompatibilität mit NVDA 2021.1

### Änderungen in 5.0.2:

* Erste Version, die auf der Webseite für NVDA-Erweiterungen verfügbar ist

[[!tag dev stable]]

[1]: https://addons.nvda-project.org/files/get.php?file=winwizard
