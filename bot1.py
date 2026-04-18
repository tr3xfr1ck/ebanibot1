import telebot
from telebot import types

TOKEN = "8783853129:AAHL87XXlW9eFnk9uw6uQVJ_Dc1Gk3C3Qc0"

bot = telebot.TeleBot(TOKEN)

ADMIN_IDS = [1061219182, 765930846]
awaiting_suggestion = set()

WELCOME_TEXT = """👋 Привет!
Добро пожаловать, меня зовут Фифи! Я официальный бот команды StudiiNet!

Тут я помогу скачать вам наш дубляж для игр, посмотреть аниме в нашей озвучке и отправить идеи или сообщения о багах в предложку!

Выбирай нужный раздел ниже 👇"""

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_games = types.InlineKeyboardButton("🎮 Наш дубляж для игр", callback_data="menu_games")
    btn_anime = types.InlineKeyboardButton("🌸 Наш дубляж для аниме", callback_data="menu_anime")
    btn_suggest = types.InlineKeyboardButton("💡 Предложка для идей и багов", callback_data="menu_suggest")

    markup.add(btn_games, btn_anime, btn_suggest)
    bot.send_message(message.chat.id, WELCOME_TEXT, reply_markup=markup, parse_mode="Markdown")


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
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_episode1 = types.InlineKeyboardButton("Эпизод 1", callback_data="episode1")
        btn_back = types.InlineKeyboardButton("← Назад", callback_data="menu_games")
        markup.add(btn_episode1, btn_back)
        bot.send_message(chat_id, "**Dispatch**\n\nВыберите эпизод:", reply_markup=markup, parse_mode="Markdown")

    elif call.data == "episode1":
        bot.answer_callback_query(call.id)
        
        text = """**Dispatch — Эпизод 1**

Dispatch — это динамичная приключенческая игра в стиле киберпанк, созданная студией AdHoc Studio в сотрудничестве с Critical Role Productions и Igloo Studio.

Вот ссылки на наш дубляж Эпизода 1:"""

        markup = types.InlineKeyboardMarkup(row_width=1)
        link1 = types.InlineKeyboardButton("Google Disk", url="https://drive.google.com/drive/folders/1MhKzU_jFra9uB-bOF0H5r-tbz-NoWwaB?usp=sharing")
        link2 = types.InlineKeyboardButton("Yandex Disk", url="https://disk.yandex.ru/d/HPhO-om90NjK3w")
        link3 = types.InlineKeyboardButton("Mega (пока нет)", url="https://mega.nz")
        btn_back = types.InlineKeyboardButton("← Назад к эпизодам", callback_data="dispatch")
        
        markup.add(link1, link2, link3, btn_back)

        bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "menu_anime":
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, "🌸 Здесь будут ссылки на наш дубляж для аниме.\n\nПока в разработке...")

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
        bot.send_message(chat_id, WELCOME_TEXT, reply_markup=markup, parse_mode="Markdown")


# Обработка предложки
@bot.message_handler(content_types=['text', 'photo', 'video', 'document', 'audio', 'voice',
                                   'video_note', 'animation', 'sticker'])
def handle_suggestion(message):
    if message.from_user.id not in awaiting_suggestion:
        return
    awaiting_suggestion.remove(message.from_user.id)

    for admin_id in ADMIN_IDS:
        try:
            bot.forward_message(admin_id, message.chat.id, message.message_id)
            bot.send_message(admin_id, f"📨 Новое предложение от {message.from_user.first_name} (ID: {message.from_user.id})")
        except:
            pass

    bot.send_message(message.chat.id, "✅ Спасибо! Ваше предложение отправлено.")


print("✅ Бот запущен!")
bot.infinity_polling(none_stop=True, interval=0, timeout=20)
