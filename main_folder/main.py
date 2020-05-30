from smtplib import SMTP
import datetime
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from vk_api.keyboard import VkKeyboard
from main_folder.data.users import User
from main_folder.data import db_session
import math

furs = ['Volvo FM']
db_session.global_init("db/users.sqlite")
token = open('static/token.txt', mode='rt').read().split('\n')[0]
vk_session = vk_api.VkApi(token=token)
longpoll = VkBotLongPoll(vk_session, 195353132)
keyboards = {'login': [True,
                       ["Войти", 'POSITIVE'],
                       'Line',
                       ["Зарегистрироваться", 'DEFAULT']],
             'вход': [False,
                      ["Зарегистрироваться", 'DEFAULT']],
             'main_menu': [False, ['Обо мне', 'DEFAULT'],
                           ['Образование', 'DEFAULT'],
                           ['Работа', 'DEFAULT'],
                           'Line',
                           ['Дом', 'PRIMARY'],
                           ['Гараж', 'PRIMARY'],
                           ['Машины', 'PRIMARY'],
                           'Line',
                           ['Kasino', 'POSITIVE'],
                           ['БАНК', 'POSITIVE'],
                           ['Vladito', 'POSITIVE'],
                           'Line',
                           ['Выход', 'NEGATIVE']],
             'edu': [False,
                     ['Среднее общее образование', 'DEFAULT'],
                     'Line',
                     ['Среднее профессиональное образование', 'DEFAULT'],
                     'Line',
                     ['Высшее образование', 'PRIMARY'],
                     'Line',
                     ['Высшее профессиональное образование', 'POSITIVE'],
                     'Line',
                     ['Вернуться назад', 'NEGATIVE']],
             'main_job': [False,
                          ['Работать', 'POSITIVE'],
                          'Line',
                          ['Сменить профессию', 'PRIMARY'],
                          'Line',
                          ['Вернуться назад', 'NEGATIVE']],
             'job': [False,
                     ['Грузчик', 'DEFAULT'],
                     'Line',
                     ['Таксист', 'DEFAULT'],
                     'Line',
                     ['Банкир', 'DEFAULT'],
                     'Line',
                     ['Сварщик', 'PRIMARY'],
                     'Line',
                     ['Дальнобойщик', 'PRIMARY'],
                     'Line',
                     ['Депутат', 'POSITIVE'],
                     'Line',
                     ['Программист', 'POSITIVE'],
                     'Line',
                     ['Вернуться назад', 'NEGATIVE']],
             'Отмена регистрации': [False,
                                    ['Отмена', 'NEGATIVE']],
             'back': [False,
                      ['Вернуться назад', 'NEGATIVE']],
             'bank': [False,
                      ['Мой счёт', 'DEFAULT'],
                      ['Перевести', 'PRIMARY'],
                      'Line',
                      ['Купить валюту', 'POSITIVE'],
                      'Line',
                      ['Вернуться назад', 'NEGATIVE']],
             'admin': [False,
                       ['Выход в главное меню', 'NEGATIVE']],
             'kazino': [False,
                        ['Мой счёт', 'DEFAULT'],
                        'Line',
                        ['Угодайка', 'POSITIVE'],
                        'Line',
                        ['Вернуться назад', 'NEGATIVE']],
             'ugodaika': [True,
                          ['1', 'DEFAULT'],
                          ['2', 'PRIMARY'],
                          ['3', 'POSITIVE'],
                          'Line',
                          ['Вернуться назад', 'NEGATIVE']
                          ]}


def mail(mail):  # отправка кода на почту
    number = random.randint(1000, 9999)
    smtpObj = SMTP('smtp.gmail.com', port=587)
    smtpObj.starttls()
    smtpObj.login('vns.social.networks@gmail.com', 'dkflxvje`,jr')
    smtpObj.sendmail("vns.social.networks@gmail.com", mail, str(number))
    smtpObj.quit()
    return number


def log(id, text, friend_id=None, give=False, sum=0):
    if text == 'admin':
        session = db_session.create_session()
        user = session.query(User).filter(User.vk == id).first()
        print(
            f'time: {datetime.datetime.now()} vk_id: {id}; text: {text}; allowed: {"True" if user.role == "admin" else "False"}')
    elif text == 'Перевод':
        print(
            f'time: {datetime.datetime.now()} Remittances from: {id} to: {friend_id} summa: {sum} heppen: {"YES" if give else "NO"}')
    else:
        print(f'time: {datetime.datetime.now()} vk_id: {id}; text: {text}')


