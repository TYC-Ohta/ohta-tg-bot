print("Starting...")

import asyncio
import json

from aiogram import Bot, Dispatcher, Router
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

CLUBS = "./clubs.json"

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
                [InlineKeyboardButton(text="Назад", callback_data="to_main")]
            ])
        case "clubs":
            with open(CLUBS) as f:
                clubs_info = json.load(f)

            buttons: list = []

            for c in clubs_info:
                buttons.append(
                    [InlineKeyboardButton(text=c["name"], url=c["vk"])]
                )

            keyboard = InlineKeyboardBuilder(buttons + [
                [InlineKeyboardButton(text="Назад", callback_data="to_main")]
            ])

    return keyboard.as_markup()


@router.message(lambda m: m.text == "/start")
async def start(message: Message) -> None:
    await message.reply("Привет! {краткая инфа про ПМЦ}",
                        reply_markup=get_menu("main"))


@router.callback_query(lambda c: c.data == "find_closest")
async def find_closest(callback_query):
    # TODO
    await callback_query.message.answer("Поиск в стадии разработки!",
                                        reply_markup=get_menu("back"))


@router.callback_query(lambda c: c.data == "to_main")
async def to_main_callback(callback_query):
    await callback_query.message.answer("Вы вернулись в главное меню:",
                                        reply_markup=get_menu("main"))


@router.callback_query(lambda c: c.data == "all")
async def to_main_callback(callback_query):
    await callback_query.message.answer("Все клубы:",
                                        reply_markup=get_menu("clubs"))


@router.callback_query(lambda c: c.data == "free_lessons")
async def to_main_callback(callback_query):
    await callback_query.message.answer("Информация о бесплатных занятиях: {}",
                                        reply_markup=get_menu("back"))


@router.callback_query(lambda c: c.data == "question")
async def to_main_callback(callback_query):
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
    print("Started")
    asyncio.run(main())

