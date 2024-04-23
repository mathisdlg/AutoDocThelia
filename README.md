# Documentation Française

Ce programme python permet de générer la documentation d'un projet Thelia à partir de ses fichiers sources.

## Utilisation

```bash
python3 thelia-doc.py
```

Le programme va ensuite vous demander quel documentation vous souhaitez générer.

## Hooks

Quand vous choississez de générer la documentation des hooks le programme vous redemandera de choisir les actions que vous souhaitez faire.  

```
> What would you like to do ([1] - help): <1 pour Help, 2 pour Hooks, 3 pour Events>
```

### Scan

Le scan permet de scanner le reépertoire passé en ligne de commande pour trouver les hooks et les répertorier dans un fichier txt.

```
> Enter the directory to scan: <Le chemin de la racine de du projet à scanner>
> Enter the file to write the hooks in [log.txt] :  <Le nom du fichier txt dans lequel écrire les hooks>
```

### Format

Le format permet de formater le fichier txt généré par le scan en fichier markdown.

```
> Enter the file to read the hooks from [log.txt] : <Le nom du fichier txt contenant les hooks>
> Do you want to sort the hooks by key [Y/n] : <Si vous voulez trier les hooks>
> Enter the file to write the hooks in [hooks.md] : <Le nom du fichier md dans lequel écrire les hooks>
```

### Integrate

L'integrate permet de prendre le fichier mardown généré par le format et de l'intégrer dans un fichier md donné en ligne de commande.

```
> Enter the file to read the hooks from [hooks.md] : <Le nom du fichier md contenant les hooks>
> Enter the file to write the hooks in [documentation.md] : <Le nom du fichier md dans lequel écrire les hooks>
```

### All

Permet de faire les trois actions en une seule commande.

```
> Enter the directory to scan: <Le chemin de la racine de du projet à scanner>
> Enter the file to write the hooks in [log.txt] :  <Le nom du fichier txt dans lequel écrire les hooks>
> Enter the file to write the hooks in [hooks.md] : <Le nom du fichier md dans lequel écrire les hooks>
> Enter the file to write the hooks in [documentation.md] : <Le nom du fichier md dans lequel écrire les hooks>
> Do you want to sort the hooks by key [Y/n] : <Si vous voulez trier les hooks>
```

### Clean

Permet de supprimer les fichiers temporaires générés par les actions.

## Récupérateur d'Événements

Ce script Bash extrait les évènements de Thelia ainsi que certaines de leurs informations et les écrits dans un fichier texte généré. Celui-ci est formaté car il est utilisé par un autre script

### Fonctionnalités

- Détection des Classes dépréciées : Identifie les classes marquées comme dépréciées (grâce à la mention @deprecated) et fournit le chemin d'accès de l'évènement le remplacement (grâce au commentaire suivant @deprecated).
- Extraction des arguments de constructeur : Extrait les arguments des constructeurs des évènements et les liste aux côtés des noms de l'évènement correspondant.
- Formatage de la sortie : Créé un fichier texte contenant des tableaux de tableaux contenant les évènements triés par dossier et par ordre alphabétique.  
  - Le texte est écrit sous format markdown afin d'être affiché par la suite.
  - Les fichiers à la racines du dossier 'Event' se trouvent dans le premier tableau qui est nommé 'no_category'.  
  - Si un fichier ne contient pas de constructeur, le message 'no constructor found in this file' remplace les arguments.  
Exemple de sortie:  
```[[no_category, event1 -> $argument1 $argument2\n ],[nomDossier1,- event1 -> $argument1 \n-  Event2 -> no constructor found in this file\n]]```

### Utilisation

```bash
./eventPreAnalyzer.sh <chemin/vers/le/répertoire/événements> [nom_fichier_sortie.txt]
```

- <chemin/vers/le/répertoire/événements> : Chemin vers le répertoire contenant les événements Thelia.
- [nom_fichier_sortie.md] (optionnel) : Nom du fichier texte de sortie. S'il n'est pas fourni, le nom par défaut sera dataArrayEvent.txt sera utilisé.

Exemple:

```bash
./eventPreAnalyzer.sh thelia/core/lib/Thelia/Core/Event liste_evenements.md
```

**⚠️ Attention:**
Le chemin fournit en parametre du script (celui pour accéder au dossier Event) apparait dans la documentation lors de sa génération (dans le chemin des évènements remplacant ceux dépréciés).

# English documentation

This python program generates the documentation for a Thelia project from its source files.

## Usage

```bash
python3 thelia-doc.py
```

The program will then ask you what documentation you want to generate.

## Hooks

When you choose to generate hook documentation, the program will ask you again to select the actions you wish to take. 

```
> What would you like to do ([1] - help): <1 for Help, 2 for Hooks, 3 for Events>
```

### Scan

The scan function scans the directory passed on the command line to find hooks and list them in a txt file.

```
> Enter the directory to scan: <The root path of the project to scan> 
> Enter the file to write the hooks in [log.txt] : <The name of the txt file to write the hooks in>.
```

### Format

Format allows you to format the txt file generated by the scan as a markdown file.

```
> Enter the file to read the hooks from [log.txt] : <The name of the txt file containing the hooks>
> Do you want to sort the hooks by key [Y/n] : <If you want to sort the hooks>
> Enter the file to write the hooks in [hooks.md] : <The name of the md file to write the hooks in>
```

### Integrate

Integrate takes the mardown file generated by the format and integrates it into a given md file on the command line.

```
> Enter the file to read the hooks from [hooks.md] : <The name of the md file containing the hooks>
> Enter the file to write the hooks in [documentation.md] : <The name of the md file in which to write the hooks>
```

### All

Allows you to perform all three actions in a single command.

```
> Enter the directory to scan: <The root path of the project to scan>
> Enter the file to write the hooks in [log.txt]: <The name of the txt file in which to write the hooks>
> Enter the file to write the hooks in [documentation.md]: <The name of the md file in which to write the hooks>
> Enter the file to write the hooks in [documentation.md]: <The name of the md file in which to write the hooks>
> Do you want to sort the hooks by key [Y/n] : <If you want to sort the hooks>
```

### Clean

Allows you to delete temporary files generated by actions.

## Event Extractor

This Bash script extracts events from Thelia along with some of their information and writes them into a generated text file. The output file is formatted as it is used by another script.

### Features

- Deprecated Class Detection: Identifies classes marked as deprecated (using the @deprecated annotation) and provides the replacement event path (through the comment following @deprecated).
- Constructor Arguments Extraction: Extracts constructor arguments of the events and lists them alongside the corresponding event names.
- Output Formatting: Generates a text file containing arrays of arrays containing events sorted by folder and alphabetically.
  - The text is written in markdown format for later display.
  - Files at the root of the 'Event' folder are placed in the first array named 'no_category'.
  - If a file does not contain a constructor, the message 'no constructor found in this file' replaces the arguments.  

Example output:

```[[no_category, event1 -> $argument1 $argument2\n ],[folderName1,- event1 -> $argument1 \n-  Event2 -> no constructor found in this file\n]]```

### Usage

```bash
./eventPreAnalyzer.sh <path/to/events/directory> [output_file_name.txt]
```

- <path/to/events/directory>: Path to the directory containing Thelia events.
- [output_file_name.md] (optional): Name of the output text file. If not provided, the default name dataArrayEvent.txt will be used.  
Example:

```bash
./eventPreAnalyzer.sh thelia/core/lib/Thelia/Core/Event liste_evenements.md
```

**⚠️ Warning:**
The path provided as a parameter of the script (the one to access the Event folder) appears in the documentation when it is generated (in the path of events replacing those deprecated).
