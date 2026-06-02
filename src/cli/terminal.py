import sys
import json

from src.config import config
from src.core.model_manager import set_model


def handle_sa_command(args: list[str]) -> str:
    if len(args) < 2:
        return "Использование: /SA <command> [args]"

    subcommand = args[1].lower()

    if subcommand == "userid":
        if len(args) < 3:
            return "Укажите Telegram ID: /SA userid <tg_id>"
        try:
            config.admin_user_id = int(args[2])
            return f"✅ ADMIN_USER_ID изменён на {config.admin_user_id}"
        except ValueError:
            return "❌ Неверный формат ID"

    if subcommand == "bot":
        if len(args) < 3:
            return "Укажите токен: /SA bot <token>"
        config.bot_token = args[2]
        return "✅ Токен бота обновлён (требуется перезапуск)"

    if subcommand == "secureb":
        config.secure_boot = not config.secure_boot
        status = "включён" if config.secure_boot else "выключен"
        return f"✅ Secure boot {status}"

    if subcommand == "model":
        if len(args) < 3:
            return "Использование: /SA model <operator> <api> <model>"
        operator = args[2] if len(args) > 2 else "opencode"
        api = args[3] if len(args) > 3 else "zen"
        model = args[4] if len(args) > 4 else ""
        return set_model(operator, api, model)

    return f"❌ Неизвестная команда: /SA {subcommand}"


def parse_cli_args():
    if len(sys.argv) > 1 and sys.argv[1] == "/SA":
        result = handle_sa_command(sys.argv[1:])
        print(result)
        sys.exit(0)
