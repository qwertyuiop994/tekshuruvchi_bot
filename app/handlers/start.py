from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from app.keyboards.default import main_menu_keyboard, examples_inline_keyboard

start_router = Router(name="start")


@start_router.message(CommandStart())
async def cmd_start(message: Message):
    """
    /start komandasiga javob beruvchi funksiya.
    """
    user_name = message.from_user.first_name if message.from_user else "Foydalanuvchi"
    welcome_text = (
        f"Assalomu alaykum, <b>{user_name}</b>! 👋\n\n"
        "Men <b>Aqlli Savol-Javob va Test Tekshiruvchi Botiman</b> 🤖✨\n\n"
        "<b>Imkoniyatlarim:</b>\n"
        "🔹 <b>Savol va javobingizni tekshirish:</b> Savol bilan birga o'z javobingizni yuborsangiz, to'g'ri yoki noto'g'riligini tekshirib, xatoingizni aniq tushuntirib beraman!\n"
        "🔹 <b>Savolga to'g'ri javob topish:</b> Istalgan fandan savol yoki test yuborsangiz, to'g'ri javobini topib, ilmiy asoslab tushuntiraman.\n"
        "🔹 <b>Testlar to'plami:</b> Bir nechta testni bitta xabarda yuborsangiz, har birini alohida tahlil qilib, kalitlarini chiqarib beraman.\n"
        "🔹 <b>Rasmli savollar:</b> Test kitobidan yoki daftardan rasm yuborsangiz ham tahlil qilaman.\n\n"
        "🚀 <i>Boshlash uchun savolingizni (va agar bor bo'lsa javobingizni) yuboring!</i>"
    )
    await message.answer(welcome_text, reply_markup=main_menu_keyboard(), parse_mode="HTML")


@start_router.message(Command("help"))
@start_router.message(F.text == "📖 Yo'riqnoma")
async def show_help(message: Message):
    """
    Botdan foydalanish bo'yicha to'liq qo'llanma.
    """
    help_text = (
        "📚 <b>Botdan foydalanish qo'llanmasi:</b>\n\n"
        "<b>1. Javobingizni tekshirtirish:</b>\n"
        "Savol va unga bergan javobingizni yozib yuboring (masalan: <i>'Savol: O'zbekiston BMTga qachon a'zo bo'lgan? Javob: 1991-yil. Shu to'g'rimi?'</i>). "
        "Bot javobingizni tekshirib, to'g'ri yoki xatoligini aniq tushuntiradi.\n\n"
        "<b>2. Savolga javob olish:</b>\n"
        "Savol yoki test variantlarini (A, B, C, D) shunchaki yuboring.\n\n"
        "<b>3. Rasm yuborish:</b>\n"
        "Test yoki savol tushirilgan sifatli rasmni yuboring."
    )
    await message.answer(help_text, parse_mode="HTML")


@start_router.message(F.text == "💡 Savol namunalari")
async def show_examples(message: Message):
    """
    Namunalar bo'limi.
    """
    text = "Quyidagi namunalardan birini tanlab ko'rishingiz mumkin:"
    await message.answer(text, reply_markup=examples_inline_keyboard())


@start_router.callback_query(F.data == "example_single")
async def callback_example_single(call: CallbackQuery):
    """
    Tekshirish namunasi.
    """
    example_text = (
        "💡 <b>Javobni tekshirish namunasi:</b>\n\n"
        "📚 <b>Savol:</b> Yer Quyosh atrofida qancha vaqtda to'liq bir marta aylanib chiqadi?\n"
        "🎯 <b>Sizning javobingiz:</b> 30 kun ➡️ <b>NOTO‘G‘RI!</b> ❌\n"
        "✅ <b>Asl to‘g‘ri javob:</b> 365 kun 6 soat (1 yil)\n"
        "📝 <b>Aniq tushuntirish:</b>\n"
        "30 kun — bu Oyning Yer atrofida aylanish davriga yaqin vaqt. "
        "Yer esa Quyosh atrofida to'liq bir marta aylanishi uchun roppa-rosa 365 kun va taxminan 6 soat sarflaydi. "
        "Shu 6 soatlar to'planib har 4 yilda kabisa yilini (366 kun) hosil qiladi."
    )
    await call.message.answer(example_text, parse_mode="HTML")
    await call.answer()


@start_router.callback_query(F.data == "example_tests")
async def callback_example_tests(call: CallbackQuery):
    """
    Testlar to'plami namunasi.
    """
    example_text = (
        "💡 <b>Testlar tahlili namunasi:</b>\n\n"
        "📚 <b>1-Savol:</b> Python qanday til?\n"
        "✅ <b>To‘g‘ri javob:</b> Yuqori darajali dasturlash tili\n"
        "📝 <b>Aniq tushuntirish:</b> Python sodda sintaksisga ega bo'lgan, interpretatsiya qilinadigan zamonaviy dasturlash tilidir.\n\n"
        "────────────────────\n\n"
        "📚 <b>2-Savol:</b> 5 * 5 + 5 nechaga teng?\n"
        "🎯 <b>Sizning javobingiz:</b> 30 ➡️ <b>TO‘G‘RI!</b> ✅\n"
        "📝 <b>Aniq tushuntirish:</b> Arifmetika qoidasiga ko'ra avval ko'paytirish bajariladi (5 * 5 = 25), so'ng qo'shiladi (25 + 5 = 30)."
    )
    await call.message.answer(example_text, parse_mode="HTML")
    await call.answer()


@start_router.message(F.text == "ℹ️ Bot haqida")
async def show_about(message: Message):
    """
    Bot haqida ma'lumot.
    """
    about_text = (
        "🤖 <b>Aqlli Savol-Javob va Tekshiruvchi Bot</b>\n\n"
        "Ushbu bot siz yuborgan savollarga javob topishdan tashqari, sizning javoblaringizni ham tekshirib, xatolaringizni aniq va mantiqiy asoslab tushuntirib beradi! 🎓"
    )
    await message.answer(about_text, parse_mode="HTML")
