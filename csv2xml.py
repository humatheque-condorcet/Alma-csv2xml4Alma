#!/usr/bin/python
# -*- coding: utf-8 -*-
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
# J. CHIAVASSA-SZENBERG, CAMPUS CONDORCET, 2019
# ******************************************************************************

import fileinput
import os.path
import sys
import time
import csv
import lxml.etree as ET

# **************************************************************************** #
#                                 Fonctions                                    #
# **************************************************************************** #

def csv_args(tabArgs):
    """ csv_args : vérification du passage des arguments. """
    if (len(tabArgs) != 2):
        print("Erreur dans le passage des arguments : ")
        print("--> usage : python csv2xml <nom-fichier-csv>")
        print("--> Vérifiez vos paramètres et relancez !")
        print("Fin du traitement")
        sys.exit(1)
    
    return (tabArgs[1])

def add_ownered_entity(balise_mere):
    """ add_ownered_entity : ajout d'un bloc standard dans chaque bloc XML. """
    # Le bloc suivant est standard :
    balise_OE = ET.SubElement(balise_mere, "owneredEntity")
    my_node = ET.SubElement(balise_OE, "creationDate").text = time.strftime('%y%m%d',time.localtime())
    return (my_node)

def ecrire_bloc(ma_colonne, ma_valeur):
    """ ecrire_bloc : écriture d'un bloc dans la structure XML.
        ma_colonne permet de retrouver le tag XML a ajouter
        ma_valeur est la valeur que le tag XML porte """
    print("Ajout du bloc suivant : ")
    print("\tColonne CSV : ", ma_colonne)
    print("\tma_valeur CSV : ", ma_valeur)
    print("\tStructure XML correspondant à la colonne dans convert_tag :", ", ".join(convert_tag[ma_colonne]))

    if len(convert_tag[ma_colonne]) == 3: # On travaille sur un tag dans un sous-bloc d'un bloc
        # On crée d'abord le sous-bloc :
        print("\ttag père : ", convert_tag[ma_colonne][2])
        print("\ttag fils : ", convert_tag[ma_colonne][1])
        print("\tvaleur : ", ma_valeur)
        mon_bloc_pere = ET.SubElement(ref_bloc[convert_tag[ma_colonne][2]], convert_tag[ma_colonne][1])
        # Puis le tag :
        mon_bloc =  ET.SubElement(mon_bloc_pere, convert_tag[ma_colonne][0]).text = str(ma_valeur)   
    elif len(convert_tag[ma_colonne]) == 2:
        print("\ttag fils : ", convert_tag[ma_colonne][1])
        print("\tvaleur : ", ma_valeur)
        mon_bloc = ET.SubElement(ref_bloc[convert_tag[ma_colonne][1]], convert_tag[ma_colonne][0]).text = str(ma_valeur)  
    return (mon_bloc)

# **************************************************************************** #
#                      Listes des tags par blocs dans XML                      #
# **************************************************************************** #
list_tag_userDetails = ("Birthdate", "b", "c", "d", "e", "f", "g", "h", "i", "j")
list_tag_owneredEntities = ("k", "l", "la", "m")
list_tag_userIdentifier = ("n", "o", "p")
list_tag_userAddress = ("q", "r", "s", "t")
list_tag_userEmail = ("u", "v")
list_tag_userCategory = ("w", "x")

# **************************************************************************** #
#                     Dictionnaire de conversion des tags                      #
#                      clef : tag csv ; valeur : tag XML                       #
# **************************************************************************** #
convert_tag={}
# Bloc userDetails du XML
convert_tag[list_tag_userDetails[0]] = ["birthDate", "userDetails"]
convert_tag[list_tag_userDetails[1]] = ["firstName", "userDetails"]
convert_tag[list_tag_userDetails[2]] = ["lastName", "userDetails"]
convert_tag[list_tag_userDetails[3]] = ["status", "userDetails"]
convert_tag[list_tag_userDetails[4]] = ["userType", "userDetails"]
convert_tag[list_tag_userDetails[5]] = ["userGroup", "userDetails"]
convert_tag[list_tag_userDetails[6]] = ["userName", "userDetails"]
convert_tag[list_tag_userDetails[7]] = ["purgeDate", "userDetails"]
convert_tag[list_tag_userDetails[8]] = ["defaultLanguage", "userDetails"]
convert_tag[list_tag_userDetails[9]] = ["campusCode", "userDetails"]
# Bloc owneredEntities du XML
convert_tag[list_tag_owneredEntities[0]] = ["creationDate", "owneredEntities"]
convert_tag[list_tag_owneredEntities[1]] = ["modificationDate", "owneredEntities"]
convert_tag[list_tag_owneredEntities[2]] = ["modifiedBy", "owneredEntities"]
convert_tag[list_tag_owneredEntities[3]] = ["createdBy", "owneredEntities"]
# Bloc userIdentifier du XML
convert_tag[list_tag_userIdentifier[0]] = ["type", "userIdentifier"]
convert_tag[list_tag_userIdentifier[1]] = ["value", "userIdentifier"]
convert_tag[list_tag_userIdentifier[2]] = ["matchId", "userIdentifier"]
# Bloc userAddress du XML
convert_tag[list_tag_userAddress[0]] = ["line1", "userAddress"]
convert_tag[list_tag_userAddress[1]] = ["line2", "userAddress"]
convert_tag[list_tag_userAddress[2]] = ["note", "userAddress"]
convert_tag[list_tag_userAddress[3]] = ["userAddressTypes", "types", "userAddress"]
# Bloc userEmail du XML
convert_tag[list_tag_userEmail[0]] = ["email", "userEmail"]
convert_tag[list_tag_userEmail[1]] = ["userEmailTypes", "types", "userEmail"]
# Bloc userCategory du XML
convert_tag[list_tag_userCategory[0]] = ["statisticalCategory", "userCategory"]
convert_tag[list_tag_userCategory[1]] = ["note", "userCategory"]

