import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from smtplib import SMTP

vk_session = vk_api.VkApi(token='1d6272d37a0861f7ab22be95d9cc244d3d8a39ba975dc3ada21eaeb4e2632f438daf1f4ad06d741632837')
longpoll = VkBotLongPoll(vk_session, 195353132)
keyboards = {'начать': [False, []]}


def create_keyboard():
    keyboard = vk_api.keyboard.VkKeyboard(one_time=False)
    # False Если клавиатура должна оставаться откртой после нажатия на кнопку
    # True если она должна закрваться
    # DEFAULT = белый
    # POSITIVE = зелёный
    # NEGATIVE = красный
    # PRIMARY = синий
    keyboard.add_button("Привет", color=vk_api.keyboard.VkKeyboardColor.DEFAULT)
    keyboard.add_button("Кнопка", color=vk_api.keyboard.VkKeyboardColor.POSITIVE)
    keyboard.add_line()  # Обозначает добавление новой строки
    keyboard.add_button("Начать", color=vk_api.keyboard.VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button("Закрыть", color=vk_api.keyboard.VkKeyboardColor.PRIMARY)
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
            keyboard = create_keyboard()
            empty_keyboard = create_empty_keyboard()
            vk = vk_session.get_api()
            if event.from_user:
                if response.lower() == "привет":
                    vk.messages.send(peer_id=event.obj.peer_id or event.message.peer_id, message="Приветики",
                                     keyboard=keyboard, random_id=0)
                elif response.lower() == "начать":
                    vk.messages.send(peer_id=event.obj.peer_id or event.message.peer_id, message="Начинаем",
                                     keyboard=keyboard, random_id=0)
                elif response.lower() == "закрыть":
                    vk.messages.send(peer_id=event.obj.peer_id or event.message.peer_id, message="Закрываем",
                                     keyboard=empty_keyboard, random_id=0)


if __name__ == '__main__':
    main()
