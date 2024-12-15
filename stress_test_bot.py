import telebot
from telebot import types
import sqlite3

API_TOKEN = '7554944563:AAH-F1rD_QUCNNhzaUnSUqpWwoI8poAxIQg'
bot = telebot.TeleBot(API_TOKEN)


# ایجاد پایگاه داده و جدول
def create_database():
    conn = sqlite3.connect('user_dataaa.db')  # نام پایگاه داده
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER NOT NULL,
            first_name TEXT ,
            last_name TEXT ,
            phone TEXT NOT NULL,
            depression_status TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


create_database()  # ایجاد پایگاه داده و جدول

questions = [
    "سوال 1: آیا در هفته گذشته احساس ناراحتی کرده‌اید؟",
    "سوال 2: آیا در هفته گذشته از فعالیت‌هایی که معمولاً از آن‌ها لذت می‌برید، لذت نبرده‌اید؟",
    "سوال 3: آیا در هفته گذشته احساس خستگی یا بی‌حالی کرده‌اید؟",
    "سوال 4: آیا در هفته گذشته احساس ناامیدی کرده‌اید؟",
    "سوال 5: آیا در هفته گذشته خواب شما مختل شده است؟",
    "سوال 6: آیا در هفته گذشته احساس بی‌ارزشی کرده‌اید؟",
    "سوال 7: آیا در هفته گذشته احساس اضطراب کرده‌اید؟",
    "سوال 8: آیا در هفته گذشته به فکر خودکشی بوده‌اید؟",
    "سوال 9: آیا در هفته گذشته احساس تنهایی کرده‌اید؟",
    "سوال 10: آیا در هفته گذشته احساس غم و اندوه کرده‌اید؟"
]


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, text='سلام! اینجا با انجام چند تا تست ساده میتونی بفهمی افسردای یا نه و اگر افسردگیت خیلی حاد باشه کارشناسان ما باهات تماس می گیرن کمک میکنن!')

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    contact_button = types.KeyboardButton("ارسال شماره تماس", request_contact=True)
    markup.add(contact_button)

    bot.send_message(message.chat.id, "لطفاً شمارت رو ارسال کن:", reply_markup=markup)
    bot.register_next_step_handler(message, get_phone_number)


def get_phone_number(message):
    if message.contact:
        user_phone = message.contact.phone_number
        user_first_name = message.from_user.first_name  # نام کاربر
        user_last_name = message.from_user.last_name if message.from_user.last_name else ""  # نام خانوادگی کاربر
        user_telegram_id = message.from_user.id  # آیدی تلگرام کاربر

        # ذخیره اطلاعات کاربر
        save_user_info(user_telegram_id, user_first_name, user_last_name, user_phone, "نامشخص")
        ask_question(message.chat.id, 0, 0)
    else:
        bot.send_message(message.chat.id, "لطفاً شماره تماس خود را با استفاده از دکمه ارسال کنید.")
        welcome(message)  # دوباره از کاربر بخواهید شماره تماس را ارسال کند


def save_user_info(telegram_id, first_name, last_name, phone, depression_status):
    conn = sqlite3.connect('user_dataaa.db')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO users (telegram_id, first_name, last_name, phone, depression_status) VALUES (?, ?, ?, ?, ?)',
        (telegram_id, first_name, last_name, phone, depression_status))
    conn.commit()
    conn.close()


def ask_question(chat_id, question_index, ppehar_count):
    if question_index < len(questions):
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add("بله", "نه")
        bot.send_message(chat_id, questions[question_index], reply_markup=markup)
        bot.register_next_step_handler_by_chat_id(chat_id, process_answer, question_index, ppehar_count)
    else:
        show_result(chat_id, ppehar_count)


def process_answer(message, question_index, ppehar_count):
    if message.text == "بله":
        ppehar_count += 1
    ask_question(message.chat.id, question_index + 1, ppehar_count)


def show_result(chat_id, ppehar_count):
    depression_status = ""
    if ppehar_count > 6:
        depression_status = "دارای افسردگی هستی."
        bot.send_message(chat_id, depression_status)
    else:
        depression_status = "تو افسرده نیستی."
        bot.send_message(chat_id, depression_status)

    # بروزرسانی وضعیت افسردگی در پایگاه داده
    update_depression_status(chat_id, depression_status)

    bot.send_message(chat_id, "از اینکه از من استفاده کردی خیلی ممنونم!")


def update_depression_status(chat_id, status):
    conn = sqlite3.connect('user_dataaa.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET depression_status = ? WHERE telegram_id = ?', (status, chat_id))
    conn.commit()
    conn.close()


bot.polling()
