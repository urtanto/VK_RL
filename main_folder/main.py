from smtplib import SMTP

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from vk_api.keyboard import VkKeyboard
from flask import request
from main_folder.data.users import User
from main_folder.data import db_session

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
             'Отмена регистрации': [False,
                                    ['Отмена', 'NEGATIVE']]}


def mail(mail):  # отправка кода на почту
    number = random.randint(1000, 9999)
    smtpObj = SMTP('smtp.gmail.com', port=587)
    smtpObj.starttls()
    smtpObj.login('vns.social.networks@gmail.com', 'dkflxvje`,jr')
    smtpObj.sendmail("vns.social.networks@gmail.com", mail, str(number))
    smtpObj.quit()
    return number


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


def enter(id):
    session = db_session.create_session()
    user = session.query(User).filter(User.vk == id).first()
    if user.enter == 'True':
        game_process(user.id, id)
    else:
        keyboard = create_keyboard('вход')
        vk = vk_session.get_api()
        vk.messages.send(user_id=id, message="Введите почту:", keyboard=keyboard, random_id=random.randint(0, 2 ** 64))
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
        vk.messages.send(user_id=id, message="Введите пароль:", keyboard=keyboard, random_id=random.randint(0, 2 ** 64))
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                password = event.obj.message['text']
                if password == user.password:
                    user.enter = 'True'
                    session.commit()
                    return game_process(user.id, id)
                elif password == 'Зарегистрироваться':
                    return register(id)
                else:
                    vk.messages.send(user_id=id, message="Не правильный пароль!\nВведите пароль:", keyboard=keyboard,
                                     random_id=random.randint(0, 2 ** 64))


def register(id):
    global keyboards
    keyboard = create_keyboard('Отмена регистрации')
    vk = vk_session.get_api()
    vk.messages.send(user_id=id, message="Регистрация:",
                     random_id=random.randint(0, 2 ** 64), keyboard=keyboard)
    vk.messages.send(user_id=id, message="Введите имя в игре:",
                     random_id=random.randint(0, 2 ** 64), keyboard=keyboard)
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
        if f:
            break
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
                    return enter(id)
                else:
                    for ev in longpoll.listen():
                        if ev.type == VkBotEventType.MESSAGE_NEW:
                            mess = ev.obj.message['text']
                            print(1)
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
    vk.messages.send(user_id=id,
                     message="Введите ваш пароль:",
                     random_id=random.randint(0, 2 ** 64), keyboard=keyboard)
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            password = event.obj.message['text']
            if event.obj.message['text'] == 'Отмена':
                return enter(id)
            break
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
    user.education = 'False'
    user.profession = 'no'
    user.enter = 'True'
    user.vk = id
    session.add(user)
    session.commit()
    return enter(id)


def main(*func):
    vk = vk_session.get_api()
    if func[0] == 1:
        keyboard = create_keyboard('main_menu')
        vk.messages.send(user_id=func[1], message="Привет",
                         keyboard=keyboard, random_id=random.randint(0, 2 ** 64))
    elif func[0] == 0:
        print('Robit')
    elif func[0] == -1:
        keyboard = create_keyboard('login')
        vk.messages.send(user_id=func[1], message="Привет",
                         keyboard=keyboard, random_id=random.randint(0, 2 ** 64))
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            print('Новое сообщение:')
            print('Для меня от:', event.obj.message['from_id'])
            print('Текст:', event.obj.message['text'])
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
                    vk.messages.send(user_id=event.obj.message['from_id'], message="Такой команды нет, попробуй снова.",
                                     random_id=random.randint(0, 2 ** 64))
                if event.obj.message['from_id'] in [463771138, 220401042] and response.lower() == 'ADMIN':
                    pass


def game_process(user_id, id):
    vk = vk_session.get_api()
    keyboard = create_keyboard('main_menu')
    vk.messages.send(user_id=id, message="Приветствуем тебя в нашей игре!", keyboard=keyboard,
                     random_id=random.randint(0, 2 ** 64))
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            message = event.obj.message['text']
            if message == 'Обо мне':
                session = db_session.create_session()
                user = session.query(User).filter(User.id == user_id).first()
                work = user.profession
                cars = '\n'.join(user.garage.split(';')[1].split(', ')) if user.garage.split(';')[
                                                                               0] == 'True' else 'нет'
                if work == 'no':
                    work = 'никем'
                vk.messages.send(user_id=id,
                                 message=f"Ваше имя: {user.name}\nВаша фамилия: {user.surname}"
                                         f"\nВаша почта: {user.email}\nУ вас: {user.money} рублей"
                                         f"\nВы работаете: {work}\nВы получаете: {user.zarplata} рублей"
                                         f"\nВаш дом: {user.home.split(';')[1] if user.home.split(';')[0] == 'True' else 'нет'}"
                                         f"\nВаш гараж: {user.garage.split(';')[1] if user.garage.split(';')[0] == 'True' else 'нет'}"
                                         f"\nВаши машины: {cars}"
                                         f"\nВаше образование: {user.education.split(';')[1] if user.education.split(';')[0] == 'True' else 'нет'}",
                                 keyboard=keyboard,
                                 random_id=random.randint(0, 2 ** 64))
            elif message == 'Выход':
                session = db_session.create_session()
                user = session.query(User).filter(User.id == user_id).first()
                user.enter = 'False'
                session.commit()
                return main(-1, id)
            else:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message="Такой команды пока нет, попробуй снова.",
                                 random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main(0)
