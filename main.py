import logging
import requests
from db import Database

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton ,InlineKeyboardMarkup
API_TOKEN = '1150143594:AAF7T-hFXFeN0NBRXPLx2qvi0MUnvSCUcow'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
channel_id = '-1001580138328'
db = Database('database.db')
admin = 693313498

def inline_buttons():
  channel_url = InlineKeyboardButton('Kanalimiz 🇺🇿🇷🇺', url='https://t.me/+civ30qIRsgMwM2Fi')
  check = InlineKeyboardButton('A\'zo boldim ✅' , callback_data='subdone')
  markup = InlineKeyboardMarkup(row_width=1).add(channel_url,check)
  return markup

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    if not db.user_exists(message.from_user.id):
      db.add_user(message.from_user.id)
    tekshir_obunani = await bot.get_chat_member(chat_id=channel_id , user_id=message.from_user.id)
    if tekshir_obunani['status'] == 'left':
      await message.answer('Telegram bot 5 ta tilni bemalol tarjima qila oladi \n Botdan foydalanish uchun kanalga obuna boling' , reply_markup=inline_buttons())
    elif tekshir_obunani['status'] == 'member':
      await message.answer(f"Assalomu Alaykum {message.from_user.first_name} \nHush kelibsiz bot sizga 5 ta tilda tarjima so\'zlar yuboradi \nIshlatish uchun biror so\'z yuboring")
    else:
      print(tekshir_obunani['status'], "else ishladi")

@dp.message_handler(commands=["sendall"])
async def sendall(message: types.Message):
    if message.chat.type == 'private':
      if message.from_user.id == admin:
        text = message.text[9:]
        users = db.get_users()
        print(sum(1 for line in users))
        for row in users:
          try:
            await bot.send_message(chat_id=row[0], text=text)
            if int(row[1]) !=1:
              db.set_active(user_id=row[0], active=1)
          except:
            db.set_active(user_id=row[0], active=0)
        await bot.send_message(chat_id=message.from_user.id, text="Xabar muvaffaqiyatli yuborildi.")

@dp.message_handler(commands=["stat"])
async def sendall(message: types.Message):
        users = db.get_users()
        son=sum(1 for line in users)
        await bot.send_message(chat_id=message.from_user.id, text=f"Botdagi obunachilar soni {son} ta")

@dp.callback_query_handler()
async def check_sub(callback: types.CallbackQuery):
      if callback.data =='subdone':
        tekshir_obunani = await bot.get_chat_member(chat_id=channel_id , user_id=callback.from_user.id )
        if tekshir_obunani['status'] == 'member':
          # print(tekshir_obunani['status'], 'if ishladi')
          await callback.message.answer(f"Assalomu Alaykum {callback.from_user.first_name} \nHush kelibsiz bot sizga 5 ta tilda tarjima so\'zlar yuboradi \nIshlatish uchun biror so\'z yuboring")
        elif callback.data == 'left':
          await callback.message.answer('Telegram bot 5 ta tilni bemalol tarjima qila oladi \n Botdan foydalanish uchun kanalga obuna boling' , reply_markup=inline_buttons())
          # print(tekshir_obunani['status'], 'elif ishladi')

        else:
          # print(tekshir_obunani['status'])
          await callback.message.answer('Telegram bot 5 ta tilni bemalol tarjima qila oladi \n Botdan foydalanish uchun kanalga obuna boling' , reply_markup=inline_buttons())

    
    
    # await bot.send_video(chat_id=message.from_user.id , video="http://n197.uzdown.space/download/serial/lutsi/uzmovi.com lutsferr 57 mob hd.mp4")



@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)
  try:
    tekshir_obunani = await bot.get_chat_member(chat_id=channel_id , user_id=message.from_user.id)
    if tekshir_obunani['status'] == 'member':
      txt = message.text
      r = requests.get(f"https://trans.noxi8.repl.co/uz/text={txt}")
      response = r.json()['text']

      resru = requests.get(f"https://trans.noxi8.repl.co/ru/text={txt}")
      ru = resru.json()['text']

      reseng = requests.get(f"https://trans.noxi8.repl.co/en/text={txt}")
      eng = reseng.json()['text']

      resar = requests.get(f"https://trans.noxi8.repl.co/ar/text={txt}")
      arab = resar.json()['text']
      
      resturk = requests.get(f"https://trans.noxi8.repl.co/tt/text={txt}")
      turk = resturk.json()['text']
      await message.answer(f"Uzbek tilidagi tarjima👇🏻`\n{response}`", parse_mode="Markdown")
      await message.answer(f'Rus tilidagi tarjima 👇🏻\n`{ru}`', parse_mode="Markdown")
      await message.answer(f'\nIngliz tilidagi tarjima 👇🏻\n`{eng}`', parse_mode="Markdown")
      await message.answer(f'Arab tilidagi tarjima 👇🏻\n`{arab}`', parse_mode="Markdown")
      await message.answer(f'Turk tilidagi tarjima 👇🏻\n`{turk}`', parse_mode="Markdown")
    else:
      await message.answer('Telegram bot 5 ta tilni bemalol tarjima qila oladi \n Botdan foydalanish uchun kanalga obuna boling' , reply_markup=inline_buttons())

  except Exception as e:
    print(e, "Exception ishlamoqda")
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)