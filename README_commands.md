# Documentation française

## Description

Ce script scrape les commandes de Thelia et de génère automatiquement la documentation de chacune d'entre elle au format markdown.

### Fonctionnement

- Recherche l'intégralité des commandes dans le projet dont le repertoire racine est saisit par l'utilisateur.
- Analyse chaque fichier de commande trouvé pour retourner un tableau regroupant les données trouvées.
- Exploite le tableau précédent pour générer un fichier markdown de documentation pour chaque commande.

### Utilisation

- Il est possible de choisir le chemin dans lequel on veut que le(s) fichier(s) soi(en)t créé(s). Par défaut, il(s) sera/seront créé(s) dans un nouveau dossier 'output' dans le répertoire courant.
- Pour lancer le programme, utilisez la forme suivante: `python3 nomFichier.py [chemin/de/sortie]`  
exemple: `python3 commands.py` ou `python3 commands.py ./doc/commands`
- Pour reconnaitre les arguments, options , descriptions et helps, le script se réfère à l'ordre des données reçues dans le tableau.  
    Exemple du format: ```python
    data_command_dict = {
    "Commande1": [
        "descriptionCommande1",
        "usageCommande1",
        [["arg1Commande1", "descArg1Commande1"],["arg2Commande1", "descArg2Commande1"]],
        [["option1Commande1", "descOption1Commande1"],["arg2Commande1", "descOption2Commande1"]],
        "help1Commande1"
    ], ...}```

________________

# English documentation

## Description

This script scrapes Thelia commands and automatically generates markdown documentation for each one.

### How it works

- Searches for all commands in the project whose root directory is entered by the user.
- Analyzes each command file found to return a table containing the data found.
- Uses the above table to generate a markdown documentation file for each command.

### Usage

- It is possible to choose the path in which you want the file(s) to be created. By default, it will be created in a new 'output' folder in the current directory.
- To launch the program, use the following structure: `python3 filename.py [output/path]`
example: `python3 commands.py` or `python3 commands.py ./doc/commands`
- To recognize arguments, options, descriptions and helps, the script refers to the order of the data received in the table.  
    Example of the format: ```python
    data_command_dict = {
    "Command1": [
        "descriptionCommand1",
        "useCommand1",
        [["arg1Command1", "descArg1Command1"],["arg2Command1", "descArg2Command1"]],
        [["option1Command1", "descOption1Command1"],["arg2Command1", "descOption2Command1"]],
        "help1Command1"
    ], ...}```
