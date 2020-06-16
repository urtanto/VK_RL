from vkbottle import Bot, Message
from smtplib import SMTP
import datetime
import random
from main_folder.data.users import User
from main_folder.data import db_session
import math
from vk_api.keyboard import VkKeyboard
import vk_api
import vkbottle

token = open('static/token.txt', mode='rt').read().split('\n')[0]
furs = ['Volvo FM']
db_session.global_init("db/users.sqlite")
bot = Bot(token)
keyboards = {'main_menu': [False, ['Обо мне', 'DEFAULT'],
                           ['Учиться', 'DEFAULT'],
                           ['Работа', 'DEFAULT'],
                           'Line',
                           ['Дом', 'PRIMARY'],
                           ['Гараж', 'PRIMARY'],
                           ['Машины', 'PRIMARY'],
                           'Line',
                           ['Kasino', 'POSITIVE'],
                           ['БАНК', 'POSITIVE'],
                           ['Vladito', 'POSITIVE']],
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


@bot.on.message_handler(text='<s1>Привет<s2>', lower=True)
async def wrapper(ans: Message, s1, s2):
    session = db_session.create_session()
    if int(ans.from_id) in [el.vk for el in session.query(User).filter(User.id != '').all()]:
        session = db_session.create_session()
        user = session.query(User).filter(User.vk == ans.from_id).first()
        user.keyboard = 'main_menu'
        user.now = 'main_menu'
        money_earn(user.vk)
        session.commit()
    else:
        session = db_session.create_session()
        user = User()
        user.money = 100
        user.zarplata = 0
        user.home = 'False'
        user.cars = 'False'
        user.garage = 'False'
        user.education = 'Основное общее образование'
        user.profession = 'False'
        user.enter = 'True'
        user.vk = ans.from_id
        user.ban = 'False'
        user.role = 'user'
        user.keyboard = 'main_menu'
        user.learning = 'False'
        user.working = 'False'
        user.now = 'main_menu'
        user.last_date = datetime.date.today()
        session.add(user)
        session.commit()
    await ans("Выбирай:", keyboard=create_keyboard('main_menu'))


@bot.on.message_handler(text='<s1>Начать<s2>', lower=True)
async def begin(ans: Message, s1, s2):
    session = db_session.create_session()
    if int(ans.from_id) in [el.vk for el in session.query(User).filter(User.id != '').all()]:
        session = db_session.create_session()
        user = session.query(User).filter(User.vk == ans.from_id).first()
        user.now = 'main_menu'
        user.keyboard = 'main_menu'
        money_earn(user.vk)
        session.commit()
    else:
        session = db_session.create_session()
        user = User()
        user.money = 100
        user.zarplata = 0
        user.home = 'False'
        user.cars = 'False'
        user.now = 'main_menu'
        user.garage = 'False'
        user.education = 'Основное общее образование'
        user.profession = 'False'
        user.enter = 'True'
        user.vk = ans.from_id
        user.ban = 'False'
        user.role = 'user'
        user.keyboard = 'main_menu'
        user.learning = 'False'
        user.working = 'False'
        user.last_date = datetime.date.today()
        session.add(user)
        session.commit()
    await ans("Выбирай:", keyboard=create_keyboard('main_menu'))


@bot.on.message_handler(text='Обо мне', lower=False)
async def about(ans: Message):
    session = db_session.create_session()
    if int(ans.from_id) in [el.vk for el in session.query(User).filter(User.id != '').all()]:
        money_earn(ans.from_id)
    else:
        session = db_session.create_session()
        user = User()
        user.money = 100
        user.zarplata = 0
        user.home = 'False'
        user.cars = 'False'
        user.now = 'main_menu'
        user.garage = 'False'
        user.education = 'Основное общее образование'
        user.profession = 'False'
        user.enter = 'True'
        user.vk = ans.from_id
        user.ban = 'False'
        user.role = 'user'
        user.keyboard = 'main_menu'
        user.learning = 'False'
        user.working = 'False'
        user.last_date = datetime.date.today()
        session.add(user)
        session.commit()
    session = db_session.create_session()
    user = session.query(User).filter(User.vk == ans.from_id).first()
    user.now = 'main_menu'
    user.keyboard = 'main_menu'
    session.commit()
    user = session.query(User).filter(User.vk == ans.from_id).first()
    cars = ', '.join(user.garage.split(';')[1].split(', ')) if user.garage.split(';')[
                                                                   0] == 'True' else 'нет'
    await ans(f"Лежит в банке: {user.money} рублей"
              f"\nВы работаете: {user.profession.split(';')[1] if user.profession.split(';')[0] == 'True' else 'никем'}\nВы получаете: {user.zarplata} рублей"
              f"\nВаш дом: {user.home.split(';')[1] if user.home.split(';')[0] == 'True' else 'нет'}"
              f"\nВаш гараж: {user.garage.split(';')[1] if user.garage.split(';')[0] == 'True' else 'нет'}"
              f"\nВаши машины: {cars}"
              f"\nВаше образование: {user.education}", keyboard=create_keyboard('main_menu'))


@bot.on.message_handler(text='Работа', lower=False)
async def robita(ans: Message):
    session = db_session.create_session()
    if int(ans.from_id) in [el.vk for el in session.query(User).filter(User.id != '').all()]:
        money_earn(ans.from_id)
    else:
        session = db_session.create_session()
        user = User()
        user.money = 100
        user.zarplata = 0
        user.home = 'False'
        user.cars = 'False'
        user.now = 'main_menu'
        user.garage = 'False'
        user.education = 'Основное общее образование'
        user.profession = 'False'
        user.enter = 'True'
        user.vk = ans.from_id
        user.ban = 'False'
        user.role = 'user'
        user.keyboard = 'main_menu'
        user.learning = 'False'
        user.working = 'False'
        user.last_date = datetime.date.today()
        session.add(user)
        session.commit()
    session = db_session.create_session()
    user = session.query(User).filter(User.vk == ans.from_id).first()
    user.now = 'main_job'
    user.keyboard = 'main_job'
    session.commit()
    await ans('Здраствуй, выбирай:', keyboard=create_keyboard('main_job'))


@bot.on.message_handler(text='Вернуться назад', lower=True)
async def back(ans: Message):
    session = db_session.create_session()
    if int(ans.from_id) in [el.vk for el in session.query(User).filter(User.id != '').all()]:
        money_earn(ans.from_id)
    else:
        session = db_session.create_session()
        user = User()
        user.money = 100
        user.zarplata = 0
        user.home = 'False'
        user.cars = 'False'
        user.now = 'main_menu'
        user.garage = 'False'
        user.education = 'Основное общее образование'
        user.profession = 'False'
        user.enter = 'True'
        user.vk = ans.from_id
        user.ban = 'False'
        user.role = 'user'
        user.keyboard = 'main_menu'
        user.learning = 'False'
        user.working = 'False'
        user.last_date = datetime.date.today()
        session.add(user)
        session.commit()
    session = db_session.create_session()
    user = session.query(User).filter(User.vk == ans.from_id).first()
    if user.now == 'main_menu':
        pass
    elif user.now == 'main_job':
        user.now = 'main_menu'
        user.keyboard = 'main_menu'
        session.commit()
    elif user.now == 'working':
        user.now = 'main_job'
        user.keyboard = 'main_job'
        session.commit()
    elif user.now == 'job':
        user.now = 'main_job'
        user.keyboard = 'main_job'
        session.commit()
    user = session.query(User).filter(User.vk == ans.from_id).first()
    await ans('Здраствуй, выбирай:', keyboard=create_keyboard(user.keyboard))


@bot.on.message_handler(text='Сменить профессию', lower=True)
async def job_change(ans: Message):
    global furs
    session = db_session.create_session()
    if int(ans.from_id) in [el.vk for el in session.query(User).filter(User.id != '').all()]:
        money_earn(ans.from_id)
    else:
        session = db_session.create_session()
        user = User()
        user.money = 100
        user.zarplata = 0
        user.home = 'False'
        user.cars = 'False'
        user.now = 'main_menu'
        user.garage = 'False'
        user.education = 'Основное общее образование'
        user.profession = 'False'
        user.enter = 'True'
        user.vk = ans.from_id
        user.ban = 'False'
        user.role = 'user'
        user.keyboard = 'main_menu'
        user.learning = 'False'
        user.working = 'False'
        user.last_date = datetime.date.today()
        session.add(user)
        session.commit()
    session = db_session.create_session()
    user = session.query(User).filter(User.vk == ans.from_id).first()
    user.now = 'job'
    user.keyboard = 'job'
    session.commit()
    session = db_session.create_session()
    keyboard = create_keyboard('job')
    await ans("Кем хотите работать?\n"
              "Для ГРУЗЧИКА(20 тыс.) нужно иметь: Основное общее образование\n"
              "Для ТАКСИСТА(30 тыс.) нужно иметь: Машина\n"
              "Для БАНКИРА(50 тыс.) нужно иметь: Среднее общее образование\n"
              "Для СВАРЩИКА(100 тыс.) нужно иметь: Среднее профессиональное образование\n"
              "Для ДАЛЬНОБОЙЩИКА(300 тыс.) нужно иметь: тягач/фура\n"
              "Для ДЕПУТАТА(300 тыс.) нужно иметь: Высшее образование\n"
              "Для ПРОГРАММИСТА(500 тыс.) нужно иметь: Высшее профессиональное образование, дом\n",
              keyboard=keyboard)


@bot.on.message_handler(text='Грузчик', lower=True)
async def gruzchik(ans: Message):
    session = db_session.create_session()
    if int(ans.from_id) in [el.vk for el in session.query(User).filter(User.id != '').all()]:
        money_earn(ans.from_id)
    else:
        session = db_session.create_session()
        user = User()
        user.money = 100
        user.zarplata = 0
        user.home = 'False'
        user.cars = 'False'
        user.now = 'main_menu'
        user.garage = 'False'
        user.education = 'Основное общее образование'
        user.profession = 'False'
        user.enter = 'True'
        user.vk = ans.from_id
        user.ban = 'False'
        user.role = 'user'
        user.keyboard = 'main_menu'
        user.learning = 'False'
        user.working = 'False'
        user.last_date = datetime.date.today()
        session.add(user)
        session.commit()
    session = db_session.create_session()
    user = session.query(User).filter(User.vk == ans.from_id).first()
    user.zarplata = 20000
    user.profession = 'True;Грузчик'
    session.commit()
    session = db_session.create_session()
    user = session.query(User).filter(User.vk == ans.from_id).first()
    user.now = 'main_job'
    user.keyboard = 'main_job'
    session.commit()
    await ans('Выбирай:', keyboard=create_keyboard(user.now))


@bot.on.message_handler(text='Таксист', lower=True)
async def taksist(ans: Message):
    session = db_session.create_session()
    if int(ans.from_id) in [el.vk for el in session.query(User).filter(User.id != '').all()]:
        money_earn(ans.from_id)
    else:
        session = db_session.create_session()
        user = User()
        user.money = 100
        user.zarplata = 0
        user.home = 'False'
        user.cars = 'False'
        user.now = 'main_menu'
        user.garage = 'False'
        user.education = 'Основное общее образование'
        user.profession = 'False'
        user.enter = 'True'
        user.vk = ans.from_id
        user.ban = 'False'
        user.role = 'user'
        user.keyboard = 'main_menu'
        user.learning = 'False'
        user.working = 'False'
        user.last_date = datetime.date.today()
        session.add(user)
        session.commit()
    session = db_session.create_session()
    user = session.query(User).filter(User.vk == ans.from_id).first()
    if user.cars.split(';')[0] == 'True':
        user.zarplata = 20000
        user.profession = 'True;Грузчик'
        session.commit()
        session = db_session.create_session()
        user = session.query(User).filter(User.vk == ans.from_id).first()
        user.now = 'main_job'
        user.keyboard = 'main_job'
        session.commit()
        await ans('Выбирай:', keyboard=create_keyboard(user.now))
    else:
        session = db_session.create_session()
        user = session.query(User).filter(User.vk == ans.from_id).first()
        user.now = 'job'
        user.keyboard = 'job'
        session.commit()
        await ans('У вас нет машины!', keyboard=create_keyboard(user.now))


@bot.on.message_handler(text='Работать', lower=True)
async def working(ans: Message):
    session = db_session.create_session()
    if int(ans.from_id) in [el.vk for el in session.query(User).filter(User.id != '').all()]:
        money_earn(ans.from_id)
    else:
        session = db_session.create_session()
        user = User()
        user.money = 100
        user.zarplata = 0
        user.home = 'False'
        user.cars = 'False'
        user.now = 'main_menu'
        user.garage = 'False'
        user.education = 'Основное общее образование'
        user.profession = 'False'
        user.enter = 'True'
        user.vk = ans.from_id
        user.ban = 'False'
        user.role = 'user'
        user.keyboard = 'main_menu'
        user.learning = 'False'
        user.working = 'False'
        user.last_date = datetime.date.today()
        session.add(user)
        session.commit()
    session = db_session.create_session()
    user = session.query(User).filter(User.vk == ans.from_id).first()
    user.now = 'working'
    user.keyboard = 'main_job'
    session.commit()
    keyboard = create_keyboard('back')
    letter = random.choice('qwertyuiopasdfghjklzxcvbnm')
    times = random.randint(10, 100)
    answer = letter * times
    session = db_session.create_session()
    user = session.query(User).filter(User.vk == ans.from_id).first()
    user.working = answer
    session.commit()
    await ans(f'Напиши букву(англ.): {letter}\nКоличество раз: {times}\nНапример: ooooo', keyboard=keyboard)


@bot.on.message_handler(text='<r>', lower=True)
async def dich(ans: Message, r):
    try:
        session = db_session.create_session()
        user = session.query(User).filter(User.vk == ans.from_id).first()
        if user.now == 'working':
            money_earn(ans.from_id)
            session = db_session.create_session()
            user = session.query(User).filter(User.vk == ans.from_id).first()
            user.now = 'main_job'
            session.commit()
            if user.working == r:
                user.money += user.zarplata
                session.commit()
                await ans(f"Правильно, ты заработал {user.zarplata} руб.", keyboard=create_keyboard('main_job'))
            else:
                await ans("Неправильно!", keyboard=create_keyboard('main_job'))
        else:
            money_earn(ans.from_id)
            await ans("Выбирай:", keyboard=create_keyboard('main_menu'))
    except Exception:
        session = db_session.create_session()
        user = User()
        user.money = 100
        user.zarplata = 0
        user.home = 'False'
        user.cars = 'False'
        user.garage = 'False'
        user.education = 'Основное общее образование'
        user.profession = 'False'
        user.enter = 'True'
        user.vk = ans.from_id
        user.ban = 'False'
        user.role = 'user'
        user.keyboard = 'main_menu'
        user.learning = 'False'
        user.working = 'False'
        user.now = 'main_menu'
        user.last_date = datetime.date.today()
        session.add(user)
        session.commit()
        await ans("Выбирай:", keyboard=create_keyboard('main_menu'))


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


if __name__ == "__main__":
    bot.run_polling()
