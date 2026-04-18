import telebot
from telebot import types

# Твой токен
TOKEN = "8783853129:AAHL87XXlW9eFnk9uw6uQVJ_Dc1Gk3C3Qc0"

bot = telebot.TeleBot(TOKEN)

# ←←← АДМИНЫ (пока только ты)
ADMIN_IDS = [1061219182]   # твой ID

# Пользователи, которые сейчас в режиме предложки
awaiting_suggestion = set()

WELCOME_TEXT = """👋 Привет! Добро пожаловать в наш бот.

Здесь ты можешь:
• Посмотреть наш дубляж для игр
• Посмотреть наш дубляж для аниме
• Предложить идею или сообщить о баге"""

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)

    btn_games = types.InlineKeyboardButton("🎮 Наш дубляж для игр", callback_data="menu_games")
    btn_anime = types.InlineKeyboardButton("🌸 Наш дубляж для аниме", callback_data="menu_anime")
    btn_suggest = types.InlineKeyboardButton("💡 Предложка для идей и багов", callback_data="menu_suggest")

    markup.add(btn_games, btn_anime, btn_suggest)

    bot.send_message(message.chat.id, WELCOME_TEXT, reply_markup=markup)


@bot.message_handler(commands=['id'])
def send_id(message):
    bot.send_message(message.chat.id, f"🔢 Твой ID: `{message.from_user.id}`")


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id

    if call.data == "menu_games":
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_dispatch = types.InlineKeyboardButton("Dispatch", callback_data="dispatch")
        btn_back = types.InlineKeyboardButton("← Назад в главное меню", callback_data="back_to_main")
        markup.add(btn_dispatch, btn_back)
        bot.send_message(chat_id, "🎮 **Наш дубляж для игр**", reply_markup=markup, parse_mode="Markdown")

    elif call.data == "dispatch":
        bot.answer_callback_query(call.id)
        text = "Dispatch от студии нет, вот 3 ссылки для вашего удобства:"
        markup = types.InlineKeyboardMarkup(row_width=1)
        link1 = types.InlineKeyboardButton("Ссылка 1", url="https://example.com/link1")
        link2 = types.InlineKeyboardButton("Ссылка 2", url="https://example.com/link2")
        link3 = types.InlineKeyboardButton("Ссылка 3", url="https://example.com/link3")
        btn_back = types.InlineKeyboardButton("← Назад", callback_data="menu_games")
        markup.add(link1, link2, link3, btn_back)
        bot.send_message(chat_id, text, reply_markup=markup)

    elif call.data == "menu_anime":
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, "🌸 Здесь будет наш дубляж для аниме.\n\nПока в разработке...")

    elif call.data == "menu_suggest":
        bot.answer_callback_query(call.id)
        awaiting_suggestion.add(call.from_user.id)
        bot.send_message(chat_id,
                         "💡 Здесь вы можете написать ваши идеи и предложения, "
                         "описать и скинуть баги и т.д.\n\n"
                         "Просто отправьте сообщение, фото, видео, файл или любой другой контент.")

    elif call.data == "back_to_main":
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_games = types.InlineKeyboardButton("🎮 Наш дубляж для игр", callback_data="menu_games")
        btn_anime = types.InlineKeyboardButton("🌸 Наш дубляж для аниме", callback_data="menu_anime")
        btn_suggest = types.InlineKeyboardButton("💡 Предложка для идей и багов", callback_data="menu_suggest")
        markup.add(btn_games, btn_anime, btn_suggest)
        bot.send_message(chat_id, WELCOME_TEXT, reply_markup=markup)


# Обработка сообщений для предложки
@bot.message_handler(content_types=['text', 'photo', 'video', 'document', 'audio', 'voice', 
                                   'video_note', 'animation', 'sticker', 'poll'])
def handle_suggestion(message):
    user_id = message.from_user.id

    if user_id not in awaiting_suggestion:
        return

    awaiting_suggestion.remove(user_id)

    # Пересылаем тебе (и потом добавим второго админа)
    for admin_id in ADMIN_IDS:
        try:
            bot.forward_message(admin_id, message.chat.id, message.message_id)
            bot.send_message(admin_id,
                             f"📨 **Новое предложение**\n"
                             f"От: {message.from_user.first_name} "
                             f"(@{message.from_user.username or 'без username'})\n"
                             f"ID: {user_id}")
        except:
            pass

    bot.send_message(message.chat.id,
                     "✅ Спасибо! Ваше предложение отправлено админам.\n"
                     "Мы обязательно его рассмотрим.")


print("✅ Бот успешно запущен! Предложка работает")
bot.infinity_polling(none_stop=True, interval=0, timeout=20)
