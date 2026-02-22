## @file main.py
#  @brief Point d'entrée de l'application Flet pour le moteur morphologique.
#  Gère l'interface graphique, les événements utilisateur et le rendu dynamique.

import flet as ft
import flet.canvas as cv
import time
import bisect
from logic.morphology import MorphologicalEngine

## @var C Palette de couleurs utilisée pour le thème "Dark Modern" de l'application.
C = {
    "bg":       "#0F1923",
    "card":     "#1A2735",
    "input":    "#0D1620",
    "accent":   "#00BFA6",
    "accent2":  "#64FFDA",
    "t1":       "#E0E0E0",
    "t2":       "#90A4AE",
    "border":   "#263545",
    "err":      "#FF5252",
    "ok":       "#69F0AE",
    "warn":     "#FFD740",
    "hover":    "#1A3035",
    "badge":    "#0D2520",
    "btn_t":    "#0F1923",
    "line":     "#00BFA6",
}

## @var ROW_H Hauteur fixe des lignes pour l'optimisation du rendu des ListView.
ROW_H = 36 


def main(page: ft.Page):
    """
    @brief Fonction principale initialisant l'interface utilisateur Flet.
    @param page Objet page de Flet représentant la fenêtre de l'application.
    """
    page.title = "محرك التحليل الصرفي العربي"
    page.rtl = True # Activation du support de droite à gauche pour l'Arabe
    page.padding = 0
    page.bgcolor = C["bg"]
    page.window.maximized = True

    # Initialisation du moteur morphologique
    engine = MorphologicalEngine()

    # ── Helpers UI ───────────────────────────────────────────
    
    def card(content, **kw):
        """
        @brief Crée un conteneur stylisé en forme de carte.
        @param content Le contenu à afficher dans la carte.
        @return Un objet Container avec bordures et ombres.
        """
        return ft.Container(
            content=content, bgcolor=C["card"],
            border_radius=16, border=ft.border.all(1, C["border"]),
            padding=25, **kw,
        )

    def inp(label, hint="", **kw):
        """@brief Crée un champ de saisie de texte (TextField) stylisé."""
        return ft.TextField(
            label=label, hint_text=hint, text_align=ft.TextAlign.RIGHT,
            label_style=ft.TextStyle(color=C["t2"]),
            text_style=ft.TextStyle(color=C["t1"], size=16),
            border_color=C["border"], focused_border_color=C["accent"],
            cursor_color=C["accent"], bgcolor=C["input"],
            border_radius=12, **kw,
        )

    def btn(text, on_click, primary=True):
        """@brief Crée un bouton interactif stylisé avec effet hover."""
        if primary:
            return ft.Container(
                content=ft.Text(text, size=14, weight=ft.FontWeight.W_600, color=C["btn_t"]),
                bgcolor=C["accent"], border_radius=12,
                padding=ft.padding.symmetric(horizontal=20, vertical=12),
                on_click=on_click,
                on_hover=lambda e: _h(e, C["accent2"], C["accent"]),
            )
        return ft.Container(
            content=ft.Text(text, size=14, weight=ft.FontWeight.W_500, color=C["accent"]),
            border=ft.border.all(1, C["accent"]), border_radius=12,
            padding=ft.padding.symmetric(horizontal=20, vertical=12),
            on_click=on_click,
            on_hover=lambda e: _h(e, C["hover"], "transparent"),
        )

    def _h(e, on, off):
        """@brief Gestionnaire interne pour les effets de survol (hover)."""
        e.control.bgcolor = on if e.data == "true" else off
        e.control.update()

    # ── Barre d'État / Sortie ────────────────────────────────
    o_icon = ft.Text("💡", size=22)
    o_main = ft.Text("جاهز...", size=16, color=C["t2"], selectable=True)
    o_sub = ft.Text("", size=13, color=C["t2"], selectable=True)
    out_bar = ft.Container(
        content=ft.Row([o_icon, ft.Column([o_main, o_sub], spacing=2)], spacing=15),
        bgcolor=C["card"], border=ft.border.all(1, C["border"]),
        border_radius=14, padding=20,
    )

    def msg(i, m, s, c, flush=True):
        """
        @brief Affiche un message dans la barre d'état.
        @param i Icône (emoji).
        @param m Message principal.
        @param s Sous-message (ex: temps de calcul).
        @param c Couleur du texte.
        @param flush Mise à jour immédiate de l'interface si True.
        """
        o_icon.value = i; o_main.value = m; o_main.color = c
        o_sub.value = s
        if flush:
            out_bar.update()

    # Cache des clés triées pour éviter les parcours répétés
    root_keys = [n.key for n in engine.roots_tree.inorder_traversal()]

    # ═════════════════════════════════════════════════════════
    # TAB 1 — المولد
    # ═════════════════════════════════════════════════════════
    gen_root = inp("الجذر", "مثال: كتب")
    gen_pat = ft.Dropdown(
        label="الوزن", options=[],
        label_style=ft.TextStyle(color=C["t2"]),
        text_style=ft.TextStyle(color=C["t1"]),
        border_color=C["border"], bgcolor=C["input"], border_radius=12,
    )
    gen_results = ft.ListView(expand=True, spacing=4, item_extent=ROW_H)

    def refresh_gen_pats():
        """@brief Met à jour la liste des schèmes dans le menu déroulant du générateur."""
        gen_pat.options = [
            ft.dropdown.Option(k, f"{k} ({v['type']})") for k, v in engine.get_all_patterns()
        ]

    def on_gen(e):
        """@brief Gère la génération d'un mot unique à partir d'une racine et d'un schème."""
        if not gen_root.value:
            msg("⚠️", "أدخل جذراً", "", C["warn"]); return
        if not gen_pat.value:
            msg("⚠️", "اختر وزناً", "", C["warn"]); return
        t0 = time.perf_counter()
        res = engine.generate(gen_root.value, gen_pat.value)
        dt = (time.perf_counter() - t0) * 1000
        if "خطأ" in res:
            msg("❌", res, f"({dt:.0f} ms)", C["err"])
        else:
            p = engine.patterns_table.get(gen_pat.value)
            msg("✅", res, f"{gen_root.value} + {gen_pat.value} ({p['type']}) — {dt:.0f} ms", C["ok"], flush=False)
            rn = engine.get_root_node(gen_root.value)
            if rn:
                rn.add_derived_word(res)
                engine.save_roots_meta()
                refresh_roots()
                roots_lv.update()
            out_bar.update()

    def on_gen_all(e):
        """@brief Génère toutes les formes possibles pour le radical saisi."""
        if not gen_root.value:
            msg("⚠️", "أدخل جذراً", "", C["warn"]); return
        t0 = time.perf_counter()
        results = engine.generate_all(gen_root.value)
        gen_results.controls = [
            ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Text(w, size=16, weight="bold", color=C["accent2"], selectable=True),
                        bgcolor=C["badge"], border_radius=6,
                        padding=ft.padding.symmetric(horizontal=10, vertical=2),
                    ),
                    ft.Text(f"{p}", size=13, weight="bold", color=C["t1"]),
                    ft.Text(f"({t})", size=12, color=C["t2"]),
                ], spacing=8),
                padding=ft.padding.only(left=8, right=28, top=4, bottom=4),
                border=ft.border.only(bottom=ft.BorderSide(1, C["border"])),
                height=ROW_H,
            ) for w, p, t in results
        ]
        
        rn = engine.get_root_node(gen_root.value)
        if rn:
            for w, _, _ in results:
                rn.add_derived_word(w)
            engine.save_roots_meta()
            refresh_roots()
            roots_lv.update()

        dt = (time.perf_counter() - t0) * 1000
        msg("✅", f"تم توليد {len(results)} كلمة من '{gen_root.value}'", f"{dt:.0f} ms", C["ok"], flush=False)
        out_bar.update()
        gen_results.update()

    gen_card = card(ft.Column([
        ft.Text("مولد الكلمات", size=20, weight="bold", color=C["t1"]),
        ft.Text("أدخل جذراً واختر وزناً أو ولّد جميع الاشتقاقات", size=13, color=C["t2"]),
        ft.Divider(color=C["border"]),
        gen_root, gen_pat,
        ft.Row([btn("توليد كلمة", on_gen), btn("توليد الكل", on_gen_all, primary=False)]),
        ft.Divider(color=C["border"]),
        gen_results,
    ], spacing=8, expand=True), expand=True)

    # ═════════════════════════════════════════════════════════
    # TAB 2 — المدقق
    # ═════════════════════════════════════════════════════════
    val_w = inp("الكلمة", "مثال: كاتب")
    val_r = inp("الجذر", "مثال: كتب")

    def on_val(e):
        """@brief Gère la validation de la dérivation d'un mot par rapport à un radical."""
        if not val_w.value or not val_r.value:
            msg("⚠️", "أدخل الكلمة والجذر", "", C["warn"]); return
        t0 = time.perf_counter()
        ok, k = engine.validate(val_w.value, val_r.value)
        dt = (time.perf_counter() - t0) * 1000
        if ok:
            p = engine.patterns_table.get(k)
            rn = engine.get_root_node(val_r.value)
            if rn:
                rn.add_derived_word(val_w.value)
                engine.save_roots_meta()
                refresh_roots()
                roots_lv.update()
            msg("✅", f"'{val_w.value}' مشتقة من '{val_r.value}'",
                f"الوزن: {k} ({p['type']}) — {dt:.0f} ms", C["ok"], flush=False)
            out_bar.update()
        else:
            msg("❌", f"'{val_w.value}' ليست مشتقة من '{val_r.value}'",
                f"لا يوجد وزن مطابق — {dt:.0f} ms", C["err"])

    val_card = card(ft.Column([
        ft.Text("المدقق", size=20, weight="bold", color=C["t1"]),
        ft.Text("تحقق من صحة اشتقاق كلمة من جذر", size=13, color=C["t2"]),
        ft.Divider(color=C["border"]),
        val_w, val_r,
        btn("تحقق", on_val),
    ], spacing=8))

    # ═════════════════════════════════════════════════════════
    # TAB 3 — الجذور  (incremental updates)
    # ═════════════════════════════════════════════════════════
    roots_inp = inp("جذر جديد", "3 أحرف")
    roots_lv = ft.ListView(expand=True, spacing=4, item_extent=ROW_H)

    def on_view_root(key):
        """@brief Affiche une boîte de dialogue avec la liste des dérivés confirmés pour une racine."""
        n = engine.roots_tree.search(key)
        if not n: return
        dw = n.value.derived_words if n and n.value else []
        freqs = n.value.frequencies if n and n.value else {}
        if not dw:
            msg("⚠️", "لا توجد مشتقات", "", C["warn"]); return
        
        lv = ft.ListView(expand=True, spacing=8)
        for w in dw:
            freq = freqs.get(w, 0)
            lv.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Container(
                            content=ft.Text(w, size=16, weight="bold", color=C["accent2"], selectable=True),
                            bgcolor=C["badge"], border_radius=6,
                            padding=ft.padding.symmetric(horizontal=10, vertical=2),
                        ),
                        ft.Text(f"التكرار: {freq}", size=13, color=C["t2"]),
                    ], spacing=10, rtl=True),
                    padding=ft.padding.only(bottom=8),
                    border=ft.border.only(bottom=ft.BorderSide(1, C["border"])),
                )
            )
            
        def close_dlg(e):
            """@brief Ferme la boîte de dialogue des dérivés."""
            if hasattr(page, "close"):
                page.close(dlg)
            else:
                dlg.open = False
                page.update()

        dlg = ft.AlertDialog(
            title=ft.Text(f"المشتقات المؤكدة للجذر: {key}", color=C["accent"], text_align=ft.TextAlign.RIGHT),
            content=ft.Container(lv, width=300, height=400, rtl=True),
            actions=[ft.TextButton("إغلاق", on_click=close_dlg)],
            bgcolor=C["card"],
            open=True,
        )
        if hasattr(page, "open"):
            page.open(dlg)
        else:
            page.overlay.append(dlg)
            page.update()

    def on_del_root_derivatives(key):
        n = engine.roots_tree.search(key)
        if not n or not n.value: return
        n.value.derived_words.clear()
        n.value.frequencies.clear()
        engine.save_roots_meta()
        
        # In-place UI update for smooth UX
        for c in roots_lv.controls:
            if c.data == key:
                # Update the text showing derivative count
                row_controls = c.content.controls
                row_controls[1].value = ""
                break
        roots_lv.update()
        msg("✅", f"تم حذف مشتقات '{key}'", "", C["ok"])

    def _make_root_row(key):
        n = engine.roots_tree.search(key)
        dw = n.value.derived_words if n and n.value else []
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Text(key, size=16, weight="bold", color=C["accent2"]),
                    bgcolor=C["badge"], border_radius=6,
                    padding=ft.padding.symmetric(horizontal=12, vertical=2),
                ),
                ft.Text(
                    f"{len(dw)} مشتقات" if dw else "",
                    size=11, color=C["t2"], expand=True,
                ),
                ft.Container(
                    content=ft.Text("👁️", size=14, color=C["accent"]),
                    on_click=lambda e, r=key: on_view_root(r),
                    padding=6, border_radius=6,
                    on_hover=lambda e: _h(e, C["hover"], "transparent"),
                    tooltip="عرض المشتقات",
                ),
                ft.Container(
                    content=ft.Text("🧹", size=14, color=C["warn"]),
                    on_click=lambda e, r=key: on_del_root_derivatives(r),
                    padding=6, border_radius=6,
                    on_hover=lambda e: _h(e, C["hover"], "transparent"),
                    tooltip="حذف المشتقات",
                ),
                ft.Container(
                    content=ft.Text("✕", size=14, color=C["err"]),
                    on_click=lambda e, r=key: on_del_root(r),
                    padding=6, border_radius=6,
                    on_hover=lambda e: _h(e, C["hover"], "transparent"),
                    tooltip="حذف الجذر",
                ),
            ], spacing=8),
            padding=ft.padding.only(left=8, right=28, top=4, bottom=4),
            border=ft.border.only(bottom=ft.BorderSide(1, C["border"])),
            height=ROW_H, data=key,
        )

    def refresh_roots():
        root_keys.clear()
        root_keys.extend(n.key for n in engine.roots_tree.inorder_traversal())
        roots_lv.controls = [_make_root_row(k) for k in root_keys]

    def on_del_root(root):
        t0 = time.perf_counter()
        if engine.delete_root(root):
            idx = -1
            for i, c in enumerate(roots_lv.controls):
                if c.data == root:
                    idx = i; break
            if idx >= 0:
                roots_lv.controls.pop(idx)
            if root in root_keys:
                root_keys.remove(root)
            dt = (time.perf_counter() - t0) * 1000
            msg("✅", f"تم حذف '{root}'", f"{dt:.0f} ms", C["ok"], flush=False)
            out_bar.update()
            roots_lv.update()

    def on_del_all_derivatives(e):
        for key in root_keys:
            n = engine.roots_tree.search(key)
            if n and n.value:
                n.value.derived_words.clear()
                n.value.frequencies.clear()
        engine.save_roots_meta()
        refresh_roots()
        roots_lv.update()
        msg("✅", "تم حذف جميع المشتقات لجميع الجذور", "", C["ok"])

    def on_add_root(e):
        r = roots_inp.value.strip() if roots_inp.value else ""
        if len(r) != 3:
            msg("⚠️", "الجذر يجب أن يكون 3 أحرف", "", C["warn"]); return
        t0 = time.perf_counter()
        if engine.add_root(r):
            roots_inp.value = ""
            idx = bisect.bisect_left(root_keys, r)
            root_keys.insert(idx, r)
            roots_lv.controls.insert(idx, _make_root_row(r))
            dt = (time.perf_counter() - t0) * 1000
            msg("✅", f"تم إضافة '{r}'", f"{dt:.0f} ms — إجمالي: {len(root_keys)}", C["ok"], flush=False)
            out_bar.update()
            roots_inp.update()
            roots_lv.update()
        else:
            dt = (time.perf_counter() - t0) * 1000
            msg("⚠️", f"'{r}' موجود", f"{dt:.0f} ms", C["warn"])

    roots_card = card(ft.Column([
        ft.Row([
            ft.Text("إدارة الجذور", size=20, weight="bold", color=C["t1"], expand=True),
            btn("حذف كل المشتقات 🧹", on_del_all_derivatives, primary=False)
        ]),
        ft.Divider(color=C["border"]),
        ft.Row([roots_inp, btn("إضافة", on_add_root)], spacing=8),
        ft.Divider(color=C["border"]),
        roots_lv,
    ], spacing=8, expand=True), expand=True)

    # ═════════════════════════════════════════════════════════
    # TAB 4 — الأوزان (incremental CRUD)
    # ═════════════════════════════════════════════════════════
    pat_k = inp("الوزن", "مثال: مفعال")
    pat_t = inp("النوع", "مثال: اسم آلة")
    pats_lv = ft.ListView(expand=True, spacing=4, item_extent=ROW_H)

    pat_keys = []  # sorted cache

    def _make_pat_row(pk, ptype):
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Text(pk, size=16, weight="bold", color=C["accent2"]),
                    bgcolor=C["badge"], border_radius=6,
                    padding=ft.padding.symmetric(horizontal=10, vertical=2),
                ),
                ft.Text(ptype, size=12, color=C["t1"], expand=True),
                ft.Container(
                    content=ft.Text("✕", size=14, color=C["err"]),
                    on_click=lambda e, k=pk: on_del_pat(k),
                    padding=6, border_radius=6,
                    on_hover=lambda e: _h(e, C["hover"], "transparent"),
                ),
            ], spacing=8),
            padding=ft.padding.only(left=8, right=28, top=4, bottom=4),
            border=ft.border.only(bottom=ft.BorderSide(1, C["border"])),
            height=ROW_H, data=pk,
        )

    def refresh_pats():
        """@brief Recharge et trie tous les schèmes morphologiques dans la vue de gestion."""
        pat_keys.clear()
        all_p = engine.get_all_patterns()
        pat_keys.extend(k for k, _ in all_p)
        pats_lv.controls = [_make_pat_row(k, v["type"]) for k, v in all_p]

    def on_add_pat(e):
        """@brief Gère l'ajout ou la mise à jour d'un schème (template + type)."""
        pk = pat_k.value.strip() if pat_k.value else ""
        pt = pat_t.value.strip() if pat_t.value else ""
        if not pk or not pt:
            msg("❌", "أدخل الوزن والنوع", "", C["err"]); return
        t0 = time.perf_counter()
        if engine.add_pattern(pk, pt):
            pat_k.value = ""; pat_t.value = ""
            # Mise à jour incrémentale de la liste UI
            for i, c in enumerate(pats_lv.controls):
                if c.data == pk:
                    pats_lv.controls.pop(i)
                    pat_keys.remove(pk)
                    break
            idx = bisect.bisect_left(pat_keys, pk)
            pat_keys.insert(idx, pk)
            pats_lv.controls.insert(idx, _make_pat_row(pk, pt))
            refresh_gen_pats()
            dt = (time.perf_counter() - t0) * 1000
            msg("✅", f"تم إضافة/تعديل '{pk}'", f"{dt:.0f} ms", C["ok"], flush=False)
            out_bar.update()
            pat_k.update(); pat_t.update()
            pats_lv.update()
            gen_pat.update()

    def on_del_pat(key):
        """@brief Gère la suppression d'un schème morphologique."""
        t0 = time.perf_counter()
        if engine.delete_pattern(key):
            for i, c in enumerate(pats_lv.controls):
                if c.data == key:
                    pats_lv.controls.pop(i); break
            if key in pat_keys:
                pat_keys.remove(key)
            refresh_gen_pats()
            dt = (time.perf_counter() - t0) * 1000
            msg("✅", f"تم حذف '{key}'", f"{dt:.0f} ms", C["ok"], flush=False)
            out_bar.update()
            pats_lv.update()
            gen_pat.update()

    pats_card = card(ft.Column([
        ft.Text("إدارة الأوزان", size=20, weight="bold", color=C["t1"]),
        ft.Divider(color=C["border"]),
        pat_k, pat_t,
        btn("إضافة / تعديل", on_add_pat),
        ft.Divider(color=C["border"]),
        pats_lv,
    ], spacing=8, expand=True), expand=True)

    # TAB 5 — شجرة AVL
    # ═════════════════════════════════════════════════════════
    NODE_W, NODE_H = 80, 50
    H_GAP, V_GAP = 10, 50

    avl_stack = ft.Stack()
    avl_root_inp = inp("جذر جديد", "3 أحرف")

    def refresh_avl():
        """@brief Calcule et rend graphiquement l'arbre AVL sur un canevas Flet."""
        t0 = time.perf_counter()
        tr = engine.roots_tree.root
        if not tr:
            avl_stack.controls = [ft.Text("الشجرة فارغة", color=C["t2"])]
            avl_stack.width = None; avl_stack.height = None
            return

        positions = {}
        edges = []
        counter = [0]

        def walk(n, d):
            if not n: return
            walk(n.left, d + 1)
            x = counter[0] * (NODE_W + H_GAP) + 20
            y = d * (NODE_H + V_GAP) + 20
            positions[id(n)] = (x, y, n)
            counter[0] += 1
            walk(n.right, d + 1)

        def walk_edges(n):
            if not n: return
            if n.left:
                edges.append((id(n), id(n.left))); walk_edges(n.left)
            if n.right:
                edges.append((id(n), id(n.right))); walk_edges(n.right)

        walk(tr, 0); walk_edges(tr)

        cw = max(x for x, _, _ in positions.values()) + NODE_W + 30
        ch = max(y for _, y, _ in positions.values()) + NODE_H + 30

        shapes = []
        for pid, cid in edges:
            px, py, _ = positions[pid]
            cx, cy, _ = positions[cid]
            shapes.append(cv.Line(
                px + NODE_W / 2, py + NODE_H,
                cx + NODE_W / 2, cy,
                paint=ft.Paint(color=C["line"], stroke_width=1.5),
            ))

        avl_stack.width = cw
        avl_stack.height = ch
        avl_stack.controls = [cv.Canvas(shapes, width=cw, height=ch)]

        for _, (x, y, n) in positions.items():
            b = engine.roots_tree._balance_factor(n)
            avl_stack.controls.append(ft.Container(
                content=ft.Column([
                    ft.Text(n.key, size=16, weight="bold", color=C["accent2"]),
                    ft.Text(f"b={b}", size=12, color=C["t2"]),
                ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER),
                bgcolor=C["card"], border=ft.border.all(1, C["accent"]),
                border_radius=5, width=NODE_W, height=NODE_H,
                left=x, top=y, alignment=ft.Alignment(0, 0),
            ))
        dt = (time.perf_counter() - t0) * 1000
        print(f"[AVL] Render: {dt:.0f} ms ({len(positions)} nodes)")

    def on_avl_add(e):
        r = avl_root_inp.value.strip() if avl_root_inp.value else ""
        if len(r) != 3:
            msg("⚠️", "3 أحرف فقط", "", C["warn"]); return
        t0 = time.perf_counter()
        if engine.add_root(r):
            avl_root_inp.value = ""
            idx = bisect.bisect_left(root_keys, r)
            root_keys.insert(idx, r)
            refresh_avl()
            dt = (time.perf_counter() - t0) * 1000
            msg("✅", f"تم إضافة '{r}'", f"{dt:.0f} ms", C["ok"])
        else:
            msg("⚠️", f"'{r}' موجود", "", C["warn"]); return
        avl_root_inp.update()
        out_bar.update()
        avl_stack.update()

    avl_card = card(ft.Column([
        ft.Row([
            ft.Text("شجرة AVL", size=20, weight="bold", color=C["t1"]),
            ft.Text(f"(h=ارتفاع, b=توازن)", size=11, color=C["t2"]),
        ], spacing=10),
        ft.Row([avl_root_inp, btn("إضافة", on_avl_add)], spacing=5),
        ft.Divider(color=C["border"]),
        ft.Container(
            content=ft.Column(
                [ft.Row([avl_stack], scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.CENTER)],
                scroll=ft.ScrollMode.AUTO, expand=True, alignment=ft.MainAxisAlignment.START,
            ),
            expand=True, bgcolor=C["bg"], border_radius=10, padding=20,
        ),
    ], spacing=6, expand=True), expand=True)

    # ═════════════════════════════════════════════════════════
    # TAB 6 — جدول التجزئة
    # ═════════════════════════════════════════════════════════
    hash_lv = ft.ListView(expand=True, spacing=3)

    def refresh_hash():
        """@brief Visualise la structure interne de la table de hachage (Buckets & Chaînage)."""
        ht = engine.patterns_table
        hash_lv.controls = []

        # Statistiques de la table
        occupied = sum(1 for b in ht.table if b)
        collisions = sum(1 for b in ht.table if len(b) > 1)
        total = sum(len(b) for b in ht.table)

        hash_lv.controls.append(ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Text(f"حجم: {ht.size}", size=12, color=C["accent2"]),
                    bgcolor=C["badge"], border_radius=8,
                    padding=ft.padding.symmetric(horizontal=10, vertical=4),
                ),
                ft.Container(
                    content=ft.Text(f"مشغول: {occupied}", size=12, color=C["t1"]),
                    bgcolor=C["badge"], border_radius=8,
                    padding=ft.padding.symmetric(horizontal=10, vertical=4),
                ),
                ft.Container(
                    content=ft.Text(f"تصادم: {collisions}", size=12,
                                    color=C["err"] if collisions else C["ok"]),
                    bgcolor=C["badge"], border_radius=8,
                    padding=ft.padding.symmetric(horizontal=10, vertical=4),
                ),
                ft.Container(
                    content=ft.Text(f"عناصر: {total}", size=12, color=C["t1"]),
                    bgcolor=C["badge"], border_radius=8,
                    padding=ft.padding.symmetric(horizontal=10, vertical=4),
                ),
            ], spacing=8),
            padding=ft.padding.only(bottom=8),
        ))

        for idx, bucket in enumerate(ht.table):
            if not bucket:
                continue
            items = [
                ft.Container(
                    content=ft.Text(f"[{idx}]", size=12, weight="bold", color=C["accent"]),
                    bgcolor=C["badge"], border_radius=6, width=45,
                    padding=ft.padding.symmetric(horizontal=6, vertical=3),
                    alignment=ft.Alignment(0, 0),
                ),
                ft.Text("→", size=13, color=C["t2"]),
            ]
            for i, (k, v) in enumerate(bucket):
                items.append(ft.Container(
                    content=ft.Row([
                        ft.Text(k, size=12, weight="bold", color=C["accent2"]),
                        ft.Text(f"({v['type'][:15]})", size=10, color=C["t2"]),
                    ], spacing=4),
                    bgcolor=C["card"], border=ft.border.all(1, C["border"]),
                    border_radius=6, padding=ft.padding.symmetric(horizontal=8, vertical=4),
                ))
                if i < len(bucket) - 1:
                    items.append(ft.Text("→", size=11, color=C["line"]))

            hash_lv.controls.append(ft.Container(
                content=ft.Row(items, spacing=6),
                padding=ft.padding.symmetric(horizontal=4, vertical=3),
                border=ft.border.only(bottom=ft.BorderSide(1, C["border"])),
            ))

    hash_card = card(ft.Column([
        ft.Text("جدول التجزئة", size=20, weight="bold", color=C["t1"]),
        ft.Text("بنية التجزئة مع سلاسل التصادم (Chaining)", size=13, color=C["t2"]),
        ft.Divider(color=C["border"]),
        hash_lv,
    ], spacing=6, expand=True), expand=True)

    # ═════════════════════════════════════════════════════════
    # TABS
    # ═════════════════════════════════════════════════════════
    body = ft.Tabs(
        selected_index=0, length=6, expand=True,
        content=ft.Column(expand=True, controls=[
            ft.Container(
                content=ft.TabBar(
                    tabs=[
                        ft.Tab(label="المولد", icon=ft.Icons.EDIT_NOTE),
                        ft.Tab(label="المدقق", icon=ft.Icons.VERIFIED),
                        ft.Tab(label="الجذور", icon=ft.Icons.PARK),
                        ft.Tab(label="الأوزان", icon=ft.Icons.VIEW_LIST),
                        ft.Tab(label="شجرة AVL", icon=ft.Icons.ACCOUNT_TREE),
                        ft.Tab(label="جدول Hash", icon=ft.Icons.GRID_VIEW),
                    ],
                    indicator_color=C["accent"],
                    label_color=C["accent2"],
                    unselected_label_color=C["t2"],
                    divider_color=C["border"],
                ),
                alignment=ft.Alignment(0, 0),
            ),
            ft.TabBarView(expand=True, controls=[
                ft.Container(content=gen_card, padding=10, expand=True),
                ft.Container(content=val_card, padding=10),
                ft.Container(content=roots_card, padding=10, expand=True),
                ft.Container(content=pats_card, padding=10, expand=True),
                ft.Container(content=avl_card, padding=10, expand=True),
                ft.Container(content=hash_card, padding=10, expand=True),
            ]),
        ]),
    )

    # ── Full Refresh ─────────────────────────────────────────
    def on_refresh(e):
        """@brief Recharge toutes les données depuis le disque et met à jour l'UI."""
        t0 = time.perf_counter()
        engine.check_for_updates()
        refresh_gen_pats(); refresh_pats(); refresh_roots()
        refresh_avl(); refresh_hash()
        dt = (time.perf_counter() - t0) * 1000
        msg("✅", "تم التحديث", f"{dt:.0f} ms", C["ok"])
        page.update()

    # ── Initial Renders ──────────────────────────────────────
    t_init = time.perf_counter()
    refresh_gen_pats(); refresh_pats(); refresh_roots(); refresh_hash(); refresh_avl()
    print(f"[INIT] Startup render: {(time.perf_counter() - t_init) * 1000:.0f} ms")

    # ── Header ───────────────────────────────────────────────
    header = ft.Container(
        content=ft.Row([
            ft.Container(
                content=ft.Icon(ft.Icons.REFRESH, color=C["accent"], size=20),
                on_click=on_refresh, border_radius=8, padding=8,
                bgcolor=C["input"], border=ft.border.all(1, C["border"]),
                on_hover=lambda e: _h(e, C["hover"], C["input"]),
            ),
            ft.Container(expand=True),
            ft.Container(
                content=ft.Text("ص", weight="bold", color=C["btn_t"]),
                bgcolor=C["accent"], padding=10, border_radius=8,
            ),
            ft.Text("محرك التحليل الصرفي", size=20, weight="bold", color=C["t1"]),
            ft.Container(expand=True),
            ft.Container(width=36),
        ], spacing=12),
        padding=ft.padding.symmetric(horizontal=20, vertical=12),
        bgcolor=C["card"],
        border=ft.border.only(bottom=ft.BorderSide(1, C["border"])),
    )

    # ── Layout ───────────────────────────────────────────────
    page.add(ft.Column([
        header,
        ft.Container(content=body, expand=True, padding=ft.padding.symmetric(horizontal=10)),
        ft.Container(content=out_bar, padding=ft.padding.symmetric(horizontal=10, vertical=10)),
    ], expand=True, spacing=0))


if __name__ == "__main__":
    ft.run(main)