def create_keyboard(text):
    global keyboards
    if keyboards[text][0]:
        keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
    else:
        keyboard = vk_api.keyboard.VkKeyboard(one_time=False)
    # False Если клавиатура должна оставаться откртой после нажатия на кнопку
    # True если она должна закрваться
    # DEFAULT = белый
    # POSITIVE = зелёный
    # NEGATIVE = красный
    # PRIMARY = синий
    for i in keyboards[text][1:]:
        if type(i) is list:
            if i[1] == 'DEFAULT':
                keyboard.add_button(i[0], color=vk_api.keyboard.VkKeyboardColor.DEFAULT)
            elif i[1] == 'POSITIVE':
                keyboard.add_button(i[0], color=vk_api.keyboard.VkKeyboardColor.POSITIVE)
            elif i[1] == 'NEGATIVE':
                keyboard.add_button(i[0], color=vk_api.keyboard.VkKeyboardColor.NEGATIVE)
            elif i[1] == 'PRIMARY':
                keyboard.add_button(i[0], color=vk_api.keyboard.VkKeyboardColor.PRIMARY)
            else:
                continue
        elif i == 'Line':
            keyboard.add_line()
        else:
            continue
    # keyboard.add_line()  # Обозначает добавление новой строки
    # keyboard = vk_api.keyboard.VkKeyboard(one_time=False)
    # keyboard.add_button(keyboards[text][1][0], color=vk_api.keyboard.VkKeyboardColor.DEFAULT)
    return keyboard.get_keyboard()


def create_empty_keyboard():
    keyboard = vk_api.keyboard.VkKeyboard.get_empty_keyboard()
    return keyboard
    # Эта функция используется для закрытия клавиатуры


def money_earn(id):
    session = db_session.create_session()
    user = session.query(User).filter(User.vk == id).first()
    a = user.last_date
    bb = datetime.date.today()
    a = a.split('-')
    aa = datetime.date(int(a[0]), int(a[1]), int(a[2]))
    cc = bb - aa
    dd = str(cc)
    if ':' in dd.split()[0]:
        return
    else:
        user.money += user.zarplata * int(dd.split()[0])
        user.last_date = str(datetime.date.today())
        session.commit()


def enter(id):
    print(1)
    session = db_session.create_session()
    print(2)
    user = session.query(User).filter(str(User.vk) == str(id)).first()
    print(3)
    if user.enter == 'True':
        print('1')
        money_earn(id)
        game_process(user.id, id)
    else:
        print('2')
        keyboard = create_keyboard('вход')
        vk = vk_session.get_api()
        vk.messages.send(user_id=id, message="Введите почту:", keyboard=keyboard, random_id=random.randint(0, 2 ** 64))
        try:
            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    post = event.obj.message['text']
                    exist = session.query(User).filter(User.email == post).first()
                    if exist:
                        user = session.query(User).filter(User.email == post).first()
                        break
                    elif post == 'Зарегистрироваться':
                        return register(id)
                    else:
                        vk.messages.send(user_id=id, message="Такой почты не зарегистрировано!\nВведите почту:",
                                         keyboard=keyboard,
                                         random_id=random.randint(0, 2 ** 64))
            vk = vk_session.get_api()
            vk.messages.send(user_id=id, message="Введите пароль:", keyboard=keyboard,
                             random_id=random.randint(0, 2 ** 64))
            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    password = event.obj.message['text']
                    if password == user.password:
                        user.enter = 'True'
                        session.commit()
                        money_earn(id)
                        return game_process(user.id, id)
                    elif password == 'Зарегистрироваться':
                        return register(id)
                    else:
                        vk.messages.send(user_id=id, message="Не правильный пароль!\nВведите пароль:",
                                         keyboard=keyboard,
                                         random_id=random.randint(0, 2 ** 64))
        except Exception:
            print('\033[31mОшибка, пытаемся перезапуститься...\033[0m')
            return main(0)


