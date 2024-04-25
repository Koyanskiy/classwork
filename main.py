import asyncio
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, BotCommand, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command

bot = Bot(token="6627111140:AAEu5m5sliiFQjlixZW94S29n8Jtfh3yQDc")
dp = Dispatcher()
router = Router()

@router.message(Command('start'))
async def start_handler(msg:Message):
   await bot.set_my_commands([
        BotCommand(command='start', description = "Запуск"),
        BotCommand(command='help', description = "Справка"),
        BotCommand(command='delete', description = "Очистить"),
   ])

   inline_markup = InlineKeyboardMarkup(inline_keyboard=[
      [InlineKeyboardButton(text='Далее', callback_data='next')]
   ])
   await msg.answer(text="1", reply_markup=inline_markup)

@router.callback_query(F.data == 'next')
async def next_handler(callback_query: CallbackQuery):
   inline_markup = InlineKeyboardMarkup(inline_keyboard=[
      [InlineKeyboardButton(text='Назад', callback_data='back')]
   ])
   await callback_query.message.edit_text(
      '2', reply_markup=inline_markup)

@router.callback_query(F.data == 'back')
async def next_handler(callback_query: CallbackQuery):
   inline_markup = InlineKeyboardMarkup(inline_keyboard=[
      [InlineKeyboardButton(text='Далее', callback_data='next')]
   ])
   await callback_query.message.delete()
   await callback_query.message.answer(
      text="1",
      reply_markup=inline_markup)

async def main():
    await dp.start_polling(bot)

dp.include_routers(router)

if __name__ == '__main__':
   asyncio.run(main())