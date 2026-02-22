class AVLNode:
    """
    @brief Représente un nœud dans l'arbre AVL.
    
    Cette classe stocke la clé (racine), la valeur (données associées), 
    la hauteur du nœud et les références vers les nœuds enfants.
    """
    def __init__(self, key, value=None):
        ## @var key Clé unique du nœud (ex: la chaîne du radical "ktb").
        self.key = key          
        ## @var value Objet RootNode contenant les dérivés et métadonnées.
        self.value = value      
        ## @var height Hauteur du nœud utilisée pour l'équilibrage (initialement 1).
        self.height = 1
        ## @var left Référence vers l'enfant gauche.
        self.left = None
        ## @var right Référence vers l'enfant droit.
        self.right = None

class AVLTree:
    """
    @brief Implémentation d'un Arbre de Recherche Binaire Auto-équilibré (AVL).
    
    Garantit des opérations de recherche, insertion et suppression en O(log n).
    """
    def __init__(self):
        ## @var root Racine de l'arbre AVL.
        self.root = None

    def _height(self, node):
        """
        @brief Récupère la hauteur d'un nœud.
        @param node Le nœud cible.
        @return La hauteur du nœud ou 0 s'il est None.
        """
        return node.height if node else 0

    def _balance_factor(self, node):
        """
        @brief Calcule le facteur d'équilibre d'un nœud.
        @param node Le nœud cible.
        @return Différence de hauteur entre le sous-arbre gauche et droit.
        """
        return self._height(node.left) - self._height(node.right) if node else 0

    def _update_height(self, node):
        """
        @brief Met à jour la hauteur d'un nœud en fonction de ses enfants.
        @param node Le nœud à mettre à jour.
        """
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _rotate_right(self, y):
        """
        @brief Effectue une rotation simple vers la droite.
        @param y Le nœud pivot de la rotation.
        @return Le nouveau nœud racine du sous-arbre.
        """
        x = y.left
        T2 = x.right

        # Effectuer la rotation
        x.right = y
        y.left = T2

        # Mise à jour des hauteurs
        self._update_height(y)
        self._update_height(x)

        return x

    def _rotate_left(self, x):
        """
        @brief Effectue une rotation simple vers la gauche.
        @param x Le nœud pivot de la rotation.
        @return Le nouveau nœud racine du sous-arbre.
        """
        y = x.right
        T2 = y.left

        # Effectuer la rotation
        y.left = x
        x.right = T2

        # Mise à jour des hauteurs
        self._update_height(x)
        self._update_height(y)

        return y

    def insert(self, key, value):
        """
        @brief Insère une nouvelle racine dans l'arbre.
        @param key La chaîne de caractères de la racine.
        @param value L'objet de données associé.
        """
        self.root = self._insert(self.root, key, value)

    def _insert(self, node, key, value):
        """
        @brief Logique récursive de l'insertion avec rééquilibrage.
        """
        if not node:
            return AVLNode(key, value)

        if key < node.key:
            node.left = self._insert(node.left, key, value)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
        else:
            return node # Doublons non autorisés

        # Mise à jour de la hauteur
        self._update_height(node)
        balance = self._balance_factor(node)

        # Cas de déséquilibre
        # Gauche Gauche
        if balance > 1 and key < node.left.key:
            return self._rotate_right(node)

        # Droite Droite
        if balance < -1 and key > node.right.key:
            return self._rotate_left(node)

        # Gauche Droite
        if balance > 1 and key > node.left.key:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Droite Gauche
        if balance < -1 and key < node.right.key:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def search(self, key):
        """
        @brief Recherche un nœud par sa clé.
        @param key La clé à rechercher.
        @return Le nœud AVLNode trouvé ou None.
        """
        return self._search(self.root, key)

    def _search(self, node, key):
        if not node or node.key == key:
            return node
        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)

    def inorder_traversal(self):
        """
        @brief Effectue un parcours infixe (ordonné) de l'arbre.
        @return Une liste de tous les nœuds triés par clé.
        """
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node)
            self._inorder(node.right, result)

    def delete(self, key):
        """
        @brief Supprime une racine de l'arbre.
        @param key La clé de la racine à supprimer.
        """
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        """
        @brief Logique récursive de suppression avec rééquilibrage.
        """
        if not node:
            return node

        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # Nœud avec un seul enfant ou sans enfant
            if not node.left:
                temp = node.right
                node = None
                return temp
            elif not node.right:
                temp = node.left
                node = None
                return temp

            # Nœud avec deux enfants : successeur inorder
            temp = self._get_min_value_node(node.right)
            node.key = temp.key
            node.value = temp.value
            node.right = self._delete(node.right, temp.key)

        if not node:
            return node

        # Mise à jour de la hauteur
        self._update_height(node)
        balance = self._balance_factor(node)

        # Rééquilibrage
        if balance > 1 and self._balance_factor(node.left) >= 0:
            return self._rotate_right(node)

        if balance > 1 and self._balance_factor(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        if balance < -1 and self._balance_factor(node.right) <= 0:
            return self._rotate_left(node)

        if balance < -1 and self._balance_factor(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def _get_min_value_node(self, node):
        if not node or not node.left:
            return node
        return self._get_min_value_node(node.left)
