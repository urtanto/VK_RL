import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from vk_api.keyboard import VkKeyboard
from flask import request
from data.users import User
from data import db_session

db_session.global_init("db/users.sqlite")
token = open('static/token.txt', mode='rt').read().split('\n')[0]
vk_session = vk_api.VkApi(token=token)
longpoll = VkBotLongPoll(vk_session, 195353132)
keyboards = {'login': [True,
                       ["Войти", 'POSITIVE'],
                       'Line',
                       ["Зарегистрироваться", 'DEFAULT']],
             'вход': [False, ["Зарегистрироваться", 'DEFAULT']],
             'main_menu': [False, ['Обо мне', 'DEFAULT']]}


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
    keyboard = create_keyboard('вход')
    vk = vk_session.get_api()
    vk.messages.send(user_id=id, message="Введите почту:", keyboard=keyboard, random_id=random.randint(0, 2 ** 64))
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            post = event.obj.message['text']
            session = db_session.create_session()
            if post in session.query(User).all():
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
                return main(1, id)
            elif password == 'Зарегистрироваться':
                return register(id)
            else:
                vk.messages.send(user_id=id, message="Не правильный пароль!\nВведите пароль:", keyboard=keyboard,
                                 random_id=random.randint(0, 2 ** 64))


def register(id):
    vk = vk_session.get_api()
    vk.messages.send(user_id=id, message="Регистрация:",
                     random_id=random.randint(0, 2 ** 64))


def main(*func):
    vk = vk_session.get_api()
    if func[0] == 1:
        keyboard = create_keyboard('main_menu')
        vk.messages.send(user_id=func[1], message="Привет",
                         keyboard=keyboard, random_id=random.randint(0, 2 ** 64))
    elif func[0] == 0:
        print('Robit')
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
                    keyboard = create_keyboard('login')
                    vk.messages.send(user_id=event.obj.message['from_id'], message="Привет", keyboard=keyboard,
                                     random_id=random.randint(0, 2 ** 64))
                if event.obj.message['from_id'] in [463771138, 0] and response.lower() == 'ADMIN':
                    pass


if __name__ == '__main__':
    main(0)
