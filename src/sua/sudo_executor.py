import asyncio
import shlex

from src.sua.password_manager import get_password
from src.sua.consent import request_sudo_approval
from src.config import config


async def execute_with_sudo(command: str) -> dict:
    approved = await request_sudo_approval(command)
    if approved is None:
        return {"success": False, "output": "⏱ Тайм-аут ожидания подтверждения"}
    if not approved:
        return {"success": False, "output": "❌ Команда отклонена администратором"}

    password = get_password()
    if not password:
        return {"success": False, "output": "❌ Пароль sudo не сохранён. Используйте /sua <password>"}

    full_command = f"echo {shlex.quote(password)} | sudo -S {command}"

    proc = await asyncio.create_subprocess_shell(
        full_command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()

    return {
        "success": proc.returncode == 0,
        "output": stdout.decode().strip() or stderr.decode().strip(),
    }
