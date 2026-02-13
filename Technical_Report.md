# Rapport Technique : Moteur de Recherche Morphologique Arabe

## 1. Introduction
Ce projet consiste en le développement d'un moteur de recherche morphologique pour la langue arabe. Le système repose sur le modèle de dérivation "Racine-Schème" (Root-Pattern). L'objectif est de fournir une interface interactive permettant de gérer des racines trilitères, d'ajouter des schèmes, de générer des familles de mots et de valider l'appartenance de mots à des racines spécifiques.

## 2. Structures de Données

### 2.1 Arbre AVL (Gestion des Racines)
Les racines arabes sont stockées dans un **Arbre AVL** (Adelson-Velsky et Landis), un arbre binaire de recherche auto-équilibré.
- **Justification** : La recherche d'une racine est l'opération la plus fréquente. Un arbre AVL garantit une complexité de recherche de **O(log n)**, même après de nombreuses insertions, contrairement à un arbre binaire classique qui pourrait devenir asymétrique.
- **Implémentation** : 
  - Chaque nœud contient la racine (clé) et une liste de dictionnaires (valeur) stockant les dérivés validés.
  - Chaque entrée de dérivé contient : le mot, le schème utilisé et sa fréquence d'utilisation.
  - Les rotations (gauche et droite) maintiennent l'équilibre de l'arbre lors de chaque insertion dynamique.

### 2.2 Table de Hachage (Gestion des Schèmes)
Les schèmes morphologiques sont gérés par une **Table de Hachage** implémentée manuellement.
- **Justification** : L'accès à un schème spécifique par son nom doit être quasi-instantané. La table de hachage offre une complexité moyenne de **O(1)**.
- **Implémentation** :
  - Utilisation d'une fonction de hachage polynomiale pour transformer les chaînes de caractères en indices numériques.
  - Gestion des collisions par **chaînage** (Linked List) pour assurer l'intégrité des données en cas de collision d'indices.

## 3. Algorithmes de Morphologie

### 3.1 Génération Morphologique
Le cœur algorithmique réside dans le `MorphologyEngine`.
- **Mécanisme** : Le système utilise les radicaux de substitution standards : 'ف' (Fa), 'ع' ('Ain) et 'ل' (Lam).
- **Algorithme** : Pour une racine R=(R1, R2, R3) et un schème S, l'algorithme parcourt S et remplace chaque occurrence de Fa par R1, 'Ain par R2 et Lam par R3. Les lettres augmentatives (lettres du schème n'étant pas des radicaux) sont conservées.
- **Génération Multiple** : Permet de générer une "famille" en itérant sur une liste de schèmes sélectionnés ou sur l'intégralité des schèmes stockés en base.

### 3.2 Validation et Décomposition
- **Validation** : Pour vérifier si un mot X appartient à une racine Y, le moteur tente de générer X à partir de Y en utilisant successivement tous les schèmes connus. Si une correspondance est trouvée, le mot est validé.
- **Décomposition** : Cet algorithme étend la validation en testant le mot contre toutes les racines de l'arbre AVL. Il permet d'identifier dynamiquement la racine et le schème d'un mot saisi sans information préalable.

## 4. Analyse de Complexité Algorithmique
- **Insertion de racine** : O(log N) - l'Arbre AVL reste équilibré.
- **Recherche de racine** : O(log N).
- **Accès aux schèmes** : O(1) en moyenne.
- **Génération d'un mot** : O(L) où L est la longueur du schème.
- **Validation d'un mot** : O(P * L) où P est le nombre de schèmes.
- **Décomposition** : O(N * P * L) - cette opération est la plus coûteuse car elle parcourt toutes les racines.

## 5. Difficultés Rencontrées et Solutions
- **Encodage et Unicode** : La manipulation des caractères arabes nécessite une gestion rigoureuse de l'encodage UTF-8, particulièrement lors de la persistance dans le fichier `roots.txt`.
- **Interface Utilisateur (RTL)** : Bien que Tkinter soit limité pour le rendu "Right-to-Left" complet, l'utilisation de l'alignement (`justify="right"`, `anchor="e"`) a permis de créer une interface intuitive pour les utilisateurs arabophones.
- **Persistance des données** : La mise à jour dynamique du fichier source tout en maintenant la cohérence avec la structure en mémoire (AVL) a nécessité une synchronisation lors de l'appel à `add_root`.

## 6. Conclusion
L'application répond à l'ensemble des exigences techniques. L'utilisation combinée d'un Arbre AVL pour la structure lexicale et d'une Table de Hachage pour les règles morphologiques offre un moteur performant et évolutif pour l'étude de la langue arabe.
