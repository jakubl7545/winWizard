# Win Wizard #

* Auteur : Oriol Gómez, maintenance actuelle par Łukasz Golonka
* Compatibilité NVDA : 2019.3 et ultérieurs
* Télécharger [version stable][1]

This add-on allows you to perform some operations on the focused window or
the process associated with it.  When killing a process, or showing / hiding
a window a confirmation beep is played when the action succeeds.  If you
find this annoying you can disable these beeps in the Win Wizard's settings
panel available from NVDA's settings dialog.

## Commandes clavier :
Toutes ces commandes peuvent être remappées à partir de la boîte de dialogue
Gestes de commandes dans la catégorie Win Wizard.
### Cacher et montrer les fenêtres cachées :
* NVDA+Windows+chiffres de 1 à 0 - masque la fenêtre actuellement focalisée
  dans l'emplacement correspondant au numéro pressé
* NVDA+Windows+flèche gauche - aller à la pile précédente de fenêtres
  cachées.
* NVDA+Windows+flèche droite - aller à la prochaine pile de fenêtres
  cachées.
* Windows+Maj+h - masque la fenêtre actuellement focalisée dans le premier
  emplacement disponible
* NVDA+Windows+h - montrer la dernière fenêtre cachée
* Windows+Maj+l - afficher la liste de toutes les fenêtres cachées
  regroupées par piles (veuillez noter que par défaut la dernière fenêtre
  cachée est sélectionnée)

### Gestion des processus :
* Windows+F4 - tue le processus associé à la fenêtre actuellement focalisée
* NVDA+Windows+p - ouvre un dialogue vous permettant de définir la priorité
  du processus associé à la fenêtre actuellement focalisée

### Commandes diverses :
* NVDA+Windows+TAB - switches between top level windows of the current
  program (useful in foobar2000, Back4Sure etc.)
* CTRL+ALT+T - vous permet de changer le titre du programme actuellement
  ciblé

## Changements :

### Changes for 5.0.4:

* Compatibility with NVDA 2022.1
* It is now possible to disable confirmation beeps in the add-ons settings
  panel
* Update translations

### Changements pour la version 5.0.3 :

* Compatibilité avec NVDA 2021.1

### Changements pour la version 5.0.2 :

* First release available from the add-ons website

[[!tag dev stable]]

[1]: https://addons.nvda-project.org/files/get.php?file=winwizard
