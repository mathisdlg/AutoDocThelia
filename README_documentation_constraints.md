# Contraintes de documentation pour automatiser la documentation

## Contraintes pour la documentation des évènements

- eventPreAnalizer.sh:
  - la mention `@deprecated` dans les fichier des évènements permet au script de reconnaitre l'évènnement comme étant déprécié.
  - le chemin de l'évènnement remplacant celui déprécié doit être noté après la mantion '@deprecated'.  
    exemple: ```php
            /**
            * @deprecated since 2.4, please use \Thelia\Model\Event\AttributeAvEvent
            */
            ```
- eventAnalizer.py:
  - Le fichier contenant la déclaration de tous les évènements doit s'appeler `TheliaEvents.php`.  
  - Le fichier fournit à 'eventAnalyser.py' doit se trouver dans le même répertoire que lui.  

Voir plus de [détails](./README_events.md)

## Contraintes pour la documentation des commandes

- Pour reconnaitre les descriptions, options, arguments et help le script se base sur l'ordre des éléments dans le tableau. Ainsi le premier élément sera la description, le deuxième sera le usage, suivi d'un tableau d'argument, d'un tableau d'options et d'un help qui est facultatif. Cet ordre provient de l'utilisation de l'option `-h` de chacune de commande.  

Voir plus de [détails](./README_commands.md)

## Contraintes pour la documentation des hooks

- Le répertoire contenant les templates doit impérativement s'appeler 'templates'.

## Contraintes pour la documentation des loops

- Pour reconnaitre le titre, description, arguments et outputs, le script se réfère à l'ordre des données reçues dans le tableau.
- La section 'Example' est reconnue grâce au patterne '## Example', ⚠️ si elle est présente dans le fichier portant le nom de la loop courrante, elle sera copié puis collé dans la nouvelle documentation sans être modifiée.
- Les liens faccultatifs placés après les outputs et les arguments sont reconnus grâce à leurs position à la fin d'un tableau ainsi qu'à leurs type différent de 'list'.

Voir plus de [détails](./README_loop.md)

# Documentation constraints to automate documentation

## Constraints for events documentation

- eventPreAnalizer.sh:
  - the mention `@deprecated` in the event files allows the script to recognize the event as being deprecated.
  - the path of the event replacing the deprecated one must be noted after the '@deprecated' statement.
    example: ```php
            /**
            * @deprecated since 2.4, please use \Thelia\Model\Event\AttributeAvEvent
            */
            ```
- eventAnalizer.py:
  - The file containing the declaration of all events must be called `TheliaEvents.php`.
  - The file provided to 'eventAnalyser.py' must be located in the same directory as it.  

Get more [details](./README_events.md)

## Constraints for commands documentation

- To recognize descriptions, options, arguments and help, the script is based on the order of the elements in the table. So the first element will be the description, the second will be the usage, followed by an argument array, an options array and a help which is optional. This order comes from the use of the `-h` option of each command.  

Get more [details](./README_commands.md)

## Constraints for hook documentation

- The directory containing the templates must be called 'templates'.

## Constraints for loop documentation

- To recognize the title, description, arguments and outputs, the script refers to the order of the data received in the table.
- The 'Example' section is recognized using the '## Example' pattern, ⚠️ if it is present in the file bearing the name of the current loop, it will be copied then pasted into the new documentation without being modified.
- Optional links placed after outputs and arguments are recognized thanks to their position at the end of an array as well as their different type of 'list'.

View more [details](./README_loop.md)
