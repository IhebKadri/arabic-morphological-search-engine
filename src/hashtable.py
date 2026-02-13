##
# @file hashtable.py
# @brief Implémentation d'une table de hachage personnalisée.
#

class HashNode:
    ##
    # @brief Représente un nœud dans la chaîne de collision de la table de hachage.
    # @param key La clé (nom du schème).
    # @param value La valeur (description ou règle associée).
    #
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class HashTable:
    ##
    # @brief Table de hachage gérant les collisions par chaînage.
    # @param capacity Capacité initiale de la table.
    #
    def __init__(self, capacity=100):
        self.capacity = capacity
        self.size = 0
        self.table = [None] * capacity

    ##
    # @brief Fonction de hachage polynomiale pour les chaînes de caractères.
    # @param key La clé à hacher.
    # @return L'index calculé dans la table.
    #
    def _hash(self, key):
        hash_val = 0
        prime = 31
        for char in key:
            hash_val = (hash_val * prime + ord(char)) % self.capacity
        return hash_val

    ##
    # @brief Insère ou met à jour un élément dans la table de hachage.
    # @param key Le nom du schème.
    # @param value La description ou règle associée.
    #
    def insert(self, key, value):
        index = self._hash(key)
        current = self.table[index]
        while current:
            if current.key == key:
                current.value = value
                return
            current = current.next
        
        new_node = HashNode(key, value)
        new_node.next = self.table[index]
        self.table[index] = new_node
        self.size += 1

    ##
    # @brief Récupère la valeur associée à une clé.
    # @param key La clé à rechercher.
    # @return La valeur correspondante ou None si absente.
    #
    def get(self, key):
        index = self._hash(key)
        current = self.table[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next
        return None

    ##
    # @brief Supprime un élément de la table.
    # @param key La clé à supprimer.
    # @return True si l'élément a été supprimé, False sinon.
    #
    def delete(self, key):
        index = self._hash(key)
        current = self.table[index]
        prev = None
        
        while current:
            if current.key == key:
                if prev:
                    prev.next = current.next
                else:
                    self.table[index] = current.next
                self.size -= 1
                return True
            prev = current
            current = current.next
        return False

    ##
    # @brief Récupère tous les couples (clé, valeur) de la table.
    # @return Une liste de tuples (key, value).
    #
    def get_all(self):
        items = []
        for i in range(self.capacity):
            current = self.table[i]
            while current:
                items.append((current.key, current.value))
                current = current.next
        return items
