import telebot
from telebot import types

bot = telebot.TeleBot("6869863561:AAEhalkqIfWY2DQCZcAsw7b3n_3yG6gBFQY")
doctors = ["Королёва Дарья Игоревна",
"Григорьев Валерий Давидович",
"Кузнецов Дмитрий Вячеславович",
"Носова Наталья Юрьевна",
"Казакова Алла Степановна",
"Козлов Фёдор Захарович"]
professions = ["(Психиатр)",
"(Кардиолог)",
"(Онколог)",
"(Стоматолог)",
"(Невролог)",
"(Хирург)"]
dates = ["10.05.2024",
"12.05.2024",
"16.05.2024",
"19.05.2024",
"22.05.2024",
"25.05.2024"]
times=["9:30",
"10:00",
"12:30",
"13:00",
"13:30",
"14:00",
"15:00"
]
name = ""
doctor = ""
year = 0
month = 0
day = 0
hours = 0
minutes = 0

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"Введите ФИО")
    bot.register_next_step_handler(message, handle_doctor)


def handle_doctor(message):
    markup = types.ReplyKeyboardMarkup(row_width=len(doctors))
    for i in range(len(doctors)):
        markup.add(types.KeyboardButton(doctors[i]+" "+professions[i]))
    global name
    name = message.text
    print(name)
    bot.send_message(message.chat.id, f"Выберите врача", reply_markup=markup)
    bot.register_next_step_handler(message, handle_data)

def handle_data(message):
    markup = types.ReplyKeyboardMarkup(row_width=len(dates))
    for i in range(len(dates)):
        markup.add(types.KeyboardButton(dates[i]))
    global doctor
    trigger = False
    doctor = message.text
    print(doctor)
    for j in range(len(doctors)):
        if doctors[j]+" "+professions[j]==doctor:
          trigger = True
    if trigger==False:
        bot.send_message(message.chat.id, f"Такого врача нет в нашей больнице")
        bot.register_next_step_handler(message, handle_data)
        return
    bot.send_message(message.chat.id, f"Выберите дату", reply_markup=markup)
    bot.register_next_step_handler(message, handle_time)

def handle_time(message):
    markup = types.ReplyKeyboardMarkup(row_width=len(times))
    for i in range(len(times)):
        markup.add(types.KeyboardButton(times[i]))
    global day, month, year
    trigger = False
    day = message.text[:2]
    print(day)
    month = message.text[3:5]
    print(month)
    year = message.text[6:]
    print(year)
    if int(month)<1 or int(month)>12:
        bot.send_message(message.chat.id, f"Введите корректную дату")
        bot.register_next_step_handler(message, handle_time)
        return
    for j in range(len(dates)):
        if dates[j]==str(f"{day}.{month}.{year}"):
          trigger = True
    if trigger==False:
        bot.send_message(message.chat.id, f"Данная дата не доступна")
        bot.register_next_step_handler(message, handle_time)
        return
    bot.send_message(message.chat.id, f"Выберите время", reply_markup=markup)
    bot.register_next_step_handler(message, handle_result)

def handle_result(message):
    global hours, minutes
    trigger = False
    hours = message.text[:2]
    print(hours)
    minutes = message.text[3:]
    print(minutes)
    if int(hours)<0 or int(hours)>23 or int(minutes)<0 or int(minutes)>59:
        bot.send_message(message.chat.id, f"Введите корректное время")
        bot.register_next_step_handler(message, handle_result)
        return
    for j in range(len(times)):
        if times[j]==str(f"{hours}:{minutes}"):
          trigger = True
    if trigger==False:
        bot.send_message(message.chat.id, f"Данное время не доступна")
        bot.register_next_step_handler(message, handle_result)
        return
    bot.send_message(message.chat.id, f"{name}, вы записаны на {hours}:{minutes} {day}.{month}.{year} к {doctor}", reply_markup=types.ReplyKeyboardRemove())


bot.polling()