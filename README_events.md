# Documentation Française

## Récupérateur d'Événements

Le script Bash eventPreAnalyser.sh extrait les évènements de Thelia ainsi que certaines de leurs informations et les écrits dans un fichier texte généré. Celui-ci est formaté pour être exploité par le script python eventAnalyser.py. Ce dernier permet d'obtenir des informations sur les constantes des événements Thelia, puis de mettre en forme les données collectées dans un fichier markdown.  

### Fonctionnalités de eventPreAnalyser.sh

- Détection des Classes dépréciées : Identifie les classes marquées comme dépréciées (grâce à la mention @deprecated) et fournit le chemin d'accès de l'évènement le remplacement (grâce au commentaire suivant @deprecated).
- Extraction des arguments de constructeur : Extrait les arguments des constructeurs des évènements et les liste aux côtés des noms de l'évènement correspondant.
- Formatage de la sortie : Créé un fichier texte contenant des tableaux de tableaux contenant les évènements triés par dossier et par ordre alphabétique.  
  - Le texte est écrit sous format markdown afin d'être affiché par la suite.
  - Les fichiers à la racines du dossier 'Event' se trouvent dans le premier tableau qui est nommé 'no_category'.  
  - Si un fichier ne contient pas de constructeur, le message 'no constructor found in this file' remplace les arguments.  
Exemple de sortie:  
```[[no_category, event1 -> $argument1 $argument2\n ],[nomDossier1,- event1 -> $argument1 \n-  Event2 -> no constructor found in this file\n]]```

### Utilisation de eventPreAnalyser.sh

```bash
./eventPreAnalyzer.sh [-r] <chemin/vers/le/répertoire/événements> [nom_fichier_sortie.txt]
```

- [-r] (optionnel) : remplace le contenu du fichier de sortie portant le même nom s'il existe.
- <chemin/vers/le/répertoire/événements> : Chemin vers le répertoire contenant les événements Thelia.
- [nom_fichier_sortie.md] (optionnel) : Nom du fichier texte de sortie. S'il n'est pas fourni, le nom par défaut sera dataArrayEvent.txt sera utilisé.

Exemple:

```bash
./eventPreAnalyzer.sh -r thelia/core/lib/Thelia/Core/Event liste_evenements.md
```

### Fonctionnalités de eventAnalyser.py

- Récupère les catégories et les constantes associées.
- Récupère les commentaires éventuels au dessus de chaque constante.
- Tri les catégories par ordre alphabétique.``
- Convertit le fichier généré par eventPreAnalyser.sh en tableau python.
- Fusionne les constantes avec les données de eventPreAnalyser.sh.
- Génère un fichier markdown mettant en page toutes ces données.
- Modifie directement la documentation des événements de Thelia.

### Utilisation de eventAnalyser.py

Pour obtenir le résultat de l'analyse dans le fichier que vous voulez :  
`python3 eventAnalyser.py [FICHIER SOURCE] [FICHIER DESTINATION]`

Pour obtenir le résultat de l'analyse dans le fichier par défaut 'parsedEvents2.md' dans le même répertoire que eventAnalyser.py :  
`python3 eventAnalyser.py [FICHIER SOURCE]`

Le fichier source doit être le fichier TheliaEvents.php.  
Vous devez inclure le chemin d'accès du fichier (nom du fichier inclu).  
Le fichier `dataArrayEvent.txt` généré par eventPreAnalyser.sh doit exister dans le repertoire courant.

Les options `-h`et `--help` permettent d'accéder rapidement à cette description (en anglais uniquement).  

Le script demandera le fichier de documentation des événements Thelia qui sera modifié.

# English documentation

## Event Extractor

The eventPreAnalyser.sh Bash script extracts events from Thelia along with some of their information and writes them into a generated text file. This is formatted for use by the python script eventAnalyser.py. This provides information on Thelia event constants, and then formats the collected data in a markdown file.  

### eventPreAnalyser.sh features

- Deprecated Class Detection: Identifies classes marked as deprecated (using the @deprecated annotation) and provides the replacement event path (through the comment following @deprecated).
- Constructor Arguments Extraction: Extracts constructor arguments of the events and lists them alongside the corresponding event names.
- Output Formatting: Generates a text file containing arrays of arrays containing events sorted by folder and alphabetically.
  - The text is written in markdown format for later display.
  - Files at the root of the 'Event' folder are placed in the first array named 'no_category'.
  - If a file does not contain a constructor, the message 'no constructor found in this file' replaces the arguments.  

Example output:

```[[no_category, event1 -> $argument1 $argument2\n ],[folderName1,- event1 -> $argument1 \n-  Event2 -> no constructor found in this file\n]]```

### eventPreAnalyser.sh usage

```bash
./eventPreAnalyzer.sh [-r] <path/to/events/directory> [output_file_name.txt]
```

- [-r] (optional): replaces the contents of the output file with the same name if it exists.
- <path/to/events/directory>: Path to the directory containing Thelia events.
- [output_file_name.md] (optional): Name of the output text file. If not provided, the default name dataArrayEvent.txt will be used.  
Example:

```bash
./eventPreAnalyzer.sh -r thelia/core/lib/Thelia/Core/Event liste_evenements.md
```

### eventAnalyser.py features

- Retrieves categories and associated constants.
- Retrieves any comments above each constant.
- Sort categories alphabetically.
- Converts the file generated by eventPreAnalyser.sh into a python array.
- Merges constants with eventPreAnalyser.sh data.
- Generates a Markdown file displaying all this data.
- Directly modifies Thelia event documentation.

### eventAnalyser.py usage

To get the parsing result in the file you want :  
`python3 eventAnalyser.py [SOURCE FILE] [DESTINATION FILE]`

To get the parsing result in the default file 'parsedEvents.md' in the same repository as eventAnalyser.py :  
`python3 eventAnalyser.py [SOURCE FILE]`

The source file should be the TheliaEvents.php file.  
You should include absolute path in the files names.  
The `dataArrayEvent.txt` file generated by eventPreAnalyser.sh must exist in the current directory.

The `-h`and `--help` options provide quick access to this description.  

The script will ask the Thelia events documentation file which will be modified.  
