# Documentation française

## Description

Ce script scrape les loop de Thelia et de génère automatiquement la documentation de chacune d'entre elle au format markdown à partir du code se trouvant dans les fichiers .php .

## Fonctionnement

- Recherche l'intégralité des loops dans le projet dont le repertoire racine est ...
- Analyse chaque fichier de loop ...
- Exploite le tableau précédent pour générer un fichier markdown de documentation pour chaque commande.

## Utilisation

- Il est possible de choisir le chemin dans lequel on veut que le fichier soit créé. Par défaut, il sera créé dans dans le répertoire courant.
- Pour lancer le programme, utilisez la forme suivante: `python3 nomFichier.py [chemin/de/sortie]`  
exemple: `python3 loopAnalyser.py` ou `python3 loopAnalyser.py ./doc/loop`
- Pour reconnaitre le titre, description, arguments et outputs, le script se réfère à l'ordre des données reçues dans le tableau. La section 'Example' est reconnue grâce au patterne '## Example', ⚠️ si elle est présente elle sera copié puis collé dans la nouvelle donc sans modifications.
    Exemple du format: ```python
    data = [
    "Mon_titre",
    "Ceci est la description",
    [["titre_colonne_argument", "titre_colonne_description", "titre_colonne_default", "titre_colonne_exemple"],["arg1", "Description de l'argument 1", "valeur_par_defaut1", "exemple1"], ["arg2", "Description de l'argument 2", "valeur_par_defaut2", "exemple2"], "dependance_supplémentaire_facculative"],
    [["titre_colonne_variable", "titre_colonne_valeur"], ["output1", "valeur_output1"], ["output2", "valeur_output2"], "link_global_output_facculatif"],
    [["titre_colonne__ascendante", "titre_colonne_descendant", "titre_colonne_trie"], ["val_ascendante1", "val_descendante1", "champs_trié1"]],
]```

________________

# English documentation

## Description

## How it works

## Usage
