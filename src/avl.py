##
# @file avl.py
# @brief Implémentation d'un arbre AVL pour le stockage des racines arabes.
#

class AVLNode:
    ##
    # @brief Représente un nœud dans l'arbre AVL.
    # @param key La racine arabe (chaîne de caractères).
    # @param value Données associées (liste de mots dérivés validés).
    #
    def __init__(self, key, value=None):
        self.key = key
        self.value = value if value is not None else []
        self.height = 1
        self.left = None
        self.right = None

class AVLTree:
    ##
    # @brief Structure de données de l'arbre AVL pour une gestion équilibrée des racines.
    #
    def __init__(self):
        self.root = None

    ##
    # @brief Récupère la hauteur d'un nœud.
    # @param node Le nœud cible.
    # @return La hauteur du nœud ou 0 s'il est None.
    #
    def _height(self, node):
        return node.height if node else 0

    ##
    # @brief Calcule le facteur d'équilibre d'un nœud.
    # @param node Le nœud cible.
    # @return La différence de hauteur entre le sous-arbre gauche et droit.
    #
    def _balance_factor(self, node):
        return self._height(node.left) - self._height(node.right) if node else 0

    ##
    # @brief Met à jour la hauteur d'un nœud basé sur ses enfants.
    # @param node Le nœud à mettre à jour.
    #
    def _update_height(self, node):
        if node:
            node.height = 1 + max(self._height(node.left), self._height(node.right))

    ##
    # @brief Effectue une rotation à droite.
    # @param y Le nœud pivot de la rotation.
    # @return Le nouveau nœud racine du sous-arbre après rotation.
    #
    def _right_rotate(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        self._update_height(y)
        self._update_height(x)
        return x

    ##
    # @brief Effectue une rotation à gauche.
    # @param x Le nœud pivot de la rotation.
    # @return Le nouveau nœud racine du sous-arbre après rotation.
    #
    def _left_rotate(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        self._update_height(x)
        self._update_height(y)
        return y

    ##
    # @brief Insère une nouvelle racine dans l'arbre AVL.
    # @param key La racine à insérer.
    # @param value Données optionnelles associées.
    #
    def insert(self, key, value=None):
        self.root = self._insert_node(self.root, key, value)

    ##
    # @brief Fonction récursive pour l'insertion d'un nœud et le rééquilibrage.
    # @param node Le nœud actuel dans la récursion.
    # @param key La clé à insérer.
    # @param value Valeur associée.
    # @return Le nœud (éventuellement nouveau ou rééquilibré).
    #
    def _insert_node(self, node, key, value):
        if not node:
            return AVLNode(key, value)
        
        if key < node.key:
            node.left = self._insert_node(node.left, key, value)
        elif key > node.key:
            node.right = self._insert_node(node.right, key, value)
        else:
            return node

        self._update_height(node)
        balance = self._balance_factor(node)

        if balance > 1 and key < node.left.key:
            return self._right_rotate(node)

        if balance < -1 and key > node.right.key:
            return self._left_rotate(node)

        if balance > 1 and key > node.left.key:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        if balance < -1 and key < node.right.key:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    ##
    # @brief Recherche une racine dans l'arbre.
    # @param key La racine à rechercher.
    # @return Le nœud correspondant ou None s'il n'est pas trouvé.
    #
    def search(self, key):
        return self._search_node(self.root, key)

    ##
    # @brief Fonction récursive de recherche.
    # @param node Le nœud actuel.
    # @param key La clé recherchée.
    # @return Le nœud trouvé ou None.
    #
    def _search_node(self, node, key):
        if not node or node.key == key:
            return node
        
        if key < node.key:
            return self._search_node(node.left, key)
        return self._search_node(node.right, key)

    ##
    # @brief Récupère toutes les racines dans l'ordre alphabétique.
    # @return Une liste de chaînes de caractères (clés).
    #
    def get_inorder(self):
        result = []
        self._inorder_traversal(self.root, result)
        return result

    ##
    # @brief Effectue un parcours infixe de l'arbre.
    # @param node Le nœud actuel.
    # @param result La liste accumulant les résultats.
    #
    def _inorder_traversal(self, node, result):
        if node:
            self._inorder_traversal(node.left, result)
            result.append(node.key)
            self._inorder_traversal(node.right, result)

    ##
    # @brief Ajoute un mot dérivé validé à la liste d'une racine.
    # @param key La racine cible.
    # @param word Le mot dérivé.
    # @param pattern Le schème utilisé.
    # @return True si l'ajout ou l'incrémentation a réussi, False sinon.
    #
    def add_derived(self, key, word, pattern):
        node = self.search(key)
        if not node:
            return False
        
        for entry in node.value:
            if entry["word"] == word:
                entry["frequency"] += 1
                return True
        
        node.value.append({
            "word": word,
            "pattern": pattern,
            "frequency": 1
        })
        return True

    ##
    # @brief Récupère la liste des dérivés validés pour une racine.
    # @param key La racine cible.
    # @return Une liste de dictionnaires contenant 'word', 'pattern' et 'frequency'.
    #
    def get_derived(self, key):
        node = self.search(key)
        if node:
            return node.value
        return []
