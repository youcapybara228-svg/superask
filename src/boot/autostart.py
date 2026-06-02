import asyncio
import subprocess

from src.config import config
from src.bot.bot import bot
from src.core.process_manager import process_manager, SAState


async def try_start_sa() -> bool:
    try:
        opencode_bin = config.opcode_dir / "packages" / "opencode" / "bin" / "opencode"
        if not opencode_bin.exists():
            return False

        proc = await asyncio.create_subprocess_exec(
            str(opencode_bin), "--version",
            cwd=config.opcode_dir,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=10)
        if proc.returncode == 0:
            process_manager.start()
            return True
        return False
    except Exception:
        return False


async def boot_sequence():
    if not config.sa_enabled:
        return

    if config.secure_boot:
        return

    success = await try_start_sa()
    if success:
        process_manager.start()
        await bot.send_message(config.admin_user_id, "🚀 Super ASK Запущен")
    else:
        await bot.send_message(
            config.admin_user_id,
            "⚠️ Super ASK не удалось запустить. Проверьте логи."
        )
