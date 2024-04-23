# (en) Event documentation with eventAnalyser

Parse the source file to get information about Thelia events constants.  
Analyze the dataArrayEvent.txt file to obtain information on Thelia event methods.  
The result is saved in a file, which can then be copied and pasted.  

## How to use the eventAnalyser

To get the parsing result in the file you want :  
`python3 eventAnalyser.py [SOURCE FILE] [DESTINATION FILE]`

To get the parsing result in the default file 'parsedEvents.md' in the same repository as eventAnalyser.sh :  
`python3 eventAnalyser.py [SOURCE FILE]`

The source file should be the TheliaEvents.php file.  
You should include absolute path in the files names.  

The `-h`and `--help` options provide quick access to this description.  

## How to comment the TheliaEvent.php file for the eventAnalyser

Category blocks must be prefixed with a comment of the form :

```php
// -- Category name
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

# (fr) Documentation des événements avec eventAnalyser

Analyse le fichier source pour obtenir des informations sur les constantes des événements Thelia.  
Analyse le fichier dataArrayEvent.txt pour obtenir les informations sur les méthodes des événements Thelia.  
Le résultat est enregistré dans un fichier, il suffit ensuite d'en copier coller le contenu.  

## Comment utiliser l'eventAnalyser

Pour obtenir le résultat de l'analyse dans le fichier que vous voulez :  
`python3 eventAnalyser.py [FICHIER SOURCE] [FICHIER DESTINATION]`

Pour obtenir le résultat de l'analyse dans le fichier par défaut 'parsedEvents2.md' dans le même répertoire que eventAnalyser.sh :  
`python3 eventAnalyser.py [FICHIER SOURCE]`

Le fichier source doit être le fichier TheliaEvents.php.  
Vous devez inclure le chemin absolu dans le nom des fichiers.  

Les options `-h`et `--help` permettent d'accéder rapidement à cette description (en anglais uniquement).  

## Comment commenter le fichier TheliaEvent.php pour l'analyseur d'événements

Les blocs de catégorie doivent être préfixés par un commentaire de la forme :

```php
// -- Nom de la catégorie
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
