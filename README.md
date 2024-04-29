# Documentation française

Ce programme python permet de générer la documentation d'un projet Thelia à partir de ses fichiers sources.

## Prérequis

- Python 3.10 ou supérieur
- Un projet Thelia
- Un shell bash

## Utilisation

```bash
python3 thelia-doc.py
```

Le programme va ensuite vous demander quel documentation vous souhaitez générer.

```text
> What would you like to do ([1] - help): <1 pour Help, 2 pour Hooks, 3 pour Events, 4 pour Commands, 9 pour All>
```

## Hooks

Quand vous choississez de générer la documentation des hooks le programme vous redemandera de choisir les actions que vous souhaitez faire.  
Pour le bon fonctionnement du programme, il est nécessaire de lancer le programme à la racine du projet Thelia et que le répertoire 'templates' soit bien nommé 'templates'.

### Scan

Le scan permet de scanner le reépertoire passé en ligne de commande pour trouver les hooks et les répertorier dans un fichier txt.

```text
> Enter the directory to scan: <Le chemin de la racine de du projet à scanner>
> Enter the file to write the hooks in [log.txt] :  <Le nom du fichier txt dans lequel écrire les hooks>
```

### Format

Le format permet de formater le fichier txt généré par le scan en fichier markdown.

```text
> Enter the file to read the hooks from [log.txt] : <Le nom du fichier txt contenant les hooks>
> Do you want to sort the hooks by key [Y/n] : <Si vous voulez trier les hooks>
> Enter the file to write the hooks in [hooks.md] : <Le nom du fichier md dans lequel écrire les hooks>
```

### Integrate

L'integrate permet de prendre le fichier mardown généré par le format et de l'intégrer dans un fichier md donné en ligne de commande.

```text
> Enter the file to read the hooks from [hooks.md] : <Le nom du fichier md contenant les hooks>
> Enter the file to write the hooks in [documentation.md] : <Le nom du fichier md dans lequel écrire les hooks>
```

### All

Permet de faire toutes actions en une seule commande.

```text
> Enter the path to the root of the Thelia project to scan (Thelia Core): <Le chemin de la racine de votre projet Thelia>
> Enter the root path of the documentation to modify: <Le chemin de la racine de la documentation à modifier>
> Would you like to sort the hooks [Y/n]: <(optionnel) Si vous voulez trier les hooks, oui par défaut>
```

### Clean

Permet de supprimer les fichiers temporaires générés par les actions.

## Events

Quand vous choisissez de générer la documentation des évènements, le programme vous demmandera de remplir des champs pour générer la documentation.

```text
> Enter the path to the event directory: <Le chemin du répertoire des évènements dans thelia>
> Enter the destination file path [parsedEvent2.md] : <Le chemin du fichier dans lequel écrire les évènements>
> Enter the events documentation file to modify : <Le chemin du fichier de documentation des évènements>
```

### Readme des scripts d'analyse des évènements

[Détails ici](./README_events.md).

### Comment commenter le fichier TheliaEvent.php pour l'analyseur d'événements

Les blocs de catégorie dans `TheliaEvents.php` doivent être préfixés par un commentaire de la forme :

```php
// -- Nom de la catégorie -----------------------------------
```

