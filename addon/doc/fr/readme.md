# Win Wizard #

* Auteur : Oriol Gómez, maintenance actuelle par Łukasz Golonka
* Compatibilité NVDA : 2019.3 et ultérieurs
* Télécharger [version stable][1]

Cette extension vous permet d'effectuer certaines opérations sur la fenêtre
focalisée ou le processus qui lui est associé. Lorsque vous tuez un
processus ou en affichant / cachant une fenêtre, un bip de confirmation est
joué lorsque l'action réussit. Si vous trouvez ceci ennuyeux, vous pouvez
désactiver ces bips dans le panneau de paramètres de Win Wizard disponible
dans le dialogue des paramètres de NVDA.

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
* NVDA+Windows+TAB - bascule entre les fenêtres de niveau supérieur du
  programme actuel (utile dans foobar2000, Back4Sure etc.)
* CTRL+ALT+T - vous permet de changer le titre du programme actuellement
  ciblé

## Changements :

### Changements pour la version 5.0.4:

* Compatibilité avec NVDA 2022.1
* Il est désormais possible de désactiver les bips de confirmation dans le
  panneau de paramètres des extensions
* Mise à jour des traductions

### Changements pour la version 5.0.3 :

* Compatibilité avec NVDA 2021.1

### Changements pour la version 5.0.2 :

* Première version disponible sur le site des extensions

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=winwizard
