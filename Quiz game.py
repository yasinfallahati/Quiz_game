import random
import time
import json
import os
import sys
import threading

# -------------------------------------------------------
# بازی کوییز مرحله‌ای (7 مرحله، هر مرحله 5 سوال، 6 ثانیه زمان هر سوال)
# -------------------------------------------------------

SAVE_FILE = "quiz_progress.json"
TIME_LIMIT = 6  # ثانیه برای هر سوال
QUESTIONS_PER_LEVEL = 5
TOTAL_LEVELS = 7

questions = [
    # ---------- مرحله 1 ----------
    {"question": "پایتخت ایران کدام شهر است؟", "options": ["تهران", "اصفهان", "شیراز", "مشهد"], "answer": "تهران"},
    {"question": "کدام سیاره به 'سیاره سرخ' معروف است؟", "options": ["زمین", "مریخ", "مشتری", "زحل"], "answer": "مریخ"},
    {"question": "بزرگ‌ترین اقیانوس جهان کدام است؟", "options": ["اقیانوس اطلس", "اقیانوس آرام", "اقیانوس هند", "اقیانوس منجمد شمالی"], "answer": "اقیانوس آرام"},
    {"question": "نتیجه‌ی 7 ضربدر 8 چند می‌شود؟", "options": ["54", "56", "58", "64"], "answer": "56"},
    {"question": "کدام عنصر شیمیایی نماد آن 'O' است؟", "options": ["طلا", "اکسیژن", "آهن", "اکسید"], "answer": "اکسیژن"},

    # ---------- مرحله 2 ----------
    {"question": "بلندترین رودخانه‌ی جهان کدام است؟", "options": ["آمازون", "نیل", "میسیسیپی", "دانوب"], "answer": "نیل"},
    {"question": "زبان برنامه‌نویسی پایتون توسط چه کسی ساخته شد؟", "options": ["گیدو ون روسوم", "بیل گیتس", "استیو جابز", "دنیس ریچی"], "answer": "گیدو ون روسوم"},
    {"question": "واحد پول ژاپن چیست؟", "options": ["وون", "ین", "یوان", "روپیه"], "answer": "ین"},
    {"question": "بزرگ‌ترین کشور جهان از نظر مساحت کدام است؟", "options": ["چین", "کانادا", "روسیه", "آمریکا"], "answer": "روسیه"},
    {"question": "ماه چندمین قمر طبیعی زمین است؟", "options": ["اولین و تنها", "دومین", "سومین", "زمین قمر ندارد"], "answer": "اولین و تنها"},

    # ---------- مرحله 3 ----------
    {"question": "نویسنده‌ی کتاب 'بوف کور' کیست؟", "options": ["صادق هدایت", "جلال آل‌احمد", "فروغ فرخزاد", "سهراب سپهری"], "answer": "صادق هدایت"},
    {"question": "سریع‌ترین حیوان خشکی جهان کدام است؟", "options": ["شیر", "یوزپلنگ", "اسب", "گورخر"], "answer": "یوزپلنگ"},
    {"question": "تعداد استخوان‌های بدن انسان بالغ چند عدد است؟", "options": ["186", "206", "226", "246"], "answer": "206"},
    {"question": "نماد شیمیایی طلا چیست؟", "options": ["Ag", "Fe", "Au", "Pb"], "answer": "Au"},
    {"question": "کدام کشور میزبان المپیک 2016 بود؟", "options": ["چین", "برزیل", "انگلیس", "روسیه"], "answer": "برزیل"},

    # ---------- مرحله 4 ----------
    {"question": "نتیجه‌ی جذر عدد 144 چند است؟", "options": ["10", "11", "12", "14"], "answer": "12"},
    {"question": "بزرگ‌ترین قاره‌ی جهان کدام است؟", "options": ["آفریقا", "آسیا", "اروپا", "آمریکای شمالی"], "answer": "آسیا"},
    {"question": "اولین فضانورد جهان چه کسی بود؟", "options": ["نیل آرمسترانگ", "یوری گاگارین", "بز آلدرین", "والنتینا ترشکووا"], "answer": "یوری گاگارین"},
    {"question": "کدام گاز برای فتوسنتز گیاهان لازم است؟", "options": ["اکسیژن", "نیتروژن", "دی‌اکسید کربن", "هیدروژن"], "answer": "دی‌اکسید کربن"},
    {"question": "پایتخت فرانسه کدام شهر است؟", "options": ["پاریس", "لندن", "رم", "مادرید"], "answer": "پاریس"},

    # ---------- مرحله 5 ----------
    {"question": "برج ایفل در کدام کشور قرار دارد؟", "options": ["ایتالیا", "فرانسه", "اسپانیا", "آلمان"], "answer": "فرانسه"},
    {"question": "کدام سیاره نزدیک‌ترین سیاره به خورشید است؟", "options": ["زهره", "زمین", "عطارد", "مریخ"], "answer": "عطارد"},
    {"question": "نام قدیم کشور تایلند چه بود؟", "options": ["سیام", "برمه", "هند شرقی", "اندونزی"], "answer": "سیام"},
    {"question": "سازنده‌ی تئوری نسبیت کیست؟", "options": ["نیوتن", "اینشتین", "گالیله", "هاوکینگ"], "answer": "اینشتین"},
    {"question": "بزرگ‌ترین صحرای جهان کدام است؟", "options": ["صحرای آفریقا", "کویر لوت", "صحرای گوبی", "جنوبگان"], "answer": "جنوبگان"},

    # ---------- مرحله 6 ----------
    {"question": "واحد اندازه‌گیری توان الکتریکی چیست؟", "options": ["وات", "ولت", "آمپر", "اهم"], "answer": "وات"},
    {"question": "کدام کشور بیشترین جمعیت جهان را دارد؟", "options": ["چین", "هند", "آمریکا", "اندونزی"], "answer": "هند"},
    {"question": "نام دیگر 'آب سنگین' در شیمی چیست؟", "options": ["دوتریوم اکسید", "هیدروژن پراکسید", "آب معدنی", "اکسید هیدروژن"], "answer": "دوتریوم اکسید"},
    {"question": "نخستین رئیس‌جمهور آمریکا چه کسی بود؟", "options": ["آبراهام لینکلن", "جورج واشنگتن", "توماس جفرسون", "بنجامین فرانکلین"], "answer": "جورج واشنگتن"},
    {"question": "بلندترین کوه جهان کدام است؟", "options": ["کی-۲", "اورست", "کیلیمانجارو", "دماوند"], "answer": "اورست"},

    # ---------- مرحله 7 ----------
    {"question": "نماد شیمیایی آهن چیست؟", "options": ["Fe", "Ir", "Al", "Au"], "answer": "Fe"},
    {"question": "کدام کشور سازنده‌ی اولین خودرو بود؟", "options": ["آمریکا", "آلمان", "ژاپن", "فرانسه"], "answer": "آلمان"},
    {"question": "تعداد سیارات منظومه شمسی چند تاست؟", "options": ["7", "8", "9", "10"], "answer": "8"},
    {"question": "پدر علم پزشکی نوین چه کسی نام دارد؟", "options": ["بقراط", "ابن سینا", "گالن", "هیپوکراتس"], "answer": "بقراط"},
    {"question": "بزرگ‌ترین جزیره‌ی جهان کدام است؟", "options": ["گرینلند", "مادگاسکار", "بورنئو", "ژاپن"], "answer": "گرینلند"},
]


