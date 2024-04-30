# Documentation française

## Description

Ce script scrape les loop de Thelia et de génère automatiquement la documentation de chacune d'entre elle au format markdown à partir du code se trouvant dans les fichiers .php .

## Fonctionnement

- Recherche l'intégralité des loops dans le projet dont le repertoire racine est ...
- Analyse chaque fichier de loop ...
- Exploite le tableau précédent pour générer un fichier markdown de documentation pour chaque commande. Ce fichier se nomme comme le nom de la loop reçue dans le tableau. Si le fichier existe déjà, il sera remplacé.  
Exemple: `maLoop.php`

## Utilisation

- Il est possible de choisir le chemin dans lequel on veut que le fichier soit créé. Par défaut, il sera créé dans dans le répertoire courant.
- Pour lancer le programme, utilisez la forme suivante: `python3 nomFichier.py [chemin/de/sortie]`  
exemple: `python3 loopAnalyser.py` ou `python3 loopAnalyser.py ./doc/loop/`
- Pour reconnaitre le titre, description, arguments et outputs, le script se réfère à l'ordre des données reçues dans le tableau.
- La section 'Example' est reconnue grâce au patterne '## Example', ⚠️ si elle est présente dans le fichier portant le nom de la loop courrante, elle sera copié puis collé dans la nouvelle documentation sans être modifiée.
- Les liens faccultatifs placés après les outputs et les arguments (tels que  'dependance_supplémentaire_facculative' et 'link_global_output_facculatif') sont reconnus pour être affiché en dehors du tableau grâce aux fait qu'ils soient à la fin de leur tableau et qu'ils ne soient pas de type list.
    Exemple du format:

    ```python

    data = [
    "Mon_titre",
    "Ceci est la description",
    [["titre_colonne_argument", "titre_colonne_description", "titre_colonne_default", "titre_colonne_exemple"],["arg1", "Description de l'argument 1", "valeur_par_defaut1", "exemple1"], ["arg2", "Description de l'argument 2", "valeur_par_defaut2", "exemple2"], "dependance_supplémentaire_facculative"],
    [["titre_colonne_variable", "titre_colonne_valeur"], ["output1", "valeur_output1"], ["output2", "valeur_output2"], "link_global_output_facculatif"],
    [["titre_colonne__ascendante", "titre_colonne_descendant", "titre_colonne_trie"], ["val_ascendante1", "val_descendante1", "champs_trié1"]]]

    ```

________________

# English documentation

## Description

This script scrapes Thelia loops and automatically generates the documentation for each of them in markdown format from the code found in the .php files.

## How it works

## Usage

- It is possible to choose the path in which you want the file to be created. By default, it will be created in the current directory.
- To launch the program, use the following form: `python3 filename.py [output/path]`
example: `python3 loopAnalyser.py` or `python3 loopAnalyser.py ./doc/loop/`
- To recognize the title, description, arguments and outputs, the script refers to the order of the data received in the table.
- The 'Example' section is recognized thanks to the '## Example' pattern, ⚠️ if it is present in the file bearing the name of the current loop, it will be copied then pasted into the new documentation without being modified.
- Optional links placed after outputs and arguments (such as 'dependance_supplémentaire_facculative' and 'link_global_output_facculatif') are recognized to be displayed outside the table thanks to the fact that they are at the end of their table and that they are not no list type.
    Example of the format:

    ```python

    data = [
    "My_title",
    "This is the description",
    [["argument_column_title", "description_column_title", "default_column_title", "example_column_title"],["arg1", "Description of argument 1", "default_value1", "example1"], ["arg2", "Description of argument 2", "default_value2", "example2"], "optional_additional_dependency"],
    [["variable_column_title", "value_column_title"], ["output1", "output_value1"], ["output2", "output_value2"], "link_global_output_optional"],
    [["ascending_column_title", "descending_column_title", "sorted_column_title"], ["ascending_val1", "descending_val1", "sorted_fields1"]]]

    ```
