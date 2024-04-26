# Constraints list

## Constraints for event documentation

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

## Constraints for commands documentation

- Pour reconnaitre les descriptions, options, arguments et help le script se base sur l'ordre des éléments dans le tableau. Ainsi le premier élément sera la description, le deuxième sera le usage, suivi de l'argument, des options et du help qui est facultatif. Cet ordre provient de l'utilisation de l'option `-h` après chacune de commande.