def register(id):
    global keyboards
    name_in_game = ''
    surname_in_game = ''
    email = ''
    password = ''
    keyboard = create_keyboard('Отмена регистрации')
    vk = vk_session.get_api()
    vk.messages.send(user_id=id, message="Регистрация:",
                     random_id=random.randint(0, 2 ** 64), keyboard=keyboard)
    vk.messages.send(user_id=id, message="Введите имя в игре:",
                     random_id=random.randint(0, 2 ** 64), keyboard=keyboard)
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                name_in_game = event.obj.message['text']
                # проверка на пустое имя
                if len(name_in_game.split()) == 0:
                    vk.messages.send(user_id=id, message="Имя должно быть не пустым!",
                                     random_id=random.randint(0, 2 ** 64), keyboard=keyboard)
                    vk.messages.send(user_id=id, message="Введите имя в игре:",
                                     random_id=random.randint(0, 2 ** 64), keyboard=keyboard)
                elif event.obj.message['text'] == 'Отмена':
                    return enter(id)
                else:
                    break
        vk.messages.send(user_id=id, message="Введите фамилию в игре:",
                         random_id=random.randint(0, 2 ** 64), keyboard=keyboard)
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                surname_in_game = event.obj.message['text']
                # проверка на пустую фамилию
                if len(surname_in_game.split()) == 0:
                    vk.messages.send(user_id=id, message="Фамилия должна быть не пустой!",
                                     random_id=random.randint(0, 2 ** 64), keyboard=keyboard)
                    vk.messages.send(user_id=id, message="Введите фамилию в игре:",
                                     random_id=random.randint(0, 2 ** 64), keyboard=keyboard)
                elif event.obj.message['text'] == 'Отмена':
                    return enter(id)
                else:
                    break

        vk.messages.send(user_id=id,
                         message="Введите email (пожалуйста, введите существующий email, так-как будет проверка):",
                         random_id=random.randint(0, 2 ** 64), keyboard=keyboard)
        f = False
        # флаг для почты
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                email = event.obj.message['text']
                exist = db_session.create_session().query(User).filter(User.email == email).first()
                if email == 'Отмена':
                    return enter(id)
                if exist:
                    vk.messages.send(user_id=id, message='Данный email уже зарегистрирован!',
                                     random_id=random.randint(0, 2 ** 64), keyboard=keyboard)
                    vk.messages.send(user_id=id,
                                     message="Введите email (пожалуйста, введите существующий email, так-как будет проверка):",
                                     random_id=random.randint(0, 2 ** 64), keyboard=keyboard)
                elif not exist:
                    number = mail(email)
                    vk.messages.send(user_id=id, message="Введите код пришедший на почту:",
                                     random_id=random.randint(0, 2 ** 64), keyboard=keyboard)
                    if event.obj.message['text'] == 'Отмена':
                        return main(0)
                    else:
                        for ev in longpoll.listen():
                            if ev.type == VkBotEventType.MESSAGE_NEW:
                                mess = ev.obj.message['text']
                                # состоит только из цифр
                                if not mess.isdigit():
                                    vk.messages.send(user_id=id, message="Код состоит только из цифр!",
                                                     random_id=random.randint(0, 2 ** 64), keyboard=keyboard)
                                    vk.messages.send(user_id=id, message="Введите код пришедший на почту:",
                                                     random_id=random.randint(0, 2 ** 64), keyboard=keyboard)
                                # правильный ли код?
                                elif int(mess) != number:
                                    vk.messages.send(user_id=id, message="Неправильный код!",
                                                     random_id=random.randint(0, 2 ** 64), keyboard=keyboard)
                                    vk.messages.send(user_id=id, message="Введите код пришедший на почту:",
                                                     random_id=random.randint(0, 2 ** 64), keyboard=keyboard)
                                elif ev.obj.message['text'] == 'Отмена':
                                    return enter(id)
                                else:
                                    f = True
                                    break
            if f:
                break
        vk.messages.send(user_id=id,
                         message="Введите ваш пароль:",
                         random_id=random.randint(0, 2 ** 64), keyboard=keyboard)
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                password = event.obj.message['text']
                if event.obj.message['text'] == 'Отмена':
                    return main(0)
                else:
                    break
    except Exception:
        print('\033[31mОшибка, пытаемся перезапуститься...\033[0m')
        return main(0)
    session = db_session.create_session()
    user = User()
    user.name = name_in_game
    user.surname = surname_in_game
    user.email = email
    user.password = password
    user.money = 100
    user.zarplata = 0
    user.home = 'False'
    user.cars = 'False'
    user.garage = 'False'
    user.education = 'Основное общее образование'
    user.profession = 'False'
    user.enter = 'True'
    user.vk = id
    user.ban = 'False'
    user.role = 'user'
    try:
        session.add(user)
        session.commit()
        session = db_session.create_session()
        user = session.query(User).filter(User.email == email).first()
        return enter(user.id)
    except Exception:
        vk.messages.send(user_id=id,
                         message="!!!Запрещается создавать больше одного аккаунта на одном и том же аккаунте вк!!!",
                         keyboard=keyboard, random_id=random.randint(0, 2 ** 64))
        return main(0, id)