def get_timed_input(prompt, timeout):
    """دریافت ورودی از کاربر با محدودیت زمانی (سازگار با ویندوز و لینوکس/مک)"""
    print(prompt, end="", flush=True)
    answer = {"value": None}

    def read_input():
        try:
            answer["value"] = input()
        except Exception:
            answer["value"] = None

    thread = threading.Thread(target=read_input, daemon=True)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        return None  # زمان تمام شد
    return answer["value"]


def load_progress():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_progress(record):
    history = load_progress()
    history.append(record)
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def print_header():
    print("=" * 55)
    print("🎮  بازی کوییز مرحله‌ای  🎮".center(55))
    print("=" * 55)


def ask_question(q_data, q_number, total_in_level, level_number):
    print(f"\n[مرحله {level_number}] سوال {q_number} از {total_in_level}:")
    print(q_data["question"])
    options = q_data["options"][:]
    random.shuffle(options)

    for i, opt in enumerate(options, start=1):
        print(f"  {i}. {opt}")

    start = time.time()
    choice = get_timed_input(f"\nجواب خود را وارد کنید (شماره گزینه) - {TIME_LIMIT} ثانیه فرصت دارید: ", TIME_LIMIT)
    elapsed = time.time() - start

    if choice is None:
        print(f"\n⏰ زمان تمام شد! ({elapsed:.1f} ثانیه گذشت)")
        return False, q_data["answer"]

    if choice.strip().isdigit() and 1 <= int(choice.strip()) <= len(options):
        selected = options[int(choice.strip()) - 1]
        return selected == q_data["answer"], q_data["answer"]

    print("❌ ورودی نامعتبر بود.")
    return False, q_data["answer"]