# Le dictionnaire suivant permettra de faire les passages d'objet aux fonctions.
# Ce n'est pas très propre mais je ne vois pas comment faire autrement pour le
# moment. 
ref_bloc={}

# **************************************************************************** #
#                                   Main                                       #
# **************************************************************************** #

# Récupération des paramètres
csv_file = csv_args (sys.argv)

# Récupération des données d'entrée.
csv_data = csv.reader(open(csv_file,'r', encoding="UTF-8"), delimiter=';')

# Fichier de sortie
xml_file = 'importUserXML.xml'

# Initialisation de la structure XML à écrire en sortie : écriture de la racine 
# et des namespaces associés
EXL_NS =  "http://com/exlibris/digitool/repository/extsystem/xmlbeans"
XSI_NS =  "http://www.w3.org/2001/XMLSchema-instance"
NS_MAP = {"xsi": XSI_NS, None:  EXL_NS}
user_records = ET.Element('userRecords', nsmap=NS_MAP)

ligne_num = 0
nb_utilisateur_insere = 0

# Lecture du fichier CSV et génération des lignes XML correspondantes
for ligne in csv_data:
    # Récupération des tags dans l'entête CSV
    if ligne_num == 0:
        tags = ligne
    else: 
        print("############ Nouvel utilisateur à insérer dans le XML ############")
        # Nouvelle ligne de données :création d'une nouvelle entrée userRecord
        # Initialisation de la structure XML, des booléens permettant 
        # de tracer les informations écrites dans les blocs XML et des références.
        userRecord = ET.SubElement(user_records, "userRecord")
        b_userRecord = False
   
        userDetails = ET.SubElement(userRecord, "userDetails")
        b_userDetails = False
        ref_bloc["userDetails"] = userDetails

        userIdentifiers = ET.SubElement(userRecord, "userIdentifiers")
        b_userIdentifiers = False
        ref_bloc["userIdentifiers"] = userIdentifiers

        userIdentifier = ET.SubElement(userIdentifiers, "userIdentifier")
        b_userIdentifier = False
        ref_bloc["userIdentifier"] = userIdentifier

        userAddressList = ET.SubElement(userRecord, "userAddressList")
        b_userAddressList = False
        ref_bloc["userAddressList"] = userAddressList

        userAddress = ET.SubElement(userAddressList, "userAddress")
        b_userAddress = False
        ref_bloc["userAddress"] = userAddress

        userEmail = ET.SubElement(userAddressList, "userEmail")
        b_userEmail = False
        ref_bloc["userEmail"] = userEmail

        userNoteList = ET.SubElement(userRecord, "userNoteList")
        b_userNoteList = False
        ref_bloc["userNoteList"] = userNoteList

        userBlockList = ET.SubElement(userRecord, "userBlockList")
        b_userBlockList = False
        ref_bloc["userBlockList"] = userBlockList

        userStatisticalCategoriesList = ET.SubElement(userRecord, "userStatisticalCategoriesList")
        b_userStatisticalCategoriesList = False
        ref_bloc["userStatisticalCategoriesList"] = userStatisticalCategoriesList

        userCategory = ET.SubElement(userStatisticalCategoriesList, "userCategory")
        b_userCategory = False
        ref_bloc["userCategory"] = userCategory
        
        # Remplissage de la structure XML
        for colonne in range(len(tags)):
            bloc = ecrire_bloc(tags[colonne], str(ligne[colonne]))
            
            # Déterminer si on doit ajouter un sous-bloc owneredEntities : on
            # ne l'écrit qu'une seule fois dans les sous-blocs concernés
            if tags[colonne] in list_tag_userDetails and not b_userDetails:
                bloc = add_ownered_entity(userDetails)
                b_userDetails = True
                nb_utilisateur_insere += 1
            elif tags[colonne] in list_tag_userIdentifier and not b_userIdentifier:
                bloc = add_ownered_entity(userIdentifier)
                b_userIdentifier = True
            elif tags[colonne] in list_tag_userAddress and not b_userAddress:
                bloc = add_ownered_entity(userAddress)
                b_userAddress = True
            elif tags[colonne] in list_tag_userEmail and not b_userEmail:
                bloc = add_ownered_entity(userEmail)
                b_userEmail = True
            elif tags[colonne] in list_tag_userCategory and not b_userCategory:
                bloc = add_ownered_entity(userCategory)
                b_userCategory = True


            """if tags[colonne] == "Birthdate":
                node = ecrire_bloc(tags[colonne], str(ligne[colonne]))
                node = ET.SubElement(userDetails, convert_tag["Birthdate"]).text = str(ligne[colonne])
            elif tags[colonne] == "noteAddress":
               node = ET.SubElement(userAddress, "note").text = str(ligne[colonne])
               userAddress.set('preferred', 'true')
            else: #cas par défaut
               node = ET.SubElement(userRecord, tags[colonne]).text = str(ligne[colonne])
            """
    ligne_num +=1

# Ajout du sous-bloc owneredEntities pour le bloc userRecord
bloc = add_ownered_entity(userRecord)

#Mise en forme de l'arbre XML dans un format de lecture indenté
tree_out = ET.tostring(user_records, pretty_print=True, encoding='unicode')

# Ecriture du fichier XML
with open(xml_file, 'w') as f:
    f.write(tree_out)

print("Nombre d'utilisateur(s) inséré(s) : ", str(nb_utilisateur_insere))
# Succès !
sys.exit(0)