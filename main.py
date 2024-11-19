import asyncio

from aiogram import Bot, Dispatcher, Router
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


def get_menu(menu: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    match menu:
        case "main":
            keyboard = InlineKeyboardBuilder([
                [InlineKeyboardButton(text="Все клубы", callback_data="all")],
                [InlineKeyboardButton(text="Бесплатные занятия", callback_data="free_lessons")],
                [InlineKeyboardButton(text="Афиша", url="https://example.com")],
                [InlineKeyboardButton(text="Задать вопрос", callback_data="question")]
            ])
        case "back":
            keyboard = InlineKeyboardBuilder([
                [InlineKeyboardButton(text="Назад", callback_data="back_to_main_menu")]
            ])
        case "clubs":
            keyboard = InlineKeyboardBuilder([
                [InlineKeyboardButton(text="Найти ближайшие", callback_data="find_closest")],
                [InlineKeyboardButton(text="Выбрать клуб", url="https://example.com")],
                [InlineKeyboardButton(text="Назад", callback_data="back_to_main_menu")]
            ])

    return keyboard.as_markup()


@router.message(lambda m: m.text == "/start")
async def start(message: Message) -> None:
    await message.reply("Привет! (краткая инфа про ПМЦ)",
                        reply_markup=get_menu("main"))


@router.callback_query(lambda c: c.data == "find_closest")
async def find_closest(callback_query):
    # TODO
    await callback_query.message.answer("Поиск в стадии разработки!",
                                        reply_markup=get_menu("back"))


@router.callback_query(lambda c: c.data == "back_to_main_menu")
async def back_to_main_menu_callback(callback_query):
    await callback_query.message.answer("Вы вернулись в главное меню:",
                                        reply_markup=get_menu("main"))


@router.callback_query(lambda c: c.data == "all")
async def back_to_main_menu_callback(callback_query):
    await callback_query.message.answer("Все клубы: {}",
                                        reply_markup=get_menu("clubs"))


@router.callback_query(lambda c: c.data == "free_lessons")
async def back_to_main_menu_callback(callback_query):
    await callback_query.message.answer("Информация о бесплатных занятиях: {}",
                                        reply_markup=get_menu("back"))


@router.callback_query(lambda c: c.data == "question")
async def back_to_main_menu_callback(callback_query):
    # TODO
    await callback_query.message.answer("Задайте ваш вопрос, и мы обязательно ответим!",
                                        reply_markup=get_menu("back"))


async def main() -> None:
    bot = Bot(token="7900208048:AAEFSShliZrdNyRVK563FW2IUYpZT7t1_zs",
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = Dispatcher()
    dp.include_router(router)

    await bot.delete_webhook(True)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