def main(*func):
    vk = vk_session.get_api()
    if func[0] == 1:
        keyboard = create_keyboard('main_menu')
        vk.messages.send(user_id=func[1], message="Привет",
                         keyboard=keyboard, random_id=random.randint(0, 2 ** 64))
    elif func[0] == 0 and len(func) == 1:
        print('Robit')
    elif func[0] == 0 and len(func) == 2:
        keyboard = create_keyboard('login')
        vk.messages.send(user_id=func[1], message="Привет",
                         keyboard=keyboard, random_id=random.randint(0, 2 ** 64))
    elif func[0] == -1:
        keyboard = create_keyboard('login')
        vk.messages.send(user_id=func[1], message="Привет",
                         keyboard=keyboard, random_id=random.randint(0, 2 ** 64))
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                log(event.obj.message['from_id'], event.obj.message['text'])
                response = event.message.text.casefold()
                vk = vk_session.get_api()
                if event.from_user:
                    if response.lower() in ["привет", "начать"]:
                        keyboard = create_keyboard('login')
                        vk.messages.send(user_id=event.obj.message['from_id'], message="Привет",
                                         keyboard=keyboard, random_id=random.randint(0, 2 ** 64))
                    elif response.lower() == "закрыть":
                        empty_keyboard = create_empty_keyboard()
                        vk.messages.send(user_id=event.obj.message['from_id'], message="Пока",
                                         keyboard=empty_keyboard, random_id=random.randint(0, 2 ** 64))
                    elif response.lower() == "войти":
                        return enter(event.obj.message['from_id'])
                    elif response.lower() == "зарегистрироваться":
                        return register(event.obj.message['from_id'])
                    else:
                        keyboard = create_keyboard('login')
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message="Такой команды нет, попробуй снова.",
                                         keyboard=keyboard, random_id=random.randint(0, 2 ** 64))
                    if event.obj.message['from_id'] in [463771138, 220401042] and response == 'ADMIN':
                        pass
    except Exception:
        print('\033[31mОшибка, пытаемся перезапуститься...\033[0m')
        return main(0)


def test1():
    return False


def test2():
    return False


def test3():
    return False


def test4():
    return False


def working(user_id, id):
    vk = vk_session.get_api()
    session = db_session.create_session()
    user = session.query(User).filter(User.id == user_id).first()
    keyboard = create_keyboard('back')
    letter = random.choice('qwertyuiopasdfghjklzxcvbnm')
    times = random.randint(10, 100)
    answer = letter * times
    vk.messages.send(user_id=id, message=f"Введите букву: {letter}\n"
                                         f"Количество раз: {times}",
                     keyboard=keyboard,
                     random_id=random.randint(0, 2 ** 64))
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                response = event.obj.message['text']
                log(event.obj.message['from_id'], 'Работает')
                if response == 'Вернуться назад':
                    return body_job(user_id, id)
                elif response == answer:
                    vk.messages.send(user_id=id, message=f"Правильно, ты заработал {user.zarplata} руб.",
                                     keyboard=keyboard,
                                     random_id=random.randint(0, 2 ** 64))
                    user.money += user.zarplata
                    session.commit()
                    return working(user_id, id)
                else:
                    vk.messages.send(user_id=id, message="Неправильно!",
                                     keyboard=keyboard,
                                     random_id=random.randint(0, 2 ** 64))
                    return working(user_id, id)
    except Exception:
        print('\033[31mОшибка, пытаемся перезапуститься...\033[0m')
        return enter(id)


