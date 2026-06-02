import asyncio
import uuid

from src.config import config
from src.bot.bot import bot
from src.bot.keyboards import sudo_approve_keyboard

pending_commands: dict[str, dict] = {}
_futures: dict[str, asyncio.Future] = {}


async def request_sudo_approval(command_text: str, user: str = "~fish") -> bool | None:
    if not config.sua_enabled:
        return False

    if config.sua_auto_approve:
        await bot.send_message(
            config.admin_user_id,
            f"🔔 Super ASK выполняет sudo-команду:\n"
            f"из: {user}\n"
            f"команда: <code>{command_text}</code>",
        )
        return True

    command_id = str(uuid.uuid4())
    pending_commands[command_id] = {
        "command": command_text,
        "user": user,
        "approved": None,
        "user_id": config.admin_user_id,
    }

    future: asyncio.Future = asyncio.get_event_loop().create_future()
    _futures[command_id] = future

    await bot.send_message(
        config.admin_user_id,
        f"из: {user}\n"
        f"команда: <code>{command_text}</code>",
        reply_markup=sudo_approve_keyboard(command_id),
    )

    try:
        result = await asyncio.wait_for(future, timeout=120)
        return result
    except asyncio.TimeoutError:
        return None
    finally:
        pending_commands.pop(command_id, None)
        _futures.pop(command_id, None)


async def notify_sudo_result(command_id: str, approved: bool):
    future = _futures.get(command_id)
    if future and not future.done():
        future.set_result(approved)
