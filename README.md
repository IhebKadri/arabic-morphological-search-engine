# Moteur de Recherche Morphologique Arabe (محرك البحث الصرفي العربي)

Ce projet est un moteur de recherche (محرك بحث) et de génération (توليد) morphologique (صرفي) pour la langue arabe. Il permet de gérer des racines (جذور) trilitères (ثلاثية) et d'appliquer des schèmes (أوزان) pour générer ou vérifier des mots dérivés (كلمات مشتقة).

## 🚀 Fonctionnalités (المميزات)

- **Gestion des Racines (إدارة الجذور)** : Ajout, recherche et suppression de racines trilitères (ثلاثية).
- **Gestion des Schèmes (إدارة الأوزان)** : Stockage et manipulation de modèles morphologiques (قوالب صرفية).
- **Génération Morphologique (التوليد الصرفي)** : Génération d'un mot à partir d'une racine et d'un schème, ou génération de toute la famille morphologique (الأسرة الصرفية).
- **Validation (التحقق)** : Vérification si un mot est dérivé d'une racine spécifique en identifiant le schème correspondant.
- **Interfaces Multiples (واجهات متعددة)** :
  - Interface Graphique (واجهة رسومية - GUI) interactive avec **Flet**.
  - Interface en Ligne de Commande (واجهة أوامر - CLI) pour une utilisation rapide.

## 🏗️ Structures de Données (هياكل البيانات)

L'efficacité du moteur repose sur deux structures de données (هياكل بيانات) fondamentales :

1.  **Arbre AVL (شجرة AVL)** : Utilisé pour stocker les racines (جذور). C'est un arbre de recherche binaire (شجرة بحث ثنائية) auto-équilibré (متوازنة تلقائياً) qui garantit des performances optimales pour la recherche ($O(\log n)$).
2.  **Table de Hachage (جدول التجزئة)** : Utilisée pour indexer les schèmes (أوزان). Elle utilise une fonction de hachage (دالة تجزئة) par roulement polynomial et gère les collisions (تصادمات) par chaînage (سلاسل التصادم).

## 📊 Analyse de Complexité (تحليل التعقيد)

### Complexité Temporelle (التعقيد الزمني)

| Opération (العملية) | Structure (الهيكل) | Cas Moyen (الحالة المتوسطة) | Pire Cas (أسوأ حالة) |
| :--- | :--- | :--- | :--- |
| **Insertion Racine (إدراج جذر)** | Arbre AVL | $O(\log n)$ | $O(\log n)$ |
| **Recherche Schème (بحث عن وزن)** | Table de Hachage | $O(1)$ | $O(k)$ |
| **Génération (توليد)** | Substitution | $O(L)$ | $O(L)$ |
| **Validation (تحقق)** | Recherche Exhaustive | $O(P \times L)$ | $O(P \times L)$ |

*Note : $n$ est le nombre de racines, $L$ la longueur du schème, et $P$ le nombre de schèmes.*

### Complexité Spatiale (التعقيد المكاني)

- **Arbre AVL** : $O(N)$ où $N$ est le nombre de racines stockées.
- **Table de Hachage** : $O(S + P)$ où $S$ est la taille de la table et $P$ le nombre de schèmes.

## 🛠️ Installation et Utilisation (التثبيت والاستخدام)

### Prérequis (المتطلبات)
- Python 3.9+
- Pip (gestionnaire de paquets)

### Installation (التثبيت)
1. Clonez le dépôt ou téléchargez les fichiers.
2. Installez les dépendances (المتطلبات) nécessaires :
   ```bash
   pip install -r requirements.txt
   ```

### Exécution (التشغيل)

#### Interface Graphique (GUI)
Pour lancer l'application avec l'interface visuelle :
```bash
python main.py
```

#### Interface Terminal (CLI)
Pour utiliser le moteur directement dans votre terminal :
```bash
python cli.py
```

#### Tests Unitaires (الاختبارات)
Pour vérifier l'intégrité du système :
```bash
python -m unittest tests/test_morphology.py
```

## 📝 Rapport Technique (Toute la documentation technique se trouve dans `rapport_technique.md`)
