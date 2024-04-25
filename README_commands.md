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
- Pour reconnaitre les arguments, options , descriptions et helps, le script se réfère aux termes `addArgument`, `addOption`, `setDescription` et `setHelp`.
- Les arguments et options à afficher sont triés. Ceux contenant les terms `InputArgument`, `InputOption` ou `null`ne seront pas affichés.

### Sources de problèmes connues

❌ Ecrire `->` juste après la parenthèse d'un élément sur plusieurs lignes entrainera un bug. Exemple à ne pas faire :

```php
...
->addOption(
    'with-dependencies',
    null,
    InputOption::VALUE_NONE,
    'option name'
)->addArgument(
    'module',
...
```

✅ Si l'élément n'est pas sur plusieurs lignes ou si les `->` ne suivent pas directement un élément sur plusieurs lignes, cela marchera. Exemples :

```php
...
->setName('module:name')
->setDescription('Do something')->addOption(
    'with-dependencies',
    null,
    InputOption::VALUE_NONE,
    'option name'
)
->addArgument(
    'module',
...
```

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
- To recognize arguments, options, descriptions and helps, the script refers to the terms `addArgument`, `addOption`, `setDescription` and `setHelp`.
- The arguments and options to display are sorted. Those containing the terms `InputArgument`, `InputOption` or `null` will not be displayed.

### Known sources of problems

❌ Writing `->` just after the parenthesis of an element on several lines will cause a bug. Example of what not to do :

```php
...
->addOption(
    'with-dependencies',
    null,
    InputOption::VALUE_NONE,
    'option name'
)->addArgument(
    'module',
...
```

✅ If the element is not on several lines or if the `->` do not directly follow an element on several lines, this will work. Examples :

```php
...
->setName('module:name')
->setDescription('Do something')->addOption(
    'with-dependencies',
    null,
    InputOption::VALUE_NONE,
    'option name'
)
->addArgument(
    'module',
...
```