def body_job(user_id, id):
    vk = vk_session.get_api()
    keyboard = create_keyboard('main_job')
    vk.messages.send(user_id=id, message="Здраствуйте, выбирайте.",
                     keyboard=keyboard,
                     random_id=random.randint(0, 2 ** 64))
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                log(event.obj.message['from_id'], event.obj.message['text'])
                response = event.obj.message['text']
                if response == 'Работать':
                    return working(user_id, id)
                elif response == 'Сменить профессию':
                    return job(id, user_id)
                elif response == 'Вернуться назад':
                    return game_process(user_id, id)
                else:
                    vk.messages.send(user_id=id, message="Нет так команды!",
                                     keyboard=keyboard,
                                     random_id=random.randint(0, 2 ** 64))
    except Exception:
        print('\033[31mОшибка, пытаемся перезапуститься...\033[0m')
        return enter(id)


def job(id, user_id):
    global furs
    vk = vk_session.get_api()
    session = db_session.create_session()
    keyboard = create_keyboard('job')
    educ = session.query(User).filter(User.id == user_id).first()
    educ = educ.education
    vk.messages.send(user_id=id, message="Кем хотите работать?\n"
                                         "Для ГРУЗЧИКА(20 тыс.) нужно иметь: Основное общее образование\n"
                                         "Для ТАКСИСТА(30 тыс.) нужно иметь: Машина\n"
                                         "Для БАНКИРА(50 тыс.) нужно иметь: Среднее общее образование\n"
                                         "Для СВАРЩИКА(100 тыс.) нужно иметь: Среднее профессиональное образование\n"
                                         "Для ДАЛЬНОБОЙЩИКА(300 тыс.) нужно иметь: тягач/фура\n"
                                         "Для ДЕПУТАТА(300 тыс.) нужно иметь: Высшее образование\n"
                                         "Для ПРОГРАММИСТА(500 тыс.) нужно иметь: Высшее профессиональное образование, дом\n",
                     keyboard=keyboard,
                     random_id=random.randint(0, 2 ** 64))
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                log(event.obj.message['from_id'], event.obj.message['text'])
                user = session.query(User).filter(User.id == user_id).first()
                response = event.obj.message['text']
                if educ == 'Высшее профессиональное образование' and response == 'Программист' and user.home.split(';')[
                    0] == 'True':
                    user.zarplata = 500000
                    user.profession = 'True;Программист'
                    session.commit()
                    return game_process(user_id, id)
                elif educ == 'Основное общее образование' and response == 'Грузчик':
                    user.zarplata = 20000
                    user.profession = 'True;Грузчик'
                    session.commit()
                    return game_process(user_id, id)
                elif educ == 'Среднее общее образование' and response == 'Банкир':
                    user.zarplata = 50000
                    user.profession = 'True;Банкир'
                    session.commit()
                    return game_process(user_id, id)
                elif educ == 'Среднее профессиональное образование' and response == 'Сварщик':
                    user.zarplata = 100000
                    user.profession = 'True;Сварщик'
                    session.commit()
                    return game_process(user_id, id)
                elif educ == 'Высшее образование' and response == 'Депутат':
                    user.zarplata = 300000
                    user.profession = 'True;Депутат'
                    session.commit()
                    return game_process(user_id, id)
                elif user.cars.split(';')[0] == 'True' and response == 'Таксист':
                    user.zarplata = 30000
                    user.profession = 'True;Таксист'
                    session.commit()
                    return game_process(user_id, id)
                elif user.cars.split(';')[0] == 'True' and response == 'Дальнобойщик':
                    if any([(lambda car: True if car in furs else False)(i) for i in
                            user.cars.split(';')[1].split(', ')]):
                        user.zarplata = 300000
                        user.profession = 'True;Дальнобойщик'
                        session.commit()
                        return game_process(user_id, id)
                    else:
                        vk.messages.send(user_id=id, message="Вы не можете им работать, у вас нет тягачей/фур!",
                                         keyboard=keyboard,
                                         random_id=random.randint(0, 2 ** 64))
                elif response == 'Вернуться назад':
                    return game_process(user_id, id)
                else:
                    vk.messages.send(user_id=id, message="Вы не можете им работать, либо такой команды нет.",
                                     keyboard=keyboard,
                                     random_id=random.randint(0, 2 ** 64))
    except Exception:
        print('\033[31mОшибка, пытаемся перезапуститься...\033[0m')
        return enter(id)


