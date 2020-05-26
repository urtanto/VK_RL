import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from vk_api.keyboard import VkKeyboard

token = open('static/token.txt', mode='rt').read().split('\n')[0]
vk_session = vk_api.VkApi(token=token)
longpoll = VkBotLongPoll(vk_session, 195353132)
keyboards = {'начать': [False,
                        ["Привет", 'DEFAULT'],
                        ["Кнопка", 'POSITIVE'],
                        'Line',
                        ["Закрыть", 'NEGATIVE']],
             'закрыть': [False, ["Закрыть", 'NEGATIVE']]}


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
        print(i)
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
        print('+')
    # keyboard.add_line()  # Обозначает добавление новой строки
    # keyboard = vk_api.keyboard.VkKeyboard(one_time=False)
    # keyboard.add_button(keyboards[text][1][0], color=vk_api.keyboard.VkKeyboardColor.DEFAULT)
    return keyboard.get_keyboard()


def create_empty_keyboard():
    keyboard = vk_api.keyboard.VkKeyboard.get_empty_keyboard()
    return keyboard
    # Эта функция используется для закрытия клавиатуры


def main():
    print('We start')
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            print('Новое сообщение:')
            print('Для меня от:', event.obj.message['from_id'])
            print('Текст:', event.obj.message['text'])
            response = event.message.text.casefold()
            vk = vk_session.get_api()
            if event.from_user:
                if response.lower() == "привет":
                    keyboard = create_keyboard('начать')
                    vk.messages.send(user_id=event.obj.message['from_id'], message="Привет",
                                     keyboard=keyboard, random_id=random.randint(0, 2 ** 64))
                elif response.lower() == "начать":
                    keyboard = create_keyboard(response.lower())
                    vk.messages.send(user_id=event.obj.message['from_id'], message="Начинаем",
                                     keyboard=keyboard, random_id=random.randint(0, 2 ** 64))
                elif response.lower() == "закрыть":
                    empty_keyboard = create_empty_keyboard()
                    vk.messages.send(user_id=event.obj.message['from_id'], message="Пока",
                                     keyboard=empty_keyboard, random_id=random.randint(0, 2 ** 64))
                else:
                    keyboard = create_keyboard('начать')
                    vk.messages.send(user_id=event.obj.message['from_id'], message="Начинаем", keyboard=keyboard, random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()
