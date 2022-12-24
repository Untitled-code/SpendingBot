#!../pythonProject/venv/bin/python
# -*- coding: utf-8 -*-
"""
telegram bot for register_next_step handler with calendar.
"""

import telebot
from telebot import types
import edata_api
import datetime
from pathlib import Path
from telebot_calendar import Calendar, CallbackData, RUSSIAN_LANGUAGE
from telebot.types import ReplyKeyboardRemove, CallbackQuery
import logging
logging.basicConfig(filename='spending_bot.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

API_TOKEN = '5086846133:AAEq1xvFstnv0Ft9j-Fdzluic2CoieO9iBA'

bot = telebot.TeleBot(API_TOKEN)

user_dict = {}

# Creates a unique calendar
calendar = Calendar(language=RUSSIAN_LANGUAGE)
calendar_1_callback = CallbackData("calendar_1", "action", "year", "month", "day")
# Creates a 2nd unique calendar
calendar2 = Calendar(language=RUSSIAN_LANGUAGE)
calendar_2_callback = CallbackData("calendar_2", "action", "year", "month", "day")

class User: #get user data
    def __init__(self, name):
        self.name = name
        self.age = None
        self.age2 = None
        self.sex = None

print("Listening...")
logging.debug("Listening...")
# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
Привіт! Я бот для роботи з spending.gov.ua. Я можу допомогти тобі отримати транзакції за будь-якій період.
                                 \n Введіть будь ласка код компанії, яку шукаєте
""")

    bot.register_next_step_handler(msg, process_name_step)

def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        if not name.isdigit():
            msg = bot.reply_to(message, 'Код ЄДРПОУ має налічувати від 8 до 10 цифр. Спробуйте ще раз')
            bot.register_next_step_handler(msg, process_name_step)
            return
        user = User(name)
        user_dict[chat_id] = user
        print(f'Working with with user {chat_id}, who selected company {user_dict[chat_id].name}')
        logging.debug(f'Working with with user {chat_id}, who selected company {user_dict[chat_id].name}')
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Отримувач', 'Розпорядник')
        msg = bot.reply_to(message, 'Вибиріть, будь ласка, категорію', reply_markup=markup) #bot replying for a certain message
        bot.register_next_step_handler(msg, process_company_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_company_step(message):
    try:
        chat_id = message.chat.id
        sex = message.text
        user = user_dict[chat_id]
        if (sex == u'Отримувач') or (sex == u'Розпорядник'):
            user.sex = sex
        else:
            raise Exception("Невірне значення")
        print(user_dict[chat_id].sex)
        bot.reply_to(message, 'Введіть будь ласка початкову дату для пошуку ') #bot replying for a certain message
        now = datetime.datetime.now()  # Get the current date
        bot.send_message(
            message.chat.id,
            "Selected date",
            reply_markup=calendar.create_calendar(
                name=calendar_1_callback.prefix,
                year=now.year,
                month=now.month,  # Specify the NAME of your calendar
            ),
        )
    except Exception as e:
        bot.reply_to(message, 'oooops')

"""Calendar 1 functions"""
@bot.callback_query_handler(
    func=lambda call: call.data.startswith(calendar_1_callback.prefix)
)

def callback_inline(call: CallbackQuery):
    """
    Обработка inline callback запросов
    :param call:
    :return:
    """

    # At this point, we are sure that this calendar is ours. So we cut the line by the separator of our calendar
    name, action, year, month, day = call.data.split(calendar_1_callback.sep)
    # Processing the calendar. Get either the date or None if the buttons are of a different type
    date = calendar.calendar_query_handler(
        bot=bot, call=call, name=name, action=action, year=year, month=month, day=day
    )
    # There are additional steps. Let's say if the date DAY is selected, you can execute your code. I sent a message.
    if action == "DAY":
        msg = bot.send_message(
            chat_id=call.from_user.id,
            text=f"You have chosen {date.strftime('%d.%m.%Y')}",
            reply_markup=ReplyKeyboardRemove(),
        )
        print(f"{calendar_1_callback}: Day: {date.strftime('%d.%m.%Y')}")
        print(date)
        chat_id = msg.chat.id
        age = date
        user = user_dict[chat_id]
        user.age = age
        message = bot.reply_to(msg, 'Введіть будь ласка кінцеву дату для пошуку ') #bot replying for a certain message
        now = datetime.datetime.now()  # Get the current date
        print(now)
        bot.send_message(
            message.chat.id,
            "Selected date",
            reply_markup=calendar.create_calendar(
                name=calendar_2_callback.prefix,
                year=now.year,
                month=now.month,  # Specify the NAME of your calendar
            ),
        )

    elif action == "CANCEL":
        bot.send_message(
            chat_id=call.from_user.id,
            text="Cancellation",
            reply_markup=ReplyKeyboardRemove(),
        )
        print(f"{calendar_1_callback}: Cancellation")

    now = datetime.datetime.now()  # Get the current date
    print(now)
"""Calendar 1 functions end"""


"""Calendar 2 functions start"""
@bot.callback_query_handler(
    func=lambda call: call.data.startswith(calendar_2_callback.prefix)
)

def callback_inline(call: CallbackQuery):
    """
    Обработка inline callback запросов
    :param call:
    :return:
    """

    # At this point, we are sure that this calendar is ours. So we cut the line by the separator of our calendar
    name, action, year, month, day = call.data.split(calendar_2_callback.sep)
    # Processing the calendar. Get either the date or None if the buttons are of a different type
    date = calendar.calendar_query_handler(
        bot=bot, call=call, name=name, action=action, year=year, month=month, day=day
    )
    # There are additional steps. Let's say if the date DAY is selected, you can execute your code. I sent a message.
    if action == "DAY":
        msg = bot.send_message(
            chat_id=call.from_user.id,
            text=f"You have chosen {date.strftime('%d.%m.%Y')}",
            reply_markup=ReplyKeyboardRemove(),
        )
        print(f"{calendar_2_callback}: Day: {date.strftime('%d.%m.%Y')}")
        print(date)
        chat_id = msg.chat.id
        age2 = date
        user = user_dict[chat_id]
        user.age2 = age2
        bot.send_message(chat_id, 'Шукаємо компанію ' + user.name + '\n З дати: '
                         + str(user.age) + '\n По дату: ' + str(user.age2) + '\n Яка є: ' + user.sex)
        """Prepairing directory with chat_id and output file with timestamp"""
        TIMESTAMP = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        directory = f'dir_{chat_id}'
        print(f'Directory: {directory}')
        logging.debug(f'Directory: {directory}')
        Path(directory).mkdir(exist_ok=True) #creating a new directory if not exist
        print(f'Directory is made... {directory}')
        logging.debug(f'Directory is made... {directory}')
        output_file = f'{directory}/output_{TIMESTAMP}.csv'
        print(f'Creating outputfile {output_file}')
        logging.debug(f'Creating outputfile {output_file}')
        amount = edata_api.request(user.name, user.sex, user.age, user.age2, output_file) #sending our variables to edata_api file
        if amount != []: #checking if get data for this company
            bot.send_message(chat_id, text='Готую файл до відправки. Почекайте...') #bot send message not depending on previous messages
            file = open(output_file, 'rb')
            bot.send_document(chat_id, file) #sending file to user
            bot.send_message(chat_id, text=f'{user.sex} {user.name} мав транзакцій на суму {sum(amount)} гривень')
            print(f'{user.sex} {user.name} мав транзакцій на суму {sum(amount)} гривень')
            logging.debug(f'{user.sex} {user.name} мав транзакцій на суму {sum(amount)} гривень')
            bot.send_message(chat_id, text="\nЯк імпортувати csv файли в ексель"
                                 "\n Читайте тут: https://support.microsoft.com/uk-ua/office/%D1%96%D0%BC%D0%BF%D0%BE%D1%80%D1%82-%D1%96-%D0%B5%D0%BA%D1%81%D0%BF%D0%BE%D1%80%D1%82-%D1%82%D0%B5%D0%BA%D1%81%D1%82%D0%BE%D0%B2%D0%B8%D1%85-%D1%84%D0%B0%D0%B9%D0%BB%D1%96%D0%B2-txt-%D0%B0%D0%B1%D0%BE-csv-5250ac4c-663c-47ce-937b-339e391393ba")
        else:
            print('No data')
            logging.debug('No data')
            bot.send_message(chat_id, text='На жаль, за вашим запитом нічого не знайдено')
        """end of Program"""


    elif action == "CANCEL":
        bot.send_message(
            chat_id=call.from_user.id,
            text="Cancellation",
            reply_markup=ReplyKeyboardRemove(),
        )
        print(f"{calendar_2_callback}: Cancellation")

"""Calendar 2 functions end"""

# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.infinity_polling()
