# 1. Kutubxonani o'rnatish
!pip install aiogram

import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

# 2. BOT SOZLAMALARI
API_TOKEN = '8640960469:AAGuyb4ceUl1JlQDL3Q1A8gPg7fkXMccu5Ys'
ADMIN_ID = 8042301004  # Sizning ID raqamingiz

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# 3. RO'YXATDAN O'TISH BOSQICHLARI
class Reg(StatesGroup):
    ism = State()
    tel = State()

# 4. START BUYRUG'I
@dp.message(Command("start"))
async def start_cmd(message: types.Message, state: FSMContext):
    await message.answer(f"Assalomu alaykum!\nYuksak ta'lim ro'yxatdan o'tish botiga xush kelibsiz.\n\nIsmingizni kiriting:")
    await state.set_state(Reg.ism)

# 5. ISMNI QABUL QILISH
@dp.message(Reg.ism)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    kb = [[types.KeyboardButton(text="📞 Raqamni yuborish", request_contact=True)]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
    await message.answer(f"Rahmat, {message.text}! Endi pastdagi tugmani bosib telefon raqamingizni yuboring:", reply_markup=keyboard)
    await state.set_state(Reg.tel)

# 6. RAQAMNI QABUL QILISH VA SIZGA (ADMINGA) YUBORISH
@dp.message(Reg.tel, F.contact)
async def get_tel(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_name = data.get("name")
    phone = message.contact.phone_number
    
    # Foydalanuvchiga tasdiq xabari
    await message.answer("Rahmat! Ma'lumotlaringiz qabul qilindi. Tez orada siz bilan bog'lanamiz.", reply_markup=types.ReplyKeyboardRemove())
    
    # SIZGA (ADMINGA) keladigan xabar
    admin_text = (
        "🆕 **Yangi o'quvchi ro'yxatdan o'tdi!**\n\n"
        f"👤 **Ismi:** {user_name}\n"
        f"📞 **Tel:** {phone}\n"
        f"🆔 **Telegram ID:** `{message.from_user.id}`"
    )
    
    try:
        await bot.send_message(ADMIN_ID, admin_text, parse_mode="Markdown")
    except Exception as e:
        print(f"Adminga xabar yuborishda xato: {e}")
    
    await state.clear()

# 7. BOTNI ISHGA TUSHIRISH
async def main():
    print("Bot ishga tushdi... Telegramdan tekshirib ko'ring!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        await main()
    except Exception as e:
        print(f"Xatolik: {e}")