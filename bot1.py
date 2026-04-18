import telebot
from telebot import types

# Твой токен
TOKEN = "8783853129:AAHL87XXlW9eFnk9uw6uQVJ_Dc1Gk3C3Qc0"

bot = telebot.TeleBot(TOKEN)

WELCOME_TEXT = """👋 Привет! Добро пожаловать в наш бот.

Здесь ты можешь:
• Посмотреть наш дубляж для игр
• Посмотреть наш дубляж для аниме
• Предложить идею или сообщить о баге"""

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)

    btn_games = types.InlineKeyboardButton("Наш дубляж для игр", callback_data="menu_games")
    btn_anime = types.InlineKeyboardButton("Наш дубляж для аниме", callback_data="menu_anime")
    btn_suggest = types.InlineKeyboardButton(" Предложка для идей и багов", callback_data="menu_suggest")

    markup.add(btn_games, btn_anime, btn_suggest)

    bot.send_message(message.chat.id, WELCOME_TEXT, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id

    if call.data == "menu_games":
        bot.answer_callback_query(call.id)
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_dispatch = types.InlineKeyboardButton("Dispatch", callback_data="dispatch")
        btn_back = types.InlineKeyboardButton("← Назад в главное меню", callback_data="back_to_main")
        markup.add(btn_dispatch, btn_back)

        bot.send_message(chat_id, "🎮 **Наш дубляж для игр**", 
                         reply_markup=markup, parse_mode="Markdown")

    elif call.data == "dispatch":
        bot.answer_callback_query(call.id)
        
        text = """Dispatch от студии нет, вот 3 ссылки для вашего удобства:"""

        markup = types.InlineKeyboardMarkup(row_width=1)
        link1 = types.InlineKeyboardButton("Ссылка 1", url="https://example.com/link1")
        link2 = types.InlineKeyboardButton("Ссылка 2", url="https://example.com/link2")
        link3 = types.InlineKeyboardButton("Ссылка 3", url="https://example.com/link3")
        btn_back = types.InlineKeyboardButton("← Назад", callback_data="menu_games")
        
        markup.add(link1, link2, link3, btn_back)

        bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "menu_anime":
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, "🌸 Здесь будет раздел с нашим дубляжом для аниме.\n\nПока в разработке...")

    elif call.data == "menu_suggest":
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, 
                         "💡 Отправь мне свою идею, предложение или описание бага.\n\n"
                         "Я передам это команде.")

    elif call.data == "back_to_main":
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_games = types.InlineKeyboardButton("🎮 Наш дубляж для игр", callback_data="menu_games")
        btn_anime = types.InlineKeyboardButton("🌸 Наш дубляж для аниме", callback_data="menu_anime")
        btn_suggest = types.InlineKeyboardButton("💡 Предложка для идей и багов", callback_data="menu_suggest")
        markup.add(btn_games, btn_anime, btn_suggest)
        bot.send_message(chat_id, WELCOME_TEXT, reply_markup=markup)


# Запуск бота
print("✅ Бот успешно запущен!")
bot.infinity_polling()