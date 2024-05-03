import asyncio
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, BotCommand, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
bot = Bot(token="6627111140:AAEu5m5sliiFQjlixZW94S29n8Jtfh3yQDc")
dp = Dispatcher()
router = Router()

class Anketa(StatesGroup):
   name = State()
   age = State()
   gender = State()

@router.message(Command("anketa"))
async def anketa_handler(msg: Message, state: FSMContext):
   await state.set_state(Anketa.name)
   markup = InlineKeyboardMarkup(inline_keyboard=[[
      InlineKeyboardButton(text='Отмена', callback_data='cancel_anketa')
   ]])
   await msg.answer('Введите ваше имя:', reply_markup=markup)

@router.message(Command("anketa"))
async def cancel_handler(callbac_query: CallbackQuery, state: FSMContext):
   await state.clear()
   await callbac_query.message.answer('Регистрация отменена')

@router.message(Anketa.name)
async def set_age_anketa_handler(msg: Message, state: FSMContext):
   await state.update_data(name=msg.text)
   await state.set_state(Anketa.age)
   markup = InlineKeyboardMarkup(inline_keyboard=[[
      InlineKeyboardButton(text='Назад', callback_data='back_anketa'),
      InlineKeyboardButton(text='Отмена', callback_data='cancel_anketa'),
   ]])
   await msg.answer('Введите ваш возраст: ', reply_markup=markup)

@router.message(Anketa.age)
async def set_age_by_anketa_handler(msg: Message, state: FSMContext):
   try:
      await state.update_data(age=int(msg.text))
   except ValueError:
      await msg.answer('Вы неверно ввели возраст')
      markup = InlineKeyboardMarkup(inline_keyboard=[[
      InlineKeyboardButton(text='Назад', callback_data='back_anketa'),
      InlineKeyboardButton(text='Отмена', callback_data='cancel_anketa'),
   ]])
      await msg.answer('Введите ваш возраст: ', reply_markup=markup)
      return

   await state.set_state(Anketa.gender)
   markup = InlineKeyboardMarkup(inline_keyboard=[
      [
         InlineKeyboardButton(text='Назад', callback_data='back_anketa'),
         InlineKeyboardButton(text='Отмена', callback_data='cancel_anketa'),
      ],[
         InlineKeyboardButton(text='Мужской', callback_data='gender_m'),
         InlineKeyboardButton(text='Женский', callback_data='gender_w'),
   ]])
   await msg.answer("Введите ваш пол", reply_markup=markup)

@router.callback_query(F.data == 'back_anketa')
async def set_age_anketa_handler(callback_query: CallbackQuery, state: FSMContext):
   current_state = await state.get_state()
   if current_state == Anketa.gender:
      await state.set_state(Anketa.age)
      markup = InlineKeyboardMarkup(inline_keyboard=[[
         InlineKeyboardButton(text='Назад', callback_data='back_anketa'),
         InlineKeyboardButton(text='Отмена', callback_data='cancel_anketa'),
      ]])
      await callback_query.message.answer('Введите ваш возраст', reply_markup=markup)

   elif current_state == Anketa.age:
      await state.set_state(Anketa.name)
      markup = InlineKeyboardMarkup(inline_keyboard=[[
         InlineKeyboardButton(text='Отмена', callback_data='cancel_anketa')
      ]])
      await callback_query.message.answer('Введите ваше имя', reply_markup=markup)

@router.callback_query(F.data.startswith('gender_') and Anketa.gender)
async def set_age_anketa_handler(callback_query: CallbackQuery, state: FSMContext):
   gender = {'gender_m': 'Мужской', 'gender_w': 'Женский'}[callback_query.data]
   await state.update_data(gender=gender)
   await callback_query.message.answer(str(await state.get_data()))
   await state.clear()

@router.message(Anketa. gender)
async def set_age_by_anketa_handler(msg: Message, state: FSMContext):
   await msg.answer("Нужно нажать кнопку")

@router.message(Command("start"))
async def start_handler(msg: Message):
   await bot.set_my_commands([
      BotCommand(command="start", description="Запуск бота"),
      BotCommand(command="anketa", description="Справка"),
      BotCommand(command="delete", description="Очитстить"),
   ])

   inline_markup = InlineKeyboardMarkup(inline_keyboard=[
      [InlineKeyboardButton(text="Далее", callback_data='next')]
   ])
   await msg.answer(text="1", reply_markup=inline_markup)

@router.callback_query(F.data == 'next')
async def next_handler(callback_query: CallbackQuery):
   inline_markup = InlineKeyboardMarkup(inline_keyboard=[
      [InlineKeyboardButton(text="Назад", callback_data='back')]
   ])
   await callback_query.message.edit_text(
      "2", reply_markup=inline_markup)


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

@router.callback_query(F.data == 'set_age_anketa')
async def set_age_anketa_handler(callback_query: CallbackQuery, state: FSMContext):
   await state.set_state(Anketa.age)
   markup = InlineKeyboardMarkup(inline_keyboard=[[
      InlineKeyboardButton(text='Назад', callback_data='set_name_anketa'),
      InlineKeyboardButton(text='Отмена', callback_data='cancel_anketa')
   ]])
   await callback_query.message.answer('Введите ваш возраст: ', reply_markup=markup)

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
