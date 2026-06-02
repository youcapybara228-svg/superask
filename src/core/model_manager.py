from src.config import config


def set_model(operator: str, api: str, model: str) -> str:
    config.model_operator = operator
    config.model_api = api
    config.model_id = f"{operator} {api} {model}".strip()
    return f"✅ Модель изменена: {config.model_id}"


def get_model_info() -> str:
    return (
        f"Текущая модель:\n"
        f"  Оператор: {config.model_operator}\n"
        f"  API: {config.model_api}\n"
        f"  Модель: {config.model_id}"
    )
