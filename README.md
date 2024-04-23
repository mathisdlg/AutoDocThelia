# Documentation Française

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

L'integrate permet de prendre le fichier mardown généré par le format et de l'intégrer dans un fichier md donné en ligne de commande.

### All

Permet de faire les trois actions en une seule commande.

### Clean

Permet de supprimer les fichiers temporaires générés par les actions.

## Events

## Récupérateur d'Événements

Ce script Bash extrait les évènements de Thelia ainsi que certaines de leurs informations et les écrits dans un fichier texte généré. Celui-ci est formaté car il est utilisé par un autre script

### Fonctionnalités

- Détection des Classes dépréciées : Identifie les classes marquées comme dépréciées (grâce à la mention @deprecated) et fournit le chemin d'accès de l'évènement le remplacement (grâce au commentaire suivant @deprecated).
- Extraction des arguments de constructeur : Extrait les arguments des constructeurs des évènements et les liste aux côtés des noms de l'évènement correspondant.
- Formatage de la sortie : Créé un fichier texte contenant des tableaux de tableaux contenant les évènements triés par dossier et par ordre alphabétique.  
    - Le texte est écrit sous format markdown afin d'être affiché par la suite.
    - Les fichiers à la racines du dossier 'Event' se trouvent dans le premier tableau qui est nommé 'no_category'.  
    - Si un fichier ne contient pas de constructeur, le message 'no constructor found in this file' remplace les arguments.  
Exemple:  
```[[no_category, event1],[nomDossier1,- event1 -> $argument1 \n-  Event2 -> no constructor found in this file\n]]```

### Utilisation

```bash
./eventExtractor.sh <chemin/vers/le/répertoire/événements> [nom_fichier_sortie.txt]
```
- <chemin/vers/le/répertoire/événements> : Chemin vers le répertoire contenant les événements Thelia.
- [nom_fichier_sortie.md] (optionnel) : Nom du fichier texte de sortie. S'il n'est pas fourni, le nom par défaut sera dataArrayEvent.txt sera utilisé.

Exemple:
```bash
./eventExtractor.sh thelia/core/lib/Thelia/Core/Event liste_evenements.md
```

...

# English documentation

## Event Extractor

This Bash script extracts events from Thelia along with some of their information and writes them into a generated text file. The output file is formatted as it is used by another script.

### Features

- Deprecated Class Detection: Identifies classes marked as deprecated (using the @deprecated annotation) and provides the replacement event path (through the comment following @deprecated).
- Constructor Arguments Extraction: Extracts constructor arguments of the events and lists them alongside the corresponding event names.
- Output Formatting: Generates a text file containing arrays of arrays containing events sorted by folder and alphabetically.
    - The text is written in markdown format for later display.
    - Files at the root of the 'Event' folder are placed in the first array named 'no_category'.
    - If a file does not contain a constructor, the message 'no constructor found in this file' replaces the arguments.  
Example:
```[[no_category, event1],[folderName1,- event1 -> $argument1 \n-  Event2 -> no constructor found in this file\n]]```

### Usage

```bash
./eventExtractor.sh <path/to/events/directory> [output_file_name.txt]
```
- <path/to/events/directory>: Path to the directory containing Thelia events.
- [output_file_name.md] (optional): Name of the output text file. If not provided, the default name dataArrayEvent.txt will be used.  
Exemple:
```bash
./eventExtractor.sh thelia/core/lib/Thelia/Core/Event liste_evenements.md
```
