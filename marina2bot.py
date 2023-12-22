from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import BotBlocked, ChatNotFound, UserDeactivated, CantInitiateConversation
import asyncio
import sqlite3
import random


class hello(StatesGroup):
    q = State()
    q1 = State()

ADMIN_ID = 5973892795
content = -1001597597158
supergroup = -1001985070992
share_link = "https://t.me/share/url?url=https://t.me/joinchat/gIqB5Zd0fvhhYmQ6"

db = sqlite3.connect('server.db')
sql = db.cursor()

bot = Bot(token='6005148898:AAENK8jrzGiabeNsknrjApOjk5Zeo6dJ_hA')
dp = Dispatcher(bot, storage=MemoryStorage())


class hello(StatesGroup):
    q = State()
    q1 = State()


def add_user(id='1'):
    sql.execute(f"SELECT id FROM user WHERE id = {id}")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO user VALUES (?,?)", (id, '1'))
        db.commit()


@dp.message_handler(commands=['start'])
async def process_admin_command(message: types.Message):
    try:
        add_user(message.from_user.id)
        if random.randint(1,5) == 3:
            await bot.copy_message(chat_id=message.from_user.id, from_chat_id=content, message_id=57,
                                   caption=f"""{message.from_user.first_name}, Welcome to my channel:
    https://t.me/+woqiFsC-8ypjYzIy""")
        else:
            m = types.InlineKeyboardMarkup().add()
            m.add(types.InlineKeyboardButton(text='SHARE THE LINK', url=share_link))

            await bot.send_message(chat_id=message.from_user.id, text=f"""<b>My group is closed from unauthorized persons, share the link 3 times and click /start to access my group</b>""",parse_mode="html", reply_markup=m)
    except:
        pass




@dp.message_handler(commands=['trafik'])
async def process_admin_command(message: types.Message):
    if message.chat.id == ADMIN_ID:
        db = sqlite3.connect('server.db')
        sql = db.cursor()
        a = sql.execute(f'SELECT COUNT(*) FROM user').fetchone()[0]
        await bot.send_message(message.chat.id, f'Users: {a}')


@dp.message_handler(commands=['send_db'])
async def process_admin_send_db(message: types.Message):
    if message.chat.id == ADMIN_ID:
        a = open('server.db', 'rb')
        await bot.send_document(chat_id=message.chat.id, document=a)


@dp.message_handler(commands=['send_users'])
async def process_admin_command(message: types.Message):
    if message.chat.id == ADMIN_ID:
        await hello.q.set()
        await bot.send_message(message.chat.id, f'Отправь пост для рассылки')


@dp.message_handler(state=hello.q, content_types=['text', 'photo', 'video', 'video_note', 'voice'])
async def process_sends_command(message: types.Message, state: FSMContext):
    if message.chat.id == ADMIN_ID:
        await state.finish()
        db = sqlite3.connect('server.db')
        sql = db.cursor()
        users = sql.execute("SELECT id FROM user").fetchall()
        await bot.send_message(message.chat.id, f'Go to {len(users)}')
        d = 0
        g = 0
        for i in users:
            await asyncio.sleep(0.06)
            try:
                try:
                    await message.copy_to(i[0])
                    g += 1
                except (BotBlocked, ChatNotFound, UserDeactivated, CantInitiateConversation):
                    try:
                        sql.execute(f'DELETE FROM user WHERE id = {i[0]}')
                        db.commit()
                        d += 1

                    except:
                        pass
            except:
                pass

        await bot.send_message(message.chat.id, f"""Отправлено: {g} \nУдалено: {d}""")



@dp.chat_join_request_handler()
async def join(update: types.ChatJoinRequest):
    try:
        add_user(update.from_user.id)
        m = types.InlineKeyboardMarkup().add()
        m.add(types.InlineKeyboardButton(text='SHARE THE LINK', url=share_link))

        await bot.copy_message(chat_id=update.from_user.id, from_chat_id=content, message_id=57, caption=f"""{update.from_user.first_name} , my love 🥰 This photo is especially for you 💕
    
    <b>My group is closed from unauthorized persons, share the link 3 times and click /start to access my group</b>""",parse_mode="html",reply_markup=m)
    except:
        pass

    try:
        await update.approve()
    except:
        pass



async def write_one_s():
    while True:
        try:
            m = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text='SHARE LINK ', url=share_link))
            mes_id = await bot.send_message(chat_id=supergroup, text="""Are you there?
    
Share the link 3 times to get access to nudes 👇🏻""", reply_markup=m)
            await asyncio.sleep(random.randint(40,70))
            await bot.delete_message(chat_id=supergroup, message_id=mes_id.message_id)
            await asyncio.sleep(random.randint(4, 11))

        except:
            pass


async def on_bot_start_up(dispatcher) -> None:
    sql.execute(""" CREATE TABLE IF NOT EXISTS user (id BIGINT,login) """)
    db.commit()
    asyncio.create_task(write_one_s())


executor.start_polling(dp, skip_updates=True, on_startup=on_bot_start_up)
