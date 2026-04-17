import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

# 1. BOT SOZLAMALARI
API_TOKEN = '8640960469:AAGuyb4ceUlJlQDL3QlA8gPg7fkXMccu5Ys'
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# 2. RO'YXATDAN O'TISH BOSQICHLARI
class Reg(StatesGroup):
    ism = State()
    tel = State()
    kurs = State()

# 3. START BUYRUG'I
@dp.message(Command("start"))
async def start_cmd(message: types.Message, state: FSMContext):
    await message.answer(
        f"Assalomu alaykum, {message.from_user.full_name}!\n"
        f"Yuksak ta'lim ro'yxatdan o'tish botiga xush kelibsiz.\n\n"
        f"Ro'yxatdan o'tish uchun ismingizni kiriting:"
    )
    await state.set_state(Reg.ism)

# 4. ISMNI QABUL QILISH
@dp.message(Reg.ism)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    kb = [
        [types.KeyboardButton(text="📞 Raqamni yuborish", request_contact=True)]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Rahmat! Endi telefon raqamingizni yuboring:", reply_markup=keyboard)
    await state.set_state(Reg.tel)

# 5. TELEFONNI QABUL QILISH
@dp.message(Reg.tel, F.contact)
async def get_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    
    kb = [
        [types.KeyboardButton(text="Arab tili"), types.KeyboardButton(text="Arab tili bolajon")],
        [types.KeyboardButton(text="Xattotlik"), types.KeyboardButton(text="Arab tili CEF")],
        [types.KeyboardButton(text="Tarix"), types.KeyboardButton(text="Rus tili")],
        [types.KeyboardButton(text="Kompyuter savodxonligi"), types.KeyboardButton(text="Grafik dizayn")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Qaysi yo'nalish bo'yicha o'qimoqchisiz?", reply_markup=keyboard)
    await state.set_state(Reg.kurs)

# 6. YAKUNLASH (Sizga xabar yuboradigan qismi)
@dp.message(Reg.kurs)
async def finish_reg(message: types.Message, state: FSMContext):
    data = await state.get_data()
    
    # ADMIN_ID degan joyga o'zingizning ID raqamingizni yozing
    ADMIN_ID = 8042301004  # <--- Shu yerga o'z ID raqamingizni qo'ying
    
    user_text = (f"✅ Ro'yxatdan o'tdingiz!\n\n"
                 f"👤 Ism: {data['name']}\n"
                 f"📞 Tel: {data['phone']}\n"
                 f"📚 Kurs: {message.text}")
    
    admin_text = (f"🔔 Yangi o'quvchi!\n\n"
                  f"👤 Ismi: {data['name']}\n"
                  f"📞 Tel: {data['phone']}\n"
                  f"📚 Kurs: {message.text}\n"
                  f"🆔 ID: @{message.from_user.username}")

    # Foydalanuvchiga tasdiqlash xabari
    await message.answer(user_text, reply_markup=types.ReplyKeyboardRemove())
    
    # SIZGA (Adminga) ma'lumotni yuborish
    try:
        await bot.send_message(ADMIN_ID, admin_text)
    except Exception as e:
        print(f"Adminga xabar yuborishda xato: {e}")

    await state.clear()

# 7. BOTNI ISHGA TUSHIRISH
async def main():
    # Eski xabarlarni o'chirib yuborish (Conflict xatosi bo'lmasligi uchun)
    await bot.delete_webhook(drop_pending_updates=True)
    print("Bot yangilandi va ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot to'xtatildi!")