import asyncio

from src.config import config
from src.bot.bot import bot
from src.core.process_manager import process_manager


async def ping_cycle():
    interval = 10
    counter = 1
    while True:
        await asyncio.sleep(interval)

        if not process_manager.can_run():
            break

        if counter == 1:
            await bot.send_message(
                config.admin_user_id,
                f"🔄 ПИНГ {interval * counter} с. SA РАБОТАЕТ"
            )
        else:
            await bot.send_message(
                config.admin_user_id,
                f"🔄 ПИНГ {interval * counter} с."
            )

        counter += 1
        if counter > 3:
            counter = 1
