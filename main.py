import datetime
import threading
import telebot
from telebot import types  # для указание типов


from data.lesson import Lesson
from data import db_session
from data.db_session import create_session

TOKEN = '5820061555:AAHeXJY7JZBLNDmzNMnEzKBmi4GDrLzzib0'

bot = telebot.TeleBot(token=TOKEN)

def main():
    db_session.global_init("db/schedule.db")


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📃 Расписание")
    btn2 = types.KeyboardButton("⏰Звонки")
    btn3 = types.KeyboardButton("❓ Задать вопрос")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id,
                     text="Привет, я бот-напоминалка".format(
                         message.from_user), reply_markup=markup)






@bot.message_handler(commands=['reminder'])
def reminder_message(message):
    bot.send_message(message.chat.id, 'Введите название напоминания:')
    bot.register_next_step_handler(message, set_reminder_name)


@bot.message_handler(commands=['add_schedule'])
def reminder_message(message):
    bot.send_message(message.chat.id, 'Введите пароль администратора:')
    type_of_change = 'shedule'
    bot.register_next_step_handler(message, check_password, type_of_change)


@bot.message_handler(commands=['add_bells'])
def reminder_message(message):
    bot.send_message(message.chat.id, 'Введите пароль администратора:')
    type_of_change = 'bell'
    bot.register_next_step_handler(message, check_password, type_of_change)


@bot.message_handler(content_types=['text'])
def func(message):
    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']

    if(message.text == "📃 Расписание" or "асп" in message.text):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Сегодня")
        btn2 = types.KeyboardButton("Завтра")
        btn3 = types.KeyboardButton("Понедельник")
        btn4 = types.KeyboardButton("Вторник")
        btn5 = types.KeyboardButton("Среда")
        btn6 = types.KeyboardButton("Четверг")
        btn7 = types.KeyboardButton("Пятница")
        btn8 = types.KeyboardButton("Суббота")
        back = types.KeyboardButton("Вернуться")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, back)
        bot.send_message(message.chat.id, text="Расписание на какой день вас интересует?", reply_markup=markup)

    elif message.text in days:
        get_week_schedule(message)

    elif (message.text == 'Сегодня' or message.text == 'Завтра'):
        get_today_schedule(message)

    elif message.text == '⏰ Звонки':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Обычный день")
        btn2 = types.KeyboardButton("С классным часом")
        back = types.KeyboardButton("Вернуться")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, text="Расписание звонков на какой день вас интересует?", reply_markup=markup)

    elif message.text in ['Обычный день', 'С классным часом']:
        get_bells(message)

    elif (message.text == "Вернуться"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("📃 Расписание")
        button2 = types.KeyboardButton("⏰ Звонки")
        button3 = types.KeyboardButton("❓ Задать вопрос")
        markup.add(button1, button2)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)



def check_password(message, type_of_change):
    password = message.text
    if password == '710754910':
        if type_of_change == 'bell':
            bot.send_message(message.chat.id, 'Пароль принят. Ведите тип дня недели и расписание:')
            bot.register_next_step_handler(message, set_bells)
        elif type_of_change == 'schedule':
            bot.send_message(message.chat.id, 'Пароль принят. Ведите номер дня недели и расписание:')
            bot.register_next_step_handler(message, set_week_schedule)
    else:
        bot.send_message(message.chat.id, 'Пароль не верный')


def get_bells(message):
    if message.text == 'Обычный день':
        f = open(f'text/bells/normal.txt', 'r')
        bot.send_message(message.chat.id, f.read())
        f.close()
    elif message.text == 'С классным часом':
        f = open(f'text/bells/dificult.txt', 'r')
        bot.send_message(message.chat.id, f.read())
        f.close()


def set_bells(message):
    try:
        user_text = message.text.split('\n')
        type = int(user_text[0])
        db_sess = create_session()
        if type == 1:
            day = 'normal'
        else:
            day = 'dificult'
        f = open(f'text/bells/{day}.txt', 'w')
        for i in range(len(user_text)):
            if i !=0:
                f.write(user_text[i])
                f.write('\n')
        f.close()

        bot.send_message(message.chat.id, 'Расписание принято')
    except ValueError:
        bot.send_message(message.chat.id, 'Вы ввели неверный формат дня недели или расписания')