def give(user_id, id):
    vk = vk_session.get_api()
    keyboard = create_keyboard('back')
    vk.messages.send(user_id=id, message="Введите id друга:", keyboard=keyboard,
                     random_id=random.randint(0, 2 ** 64))
    session = db_session.create_session()
    user = session.query(User).filter(User.id == user_id).first()
    friend_id = 0
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                response = event.obj.message['text']
                try:
                    if int(response) in [int(i[0]) for i in session.query(User.vk).all()]:
                        friend_id = int(response)
                        vk.messages.send(user_id=id, message="Введите сумму перевода:", keyboard=keyboard,
                                         random_id=random.randint(0, 2 ** 64))
                        break
                    else:
                        vk.messages.send(user_id=id, message="Нет такого id, попробуйте снова:", keyboard=keyboard,
                                         random_id=random.randint(0, 2 ** 64))
                except Exception:
                    vk.messages.send(user_id=id, message=f"Неправильный ввод данных, попробуйте снова:",
                                     keyboard=keyboard,
                                     random_id=random.randint(0, 2 ** 64))
        _sum = 0
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                response = event.obj.message['text']
                try:
                    _sum = int(response)
                    break
                except Exception:
                    vk.messages.send(user_id=id, message="Не правильный формат ввода.", keyboard=keyboard,
                                     random_id=random.randint(0, 2 ** 64))
    except Exception:
        print('\033[31mОшибка, пытаемся перезапуститься...\033[0m')
        return enter(id)
    try:
        friend = session.query(User).filter(User.vk == friend_id).first()
        if user.money - _sum < 0:
            assert 1 / 0
        friend.money += _sum
        user.money -= _sum
        session.commit()
        vk.messages.send(user_id=id,
                         message=f"Перевод выполнен.\nС вас списали: {_sum}\nВаш счёт на данный момент составляет: {user.money}",
                         keyboard=keyboard,
                         random_id=random.randint(0, 2 ** 64))
        log(id, 'Перевод', friend_id, True, _sum)
        return bank(user_id, id)
    except Exception:
        vk.messages.send(user_id=id,
                         message=f"Перевод не выполнен.",
                         keyboard=keyboard,
                         random_id=random.randint(0, 2 ** 64))
        log(id, 'Перевод', friend_id, False, _sum)
        return bank(user_id, id)


def bank(user_id, id):
    vk = vk_session.get_api()
    session = db_session.create_session()
    user = session.query(User).filter(User.id == user_id).first()
    keyboard = create_keyboard('bank')
    vk.messages.send(user_id=id, message="Выбирай", keyboard=keyboard,
                     random_id=random.randint(0, 2 ** 64))
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                log(event.obj.message['from_id'], event.obj.message['text'])
                response = event.obj.message['text']
                if response == 'Перевести':
                    return give(user_id, id)
                elif response == 'Вернуться назад':
                    return game_process(user_id, id)
                elif response == 'Мой счёт':
                    vk.messages.send(user_id=id, message=f"На данный момент ваш счёт составляет: {user.money}",
                                     keyboard=keyboard,
                                     random_id=random.randint(0, 2 ** 64))
                else:
                    if response == 'Купить валюту':
                        vk.messages.send(user_id=id, message="В будщем будет добавленна.", keyboard=keyboard,
                                         random_id=random.randint(0, 2 ** 64))
                    else:
                        vk.messages.send(user_id=id, message="Такой функции нет.", keyboard=keyboard,
                                         random_id=random.randint(0, 2 ** 64))
    except Exception:
        print('\033[31mОшибка, пытаемся перезапуститься...\033[0m')
        return enter(id)


