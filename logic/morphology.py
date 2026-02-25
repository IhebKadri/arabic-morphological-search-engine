import os
import time
import threading
import json
from data_structures.avl_tree import AVLTree
from data_structures.hash_table import HashTable
from data_structures.root_node import RootNode

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
ROOTS_FILE = os.path.join(DATA_DIR, "roots.txt")
PATTERNS_FILE = os.path.join(DATA_DIR, "patterns.txt")
ROOTS_META_FILE = os.path.join(DATA_DIR, "roots_metadata.json")

class MorphologicalEngine:
    """
    @brief Moteur principal de l'analyse et de la génération morphologique.
    
    Cette classe gère les racines (arbre AVL), les schèmes (table de hachage),
    les opérations de génération/validation et la persistance des données.
    """
    def __init__(self):
        ## @var roots_tree Arbre AVL stockant les objets RootNode.
        self.roots_tree = AVLTree()
        ## @var patterns_table Table de hachage stockant les schèmes morphologiques.
        self.patterns_table = HashTable(size=100)
        ## @var last_roots_mtime Horodatage de la dernière modification du fichier racines.
        self.last_roots_mtime = 0
        ## @var last_patterns_mtime Horodatage de la dernière modification du fichier schèmes.
        self.last_patterns_mtime = 0
        
        # Chargement initial des données
        self._load_patterns()
        self._load_roots()
        self._load_roots_meta()

    # ─── File I/O & Monitoring ───────────────────────────────

    def check_for_updates(self):
        """
        @brief Vérifie si les fichiers de données ont été modifiés sur le disque.
        
        Réinitialise les structures de données et recharge les fichiers si nécessaire.
        @return True si une mise à jour a été effectuée, False sinon.
        """
        updated = False
        try:
            # Vérification des racines
            if os.path.exists(ROOTS_FILE):
                mtime = os.path.getmtime(ROOTS_FILE)
                if abs(mtime - self.last_roots_mtime) > 0.1:
                    self.roots_tree = AVLTree() # Réinitialisation de l'arbre
                    self._load_roots()
                    updated = True
            
            # Vérification des schèmes
            if os.path.exists(PATTERNS_FILE):
                mtime = os.path.getmtime(PATTERNS_FILE)
                if abs(mtime - self.last_patterns_mtime) > 0.1:
                    self.patterns_table = HashTable(size=100) # Réinitialisation de la table
                    self._load_patterns()
                    updated = True
        except Exception:
            pass
        return updated

    def _load_roots(self):
        """
        @brief Charge les racines à partir du fichier texte (une par ligne).
        """
        if not os.path.exists(ROOTS_FILE):
            return
        try:
            self.last_roots_mtime = os.path.getmtime(ROOTS_FILE)
            with open(ROOTS_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    root = line.strip()
                    if len(root) == 3:
                        self.add_root(root, save=False)
        except Exception:
            pass

    def _load_roots_meta(self):
        """
        @brief Charge les dérivés et fréquences depuis le fichier JSON.
        
        Associe les données chargées aux objets RootNode existants dans l'arbre.
        """
        if not os.path.exists(ROOTS_META_FILE):
            return
        try:
            with open(ROOTS_META_FILE, "r", encoding="utf-8") as f:
                meta = json.load(f)
            for root, data in meta.items():
                rn = self.get_root_node(root)
                if rn:
                    rn.value.derived_words = data.get("derived_words", [])
                    rn.value.frequencies = data.get("frequencies", {})
        except Exception as e:
            print(f"Erreur lors du chargement des métadonnées: {e}")

    def _load_patterns(self):
        """
        @brief Charge les schèmes depuis le fichier patterns.txt (format template|type).
        """
        if not os.path.exists(PATTERNS_FILE):
            return
        try:
            self.last_patterns_mtime = os.path.getmtime(PATTERNS_FILE)
            with open(PATTERNS_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if "|" in line:
                        template, ptype = line.split("|", 1)
                        self.patterns_table.insert(
                            template.strip(),
                            {"template": template.strip(), "type": ptype.strip()},
                        )
        except Exception:
            pass

    def save_roots(self):
        """
        @brief Enregistre les racines actuelles dans roots.txt.
        """
        os.makedirs(DATA_DIR, exist_ok=True)
        nodes = self.roots_tree.inorder_traversal()
        with open(ROOTS_FILE, "w", encoding="utf-8") as f:
            for node in nodes:
                f.write(node.key + "\n")
        self.last_roots_mtime = os.path.getmtime(ROOTS_FILE)
        self.save_roots_meta()

    def save_roots_meta(self):
        """
        @brief Enregistre les mots dérivés et les fréquences dans le fichier JSON.
        """
        os.makedirs(DATA_DIR, exist_ok=True)
        meta = {}
        nodes = self.roots_tree.inorder_traversal()
        for node in nodes:
            # Ne sauvegarder que les données non vides
            if node.value.derived_words or node.value.frequencies:
                meta[node.key] = {
                    "derived_words": node.value.derived_words,
                    "frequencies": node.value.frequencies
                }
        with open(ROOTS_META_FILE, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=4)

    def save_patterns(self):
        """
        @brief Enregistre les schèmes actuels dans patterns.txt.
        """
        os.makedirs(DATA_DIR, exist_ok=True)
        patterns = self.patterns_table.get_all()
        # Tri par clé pour une meilleure lisibilité du fichier
        patterns.sort(key=lambda x: x[0]) 
        with open(PATTERNS_FILE, "w", encoding="utf-8") as f:
            for p_key, p_val in patterns:
                f.write(f"{p_key}|{p_val['type']}\n")
        self.last_patterns_mtime = os.path.getmtime(PATTERNS_FILE)

    def add_pattern(self, template: str, ptype: str):
        """
        @brief Ajoute ou met à jour un schème morphologique.
        @param template Modèle du schème (ex: "فَاعِل").
        @param ptype Type grammatical (ex: "اسم فاعل").
        @return True si ajouté avec succès.
        """
        if not template or not ptype:
            return False
        self.patterns_table.insert(template, {"template": template, "type": ptype})
        self.save_patterns()
        return True

    def delete_pattern(self, template: str):
        """
        @brief Supprime un schème de la table et du disque.
        @param template Le modèle à supprimer.
        @return True si supprimé.
        """
        if self.patterns_table.delete(template):
            self.save_patterns()
            return True
        return False

    # ─── Logic ───────────────────────────────────────────────

    def _strip_tashkeel(self, text: str) -> str:
        """@brief Supprime les diacritiques (tashkeel) d'un texte arabe."""
        tashkeel = ["\u064B", "\u064C", "\u064D", "\u064E", "\u064F", "\u0650", "\u0651", "\u0652"]
        res = ""
        for c in text:
            if c not in tashkeel:
                res += c
        return res

    def generate(self, root: str, pattern_key: str, vocalized: bool = True) -> str:
        """
        @brief Génère un mot dérivé en insérant les consonnes de la racine dans un schème.
        
        Implémente l'algorithme de substitution : 'ف' -> radical-1, 'ع' -> radical-2, 'ل' -> radical-3.
        Gère également la substitution avec Shadda (redoublement).
        
        @param root Le radical (doit faire 3 caractères).
        @param pattern_key Le schème à appliquer.
        @param vocalized Si False, retourne le mot sans diacritiques.
        @return Le mot généré ou un message d'erreur.
        """
        if len(root) != 3:
            return "خطأ: الجذر يجب أن يكون 3 أحرف"

        pattern_data = self.patterns_table.get(pattern_key)
        if not pattern_data:
            return "خطأ: الوزن غير موجود"

        pattern_template = pattern_data["template"]
        r1, r2, r3 = root[0], root[1], root[2]

        result = []
        i = 0
        while i < len(pattern_template):
            char = pattern_template[i]
            # Gestion de la substitution avec shadda
            if i + 1 < len(pattern_template) and pattern_template[i + 1] == "\u0651":
                if char == "ف": result.append(r1 + "\u0651")
                elif char == "ع": result.append(r2 + "\u0651")
                elif char == "ل": result.append(r3 + "\u0651")
                else: result.append(char + "\u0651")
                i += 2; continue

            if char == "ف": result.append(r1)
            elif char == "ع": result.append(r2)
            elif char == "ل": result.append(r3)
            else: result.append(char)
            i += 1

        generated = "".join(result)
        return generated if vocalized else self._strip_tashkeel(generated)

    def generate_all(self, root: str, vocalized: bool = True):
        """
        @brief Génère tous les mots possibles pour une racine donnée en traversant tous les schèmes.
        @param root Le radical de 3 lettres.
        @param vocalized Si False, retourne les mots sans diacritiques.
        @return Liste de tuples (mot, schème, type).
        """
        results = []
        for p_key, p_val in self.get_all_patterns():
            word = self.generate(root, p_key, vocalized=vocalized)
            if "خطأ" not in word:
                results.append((word, p_key, p_val["type"]))
        return results

    def validate(self, word: str, root: str) -> tuple:
        """
        @brief Valide si un mot peut être dérivé d'une racine spécifique.
        
        Effectue une recherche exhaustive sur tous les schèmes disponibles.
        @param word Le mot à vérifier.
        @param root Le radical source supposé.
        @return (True, schème) si valide, (False, None) sinon.
        """
        all_patterns = self.patterns_table.get_all()
        for p_key, _ in all_patterns:
            generated = self.generate(root, p_key)
            if generated == word:
                return True, p_key
        return False, None

    def add_root(self, root: str, save=True):
        """
        @brief Ajoute une nouvelle racine à l'arbre AVL.
        @param root Le radical de 3 caractères.
        @param save Si True, enregistre immédiatement sur le disque.
        @return True si ajouté, False si déjà présent ou invalide.
        """
        if len(root) != 3:
            return False
        if not self.roots_tree.search(root):
            self.roots_tree.insert(root, RootNode(root))
            if save:
                self.save_roots()
            return True
        return False

    def delete_root(self, root: str):
        """
        @brief Supprime une racine de l'arbre et du disque.
        @param root Le radical à supprimer.
        @return True si supprimé avec succès.
        """
        if self.roots_tree.search(root):
            self.roots_tree.delete(root)
            self.save_roots()
            return True
        return False

    def get_root_node(self, root: str):
        """
        @brief Récupère l'objet de données associé à une racine.
        @param root La chaîne de radical.
        @return L'objet RootData ou None.
        """
        node = self.roots_tree.search(root)
        return node.value if node else None

    def get_all_patterns(self):
        """
        @brief Récupère tous les schèmes triés alphabétiquement.
        @return Liste de tuples (clé, data).
        """
        pats = self.patterns_table.get_all()
        pats.sort(key=lambda x: x[0])
        return pats

    def reverse_search(self, word: str) -> list:
        """
        @brief Analyse un mot pour trouver ses racines et schèmes possibles.
        @param word Le mot à analyser (avec ou sans voyelles).
        @return Liste de dictionnaires [{"root": "...", "pattern": "...", "type": "..."}]
        """
        stripped_word = self._strip_tashkeel(word)
        matches = []
        
        all_roots = [n.key for n in self.roots_tree.inorder_traversal()]
        all_pats = self.get_all_patterns()
        
        for r in all_roots:
            for p_key, p_val in all_pats:
                # On compare sans voyelles pour plus de flexibilité
                gen_vocalized = self.generate(r, p_key)
                gen_stripped = self._strip_tashkeel(gen_vocalized)
                
                if gen_stripped == stripped_word:
                    matches.append({
                        "root": r,
                        "pattern": p_key,
                        "type": p_val["type"],
                        "vocalized": gen_vocalized
                    })
        return matches

    def export_data(self) -> str:
        """
        @brief Exporte toute la base de données (racines, dérivés, schèmes) en format texte lisible.
        @return Chaîne de caractères formatée.
        """
        out = "=== ARABIC MORPHOLOGICAL ENGINE EXPORT ===\n\n"
        
        out += "--- PATTERNS ---\n"
        for k, v in self.get_all_patterns():
            out += f"{k} | {v['type']}\n"
        
        out += "\n--- ROOTS & DERIVATIVES ---\n"
        for n in self.roots_tree.inorder_traversal():
            out += f"Root: {n.key}\n"
            dw = n.value.derived_words
            if dw:
                out += "  Derivatives: " + ", ".join(dw) + "\n"
            else:
                out += "  No verified derivatives.\n"
            out += "\n"
            
        return out