def get_today_schedule(message):
    if message.text == 'Сегодня':
        day = datetime.datetime.today().weekday()
        f = open(f'text/week/{day+1}.txt', 'r')
        print(day)
        bot.send_message(message.chat.id, f.read())
        f.close()
    elif message.text == 'Завтра':
        day = datetime.datetime.today().weekday()
        print(datetime.datetime.today())
        f = open(f'text/week/{(day + 2)%8}.txt', 'r')
        bot.send_message(message.chat.id, f.read())
        f.close()


def get_week_schedule(message):
    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    day = days.index(message.text) + 1
    print(day)
    f = open(f'text/week/{day}.txt', 'r')
    bot.send_message(message.chat.id, f.read())
    f.close()
    '''
    f = open('static/img/capybara.gif', 'rb')
    bot.send_document(message.chat.id, f)
    f.close()
    '''


def set_week_schedule(message):
    try:
        user_text = message.text.split('\n')
        day = int(user_text[0])
        db_sess = create_session()
        f = open(f'text/week/{day}.txt', 'w')
        for i in range(len(user_text)):
            if i !=0:
                f.write(user_text[i])
                f.write('\n')
        f.close()

        bot.send_message(message.chat.id, 'Расписание принято')
    except ValueError:
        bot.send_message(message.chat.id, 'Вы ввели неверный формат дня недели или расписания')



def set_reminder_name(message):
    user_data = {}
    user_data[message.chat.id] = {'reminder_name': message.text}
    bot.send_message(message.chat.id, 'Введите дату и время, когда вы хотите получить напоминание в формате ГГГГ-ММ-ДД чч:мм:сс.')
    bot.register_next_step_handler(message, reminder_set, user_data)




def reminder_set(message, user_data):
    try:
        # Преобразуем введенную пользователем дату и время в формат datetime
        reminder_time = datetime.datetime.strptime(message.text, '%Y-%m-%d %H:%M:%S')
        now = datetime.datetime.now()
        delta = reminder_time - now
        # Если введенная пользователем дата и время уже прошли, выводим сообщение об ошибке
        if delta.total_seconds() <= 0:
            bot.send_message(message.chat.id, 'Вы ввели прошедшую дату, попробуйте еще раз.')
            # Если пользователь ввел корректную дату и время, устанавливаем напоминание и запускаем таймер
        else:
            reminder_name = user_data[message.chat.id]['reminder_name']
            bot.send_message(message.chat.id, 'Напоминание "{}" установлено на {}.'.format(reminder_name, reminder_time))
            reminder_timer = threading.Timer(delta.total_seconds(), send_reminder, [message.chat.id, reminder_name])
            reminder_timer.start()
            # Если пользователь ввел некорректную дату и время, выводим сообщение об ошибке
    except ValueError:
        bot.send_message(message.chat.id, 'Вы ввели неверный формат даты и времени, попробуйте еще раз.')



# Функция, которая отправляет напоминание пользователю
def send_reminder(chat_id, reminder_name):
    bot.send_message(chat_id, 'Время получить ваше напоминание "{}"!'.format(reminder_name))


# Обработчик любого сообщения от пользователя
@bot.message_handler(func=lambda message: True)
def handle_all_message(message):
    bot.send_message(message.chat.id, 'Я не понимаю, что вы говорите. Чтобы создать напоминание, введите /reminder.')



def check_date():
    now_date = datetime.datetime.now()
    users_to_delete = []
    for chat_id, value in users.items():
        user_date = value[0]
        msg = value[1]
        if now_date >= user_date:
            bot.send_message(chat_id, msg)
            users_to_delete.append(chat_id)
    for user in users_to_delete:
        del users[user]
    threading.Timer(1, check_date).start()



if __name__ == '__main__':
    users = {}
    main()
    bot.polling(none_stop=True)