def education(id, user_id):
    vk = vk_session.get_api()
    session = db_session.create_session()
    user = session.query(User).filter(User.id == user_id).first()
    educ = user.education
    keyboard = create_keyboard('edu')
    vk.messages.send(user_id=id, message="Выбирай", keyboard=keyboard,
                     random_id=random.randint(0, 2 ** 64))
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                log(event.obj.message['from_id'], event.obj.message['text'])
                response = event.obj.message['text']
                if response == 'Среднее общее образование' and educ == 'Основное общее образование':
                    result = test1()
                    if result:
                        user.education = 'Среднее общее образование'
                        session.commit()
                        return game_process(user_id, id)
                    else:
                        vk.messages.send(user_id=id,
                                         message=f"{'Вы не прошли тест' if not result else 'Нужно предыдущее образование'}",
                                         keyboard=keyboard,
                                         random_id=random.randint(0, 2 ** 64))
                elif response == 'Среднее профессиональное образование' and educ == 'Среднее общее образование':
                    result = test2()
                    if result:
                        user.education = 'Среднее профессиональное образование'
                        session.commit()
                        return game_process(user_id, id)
                    else:
                        vk.messages.send(user_id=id,
                                         message=f"{'Вы не прошли тест' if not result else 'Нужно предыдущее образование'}",
                                         keyboard=keyboard,
                                         random_id=random.randint(0, 2 ** 64))
                elif response == 'Высшее образование' and educ == 'Среднее профессиональное образование':
                    result = test3()
                    if result:
                        user.education = 'Высшее образованиее'
                        session.commit()
                        return game_process(user_id, id)
                    else:
                        vk.messages.send(user_id=id,
                                         message=f"{'Вы не прошли тест' if not result else 'Нужно предыдущее образование'}",
                                         keyboard=keyboard,
                                         random_id=random.randint(0, 2 ** 64))
                elif response == 'Высшее профессиональное образование' and educ == 'Высшее образование':
                    result = test4()
                    if result:
                        user.education = 'Высшее профессиональное образование'
                        session.commit()
                        return game_process(user_id, id)
                    else:
                        vk.messages.send(user_id=id,
                                         message=f"{'Вы не прошли тест' if not result else 'Нужно предыдущее образование'}",
                                         keyboard=keyboard,
                                         random_id=random.randint(0, 2 ** 64))
                elif response == 'Вернуться назад':
                    return game_process(user_id, id)
                else:
                    vk.messages.send(user_id=id, message="Попробуй снова.", keyboard=keyboard,
                                     random_id=random.randint(0, 2 ** 64))
    except Exception:
        print('\033[31mОшибка, пытаемся перезапуститься...\033[0m')
        return enter(id)


def ugodaika(user_id, id):
    vk = vk_session.get_api()
    session = db_session.create_session()
    user = session.query(User).filter(User.id == user_id).first()
    keyboard = create_keyboard('back')
    _sum = 100
    vk.messages.send(user_id=id, message="!!!Внимание!!!"
                                         "\nЗа игру снимаються деньги с игрового счёта!", keyboard=keyboard,
                     random_id=random.randint(0, 2 ** 64))
    vk.messages.send(user_id=id, message="Введите сумму(мин. = 100): ", keyboard=keyboard,
                     random_id=random.randint(0, 2 ** 64))
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                log(event.obj.message['from_id'], event.obj.message['text'])
                response = event.obj.message['text']
                if str(response).isdigit():
                    _sum = int(response)
                    user.money -= _sum
                    break
                elif response == 'Вернуться назад':
                    return kasino(user_id, id)
                else:
                    vk.messages.send(user_id=id, message="Сумма меньше 100!\nВведите больше:", keyboard=keyboard,
                                     random_id=random.randint(0, 2 ** 64))
        session.commit()
        right = random.randint(1, 3)
        keyboard = create_keyboard('ugodaika')
        vk.messages.send(user_id=id, message="Угадай цифру!", keyboard=keyboard,
                         random_id=random.randint(0, 2 ** 64))
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                log(event.obj.message['from_id'], event.obj.message['text'])
                response = event.obj.message['text']
                try:
                    if response == 'Вернуться назад':
                        log(event.obj.message['from_id'], event.obj.message['text'])
                        return kasino(user_id, id)
                    elif int(response) == right:
                        vk.messages.send(user_id=id, message=f"Правильно, ты заработал {math.ceil(_sum * 1.5)} руб.",
                                         keyboard=keyboard,
                                         random_id=random.randint(0, 2 ** 64))
                        user.money += math.ceil(_sum * 1.5)
                        session.commit()
                        return ugodaika(user_id, id)
                    else:
                        vk.messages.send(user_id=id, message=f"Неправильно! Правильно: {right}",
                                         random_id=random.randint(0, 2 ** 64))
                        return ugodaika(user_id, id)
                except Exception:
                    vk.messages.send(user_id=id, message="Неправильно!",
                                     random_id=random.randint(0, 2 ** 64))
                    return ugodaika(user_id, id)
    except Exception:
        print('\033[31mОшибка, пытаемся перезапуститься...\033[0m')
        return enter(id)


