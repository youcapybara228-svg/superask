from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from src.config import config
from src.bot.bot import bot
from src.sua.password_manager import save_password, get_password, clear_password
from src.sua.consent import pending_commands, notify_sudo_result
from src.core.engine import (
    test_neural_network,
    start_sa,
    stop_sa,
    stop_current_session,
    disable_sa_permanently,
    stop_active_process,
)

router = Router()


def is_admin(message: Message) -> bool:
    return message.from_user and message.from_user.id == config.admin_user_id


@router.message(Command("test"))
async def cmd_test(message: Message):
    if not is_admin(message):
        return
    await message.answer("🧪 Тестирую нейросеть и права sudo...")
    result = await test_neural_network()
    await message.answer(result)


@router.message(Command("on"))
async def cmd_on(message: Message):
    if not is_admin(message):
        return
    await message.answer("🔄 Включаю Super ASK...")
    result = await start_sa()
    await message.answer(result)


@router.message(Command("off"))
async def cmd_off(message: Message):
    if not is_admin(message):
        return
    await message.answer("🔄 Выключаю Super ASK...")
    result = await stop_sa()
    await message.answer(result)


@router.message(Command("offc"))
async def cmd_offc(message: Message):
    if not is_admin(message):
        return
    result = await stop_current_session()
    await message.answer(result)


@router.message(Command("offall"))
async def cmd_offall(message: Message):
    if not is_admin(message):
        return
    result = await disable_sa_permanently()
    await message.answer(result)


@router.message(Command("stop"))
async def cmd_stop(message: Message):
    if not is_admin(message):
        return
    result = await stop_active_process()
    await message.answer(result)


@router.message(Command("sua"))
async def cmd_sua(message: Message):
    if not is_admin(message):
        return
    parts = message.text.strip().split(maxsplit=1)
    if len(parts) == 2:
        password = parts[1]
        save_password(password)
        config.sua_enabled = True
        await message.answer("✅ Пароль sudo сохранён. Нейросеть может использовать sudo с вашего подтверждения.")
    else:
        config.sua_auto_approve = True
        config.sua_enabled = True
        await message.answer(
            "✅ Нейросети выдано право выполнять sudo-команды без подтверждения. "
            "Уведомления будут отправляться."
        )


@router.message(Command("suaoff"))
async def cmd_suaoff(message: Message):
    if not is_admin(message):
        return
    config.sua_enabled = False
    config.sua_auto_approve = False
    await message.answer("🔒 Права sudo у Super ASK отозваны.")


@router.message(Command("suaon"))
async def cmd_suaon(message: Message):
    if not is_admin(message):
        return
    config.sua_enabled = True
    await message.answer("✅ Права sudo выданы для Super ASK.")


@router.callback_query(F.data.startswith("sua_"))
async def on_sudo_approve(callback: CallbackQuery):
    action, command_id = callback.data.split(":", 1)
    approved = action == "sua_approve"

    if command_id in pending_commands:
        entry = pending_commands[command_id]
        if entry["user_id"] != config.admin_user_id:
            await callback.answer("Недостаточно прав")
            return
        entry["approved"] = approved
        await callback.message.edit_text(
            f"✅ Команда {'одобрена' if approved else 'отклонена'}:\n"
            f"<code>{entry['command']}</code>"
        )
        await notify_sudo_result(command_id, approved)
    else:
        await callback.answer("Команда уже обработана", show_alert=True)

    await callback.answer()
