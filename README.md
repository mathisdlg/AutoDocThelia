# Documentation

Ce programme python permet de générer la documentation d'un projet Thelia à partir de ses fichiers sources.

## Utilisation

```bash
python3 thelia-doc.py
```

Le programme va ensuite vous demander quel documentation vous souhaitez générer.

## Hooks

Quand vous choississez de générer la documentation des hooks le programme vous redemandera de choisir les actions que vous souhaitez faire.  

### Scan

Le scan permet de scanner le reépertoire passé en ligne de commande pour trouver les hooks et les répertorier dans un fichier txt.

### Format

Le format permet de formater le fichier txt généré par le scan en fichier markdown.

### Integrate

L'ibntegrate permet de prendre le fichier mardown généré par le format et de l'intégrer dans un fichier md donné en ligne de commande.

### All

Permet de faire les trois actions en une seule commande.

### Clean

Permet de supprimer les fichiers temporaires générés par les actions.

## Events

...
