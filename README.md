# FlyingSnake
a helper bot for ttrpg games on discord (dice rolls, calculus, variables)


### Need Help ?

`/help <optionel:commande>`
Affiche l'aide (se supprime au bout d'une minute avec log pour s'assurer que ça se fasse bien ?) (alias: `/h /fsh /fshelp`)

### Formulas Commands

`<formule> <optionel:formules>`
Résouds une ou plusieurs formules arithmétiques contenant des nombres (entier ou à virgule), opérateur (+-*/), des dés et variables (alias: `/fs /roll /fsroll`). `/` pour avoir le détail du calcul (alias: `/FS /ROLL /FSROLL`).

### Variables Commands

`/set <variable> <optionel:valeur>`
Créer ou modifie une variable (une variable est un champ de texte qui pourra ensuite être interprété différement selon le contexte d'utilisation selon qu'il représente un nombre, une formule ou du texte) (alias: `/s /fss /fsset`).

`/get <optionel:variable>`
Affiche la valeur d'une variable. Si aucune variable renseignée, affiche le nom de toutes les variables stockées (alias: `/g /fsg /fsget`). `/GET <optionel:variable>` Affiche l'historique des valeurs d'une variable. Si aucune variable n'est renseignée, affiche le nom de toutes les variables stockées (alias: `/G /FSG /FSGET`). `/getall` pour afficher la valeur de toutes les variables (alias: `/ga /fsga /fsgetall`). `/GETALL` pour  l'historique des valeurs de toutes les variables (alias: `/GA /FSGA /FSGETALL`).

`/del variable>`
Supprime une variable avec possibilité d'undo (alias: `/d /fsd /fsdel /delete /fsdelete`), `/delall>` pour supprimer toutes les variables (alias: `/da /fsda /fsdelall /deleteall /fsdeleteal`). `/DEL variable>` pour supprimer définitivement une variable (alias: `/D /FSD /FSDEL /DELETE /FSDELETE`), `/DELALL` pour supprimer définitivement toutes les variables (alias: `/DA /FSDA /FSDELALL /DELETEALL /FSDELETEALL`)

`/undo <optionel:variable>`
Annule la dernière modification d'une variable (alias: `/u /fsu /fsundo`). 

`/redo <optionel:variable>`
Restore la dernière modification d'une variable (alias: `/r /fsr /fsredo`). `/REFO <variable>` pour restaurer la toute dernière version d'une variable (alias: `/R /FSR /FSREDO`)..

### Parameters

`/parameters <paramètre> <valeur>`
Modifie le comportement de FlyingSnake  (alias: `/p /fsp /fsparameters`)

- `forceprefix <true/false>` (default: false) 
Force l'usage du préfixe "fs" sur toutes les commandes (évite l'ambiguité avec d'autres bots)
- `strictmode <true/false>` (default: false)
Interdit aux commandes d'avoir du texte en queue et n'essais pas de corriger les erreur mineure lors de commandes.
- `verbose <true/false>` (default: false) réagir par des icones/réactions ?

/wipe

(DEX)


off/minimal/partial/full
0/1/2/3