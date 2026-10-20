# Python collections — exercices 1 à 9

Chaque fichier numéroté se lance séparément, par exemple :

```sh
python3 06_name_validation.py
```

Pour tout lancer dans l’ordre : `python3 exercises.py`. Aucune dépendance externe.

- `01_favorite_numbers.py`
- `02_tuple.py`
- `03_basket.py`
- `04_floats.py`
- `05_for_loop.py`
- `06_name_validation.py`
- `07_favorite_fruits.py`
- `08_pizza_toppings.py`
- `09_cinemax_tickets.py`

Les nombres préférés sont des exemples à personnaliser.
Un tuple est immuable : on ne peut ni ajouter ni modifier ses éléments en place.
L’exercice 2 intercepte l’erreur de `append`, puis crée un nouveau tuple par concaténation.
Les indices pairs sont 0, 2, ..., 18 : les nombres affichés sont 1, 3, ..., 19.
Le nom doit contenir au moins trois lettres, uniquement alphabétiques (accents acceptés).
Les fruits sont séparés par des espaces et comparés sans tenir compte de la casse.
`quit` termine la saisie des garnitures et des âges. Les âges négatifs ou non entiers sont refusés.
Le bonus demande un nom et un âge pour chaque participant et conserve les 16–21 ans inclus.

Les résultats des tests sont consignés dans `TEST_RESULTS.md`.
