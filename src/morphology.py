##
# @file morphology.py
# @brief Moteur de morphologie pour la génération et la validation de mots arabes.
#

class MorphologyEngine:
    ##
    # @brief Initialise le moteur avec les constantes des radicaux (Fa, 'Ain, Lam).
    #
    def __init__(self):
        self.FA = 'ف'
        self.AIN = 'ع'
        self.LAM = 'ل'

    ##
    # @brief Génère un mot à partir d'une racine trilitère et d'un schème.
    # @param root La racine de 3 caractères (ex: "كتب").
    # @param pattern Le schème (ex: "مفعول").
    # @return Le mot généré ou None si la racine est invalide.
    #
    def generate(self, root, pattern):
        if len(root) != 3:
            return None

        r1, r2, r3 = root[0], root[1], root[2]
        
        result = []
        for char in pattern:
            if char == self.FA:
                result.append(r1)
            elif char == self.AIN:
                result.append(r2)
            elif char == self.LAM:
                result.append(r3)
            else:
                result.append(char)
        
        return "".join(result)

    ##
    # @brief Génère plusieurs mots pour une racine donnée avec plusieurs schèmes.
    # @param root La racine trilitère.
    # @param patterns Liste de schèmes.
    # @return Une liste de tuples (schème, mot).
    #
    def generate_multiple(self, root, patterns):
        results = []
        for pattern in patterns:
            word = self.generate(root, pattern)
            if word:
                results.append((pattern, word))
        return results

    ##
    # @brief Génère la famille morphologique complète d'une racine.
    # @param root La racine trilitère.
    # @param all_patterns Liste de tous les schèmes connus.
    # @return Une liste de tuples (racine, schème, mot).
    #
    def generate_family(self, root, all_patterns):
        family = []
        for pattern in all_patterns:
            word = self.generate(root, pattern)
            if word:
                family.append((root, pattern, word))
        return family

    ##
    # @brief Valide si un mot appartient à une racine via un schème connu.
    # @param word Le mot à valider.
    # @param root La racine cible.
    # @param patterns_list Liste des schèmes à tester.
    # @return Un tuple (True, schème) si validé, sinon (False, None).
    #
    def validate(self, word, root, patterns_list):
        if len(root) != 3:
            return (False, None)
        
        for pattern in patterns_list:
            generated = self.generate(root, pattern)
            if generated == word:
                return (True, pattern)
        
        return (False, None)

    ##
    # @brief Décompose un mot pour trouver sa racine et son schème.
    # @param word Le mot arabe à décomposer.
    # @param all_roots Liste de toutes les racines connues.
    # @param patterns_list Liste de tous les schèmes connus.
    # @return Un tuple (racine, schème) ou (None, None).
    #
    def decompose(self, word, all_roots, patterns_list):
        for root in all_roots:
            if len(root) != 3:
                continue
            for pattern in patterns_list:
                generated = self.generate(root, pattern)
                if generated == word:
                    return (root, pattern)
        return (None, None)

    ##
    # @brief (Obsolète) Recherche le schème pour un mot et une racine.
    # @param word Le mot.
    # @param root La racine.
    # @param patterns_list Liste des schèmes.
    # @return Le schème trouvé ou None.
    #
    def find_pattern(self, word, root, patterns_list):
        for pattern in patterns_list:
            if self.generate(root, pattern) == word:
                return pattern
        return None
