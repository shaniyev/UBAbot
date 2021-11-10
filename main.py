import telebot
from telebot import types
import pickledb 
db = pickledb.load('ubaDB.db', True)


print('Bot started ...')
API_TOKEN = '1874001836:***'

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['language'])
def change_language(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Қазақ тілі', 'Русский язык')
    msg = bot.reply_to(message, "Тілді таңдаңыз / Выберите язык", reply_markup = markup)
    bot.register_next_step_handler(msg, save_language)

def save_language(message):
    if db.get(str(message.from_user.id)):
        region = db.get(str(message.from_user.id)).split('|')[1]
    db.set(str(message.from_user.id), message.text+'|')
    db.append(str(message.from_user.id), region)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Қазақ тілі', 'Русский язык')
    msg = bot.reply_to(message, """\
Ұлттық білім академиясы! Национальная академия образования!
Тілді таңдаңыз / Выберите язык
""", reply_markup = markup)
    bot.register_next_step_handler(msg, process_lang_step)
    
    # if not db.get(str(message.from_user.id)):
    #     bot.register_next_step_handler(msg, process_lang_step)
    # else:
    #     bot.register_next_step_handler(msg, show_menu)

@bot.message_handler(commands=['statistics'])
def get_statistics(message):
    kaz = 0
    rus = 0
    cities = {'Нұр-Сұлтан қаласы': 1, 'Алматы қаласы': 2, 'Ақмола облысы': 3, 'Ақтөбе облысы': 4, 'Алматы облысы': 5, 'Атырау облысы': 6, 'Батыс Қазақстан облысы': 7, 'Жамбыл облысы': 8, 'Қарағанды облысы': 9, 'Қостанай облысы': 10, 'Қызылорда облысы': 11, 'Маңғыстау облысы': 12, 'Түркістан облысы': 13, 'Павлодар облысы': 14, 'Солтүстік Қазақстан облысы': 15, 'Шығыс Қазақстан облысы': 16, 'Шымкент қаласы': 17, 'город Нур-Султан': 1, 'город Алматы': 2, 'Акмолинская область': 3, 'Актюбинская область': 4, 'Алматинская область': 5, 'Атырауская область': 6, 'Западно-Казахстанская область': 7, 'Жамбылская область': 8, 'Карагандинская область': 9, 'Костанайская область': 10, 'Кызылординская область': 11, 'Мангистауская область': 12, 'Туркестанская область': 13, 'Павлодарская область': 14, 'Северо-Казахстанская область': 15, 'Восточно-Казахстанская область': 16, 'город Шымкент': 17}
    region = [0] * 20
    valid_cities = ['Нұр-Сұлтан қаласы', 'Алматы қаласы', 'Ақмола облысы', 'Ақтөбе облысы', 'Алматы облысы', 'Атырау облысы', 'Батыс Қазақстан облысы', 'Жамбыл облысы', 'Қарағанды облысы', 'Қостанай облысы', 'Қызылорда облысы', 'Маңғыстау облысы', 'Түркістан облысы', 'Павлодар облысы', 'Солтүстік Қазақстан облысы', 'Шығыс Қазақстан облысы', 'Шымкент қаласы', 'город Нур-Султан', 'город Алматы', 'Акмолинская область', 'Актюбинская область', 'Алматинская область', 'Атырауская область', 'Западно-Казахстанская область', 'Жамбылская область', 'Карагандинская область', 'Костанайская область', 'Кызылординская область', 'Мангистауская область', 'Туркестанская область', 'Павлодарская область', 'Северо-Казахстанская область', 'Восточно-Казахстанская область', 'город Шымкент']
    for i in db.getall():
        k = db.get(i).split('|')
        if k[1] in valid_cities:
            region[cities[k[1]]] += 1
        if k[0] == 'Қазақ тілі':
            kaz += 1
        else:
            rus += 1
    regions = ['Нұр-Сұлтан қаласы', 'Алматы қаласы', 'Ақмола облысы', 'Ақтөбе облысы', 'Алматы облысы', 'Атырау облысы', 'Батыс Қазақстан облысы', 'Жамбыл облысы', 'Қарағанды облысы', 'Қостанай облысы', 'Қызылорда облысы', 'Маңғыстау облысы', 'Түркістан облысы', 'Павлодар облысы', 'Солтүстік Қазақстан облысы', 'Шығыс Қазақстан облысы', 'Шымкент қаласы']
    msg = 'Қолданушылар саны : ' + str(kaz + rus) + '\nҚазақ тілін таңдағандар : ' + str(kaz) + '\nОрыс тілін таңдағандар : ' + str(rus) + '\n'
    msg += '=========================\n'
    for i in range(1,18):
        msg += str(regions[i - 1]) + ' : ' + str(region[i]) + '\n'
    chat_id = message.chat.id
    bot.send_message(chat_id, msg)

def process_lang_step(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    language = message.text
    if language == 'Қазақ тілі':
        question = 'Өңіріңізді таңдаңыз'
        fileName = 'regionsKZ.txt'
    elif language == 'Русский язык':
        question = 'Выберите регион'
        fileName = 'regionsRU.txt'
    db.set(str(message.from_user.id), language+'|')
    file = open(fileName, 'r')
    regions = file.readlines()
    for i in regions:
        markup.add(i)
    msg = bot.reply_to(message, question, reply_markup = markup)
    bot.register_next_step_handler(msg, process_region_step)

def process_region_step(message):
    try:
        chat_id = message.chat.id
        region = message.text
    except Exception as e:
        bot.reply_to(message, 'region step exception')

    db.append(str(message.from_user.id), region)
    language = db.get(str(message.from_user.id)).split('|')[0]
    if language == 'Қазақ тілі':
        msg = "Негізгі мәзірге өту үшін /menu теріңіз"
    else:
        msg = "Введите /menu для отображения основного меню"
    bot.send_message(chat_id, msg)
    # print(user_dict)

@bot.message_handler(commands=['menu'])
def show_menu(message):
    try:
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        language = db.get(str(message.from_user.id)).split('|')[0] 
        if language == 'Қазақ тілі':
            msg = 'Негізгі мәзір'
            fileName = 'menuKZ.txt'
        elif language == 'Русский язык':
            msg = 'Основное меню'
            fileName = 'menuRU.txt'
        file = open(fileName, 'r')
        menu = file.readlines()
        for line in menu:
            markup.add(line)
        msg = bot.reply_to(message, msg, reply_markup = markup)
        bot.register_next_step_handler(msg, next_menu)
    except Exception as e:
        bot.reply_to(message, 'Негізгі мәзірге оралу үшін /menu теріңіз \nДля перехода на основное меню введите /menu')
def next_menu(message):
    try:
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        language = db.get(str(message.from_user.id)).split('|')[0] 
        if language == 'Қазақ тілі':
            m = message.text + ' мәзірі'
            fileName = message.text + '.txt'
        elif language == 'Русский язык':
            m = 'Меню ' + message.text
            fileName = message.text + '.txt'
        file = open(fileName, 'r')
        menu = file.readlines()
        for line in menu:
            markup.add(line)
        msg = bot.reply_to(message, m, reply_markup = markup)
        bot.register_next_step_handler(msg, send_file)
    except Exception as e:
        bot.reply_to(message, 'Негізгі мәзірге оралу үшін /menu теріңіз \nДля перехода на основное меню введите /menu')
def send_file(message):
    try:
        chat_id = message.chat.id
        fileName = message.text+'.pdf'
        f = open('content/'+fileName, 'rb')
        language = db.get(str(message.from_user.id)).split('|')[0] 
        bot.send_document(message.chat.id, f)
        if language == 'Қазақ тілі':
            msg = 'Негізгі мәзірге оралу үшін /menu теріңіз'
        else:
            msg = 'Для перехода на основное меню введите /menu'
        bot.send_message(chat_id, msg)
    except Exception as e:
        bot.reply_to(message, 'Негізгі мәзірге оралу үшін /menu теріңіз \nДля перехода на основное меню введите /menu')
if __name__ == '__main__':
     bot.infinity_polling()