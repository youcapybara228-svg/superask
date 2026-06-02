from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def sudo_approve_keyboard(command_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Одобрить", callback_data=f"sua_approve:{command_id}"),
            InlineKeyboardButton(text="Отклонить", callback_data=f"sua_reject:{command_id}"),
        ]
    ])
