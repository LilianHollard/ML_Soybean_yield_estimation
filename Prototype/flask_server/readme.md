# **Table of Contents**
- [**Table of Contents**](#table-of-contents)
  - [**Start**](#start)
    - [Fichier : Start.py](#fichier--startpy)
  - [**FLASK** (application web *serveur*)](#flask-application-web-serveur)
    - [Fichier : hello.py](#fichier--hellopy)
  - [**CSV / static / templates**](#csv--static--templates)
  - [**Année référence**](#année-référence)
    - [Fichier : Annee_Reference.py](#fichier--annee_referencepy)
    - [__*Classe AnneeRef*__](#classe-anneeref)
      - [__Init__ @params : Annee, Dataframe](#init-params--annee-dataframe)
      - [**change_YEAR** @type: function | @params: year](#change_year-type-function--params-year)
      - [**change_CoeffProd** @type: function | @params: new_coeff](#change_coeffprod-type-function--params-new_coeff)
      - [**addRow()** @type: function | @params: row](#addrow-type-function--params-row)
      - [**addRowIncomplete()** @type: function | @params: row](#addrowincomplete-type-function--params-row)
      - [**slight_mean()** @type: function | @params: Annee, Dataframe](#slight_mean-type-function--params-annee-dataframe)
      - [**historical_average()** @type: function | @params: Dataset](#historical_average-type-function--params-dataset)


## **Start**
### Fichier : Start.py 
Permet la préparation des différents fichiers csv (Suite aux différents travaux de recherche).
1. Découper le dataset selon les conditions / temps de pousse de la culture.
2. Vérifier l'état du dataset et modifier en fonction (NaN / neg value / ...)
3. Séprarer l'année 2019 du jeu de données météorologiques pour simuler le modèle si besoin.
4. Lier le jeu de données météorologiques avec les données historique de production.
5. Ajouter le coeff de production.
6. Ajouter le coeff de production pour 2019 (moyenne sur 10 ans (modifiable)).
## **FLASK** (application web *serveur*)
### Fichier : hello.py
Le modèle est créé lors du lancement du serveur. 

Gestion du formulaire d'entrées de données (Améliorable en fonction de la demande / de ce qui est proposé en front-end).

Le résultat du formulaire est récupérable au format CSV dans le dossier CSV/AnneeRef_csv/ 
## **CSV / static / templates**
Site web.
## **Année référence**
### Fichier : Annee_Reference.py 
**DOCUMENTATION**
### __*Classe AnneeRef*__
#### __Init__ @params : Annee, Dataframe
* Création d'une année référence en fonction de l'année courante (1er param) & d'un jeu de données météorologique (2eme param).
#### **change_YEAR** @type: function | @params: year
* Change l'année du dataset historique pour correspondre à l'année en paramètre.
#### **change_CoeffProd** @type: function | @params: new_coeff
* Change la variable coeff_prod du dataset historique pour correspondre à un nouveau coeff en paramètre.
#### **addRow()** @type: function | @params: row
* Ajout d'une ligne dans le jeu de données. 
* DOY (Day Of Year) : Incrémenté de 1.
#### **addRowIncomplete()** @type: function | @params: row
* Ajout d'une ligne incomplete (ou complete) dans le jeu de données.
* DOY (Day Of Year) : Incrémenté de 1.
#### **slight_mean()** @type: function | @params: Annee, Dataframe
* Effectue la moyenne du jeu de données météorologique de l'objet avec une nouvelle année issue d'un jeu de données en paramètre.
#### **historical_average()** @type: function | @params: Dataset
* Effectue une année dite "référence" en faisant la moyenne du jeu de données météorologique de l'objet avec l'historique des dernières années issue d'un jeu de données en paramètre.

