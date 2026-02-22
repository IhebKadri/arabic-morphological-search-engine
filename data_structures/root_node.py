class RootData:
    """
    @brief Structure associée à une racine contenant les mots dérivés et leurs fréquences.
    """
    def __init__(self):
        ## @var derived_words Liste des mots dérivés confirmés.
        self.derived_words = []
        ## @var frequencies Dictionnaire associant chaque mot à son nombre de générations.
        self.frequencies = {}

    def add_derived_word(self, word):
        """
        @brief Ajoute un mot dérivé ou incrémente sa fréquence.
        @param word Le mot à enregistrer.
        """
        if word not in self.derived_words:
            self.derived_words.append(word)
            self.frequencies[word] = 0
        self.frequencies[word] += 1

class RootNode:
    """
    @brief Représente l'unité logique d'une racine dans l'arbre AVL.
    
    Fait le lien entre la chaîne du radical et ses métadonnées.
    """
    def __init__(self, root_str):
        ## @var key Chaine de caractères de la racine.
        self.key = root_str
        ## @var value Pointeur vers la structure RootData associée (exigence PRD).
        self.value = RootData()

    @property
    def derived_words(self):
        """@return Liste des mots dérivés."""
        return self.value.derived_words

    @property
    def frequencies(self):
        """@return Dictionnaire des fréquences."""
        return self.value.frequencies

    def add_derived_word(self, word):
        """
        @brief Délègue l'ajout du mot à l'objet RootData.
        """
        self.value.add_derived_word(word)


