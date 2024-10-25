from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import os

# Вставьте свой токен бота
bot = Bot(token=os.getenv('TG_TOKEN'))
dp = Dispatcher(bot)

# Создаем словарь для хранения категорий и подкатегорий
data = {}

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    keyboard_markup = types.InlineKeyboardMarkup(row_width=3)
    for category in data:
        button = types.InlineKeyboardButton(category, callback_data=f"category:{category}")
        keyboard_markup.add(button)
    await bot.send_message(message.chat.id, 'Выберите категорию', reply_markup=keyboard_markup)

@dp.callback_query_handler(lambda call: call.data.startswith('category'))
async def process_callback_button1(callback_query: types.CallbackQuery):
    category = callback_query.data.split(':')[1]
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, '\n'.join(data[category]))

@dp.message_handler(commands=['add_category'])
async def process_add_category_command(message: types.Message):
    await message.reply("Введите название категории")

@dp.message_handler()
async def process_category_name(message: types.Message):
    category_name = message.text
    if category_name not in data:
        data[category_name] = []
        await message.reply(f"Категория '{category_name}' была создана.\nВведите подкатегорию для этой категории:")
    else:
        data[category_name].append(message.text)
        await message.reply(f"Подкатегория '{message.text}' добавлена в категорию '{category_name}'\n")

if __name__ == '__main__':
    executor.start_polling(dp)