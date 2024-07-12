import psycopg2

from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.methods.forward_message import ForwardMessage

import app.fun_button as kb
from config import BOT_TOKEN, host, user, password, dbname

router = Router()
bot = Bot(token=BOT_TOKEN)

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=dbname
        )
        conn.autocommit = True
        cur = conn.cursor()

        print('PostgreSQL database version:')
        cur.execute('SELECT version()')


        db_version = cur.fetchone()
        print(db_version)

        return conn
        # display the PostgreSQL database server version

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


connection = connect()
connection.autocommit = True
cur = connection.cursor()


@router.message(Command('start'))
async def start_handler(message: Message):
    
    cur.execute('SELECT * FROM users WHERE chat_id = %s', [str(message.chat.id)])#проверка на то что зарегестрирован пользователь или нет
    if cur.fetchone():
        await message.answer('Здраствуйте вот доступный функционал', reply_markup=kb.user_menu)#если пользователь зарегестрирован то ему предлягается выбрать действие
    else:
        await message.answer("Привет! Я бот-помошник IT-отдела компании ..., чем я могу помочь вам?", reply_markup=kb.register_button)


#регистрация пользователя с помощью кода
class register(StatesGroup):
    code = State()
    text = State()

@router.callback_query(F.data == 'riec_registrate')
async def registrate(callback: CallbackQuery, state: FSMContext):
    await state.set_state(register.code)
    await callback.message.answer("Пожалуйста напишите ваш код")

@router.message(register.code)
async def registrate(message: Message, state: FSMContext):
    await state.update_data(code=message.text)

    cur.execute('SELECT * FROM users WHERE verification_code = %s', [message.text])#поиск кода в таблице если он есть то id чата сохраняют для того что бы не регистрироватся вновь
    if cur.fetchone():
        await message.answer('Добро пожаловать', reply_markup=kb.user_menu)
        cur.execute('UPDATE users SET chat_id = %s WHERE verification_code = %s', [str(message.chat.id), message.text])
    else:
        await message.answer('Вы не зарегестрированы обратитеть к администратору для уточнения')

@router.callback_query(F.data == 'riec_registrate')
async def registrate(callback: CallbackQuery, state: FSMContext):
    await state.set_state(register.code)
    await callback.message.answer(f"Пожалуйста напишите ваш код из РИЕС")

#уголок сотрудника
@router.message(F.text == 'Что умеет бот?')
async def help(message: Message):
    await message.answer('Этот бот предназначен для оставления заявки о технических неполадках, если у вас взникла проблема нажмите на кнопку "оставить заявку", если хотите посмотреть статус оставленых заявок нажмите на "мои заявки"')

@router.message(F.text == 'Оставить заявку')
async def application_group(message: Message):
    await message.answer('Выберите вашу проблему', reply_markup=kb.application_list)

@router.callback_query(F.data == 'error_group')
async def application_description(callback: CallbackQuery, state: FSMContext):
    await state.set_state(register.text)
    await callback.message.answer('Опишите вашу проблему')

@router.message(register.text)
async def application_text(message: Message, state:FSMContext):
    print(message.chat.id, message.message_id)

    await bot.forward_message(chat_id=5941107646,
                            from_chat_id=5941107646,
                            message_id=199)