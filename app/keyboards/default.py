from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    """
    Asosiy doimiy menyu tugmalari.
    """
    kb = [
        [
            KeyboardButton(text="💡 Savol namunalari"),
            KeyboardButton(text="📖 Yo'riqnoma")
        ],
        [
            KeyboardButton(text="ℹ️ Bot haqida")
        ]
    ]
    return ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Savol yoki rasmni yuboring..."
    )


def examples_inline_keyboard() -> InlineKeyboardMarkup:
    """
    Namunalar uchun inline tugmalar.
    """
    kb = [
        [
            InlineKeyboardButton(text="📝 Oddiy savol namunasi", callback_data="example_single"),
        ],
        [
            InlineKeyboardButton(text="📊 Test to'plami namunasi", callback_data="example_tests")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)
