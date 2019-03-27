# csv2xml4Alma

Le script Python (3.7) csv2xml est utilisable dans le cadre du projet GED du Campus Condorcet pour convertir en XML un fichier CSV contenant des informations en provenance du référentiel d'identité du Cammus Condorcet et relatives aux utilisateurs de la bibliothèque. 

Le fichier XML est importable dans Alma. 

Cartouche du programme :
# ******************************************************************************
# PROGRAMME   : csv2xml.py
# DESCRIPTION : Ce traitement convertit un fichier CSV venu du référentiel 
#               d'identité du Campus Condorcet en un fichier XML pouvant être
#               importer dans Alma pour créer / mettre à jour un utilisateur.
#               ATTENTION : le séparateur de champ dans le CSV doit être ';'
#               La première du fichier CSV doit être contenir des balises à
#               convertir. Le CSV doit être en UTF-8.
# ENTREE      : nom du fichier CSV à convertir, répondant aux normes ci-dessus.
# SORTIE      : fichier xml converti
# J. C.-S., CAMPUS CONDORCET, 2019
# ******************************************************************************

Dans ce programme, plusieurs structures de données doivent être paramétrées pour l'analyse du CSV et la création de la structure XML. 

A FAIRE :
- Documenter ces structures quand celles du fichier CSV d'entrée et du fichier XML de sortie seront mieux connues ;
- Mettre toutes ces structures dans un fichier séparé à importer dans le script principal.
