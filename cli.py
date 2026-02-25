import sys
import os
import arabic_reshaper
from bidi.algorithm import get_display
from logic.morphology import MorphologicalEngine

def fix_rtl(text):
    """Reshapes and reorders Arabic text for proper terminal display."""
    if not text:
        return ""
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    return bidi_text

def print_banner():
    print("=" * 50)
    msg = fix_rtl("   محرك التحليل الصرفي العربي - واجهة الأوامر")
    print(msg)
    print("   Arabic Morphological Engine - CLI")
    print("=" * 50)

def print_help():
    print(f"\n{fix_rtl('الأوامر المتاحة')} (Available Commands):")
    print(f"  add <root>        : {fix_rtl('إضافة جذر جديد')} (Add a new root)")
    print(f"  search <root>     : {fix_rtl('البحث عن جذر')} (Search for a root)")
    print(f"  del <root>        : {fix_rtl('حذف جذر')} (Delete a root)")
    print(f"  gen <root> <pat>  : {fix_rtl('توليد كلمة')} (Generate a word)")
    print(f"  all <root>        : {fix_rtl('توليد جميع الاشتقاقات')} (Generate all derivations)")
    print(f"  val <word> <root> : {fix_rtl('التحقق من اشتقاق')} (Validate derivation)")
    print(f"  patterns          : {fix_rtl('عرض جميع الأوزان')} (List all patterns)")
    print(f"  help              : {fix_rtl('عرض هذه المساعدة')} (Show this help)")
    print(f"  exit              : {fix_rtl('الخروج')} (Exit)")

def main():
    engine = MorphologicalEngine()
    print_banner()
    print_help()

    while True:
        try:
            cmd_input = input("\n> ").strip().split()
            if not cmd_input:
                continue

            cmd = cmd_input[0].lower()
            args = cmd_input[1:]

            if cmd == "exit":
                print(fix_rtl("مع السلامة! (Goodbye!)"))
                break

            elif cmd == "help":
                print_help()

            elif cmd == "add":
                if len(args) < 1:
                    print(fix_rtl("⚠️ يرجى إدخال الجذر (Please provide a root)"))
                else:
                    root = args[0]
                    if engine.add_root(root):
                        print(fix_rtl(f"✅ تم إضافة الجذر '{root}' بنجاح"))
                    else:
                        print(fix_rtl(f"❌ فشل إضافة الجذر '{root}' (قد يكون موجوداً بالفعل)"))

            elif cmd == "search":
                if len(args) < 1:
                    print(fix_rtl("⚠️ يرجى إدخال الجذر"))
                else:
                    root = args[0]
                    node = engine.get_root_node(root)
                    if node:
                        print(fix_rtl(f"🔍 الجذر '{root}' موجود"))
                        print(fix_rtl(f"📄 المشتقات المؤكدة: {len(node.derived_words)}"))
                    else:
                        print(fix_rtl(f"❌ الجذر '{root}' غير موجود"))

            elif cmd == "del":
                if len(args) < 1:
                    print(fix_rtl("⚠️ يرجى إدخال الجذر"))
                else:
                    root = args[0]
                    if engine.delete_root(root):
                        print(fix_rtl(f"✅ تم حذف الجذر '{root}'"))
                    else:
                        print(fix_rtl(f"❌ فشل حذف الجذر"))

            elif cmd == "gen":
                if len(args) < 2:
                    print(fix_rtl("⚠️ يرجى إدخال الجذر والوزن (Usage: gen <root> <pattern>)"))
                else:
                    root, pat = args[0], args[1]
                    res = engine.generate(root, pat)
                    print(fix_rtl(f"✨ النتيجة: {res}"))

            elif cmd == "all":
                if len(args) < 1:
                    print(fix_rtl("⚠️ يرجى إدخال الجذر"))
                else:
                    root = args[0]
                    results = engine.generate_all(root)
                    print(fix_rtl(f"📚 الاشتقاقات الممكنة لـ '{root}':"))
                    for w, p, t in results:
                        print(fix_rtl(f"  - {w} ({p}) : {t}"))

            elif cmd == "val":
                if len(args) < 2:
                    print(fix_rtl("⚠️ يرجى إدخال الكلمة والجذر (Usage: val <word> <root>)"))
                else:
                    word, root = args[0], args[1]
                    ok, pat = engine.validate(word, root)
                    if ok:
                        print(fix_rtl(f"✅ نعم، '{word}' مشتقة من '{root}' على وزن '{pat}'"))
                    else:
                        print(fix_rtl(f"❌ لا، '{word}' ليست مشتقة من '{root}'"))

            elif cmd == "patterns":
                pats = engine.get_all_patterns()
                print(fix_rtl(f"📋 الأوزان المتوفرة ({len(pats)}):"))
                for k, v in pats:
                    print(fix_rtl(f"  - {k} : {v['type']}"))

            else:
                print(fix_rtl(f"❓ أمر غير معروف: {cmd}"))

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"⚠️ خطأ: {e}")

if __name__ == "__main__":
    main()
