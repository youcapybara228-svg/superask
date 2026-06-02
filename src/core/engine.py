import asyncio
import subprocess
from pathlib import Path

from src.config import config
from src.core.process_manager import process_manager


async def _run_opencode(args: list[str], timeout: int = 60) -> str:
    opencode_bin = Path(config.opcode_dir) / "packages" / "opencode" / "bin" / "opencode"
    if not opencode_bin.exists():
        return "❌ opencode бинарник не найден"

    try:
        proc = await asyncio.create_subprocess_exec(
            str(opencode_bin),
            *args,
            cwd=config.opcode_dir,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        output = stdout.decode().strip() or stderr.decode().strip()
        return output if output else "✅ Выполнено (без вывода)"
    except asyncio.TimeoutError:
        if proc:
            proc.kill()
        return "⏱ Тайм-аут выполнения"
    except Exception as e:
        return f"❌ Ошибка: {e}"


async def test_neural_network() -> str:
    result = await _run_opencode(["-p", "Тест: ответь 'OK' если работаешь"])
    return f"🧪 Результат теста:\n{result}"


async def start_sa() -> str:
    if process_manager.is_running:
        return "⚠️ Super ASK уже запущен"
    process_manager.start()
    return "✅ Super ASK запущен"


async def stop_sa() -> str:
    if not process_manager.is_running:
        return "⚠️ Super ASK не запущен"
    process_manager.stop()
    return "✅ Super ASK остановлен"


async def stop_current_session() -> str:
    process_manager.stop_session()
    return "✅ Текущая сессия отключена"


async def disable_sa_permanently() -> str:
    process_manager.disable_permanently()
    config.sa_enabled = False
    return "✅ Super ASK отключён навсегда. Для включения используйте /on"


async def stop_active_process() -> str:
    process_manager.stop_active()
    return "✅ Активный процесс остановлен"
