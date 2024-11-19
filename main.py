
import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties

# Инициализируем роутер
router = Router()

# Обработчик команды /start
@router.message(CommandStart())
async def start(message: Message) -> None:
    # Создаем клавиатуру для стартового меню с использованием билдера
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Все клубы", callback_data="All_Clubs"))
    keyboard.add(InlineKeyboardButton(text="Бесплатные занятия", callback_data="free_z"))
    keyboard.add(InlineKeyboardButton(text="Афиша", callback_data="Afisha"))
    keyboard.add(InlineKeyboardButton(text="Задать вопрос", callback_data="question"))
    
    await message.reply("Привет это бот пмц ОХТА!!!!", 
                        reply_markup=keyboard.as_markup())

# Обработчик нажатия на кнопку "Бесплатные занятия"
@router.message(lambda message: message.text == "Бесплатные занятия")
async def free_classes(message: Message) -> None:
    # Ответ по кнопке бесплатных занятий
    await message.reply("Информация о бесплатных занятиях будет скоро доступна.",
                         reply_markup=InlineKeyboardBuilder().add(InlineKeyboardButton(text="Назад", callback_data="back_to_main_menu")).as_markup(resize_keyboard=True))

# Обработчик нажатия на кнопку "Афиша"
@router.message(lambda message: message.text == "Афиша")
async def events(message: Message) -> None:
    # Ответ по кнопке афиши
    await message.reply("Афиша доступна на нашем сайте: https://example.com/afisha",
                         reply_markup=InlineKeyboardBuilder().add(InlineKeyboardButton(text="Назад", callback_data="back_to_main_menu")).as_markup(resize_keyboard=True))

# Обработчик нажатия на кнопку "Задать вопрос"
@router.message(lambda message: message.text == "Задать вопрос")
async def ask_question(message: Message) -> None:
    # Ответ по кнопке для задавания вопроса
    await message.reply("Задайте ваш вопрос, и мы обязательно ответим!",
                         reply_markup=InlineKeyboardBuilder().add(InlineKeyboardButton(text="Назад", callback_data="back_to_main_menu")).as_markup(resize_keyboard=True))

# Обработчик нажатия на кнопку "Найти ближайшие" (инлайн-кнопка)
@router.callback_query(lambda c: c.data == "find_closest")
async def find_closest(callback_query):
    # Ответ по кнопке "Найти ближайшие"
    await callback_query.message.answer("Найдено 3 ближайших клуба. Дополнительная информация будет скоро доступна.",
                                         reply_markup=InlineKeyboardBuilder().add(InlineKeyboardButton(text="Назад", callback_data="back_to_main_menu")).as_markup())

# Обработчик нажатия на кнопку "Назад" из инлайн-кнопок
@router.callback_query(lambda c: c.data == "back_to_main_menu")
async def back_to_main_menu_callback(callback_query):
    # Возвращаем в главное меню с кнопками
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Все клубы", callback_data="All_Clubs"))
    keyboard.add(InlineKeyboardButton(text="Бесплатные занятия", callback_data="free_z"))
    keyboard.add(InlineKeyboardButton(text="Афиша", callback_data="Afisha"))
    keyboard.add(InlineKeyboardButton(text="Задать вопрос", callback_data="question"))
    
    await callback_query.message.answer("Вы вернулись в главное меню:",
                                         reply_markup=keyboard.as_markup(resize_keyboard=True))


@router.callback_query(lambda c: c.data == "All_Clubs")
async def back_to_main_menu_callback(callback_query):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Найти ближайшие", callback_data="find_closest"))
    keyboard.add(InlineKeyboardButton(text="Выбрать клуб", url="https://example.com"))
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data="back_to_main_menu"))
    
    await callback_query.message.answer("Все клубы: вот вот",
                                         reply_markup=keyboard.as_markup(resize_keyboard=True))

@router.callback_query(lambda c: c.data == "free_z")
async def back_to_main_menu_callback(callback_query):
    # Тут доделать
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data="back_to_main_menu"))

    await callback_query.message.answer("Информация о бесплатных занятиях: на держи",
                                         reply_markup=keyboard.as_markup(resize_keyboard=True))

@router.callback_query(lambda c: c.data == "Afisha")
async def back_to_main_menu_callback(callback_query):
    # Тут доделать
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data="back_to_main_menu"))

    await callback_query.message.answer("Афиша:",
                                         reply_markup=keyboard.as_markup(resize_keyboard=True))


@router.callback_query(lambda c: c.data == "question")
async def back_to_main_menu_callback(callback_query):
    # тут доделать
    await callback_query.message.answer("Задайте ваш вопрос, и мы обязательно ответим!",
                                         reply_markup=InlineKeyboardBuilder().add(InlineKeyboardButton(text="Назад", callback_data="back_to_main_menu")).as_markup(resize_keyboard=True))    

# Основная функция для запуска бота
async def main() -> None:
    # Создаем объект бота
    bot = Bot(token="7900208048:AAEFSShliZrdNyRVK563FW2IUYpZT7t1_zs",  default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    
    # Создаем диспетчер
    dp = Dispatcher()
    dp.include_router(router)

    # Очищаем вебхук (если был ранее настроен)
    await bot.delete_webhook(True)
    
    # Запускаем polling
    await dp.start_polling(bot)

# Запуск бота
if __name__ == "__main__":
    asyncio.run(main())
