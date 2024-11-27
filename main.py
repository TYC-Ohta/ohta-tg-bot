import asyncio
import json

from aiogram import Bot, Dispatcher, Router
from aiogram import F
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder

CLUBS: str = "./clubs.json"
DESCR: str = (
    '<b>Молодёжный центр "Охта"</b> – это 21 молодёжный клуб и более 300 студий, расположенных в разных уголках '
    'Красногвардейского района Санкт-Петербурга.\n'
    'Наша миссия – создать среду, которая поможет тебе раскрыть свой творческий потенциал и самореализоваться!\n\n'
    'Нажми на кнопку под сообщением чтобы получить больше информации 👇')

file_lock: asyncio.Lock = asyncio.Lock()
router: Router = Router()


async def get_menu(menu: str) -> InlineKeyboardMarkup:
    keyboard: InlineKeyboardBuilder = InlineKeyboardBuilder()
    match menu:
        case "main":
            keyboard = InlineKeyboardBuilder([
                [InlineKeyboardButton(text="Записаться", url="https://vk.com/app5708398_-28488795")],
                [InlineKeyboardButton(text="Все клубы", callback_data="all")],
                [InlineKeyboardButton(text="Найти ближайшие", callback_data="find")],
                # [InlineKeyboardButton(text="Задать вопрос", callback_data="question")]
            ])
        case "back":
            keyboard = InlineKeyboardBuilder([
                [InlineKeyboardButton(text="Назад", callback_data="main")]
            ])
        case "clubs":
            async with file_lock:
                with open(CLUBS) as f:
                    clubs: list[dict[str: any]] = json.load(f)

            keyboard = await format_clubs(tuple(enumerate(clubs)))

    return keyboard.as_markup()


async def format_clubs(clubs: tuple) -> InlineKeyboardBuilder:
    buttons: list = []

    for i, club in clubs:
        buttons.append(
            [InlineKeyboardButton(text=club["name"], callback_data=f"club:{i}")]
        )

    return InlineKeyboardBuilder(buttons + [
        [InlineKeyboardButton(text="Назад", callback_data="main")]
    ])


@router.message(lambda m: m.text == "/start")
async def start(message: Message) -> None:
    await message.reply(
        f'Привет!\n\n{DESCR}',
        reply_markup=await get_menu("main"))


@router.callback_query(lambda c: c.data == "find")
async def find(callback: CallbackQuery) -> None:
    await callback.message.answer(
        "Отправь свои координаты, чтобы найти ближайшие клубы!",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Поделиться локацией", request_location=True)]], resize_keyboard=True
        ),
    )


@router.message(F.location)
async def find_closest(message: Message) -> None:
    msg: Message = await message.reply(
        f'Идёт поиск...',
        reply_markup=ReplyKeyboardRemove()
    )

    async with file_lock:
        with open(CLUBS) as f:
            clubs = json.load(f)

    clubs = ((i, c) for i, c in enumerate(clubs))  # Indexing for correct work with callback

    # Sorting based on location and taking the first three (sorry for formatting lol)
    clubs = tuple(sorted(
        clubs,
        key=lambda c: abs(c[1]["coordinates"][0] - message.location.latitude)
                      + abs(c[1]["coordinates"][1] - message.location.longitude))[:3])

    await msg.delete()

    await message.reply(
        "Вот 3 ближайших клуба к тебе!",
        reply_markup=(await format_clubs(clubs)).as_markup()
    )


@router.callback_query(lambda c: c.data == "main")
async def back_to_main(callback: CallbackQuery) -> None:
    await callback.message.answer(
        f"Вы вернулись в главное меню!\n\n{DESCR}",
        reply_markup=await get_menu("main"))


@router.callback_query(lambda c: c.data == "all")
async def show_all_clubs(callback: CallbackQuery) -> None:
    await callback.message.answer(
        'Ниже представлены все клубы ПМЦ "Охта".\n'
        'Нажми на кнопку, чтобы получить более подробную информацию о клубе.',
        reply_markup=await get_menu("clubs"))


@router.callback_query(lambda c: c.data == "question")
async def ask_question(callback: CallbackQuery) -> None:
    # TODO
    await callback.message.answer(
        "Задайте ваш вопрос, и мы обязательно ответим!",
        reply_markup=await get_menu("back"))


@router.callback_query(lambda c: c.data.startswith("club:"))
async def get_club_info(callback: CallbackQuery) -> None:
    async with file_lock:
        with open(CLUBS) as f:
            club: dict[str: any] = json.load(f)[int(callback.data.split(':')[-1])]

    await callback.message.answer(
        f'<b>{club["name"]}</b>\n'
        f'<i>{club["address"]}</i>\n\n'
        f'Направления:\n- {';\n- '.join(club["sections"])}.\n',
        reply_markup=InlineKeyboardBuilder(
            [
                [InlineKeyboardButton(text='Я.Карты', url=club["y_maps"])],
                [InlineKeyboardButton(text='ВКонтакте', url=club["vk"])],
                [InlineKeyboardButton(text="Назад", callback_data="main")]
            ]
        ).as_markup()
    )


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
