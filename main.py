import logging
import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton ,InlineKeyboardMarkup
API_TOKEN = '1150143594:AAF7T-hFXFeN0NBRXPLx2qvi0MUnvSCUcow'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
channel_id = '-1001580138328'

def inline_buttons():
  channel_url = InlineKeyboardButton('Kanalimiz', url='https://t.me/ruscha_toplam')
  check = InlineKeyboardButton('A\'zo boldim' , callback_data='subdone')
  markup = InlineKeyboardMarkup(row_width=1).add(channel_url,check)
  return markup

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    tekshir_obunani = await bot.get_chat_member(chat_id=channel_id , user_id=message.from_user.id)
    if tekshir_obunani['status'] != 'left':
      await message.reply(f"Assalomu Alaykum {message.from_user.first_name} \nHush kelibsiz bot sizga 3 ta tilda tarjima so\'zlar yuboradi \nIshlatish uchun biror so\'z yuboring")
    else:
      await message.reply('Telegram bot 3 ta tilni bemalol tarjima qila oladi \n Botdan foydalanish uchun kanalga obuna boling' , reply_markup=inline_buttons())
    
    @dp.callback_query_handler()
    async def check_sub(callback: types.CallbackQuery):
      if callback.data =='subdone':
        tekshir_obunani = await bot.get_chat_member(chat_id=channel_id , user_id=callback.message.from_user.id)
        if tekshir_obunani['status'] != 'left':
          await callback.message.reply(f"Assalomu Alaykum {callback.message.from_user.first_name} \nHush kelibsiz bot sizga 3 ta tilda tarjima so\'zlar yuboradi \nIshlatish uchun biror so\'z yuboring")
        else:
          await callback.message.reply('Telegram bot 3 ta tilni bemalol tarjima qila oladi \n Botdan foydalanish uchun kanalga obuna boling' , reply_markup=inline_buttons())
    
    
    
    # await bot.send_video(chat_id=message.from_user.id , video="http://n197.uzdown.space/download/serial/lutsi/uzmovi.com lutsferr 57 mob hd.mp4")



@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)
  try:
    txt = message.text
    r = requests.get(f"https://trans.noxi8.repl.co/uz/text={txt}")
    response = r.json()['text']
    resru = requests.get(f"https://trans.noxi8.repl.co/ru/text={txt}")
    ru = resru.json()['text']
    reseng = requests.get(f"https://trans.noxi8.repl.co/en/text={txt}")
    eng = reseng.json()['text']
    await message.reply(f"Uzbek tilidagi tarjima👇🏻`\n{response}`\nRus tilidagi tarjima 👇🏻\n`{ru}`\nIngliz tilidagi tarjima 👇🏻\n`{eng}`", parse_mode="Markdown")
    if response=="null":
      message.reply("Afsus tarjima qila olmadim !" )
  except Exception as e:
    print(e)
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)