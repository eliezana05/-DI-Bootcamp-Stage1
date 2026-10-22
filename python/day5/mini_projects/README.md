# Day 5 — Mini-projets Python

Deux jeux en terminal, sans dépendance à installer. Le code et les commentaires sont en anglais simple.

Depuis la racine du dépôt :

```sh
python3 python/day5/mini_projects/tic_tac_toe.py
python3 python/day5/mini_projects/hangman.py
```

## Morpion

Deux joueurs : X commence, puis O. Saisir séparément une ligne et une colonne entre 1 et 3.
Une case occupée ou une saisie invalide ne fait pas perdre son tour.
Les fonctions `display_board`, `player_input`, `check_win`, `check_tie` et `play` séparent les étapes.
La grille est passée aux fonctions pour éviter une variable globale.

## Pendu

Un mot ou une expression est choisi au hasard dans la liste fournie par le cours.
Proposer une lettre à la fois. Les majuscules sont acceptées et les espaces sont révélés automatiquement.
Six erreurs complètent le dessin : tête, corps, bras gauche, bras droit, jambe gauche, jambe droite.
Les saisies invalides et les répétitions ne coûtent aucune chance.

Pour arrêter un jeu : Ctrl+C.

## Validation

```sh
python3 -m unittest discover -s python/day5/mini_projects -v
```

22 octobre 2026 : **19 tests réussis**, dont :

- Les huit lignes gagnantes pour chaque symbole et l'indépendance des lignes de la grille.
- Parties complètes en terminal : victoire de X, victoire de O, égalité, victoire au neuvième coup.
- Saisies invalides et cases occupées.
- Lettres répétées, mots avec plusieurs occurrences et expression `credit card`.
- Victoire, six erreurs, jeu aléatoire en terminal et arrêt quand l'entrée se termine.

Les tests utilisent des entrées simulées ; les appels en terminal ont une limite de cinq secondes.

## Énoncés

- [Tic Tac Toe](https://octopus.developers.institute/courses/collection/254/course/1067/section/56/chapter/278)
- [Hangman](https://octopus.developers.institute/courses/collection/254/course/1067/section/56/chapter/279)

Chaque jeu est un fichier autonome à soumettre séparément.