def kasino(user_id, id):
    vk = vk_session.get_api()
    session = db_session.create_session()
    user = session.query(User).filter(User.id == user_id).first()
    keyboard = create_keyboard('kazino')
    vk.messages.send(user_id=id, message="Выбирай", keyboard=keyboard,
                     random_id=random.randint(0, 2 ** 64))
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                response = event.obj.message['text']
                if response == 'Мой счёт':
                    log(event.obj.message['from_id'], event.obj.message['text'])
                    vk.messages.send(user_id=id, message=f"На данный момент ваш счёт составляет: {user.money}",
                                     keyboard=keyboard,
                                     random_id=random.randint(0, 2 ** 64))
                elif response == 'Угодайка':
                    log(event.obj.message['from_id'], event.obj.message['text'])
                    return ugodaika(user_id, id)
                elif response == 'Вернуться назад':
                    log(event.obj.message['from_id'], event.obj.message['text'])
                    return game_process(user_id, id)
                else:
                    vk.messages.send(user_id=id, message="Такой функции нет.", keyboard=keyboard,
                                     random_id=random.randint(0, 2 ** 64))
    except Exception:
        print('\033[31mОшибка, пытаемся перезапуститься...\033[0m')
        return enter(id)


def game_process(user_id, id, rerun=False):
    if rerun:
        print('Робит')
    vk = vk_session.get_api()
    keyboard = create_keyboard('main_menu')
    vk.messages.send(user_id=id, message="Выбирай", keyboard=keyboard,
                     random_id=random.randint(0, 2 ** 64))
    session = db_session.create_session()
    user = session.query(User).filter(User.id == user_id).first()
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                log(event.obj.message['from_id'], event.obj.message['text'])
                message = event.obj.message['text']
                if message == 'Обо мне':
                    session = db_session.create_session()
                    user = session.query(User).filter(User.id == user_id).first()
                    cars = ', '.join(user.garage.split(';')[1].split(', ')) if user.garage.split(';')[
                                                                                   0] == 'True' else 'нет'
                    vk.messages.send(user_id=id,
                                     message=f"Ваше имя: {user.name}\nВаша фамилия: {user.surname}"
                                             f"\nВаша почта: {user.email}\nУ вас: {user.money} рублей"
                                             f"\nВы работаете: {user.profession.split(';')[1] if user.profession.split(';')[0] == 'True' else 'никем'}\nВы получаете: {user.zarplata} рублей"
                                             f"\nВаш дом: {user.home.split(';')[1] if user.home.split(';')[0] == 'True' else 'нет'}"
                                             f"\nВаш гараж: {user.garage.split(';')[1] if user.garage.split(';')[0] == 'True' else 'нет'}"
                                             f"\nВаши машины: {cars}"
                                             f"\nВаше образование: {user.education}",
                                     keyboard=keyboard,
                                     random_id=random.randint(0, 2 ** 64))
                elif message == 'Выход':
                    user.enter = 'False'
                    session.commit()
                    return main(-1, id)
                elif message == 'Образование':
                    education(id, user_id)
                elif message == 'Kasino':
                    kasino(user_id, id)
                elif message == 'Работа':
                    body_job(user_id, id)
                elif message == 'БАНК':
                    bank(user_id, id)
                elif user.role == 'admin' and message == 'ADMIN':
                    pass
                else:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message="Такой команды пока нет.",
                                     random_id=random.randint(0, 2 ** 64))
    except Exception:
        print('\033[31mОшибка, пытаемся перезапуститься...\033[0m')
        return game_process(user_id, id, True)


if __name__ == '__main__':
    try:
        main(0)
    except Exception:
        print('\033[35mОшибка, мы не смогли решить её.\033[0m')
