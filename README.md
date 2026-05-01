# Mémoire - La route du cacao entre la Côte d'Ivoire et l'Europe du Nord

© 2026 Camille Tuncq — IAE Nantes — Tous droits réservés
Ce code est partagé à des fins de transparence académique uniquement.
Toute réutilisation sans autorisation est interdite.

## Auteur
Camille Tuncq — Master 1 Finance, Logistique et Maritime — IAE Nantes — 2025-2026

## Description
Ce repository contient le code Python utilisé pour les analyses empiriques du mémoire :
"La route du cacao entre la Côte d'Ivoire et l'Europe du Nord : analyse des prix, 
des flux maritimes et des risques logistiques"

## Problématique
Comment la volatilité des cours du cacao influence-t-elle la structuration logistique 
et économique de la route Côte d'Ivoire – Europe du Nord ?

  ## Fichiers

### Code Python
- `mémoireh1.py` — Test de H1 : corrélation entre volatilité annuelle et 
volumes exportés
- `mémoireh2.py` — Test de H2 : analyse des prix du cacao, volatilité, 
statistiques descriptives et corrélation avec le Baltic Dry Index

### Données
- `US Cocoa Futures Historical Data.xlsx` — Prix journaliers du cacao 
(ICE Futures US, 2010-2026) — Source : Investing.com
- `Baltic Dry Index Historical Data.xlsx` — Données journalières du BDI 
(2010-2026) — Source : Investing.com
- `FAOSTAT_data_en_4-2-2026.xlsx` — Volumes annuels d'exportation de cacao 
en fèves depuis la Côte d'Ivoire (2010-2024) — Source : FAOSTAT

## Hypothèses testées
- **H1** : Une hausse de la volatilité des prix du cacao entraîne une réduction 
des volumes exportés depuis la Côte d'Ivoire → **Partiellement confirmée** (r = -0,227)
- **H2** : Les périodes de forte volatilité des cours sont corrélées aux coûts 
de fret maritime → **Rejetée** (r = 0,057 à 0,092)

## Bibliothèques Python requises
- pandas
- numpy
- plotly
- kaleido (pour l'export des graphiques en PNG)

## Utilisation
1. Cloner le repository
2. Placer tous les fichiers Excel dans le même dossier que les scripts Python
3. Lancer mémoireh1.py pour le test de H1
4. Lancer mémoireh2.py pour le teste de H2
