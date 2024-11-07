from telegram import ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, MessageHandler, filters
from random import randint
import math

# Foydalanuvchiga ko'rsatiladigan tugmalar
buttons = ReplyKeyboardMarkup([
    ["Qo'shish➕", "Ayirish➖"], 
    ["Ko'paytirish✖️", "Bo'lish➗"], 
    ["Ekub📏", "Ekuk📊"]
], resize_keyboard=True)

# Konversatsiya holatlari
CHOICE = 1
ANSWER = 2

# Misollar va to'g'ri javoblarni saqlash uchun ro'yxat
problems = []  # Har bir element: (savol, to'g'ri javob)

# Foydalanuvchi tanlagan mavzuni saqlash uchun
current_topic = ""

async def start(update, context):
    await update.message.reply_text(
        f"Salom {update.message.from_user.first_name}, Matematikadan misollar to'plamiga xush kelibsiz!\n"
        f"Iltimos, quyidagi tugmalardan birini tanlang:", 
        reply_markup=buttons
    )
    return CHOICE

async def choice(update, context):
    global current_topic
    user_choice = update.message.text
    problems.clear()  # Yangi misollar yaratishdan oldin eski javoblarni tozalash

    if user_choice == "Qo'shish➕":
        current_topic = "Qo'shish"
        for i in range(15):
            a = randint(10, 99)
            b = randint(10, 99)
            question = f"{i + 1}. {a} + {b} = ?"
            answer = a + b
            problems.append((question, answer))
            await update.message.reply_text(question)
    
    elif user_choice == "Ayirish➖":
        current_topic = "Ayirish"
        for i in range(15):
            a = randint(10, 99)
            b = randint(10, 99)
            question = f"{i + 1}. {a} - {b} = ?"
            answer = a - b
            problems.append((question, answer))
            await update.message.reply_text(question)
    
    elif user_choice == "Ko'paytirish✖️":
        current_topic = "Ko'paytirish"
        for i in range(15):
            a = randint(1, 9)
            b = randint(1, 9)
            question = f"{i + 1}. {a} * {b} = ?"
            answer = a * b
            problems.append((question, answer))
            await update.message.reply_text(question)
    
    elif user_choice == "Bo'lish➗":
        current_topic = "Bo'lish"
        for i in range(15):
            b = randint(1, 49)
            a = b * randint(2, 10)  # Bu yerda a, b ning butun bo'linishini ta'minlash
            question = f"{i + 1}. {a} : {b} = ?"
            answer = a // b
            problems.append((question, answer))
            await update.message.reply_text(question)
 
    elif user_choice == "Ekub📏":
        current_topic = "EKUB"
        for i in range(15):
            a = randint(50, 999)
            b = randint(50, 999)
            ekub = math.gcd(a, b)  # To'g'ri javob
            question = f"{i + 1}. {a} va {b} sonlarining EKUBi: ?"
            problems.append((question, ekub))
            await update.message.reply_text(question)
    elif user_choice == "Bo'lish➗":
        current_topic = "Bo'lish"
        for i in range(15):
            b = randint(1, 49)
            a = b * randint(2, 10) 
            question = f"{i + 1}. {a} : {b} = ?"
            answer = a // b
            problems.append((question, answer))
            await update.message.reply_text(question)
    
    elif user_choice == "Ekuk📊":
        current_topic = "EKUK"
        for i in range(15):
            a = randint(50, 999)
            b = randint(50, 999)
            ekub = math.gcd(a, b)
            ekuk = abs(a * b) // ekub  # To'g'ri javob
            question = f"{i + 1}. {a} va {b} sonlarining EKUKi: ?"
            problems.append((question, ekuk))
            await update.message.reply_text(question)

    await update.message.reply_text(
        "Iltimos, barcha misollarni yechib, javoblaringizni kiriting.\n"
        "Javoblarni quyidagi formatda yozing:\n"
        "Masalan:\n106 132 55 87 128 131 155 131 126 67 29 71 77 121 85",
        reply_markup=None
    )
    
    return ANSWER


async def check_answer(update, context):
    user_input = update.message.text
    user_answers = user_input.strip().split()
    correct_count = 0
    incorrect_count = 0
    feedback = ""

    if len(user_answers) != len(problems):
        await update.message.reply_text(
            f"Javoblar soni noto'g'ri. Siz {len(user_answers)} ta javob kiritdingiz, lekin {len(problems)} ta misol bor.\n"
            "Iltimos, barcha misollarni yeching va javoblaringizni to'liq kiriting."
        )
        return ANSWER

    for i, user_answer in enumerate(user_answers):
        try:
            user_ans_int = int(user_answer)
            correct_ans = problems[i][1]
            if user_ans_int == correct_ans:
                correct_count += 1
                feedback += f"{i + 1}. To'g'ri\n"
            else:
                incorrect_count += 1
                feedback += f"{i + 1}. Noto'g'ri (To'g'ri javob: {correct_ans})\n"
        except ValueError:
            feedback += f"{i + 1}. Javob noto'g'ri formatda. Iltimos, faqat sonlardan foydalaning.\n"
            return ANSWER

    summary = (
        f"Mavzu: {current_topic}\n"
        f"To'g'ri javoblar✅: {correct_count}\n"
        f"Noto'g'ri javoblar❌: {incorrect_count}\n\n"
        f"Detalizatsiya:\n{feedback}"
    )

    await update.message.reply_text(summary, reply_markup=buttons)

    return CHOICE

async def cancel(update, context):
    await update.message.reply_text('Suhbat tugatildi.', reply_markup=None)
    return ConversationHandler.END

def main():
    TOKEN = '7764131522:AAFFGNNHDFLn7BUwwxFuSmM3ZtM9tV9p-OI'

    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, choice)],
            ANSWER: [MessageHandler(filters.TEXT & ~filters.COMMAND, check_answer)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == '__main__':
    main()
