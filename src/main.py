##
# @file main.py
# @brief Interface graphique (Tkinter) pour le moteur de morphologie arabe.
#

import tkinter as tk
from tkinter import ttk, messagebox
import os

try:
    from src.avl import AVLTree
    from src.hashtable import HashTable
    from src.morphology import MorphologyEngine
except ImportError:
    from avl import AVLTree
    from hashtable import HashTable
    from morphology import MorphologyEngine

class MorphApp:
    ##
    # @brief Classe principale gérant l'application et l'interface utilisateur.
    # @param root L'instance principale de Tkinter.
    #
    def __init__(self, root):
        self.root = root
        self.root.title("محرك الاشتقاق الصرفي العربي")
        self.root.geometry("950x700")

        self.setup_styles()

        self.avl = AVLTree()
        self.hashtable = HashTable(100)
        self.morph_engine = MorphologyEngine()

        self._seed_data()

        main_container = ttk.Frame(root, padding="10")
        main_container.pack(fill="both", expand=True)

        self.tab_control = ttk.Notebook(main_container)

        self.tab_roots = ttk.Frame(self.tab_control, padding="20")
        self.tab_patterns = ttk.Frame(self.tab_control, padding="20")
        self.tab_generator = ttk.Frame(self.tab_control, padding="20")
        self.tab_validator = ttk.Frame(self.tab_control, padding="20")
        self.tab_derived = ttk.Frame(self.tab_control, padding="20")

        self.tab_control.add(self.tab_roots, text='  إدارة الجذور  ')
        self.tab_control.add(self.tab_patterns, text='  إدارة الأوزان  ')
        self.tab_control.add(self.tab_generator, text='  المولّد الصرفي  ')
        self.tab_control.add(self.tab_validator, text='  التحقق الصرفي  ')
        self.tab_control.add(self.tab_derived, text='  المشتقات المسجلة  ')

        self.tab_control.pack(expand=1, fill="both")

        self.setup_roots_tab()
        self.setup_patterns_tab()
        self.setup_generator_tab()
        self.setup_validator_tab()
        self.setup_derived_tab()

    ##
    # @brief Configure les styles visuels de l'interface (couleurs, polices).
    #
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        PRIMARY_COLOR = "#2980b9"
        SECONDARY_COLOR = "#27ae60"
        BG_COLOR = "#ecf0f1"
        TEXT_COLOR = "#2c3e50"
        DANGER_COLOR = "#c0392b"

        style.configure(".", background=BG_COLOR, foreground=TEXT_COLOR, font=("Segoe UI", 11))
        style.configure("TFrame", background=BG_COLOR)
        style.configure("TLabel", background=BG_COLOR, foreground=TEXT_COLOR)
        style.configure("TButton", background=PRIMARY_COLOR, foreground="white", padding=6,
                        font=("Segoe UI", 10, "bold"))
        style.map("TButton", background=[("active", "#3498db")])

        style.configure("Green.TButton", background=SECONDARY_COLOR, foreground="white")
        style.map("Green.TButton", background=[("active", "#2ecc71")])

        style.configure("Red.TButton", background=DANGER_COLOR, foreground="white")
        style.map("Red.TButton", background=[("active", "#e74c3c")])

        style.configure("TEntry", fieldbackground="white", padding=5)
        style.configure("TCombobox", padding=5)

        style.configure("TNotebook", background=BG_COLOR)
        style.configure("TNotebook.Tab", padding=[12, 8], font=("Segoe UI", 11, "bold"),
                        background="#bdc3c7", foreground="#7f8c8d")
        style.map("TNotebook.Tab", background=[("selected", PRIMARY_COLOR)],
                  foreground=[("selected", "white")])

        style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground=PRIMARY_COLOR)
        style.configure("SubHeader.TLabel", font=("Segoe UI", 12, "bold"), foreground="#7f8c8d")
        style.configure("Result.TLabel", font=("Segoe UI", 14, "bold"), foreground=PRIMARY_COLOR,
                        background="#d5dbdb", padding=10)
        style.configure("Valid.TLabel", font=("Segoe UI", 14, "bold"), foreground=SECONDARY_COLOR,
                        background="#d5f5e3", padding=10)
        style.configure("Invalid.TLabel", font=("Segoe UI", 14, "bold"), foreground=DANGER_COLOR,
                        background="#fadbd8", padding=10)

        style.configure("Treeview", font=("Segoe UI", 11), rowheight=28)
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"),
                        foreground=PRIMARY_COLOR)

    ##
    # @brief Charge les données initiales (racines depuis fichier, schèmes par défaut).
    #
    def _seed_data(self):
        roots_paths = ["data/roots.txt", "data\\roots.txt",
                       os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "roots.txt")]

        loaded = False
        for path in roots_paths:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        root_val = line.strip()
                        if len(root_val) == 3:
                            self.avl.insert(root_val)
                loaded = True
                break
            except FileNotFoundError:
                continue

        if not loaded:
            for r in ["كتب", "فعل", "درس", "نصر", "خرج", "دخل", "جلس", "سمع", "شرب", "لعب"]:
                self.avl.insert(r)

        default_patterns = [
            ("فاعل", "اسم الفاعل"),
            ("مفعول", "اسم المفعول"),
            ("تفعيل", "مصدر التفعيل"),
            ("افتعل", "وزن افتعل"),
            ("فعّال", "صيغة المبالغة"),
            ("مفعل", "اسم المكان"),
            ("فعيل", "صفة مشبهة"),
            ("أفعل", "وزن أفعل"),
        ]
        for pattern, description in default_patterns:
            self.hashtable.insert(pattern, description)

    ##
    # @brief Configure l'onglet de gestion des racines.
    #
    def setup_roots_tab(self):
        ttk.Label(self.tab_roots, text="إدارة الجذور", style="Header.TLabel").pack(anchor="e", pady=(0, 20))

        frame_input = ttk.LabelFrame(self.tab_roots, text="إضافة جذر جديد", padding=15)
        frame_input.pack(fill="x", pady=10)

        ttk.Button(frame_input, text="إضافة", command=self.add_root,
                   style="Green.TButton").pack(side=tk.RIGHT, padx=10)
        self.root_entry = ttk.Entry(frame_input, width=20, font=("Segoe UI", 12), justify="right")
        self.root_entry.pack(side=tk.RIGHT, padx=5)
        ttk.Label(frame_input, text=":الجذر (٣ حروف)").pack(side=tk.RIGHT, padx=(0, 10))

        frame_search = ttk.LabelFrame(self.tab_roots, text="البحث عن جذر", padding=15)
        frame_search.pack(fill="x", pady=10)

        ttk.Button(frame_search, text="بحث", command=self.search_root).pack(side=tk.RIGHT, padx=10)
        self.search_root_entry = ttk.Entry(frame_search, width=20, font=("Segoe UI", 12), justify="right")
        self.search_root_entry.pack(side=tk.RIGHT, padx=5)
        ttk.Label(frame_search, text=":الجذر للبحث").pack(side=tk.RIGHT, padx=(0, 10))

        self.search_result_label = ttk.Label(self.tab_roots, text="", style="Result.TLabel", anchor="center")
        self.search_result_label.pack(fill="x", pady=5, padx=50)

        ttk.Label(self.tab_roots, text="الجذور المخزنة", style="SubHeader.TLabel").pack(anchor="e", pady=(15, 5))

        frame_list = ttk.Frame(self.tab_roots)
        frame_list.pack(fill="both", expand=True)

        self.roots_listbox = tk.Listbox(frame_list, font=("Courier New", 12), borderwidth=0,
                                        highlightthickness=1, relief="flat", bg="white",
                                        fg="#2c3e50", justify="right")
        self.roots_listbox.pack(side=tk.LEFT, fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame_list, orient="vertical", command=self.roots_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.roots_listbox.config(yscrollcommand=scrollbar.set)

        btn_frame = ttk.Frame(self.tab_roots)
        btn_frame.pack(pady=10, fill="x")
        ttk.Button(btn_frame, text="تحديث القائمة", command=self.refresh_roots).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="عرض المشتقات", command=self.show_root_derivatives).pack(side=tk.RIGHT, padx=5)

        self.refresh_roots()

    ##
    # @brief Configure l'onglet de gestion des schèmes.
    #
    def setup_patterns_tab(self):
        ttk.Label(self.tab_patterns, text="إدارة الأوزان", style="Header.TLabel").pack(anchor="e", pady=(0, 20))

        frame_input = ttk.LabelFrame(self.tab_patterns, text="إضافة وزن جديد", padding=15)
        frame_input.pack(fill="x", pady=10)

        ttk.Button(frame_input, text="إضافة", command=self.add_pattern,
                   style="Green.TButton").pack(side=tk.RIGHT, padx=10)
        self.pattern_desc_entry = ttk.Entry(frame_input, width=20, font=("Segoe UI", 11), justify="right")
        self.pattern_desc_entry.pack(side=tk.RIGHT, padx=5)
        ttk.Label(frame_input, text=":الوصف").pack(side=tk.RIGHT, padx=(0, 5))
        self.pattern_entry = ttk.Entry(frame_input, width=15, font=("Segoe UI", 12), justify="right")
        self.pattern_entry.pack(side=tk.RIGHT, padx=5)
        ttk.Label(frame_input, text=":الوزن").pack(side=tk.RIGHT, padx=(0, 10))

        ttk.Label(self.tab_patterns, text="الأوزان النشطة", style="SubHeader.TLabel").pack(anchor="e", pady=(15, 5))

        frame_list = ttk.Frame(self.tab_patterns)
        frame_list.pack(fill="both", expand=True)

        self.patterns_tree = ttk.Treeview(frame_list, columns=("pattern", "description"),
                                          show="headings", height=8)
        self.patterns_tree.heading("pattern", text="الوزن")
        self.patterns_tree.heading("description", text="الوصف")
        self.patterns_tree.column("pattern", width=150, anchor="center")
        self.patterns_tree.column("description", width=300, anchor="center")
        self.patterns_tree.pack(side=tk.LEFT, fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame_list, orient="vertical", command=self.patterns_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.patterns_tree.config(yscrollcommand=scrollbar.set)

        btn_frame = ttk.Frame(self.tab_patterns)
        btn_frame.pack(pady=10, fill="x")
        ttk.Button(btn_frame, text="تحديث", command=self.refresh_patterns).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="حذف المحدد", command=self.delete_pattern,
                   style="Red.TButton").pack(side=tk.RIGHT, padx=5)

        self.refresh_patterns()

    ##
    # @brief Configure l'onglet de génération morphologique.
    #
    def setup_generator_tab(self):
        ttk.Label(self.tab_generator, text="المولّد الصرفي", style="Header.TLabel").pack(anchor="center",
                                                                                          pady=(10, 20))

        top_frame = ttk.Frame(self.tab_generator)
        top_frame.pack(fill="x", padx=20)

        root_frame = ttk.LabelFrame(top_frame, text="اختر الجذر", padding=10)
        root_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=(0, 10))

        self.gen_root_combo = ttk.Combobox(root_frame, width=20, font=("Segoe UI", 12),
                                           state="readonly", justify="right")
        self.gen_root_combo.pack(pady=5)

        pattern_frame = ttk.LabelFrame(top_frame, text="اختر الوزن / الأوزان", padding=10)
        pattern_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=(10, 0))

        self.gen_pattern_listbox = tk.Listbox(pattern_frame, selectmode=tk.MULTIPLE, font=("Segoe UI", 11),
                                              height=6, justify="right", bg="white",
                                              fg="#2c3e50", exportselection=False)
        self.gen_pattern_listbox.pack(fill="both", expand=True)

        btn_frame = ttk.Frame(self.tab_generator)
        btn_frame.pack(pady=15)

        ttk.Button(btn_frame, text="تحديث الخيارات", command=self.refresh_combos).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="توليد", command=self.generate_word,
                   style="Green.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="توليد العائلة الكاملة", command=self.generate_family).pack(side=tk.LEFT, padx=5)

        ttk.Label(self.tab_generator, text="النتائج", style="SubHeader.TLabel").pack(anchor="center", pady=(10, 5))

        result_frame = ttk.Frame(self.tab_generator)
        result_frame.pack(fill="both", expand=True, padx=20)

        self.gen_tree = ttk.Treeview(result_frame, columns=("root", "pattern", "word"),
                                     show="headings", height=8)
        self.gen_tree.heading("root", text="الجذر")
        self.gen_tree.heading("pattern", text="الوزن")
        self.gen_tree.heading("word", text="الكلمة المشتقة")
        self.gen_tree.column("root", width=120, anchor="center")
        self.gen_tree.column("pattern", width=150, anchor="center")
        self.gen_tree.column("word", width=200, anchor="center")
        self.gen_tree.pack(side=tk.LEFT, fill="both", expand=True)

        scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.gen_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.gen_tree.config(yscrollcommand=scrollbar.set)

        self.refresh_combos()

    ##
    # @brief Configure l'onglet de validation morphologique.
    #
    def setup_validator_tab(self):
        ttk.Label(self.tab_validator, text="التحقق الصرفي", style="Header.TLabel").pack(anchor="center",
                                                                                          pady=(20, 30))

        frame = ttk.Frame(self.tab_validator)
        frame.pack(anchor="center")

        ttk.Label(frame, text=":الكلمة للتحقق").grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.val_word_entry = ttk.Entry(frame, width=25, font=("Segoe UI", 11), justify="right")
        self.val_word_entry.grid(row=0, column=0, padx=10, pady=10)

        ttk.Label(frame, text=":الجذر المقابل").grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.val_root_entry = ttk.Entry(frame, width=25, font=("Segoe UI", 11), justify="right")
        self.val_root_entry.grid(row=1, column=0, padx=10, pady=10)

        btn_frame = ttk.Frame(self.tab_validator)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="تحقق", command=self.validate_word,
                   style="Green.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="تحليل الكلمة (بدون جذر)", command=self.decompose_word).pack(side=tk.LEFT, padx=5)

        self.val_result_label = ttk.Label(self.tab_validator, text="...في انتظار الإدخال",
                                          style="Result.TLabel", anchor="center")
        self.val_result_label.pack(fill="x", pady=20, padx=50)

    ##
    # @brief Configure l'onglet d'affichage des dérivés validés.
    #
    def setup_derived_tab(self):
        ttk.Label(self.tab_derived, text="المشتقات المسجلة", style="Header.TLabel").pack(anchor="center",
                                                                                           pady=(10, 20))

        select_frame = ttk.Frame(self.tab_derived)
        select_frame.pack(pady=10)

        ttk.Label(select_frame, text=":اختر الجذر").pack(side=tk.RIGHT, padx=10)
        self.derived_root_combo = ttk.Combobox(select_frame, width=20, font=("Segoe UI", 12),
                                                state="readonly", justify="right")
        self.derived_root_combo.pack(side=tk.RIGHT, padx=5)
        ttk.Button(select_frame, text="عرض", command=self.show_derived).pack(side=tk.RIGHT, padx=10)
        ttk.Button(select_frame, text="تحديث", command=self.refresh_derived_combo).pack(side=tk.RIGHT, padx=5)

        result_frame = ttk.Frame(self.tab_derived)
        result_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.derived_tree = ttk.Treeview(result_frame, columns=("word", "pattern", "frequency"),
                                          show="headings", height=10)
        self.derived_tree.heading("word", text="الكلمة")
        self.derived_tree.heading("pattern", text="الوزن")
        self.derived_tree.heading("frequency", text="التكرار")
        self.derived_tree.column("word", width=200, anchor="center")
        self.derived_tree.column("pattern", width=200, anchor="center")
        self.derived_tree.column("frequency", width=100, anchor="center")
        self.derived_tree.pack(side=tk.LEFT, fill="both", expand=True)

        scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.derived_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.derived_tree.config(yscrollcommand=scrollbar.set)

        self.refresh_derived_combo()

    ##
    # @brief Ajoute une nouvelle racine à l'AVL et au fichier texte.
    #
    def add_root(self):
        val = self.root_entry.get().strip()
        if len(val) != 3:
            messagebox.showerror("خطأ", "يجب أن يتكون الجذر من ٣ حروف بالضبط.")
            return
        if self.avl.search(val):
            messagebox.showinfo("تنبيه", f"الجذر '{val}' موجود مسبقاً.")
            return
        
        self.avl.insert(val)
        
        try:
            data_dir = "data"
            if not os.path.exists(data_dir):
                data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
            
            file_path = os.path.join(data_dir, "roots.txt")
            
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(f"{val}\n")
        except Exception as e:
            print(f"Error saving to file: {e}")

        self.root_entry.delete(0, tk.END)
        self.refresh_roots()
        self.refresh_combos()
        self.refresh_derived_combo()
        messagebox.showinfo("نجاح", f"تمت إضافة الجذر '{val}' بنجاح.")

    ##
    # @brief Recherche une racine choisie par l'utilisateur.
    #
    def search_root(self):
        val = self.search_root_entry.get().strip()
        if not val:
            return
        node = self.avl.search(val)
        if node:
            count = len(node.value)
            self.search_result_label.config(
                text=f" الجذر '{val}' موجود — {count} مشتق(ات) مسجلة",
                style="Valid.TLabel"
            )
        else:
            self.search_result_label.config(
                text=f" الجذر '{val}' غير موجود في الشجرة",
                style="Invalid.TLabel"
            )

    ##
    # @brief Actualise la liste des racines affichées.
    #
    def refresh_roots(self):
        self.roots_listbox.delete(0, tk.END)
        roots = self.avl.get_inorder()
        for r in roots:
            node = self.avl.search(r)
            count = len(node.value) if node else 0
            self.roots_listbox.insert(tk.END, f"{r}  ({count} مشتقات)")

    ##
    # @brief Affiche les dérivés d'une racine sélectionnée dans l'onglet dédié.
    #
    def show_root_derivatives(self):
        selection = self.roots_listbox.curselection()
        if not selection:
            messagebox.showwarning("تنبيه", "يرجى اختيار جذر من القائمة.")
            return
        text = self.roots_listbox.get(selection[0])
        root_val = text.split()[0].strip()

        self.derived_root_combo.set(root_val)
        self.show_derived()
        self.tab_control.select(self.tab_derived)

    ##
    # @brief Ajoute un nouveau schème à la table de hachage.
    #
    def add_pattern(self):
        val = self.pattern_entry.get().strip()
        desc = self.pattern_desc_entry.get().strip()
        if not val:
            messagebox.showerror("خطأ", "يرجى إدخال الوزن.")
            return
        if not desc:
            desc = val
        self.hashtable.insert(val, desc)
        self.pattern_entry.delete(0, tk.END)
        self.pattern_desc_entry.delete(0, tk.END)
        self.refresh_patterns()
        self.refresh_combos()
        messagebox.showinfo("نجاح", f"تمت إضافة الوزن '{val}' بنجاح.")

    ##
    # @brief Supprime le schème sélectionné.
    #
    def delete_pattern(self):
        selected = self.patterns_tree.selection()
        if not selected:
            messagebox.showwarning("تنبيه", "يرجى اختيار وزن من القائمة.")
            return
        item = self.patterns_tree.item(selected[0])
        pattern_key = item["values"][0]
        if messagebox.askyesno("تأكيد الحذف", f"هل تريد حذف الوزن '{pattern_key}'?"):
            self.hashtable.delete(pattern_key)
            self.refresh_patterns()
            self.refresh_combos()

    ##
    # @brief Actualise l'affichage des schèmes.
    #
    def refresh_patterns(self):
        for item in self.patterns_tree.get_children():
            self.patterns_tree.delete(item)
        patterns = self.hashtable.get_all()
        for key, value in patterns:
            self.patterns_tree.insert("", tk.END, values=(key, value))

    ##
    # @brief Actualise les listes déroulantes de choix (racines, schèmes).
    #
    def refresh_combos(self):
        roots = self.avl.get_inorder()
        self.gen_root_combo['values'] = roots

        self.gen_pattern_listbox.delete(0, tk.END)
        patterns = self.hashtable.get_all()
        for key, value in patterns:
            self.gen_pattern_listbox.insert(tk.END, key)

    ##
    # @brief Génère des mots dérivés pour les schèmes sélectionnés.
    #
    def generate_word(self):
        root_val = self.gen_root_combo.get()
        if not root_val:
            messagebox.showwarning("تنبيه", "يرجى اختيار الجذر.")
            return

        selected_indices = self.gen_pattern_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("تنبيه", "يرجى اختيار وزن واحد على الأقل.")
            return

        selected_patterns = [self.gen_pattern_listbox.get(i) for i in selected_indices]
        results = self.morph_engine.generate_multiple(root_val, selected_patterns)

        for item in self.gen_tree.get_children():
            self.gen_tree.delete(item)

        for pattern, word in results:
            self.gen_tree.insert("", tk.END, values=(root_val, pattern, word))
            self.avl.add_derived(root_val, word, pattern)

    ##
    # @brief Génère tous les dérivés possibles pour une racine.
    #
    def generate_family(self):
        root_val = self.gen_root_combo.get()
        if not root_val:
            messagebox.showwarning("تنبيه", "يرجى اختيار الجذر.")
            return

        all_patterns = [k for k, v in self.hashtable.get_all()]
        family = self.morph_engine.generate_family(root_val, all_patterns)

        for item in self.gen_tree.get_children():
            self.gen_tree.delete(item)

        for root_str, pattern, word in family:
            self.gen_tree.insert("", tk.END, values=(root_str, pattern, word))
            self.avl.add_derived(root_val, word, pattern)

    ##
    # @brief Valide si un mot correspond à une racine et un schème.
    #
    def validate_word(self):
        word = self.val_word_entry.get().strip()
        root_val = self.val_root_entry.get().strip()

        if not word or not root_val:
            messagebox.showwarning("تنبيه", "يرجى إدخال الكلمة والجذر.")
            return

        if not self.avl.search(root_val):
            self.val_result_label.config(
                text=f" لا — الجذر '{root_val}' غير موجود في القاموس",
                style="Invalid.TLabel"
            )
            return

        patterns = [k for k, v in self.hashtable.get_all()]
        is_valid, matched_pattern = self.morph_engine.validate(word, root_val, patterns)

        if is_valid:
            self.val_result_label.config(
                text=f"نعم — الكلمة '{word}' مشتقة من الجذر '{root_val}' على وزن '{matched_pattern}'",
                style="Valid.TLabel"
            )
            self.avl.add_derived(root_val, word, matched_pattern)
        else:
            self.val_result_label.config(
                text=f"لا — الكلمة '{word}' لا تنتمي إلى الجذر '{root_val}'",
                style="Invalid.TLabel"
            )

    ##
    # @brief Analyse un mot pour extraire sa racine et son schème.
    #
    def decompose_word(self):
        word = self.val_word_entry.get().strip()
        if not word:
            messagebox.showwarning("تنبيه", "يرجى إدخال الكلمة.")
            return

        all_roots = self.avl.get_inorder()
        all_patterns = [k for k, v in self.hashtable.get_all()]

        found_root, found_pattern = self.morph_engine.decompose(word, all_roots, all_patterns)

        if found_root:
            self.val_result_label.config(
                text=f" تحليل: '{word}' = الجذر '{found_root}' + الوزن '{found_pattern}'",
                style="Valid.TLabel"
            )
            self.avl.add_derived(found_root, word, found_pattern)
        else:
            self.val_result_label.config(
                text=f" لم يتم التعرف على الكلمة '{word}' في أي جذر معروف",
                style="Invalid.TLabel"
            )

    ##
    # @brief Actualise la liste déroulante des dérivés.
    #
    def refresh_derived_combo(self):
        roots = self.avl.get_inorder()
        self.derived_root_combo['values'] = roots

    ##
    # @brief Affiche les dérivés enregistrés pour la racine sélectionnée.
    #
    def show_derived(self):
        root_val = self.derived_root_combo.get()
        if not root_val:
            messagebox.showwarning("تنبيه", "يرجى اختيار الجذر.")
            return

        for item in self.derived_tree.get_children():
            self.derived_tree.delete(item)

        derivatives = self.avl.get_derived(root_val)
        if not derivatives:
            self.derived_tree.insert("", tk.END, values=("لا توجد مشتقات", "—", "—"))
            return

        for entry in derivatives:
            self.derived_tree.insert("", tk.END,
                                     values=(entry["word"], entry["pattern"], entry["frequency"]))

if __name__ == "__main__":
    root = tk.Tk()
    app = MorphApp(root)
    root.mainloop()