Ils peuvent être fermés par (ce n'est pas obligatoire) :

```php
// -- End nom de la catégorie`
```

Tout commentaire relatif à une constante doit être écrit au-dessus de celle-ci sous la forme :

```php
/*
* Commentaire
*/
```

En suivant ces règles, vous pouvez classer tous les événements et afficher chaque commentaire pour chaque constante.  
Notez que la casse n'importe pas.  

### Comment commenter les fichiers d'évènements pour le pré-analyseur d'évènements

Pour identifier les classes dépréciées et le chemin d'accès de l'évènement le remplaçant, le script se base sur la mention:

```php
/*
 * @deprecated since X.Y, please use \Thelia\Model\Event\AnEventFile
 */
```

## Commandes

Quand vous choisissez de générer la documentation des commandes, le programme vous demandera de remplir des champs pour générer la documentation.

```text
> Enter the directory to scan commands: <La racine du projet Thelia>
> Enter the output directory for commands [./ouput/]: <Le répertoire de sortie pour les commandes>
```

### Readme du script des commandes

[Détails ici](./README_commands.md).

## All

Permet de faire la documentation des hooks et des évènements en une seule commande et de nettoyer les fichiers temporaires générés.

```text
> Enter the path to the event directory: <Le chemin du répertoire des évènements dans thelia>
> Enter the destination file path [parsedEvent2.md] : <Le chemin du fichier dans lequel écrire les évènements>
> Enter the events documentation file to modify : <Le chemin du fichier de documentation des évènements>
> Enter the directory to scan: <Le chemin de la racine de du projet à scanner>
> Enter the file to write the hooks in [log.txt] :  <Le nom du fichier txt dans lequel écrire les hooks>
> Enter the file to write the hooks in [hooks.md] : <Le nom du fichier md dans lequel écrire les hooks>
> Enter the file to write the hooks in [documentation.md] : <Le nom du fichier md dans lequel écrire les hooks>
> Do you want to sort the hooks by key [Y/n] : <Si vous voulez trier les hooks>
> Enter the directory to scan: <Le chemin de la racine de du projet à scanner>
> Enter the output directory for commands [./ouput/]: <Le chemin du répertoire de sortie pour les commandes>
```

# English documentation

This python program generates the documentation for a Thelia project from its source files.

## Requirements

- Python 3.10 or higher
- A Thelia project
- A bash shell

## Usage

```bash
python3 thelia-doc.py
```

The program will then ask you what documentation you want to generate.

```text
> What would you like to do ([1] - help): <1 for Help, 2 for Hooks, 3 for Events, 4 for Commands, 9 for All>
```

## Hooks

When you choose to generate hook documentation, the program will ask you again to select the actions you wish to take.  
For the program to work properly, it is necessary to run the program at the root of the Thelia project and that the 'templates' directory is correctly named 'templates'.

### Scan

The scan function scans the directory passed on the command line to find hooks and list them in a txt file.

```text
> Enter the directory to scan: <The root path of the project to scan> 
> Enter the file to write the hooks in [log.txt] : <The name of the txt file to write the hooks in>.
```

### Format

Format allows you to format the txt file generated by the scan as a markdown file.

```text
> Enter the file to read the hooks from [log.txt] : <The name of the txt file containing the hooks>
> Do you want to sort the hooks by key [Y/n] : <If you want to sort the hooks>
> Enter the file to write the hooks in [hooks.md] : <The name of the md file to write the hooks in>
```

### Integrate

Integrate takes the mardown file generated by the format and integrates it into a given md file on the command line.

```text
> Enter the file to read the hooks from [hooks.md] : <The name of the md file containing the hooks>
> Enter the file to write the hooks in [documentation.md] : <The name of the md file in which to write the hooks>
```

### All

Allows you to perform all three actions in a single command.

```text
> Enter the path to the root of the Thelia project to scan (Thelia Core): <path of the root of your Thelia project>
> Enter the root path of the documentation to modify: <The root path of the documentation to modify>
> Would you like to sort the hooks [Y/n]: <(optional) If you want to sort the hooks, yes by default>
```

### Clean

Allows you to delete temporary files generated by actions.

## Events

When you choose to generate event documentation, the program will ask you to fill in fields to generate the documentation.

```text
> Enter the path to the event directory: <The path to the events directory in Thelia>
> Enter the destination file path [parsedEvent2.md] : <The path to the file to write the events in>
> Enter the events documentation file to modify : <The path to the events documentation file>
```

### Readme of the event analysis scripts

[Details here](./README_events.md).

### How to comment the TheliaEvent.php file for the eventAnalyser

Category blocks must be prefixed with a comment of the form :

```php
// -- Category name ----------------------------------------
```

They can be closed with (this is not mandatory) :

```php
// -- End category name`
```

Any comment relating to a constant must be written above it in the form :

```php
/*
* Comment
*/
```  

By following these rules, you can categorize all events and display each comment for each constant.  
Note that case is not important.  

### How to comment the events files for the eventPreAnalyser

To identify the deprecated classes and the access path of the event replacing them, the script is based on the mention:

```php
/*
 * @deprecated since X.Y, please use \Thelia\Model\Event\AnEventFile
 */
```

## Commands

When you choose to generate command documentation, the program will ask you to fill in fields to generate the documentation.

```text
> Enter the directory to scan commands: <The root path of the project to scan>
> Enter the output directory for commands [./ouput/]: <The output directory for commands>
```

### Readme of the command script

[Details here](./README_commands.md).

## All

Allows you to do the documentation of hooks and events in a single command and clean up the temporary files generated.

```text
> Enter the path to the event directory: <The path to the events directory in Thelia>
> Enter the destination file path [parsedEvent2.md] : <The path to the file to write the events in>
> Enter the events documentation file to modify : <The path to the events documentation file>
> Enter the directory to scan: <The root path of the project to scan>
> Enter the file to write the hooks in [log.txt] : <The name of the txt file in which to write the hooks>
> Enter the file to write the hooks in [hooks.md] : <The name of the md file in which to write the hooks>
> Enter the file to write the hooks in [documentation.md] : <The name of the md file in which to write the hooks>
> Do you want to sort the hooks by key [Y/n] : <If you want to sort the hooks>
> Enter the directory to scan commands: <The root path of the project to scan>
> Enter the output directory for commands [./ouput/]: <The output directory for commands>
```

## Made by

- [Mnordest](https://github.com/mnordest)
- [Noa](https://github.com/NoaSlld)
- [Mathisdlg](https://github.com/mathisdlg)
