import asyncio
import logging

from src.config import config
from src.cli.terminal import parse_cli_args
from src.bot.bot import dp, bot
from src.bot.handlers import router
from src.boot.autostart import boot_sequence
from src.boot.monitor import ping_cycle
from src.core.process_manager import process_manager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("logs/superask.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("superask")


async def main():
    parse_cli_args()

    if not config.bot_token:
        logger.error("BOT_TOKEN не задан. Укажите через /SA bot <token> или .env")
        return

    if not config.admin_user_id:
        logger.warning("ADMIN_USER_ID не задан. Команды бота будут игнорироваться.")

    dp.include_router(router)

    if config.sa_enabled:
        await boot_sequence()

    monitor_task = asyncio.create_task(ping_cycle())

    try:
        logger.info("Super ASK запущен. Запускаю polling...")
        await dp.start_polling(bot)
    finally:
        monitor_task.cancel()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