def play_quiz():
    print_header()
    name = input("لطفاً نام خود را وارد کنید: ").strip()
    print(f"\nسلام {name}! بازی با {TOTAL_LEVELS} مرحله شروع می‌شود.")
    print(f"هر مرحله شامل {QUESTIONS_PER_LEVEL} سوال است و برای هر سوال {TIME_LIMIT} ثانیه فرصت دارید.\n")
    time.sleep(1)

    total_score = 0
    total_questions = len(questions)
    level_results = []
    start_time = time.time()

    for level in range(1, TOTAL_LEVELS + 1):
        start_idx = (level - 1) * QUESTIONS_PER_LEVEL
        end_idx = start_idx + QUESTIONS_PER_LEVEL
        level_questions = questions[start_idx:end_idx]

        print("\n" + "-" * 55)
        print(f"🚩 شروع مرحله {level} از {TOTAL_LEVELS}".center(55))
        print("-" * 55)

        level_score = 0
        for i, q in enumerate(level_questions, start=1):
            is_correct, correct_answer = ask_question(q, i, QUESTIONS_PER_LEVEL, level)
            if is_correct:
                print("✅ آفرین! جواب درست بود.")
                level_score += 1
                total_score += 1
            else:
                print(f"❌ اشتباه بود. جواب درست: {correct_answer}")
            time.sleep(0.4)

        level_results.append({"level": level, "score": level_score, "out_of": QUESTIONS_PER_LEVEL})

        if level < TOTAL_LEVELS:
            print(f"\n🎉 شما مرحله {level} را با امتیاز {level_score} از {QUESTIONS_PER_LEVEL} تمام کردید.")
            print(f"➡️  شما به مرحله {level + 1} رفتید!")
            time.sleep(1.5)
        else:
            print(f"\n🏁 مرحله {level} (آخرین مرحله) با امتیاز {level_score} از {QUESTIONS_PER_LEVEL} تمام شد.")

    elapsed_total = time.time() - start_time

    print("\n" + "=" * 55)
    print("🏆 نتیجه‌ی نهایی بازی 🏆".center(55))
    print("=" * 55)
    print(f"نام: {name}")
    print(f"امتیاز کل: {total_score} از {total_questions}")
    print(f"زمان کل بازی: {elapsed_total:.1f} ثانیه")
    print("\nریز نتایج مراحل:")
    for lr in level_results:
        print(f"  مرحله {lr['level']}: {lr['score']} از {lr['out_of']}")

    percentage = (total_score / total_questions) * 100
    if percentage == 100:
        print("\n🏆 عالی بود! نمره کامل گرفتی!")
    elif percentage >= 70:
        print("\n👏 خیلی خوب بود!")
    elif percentage >= 40:
        print("\n🙂 بد نبود، می‌تونی بهتر بشی.")
    else:
        print("\n😅 نگران نباش، با تمرین بیشتر بهتر می‌شی.")

    print("=" * 55)

    # ذخیره‌ی اطلاعات بازی
    record = {
        "name": name,
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_score": total_score,
        "total_questions": total_questions,
        "time_seconds": round(elapsed_total, 1),
        "levels": level_results,
    }
    save_progress(record)
    print(f"\n💾 اطلاعات بازی شما در فایل '{SAVE_FILE}' ذخیره شد.")


def show_history():
    history = load_progress()
    if not history:
        print("\nهنوز هیچ بازی‌ای ذخیره نشده است.")
        return
    print("\n" + "=" * 55)
    print("📜 تاریخچه‌ی بازی‌ها 📜".center(55))
    print("=" * 55)
    for record in history:
        print(f"- {record['name']} | {record['date']} | امتیاز: {record['total_score']}/{record['total_questions']} | زمان: {record['time_seconds']} ثانیه")
    print("=" * 55)


def main():
    while True:
        play_quiz()
        print("\nگزینه‌ها:")
        print("  1. بازی مجدد")
        print("  2. مشاهده‌ی تاریخچه")
        print("  3. خروج")
        choice = input("انتخاب شما: ").strip()

        if choice == "2":
            show_history()
            again = input("\nمی‌خواهید دوباره بازی کنید؟ (بله/خیر): ").strip()
            if again not in ["بله", "ب", "yes", "y"]:
                print("\nممنون که بازی کردید! خداحافظ 👋")
                break
        elif choice == "3":
            print("\nممنون که بازی کردید! خداحافظ 👋")
            break
        elif choice != "1":
            print("\nممنون که بازی کردید! خداحافظ 👋")
            break

        print("\n" * 2)


if __name__ == "__main__":
    main()
