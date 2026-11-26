import asyncio
import logging
import os
import sys
from html import escape

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# BOT SOZLAMALARI
# Token kodda yozilmaydi! Serverda (Railway/Render/Heroku) "Variables" bo'limiga
# BOT_TOKEN va ADMIN_ID qo'shing.
API_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "8042301004"))

if not API_TOKEN:
    sys.exit("BOT_TOKEN topilmadi. Serverda BOT_TOKEN o'zgaruvchisini qo'shing.")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


# RO'YXATDAN O'TISH BOSQICHLARI
class Reg(StatesGroup):
    ism = State()
    tel = State()


def tel_keyboard():
    kb = [[types.KeyboardButton(text="📞 Raqamni yuborish", request_contact=True)]]
    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)


# START BUYRUG'I
@dp.message(Command("start"))
async def start_cmd(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Assalomu alaykum!\nYuksak ta'lim ro'yxatdan o'tish botiga xush kelibsiz.\n\nIsmingizni kiriting:",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await state.set_state(Reg.ism)


# ISMNI QABUL QILISH
@dp.message(Reg.ism, F.text)
async def get_name(message: types.Message, state: FSMContext):
    name = message.text.strip()[:60]
    await state.update_data(name=name)
    await message.answer(
        f"Rahmat, {name}! Endi pastdagi tugmani bosib telefon raqamingizni yuboring:",
        reply_markup=tel_keyboard(),
    )
    await state.set_state(Reg.tel)


@dp.message(Reg.ism)
async def name_not_text(message: types.Message):
    await message.answer("Iltimos, ismingizni matn ko'rinishida yozing.")


# RAQAMNI QABUL QILISH VA ADMINGA YUBORISH
@dp.message(Reg.tel, F.contact)
async def get_tel(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_name = data.get("name", "—")
    phone = message.contact.phone_number

    await message.answer(
        "Rahmat! Ma'lumotlaringiz qabul qilindi. Tez orada siz bilan bog'lanamiz.",
        reply_markup=types.ReplyKeyboardRemove(),
    )

    username = f"@{message.from_user.username}" if message.from_user.username else "—"
    admin_text = (
        "🆕 <b>Yangi o'quvchi ro'yxatdan o'tdi!</b>\n\n"
        f"👤 <b>Ismi:</b> {escape(user_name)}\n"
        f"📞 <b>Tel:</b> {escape(phone)}\n"
        f"💬 <b>Telegram:</b> {escape(username)}\n"
        f"🆔 <b>Telegram ID:</b> <code>{message.from_user.id}</code>"
    )
    try:
        await bot.send_message(ADMIN_ID, admin_text, parse_mode="HTML")
    except Exception as e:
        logging.error("Adminga xabar yuborishda xato: %s", e)

    await state.clear()


@dp.message(Reg.tel)
async def tel_not_contact(message: types.Message):
    await message.answer(
        "Iltimos, pastdagi «📞 Raqamni yuborish» tugmasini bosing.",
        reply_markup=tel_keyboard(),
    )


# BOTNI ISHGA TUSHIRISH
async def main():
    logging.info("Bot ishga tushdi...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
