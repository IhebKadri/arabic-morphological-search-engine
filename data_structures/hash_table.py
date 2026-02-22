class HashTable:
    """
    @brief Une implémentation d'une Table de Hachage avec résolution de collisions par chaînage.
    
    Permet un stockage et une récupération efficaces des schèmes morphologiques.
    """
    def __init__(self, size=100):
        ## @var size Taille de la table de hachage.
        self.size = size
        ## @var table Tableau de listes (buckets) pour gérer les collisions.
        self.table = [[] for _ in range(size)]

    def _hash(self, key):
        """
        @brief Fonction de hachage par roulement polynomial pour les chaînes.
        
        Algorithme : hash = (c1 * p^(n-1) + c2 * p^(n-2) + ... + cn * p^0) mod size
        @param key La chaîne de caractères à hacher.
        @return L'index calculé dans la table.
        """
        hash_val = 0
        prime = 37 # Nombre premier adapté pour les caractères Unicode
        
        for char in key:
            hash_val = (hash_val * prime + ord(char)) % (2**31 - 1)
        
        return hash_val % self.size

    def insert(self, key, value):
        """
        @brief Insère une paire clé-valeur dans la table.
        @param key Le nom du schème (ex: "فَاعِل").
        @param value Les données associées au schème.
        """
        index = self._hash(key)
        bucket = self.table[index]
        
        # Mise à jour si la clé existe déjà
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        
        # Ajout sinon
        bucket.append((key, value))

    def get(self, key):
        """
        @brief Récupère la valeur associée à une clé.
        @param key La clé à rechercher.
        @return La valeur trouvée ou None.
        """
        index = self._hash(key)
        bucket = self.table[index]
        
        for k, v in bucket:
            if k == key:
                return v
        return None

    def delete(self, key):
        """
        @brief Supprime une clé de la table.
        @param key La clé à supprimer.
        @return True si supprimé, False sinon.
        """
        index = self._hash(key)
        bucket = self.table[index]
        
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                return True
        return False

    def get_all(self):
        """
        @brief Récupère tous les éléments de la table.
        @return Une liste de tuples (clé, valeur).
        """
        all_items = []
        for bucket in self.table:
            for item in bucket:
                all_items.append(item)
        return all_items
