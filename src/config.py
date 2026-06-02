import os
from dataclasses import dataclass, field
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    bot_token: str = field(default_factory=lambda: os.getenv("BOT_TOKEN", ""))
    admin_user_id: int = field(default_factory=lambda: int(os.getenv("ADMIN_USER_ID", "0")))
    encryption_key: str = field(default_factory=lambda: os.getenv("ENCRYPTION_KEY", ""))
    opcode_dir: str = field(default_factory=lambda: os.getenv("OPCODE_DIR", str(Path.home() / "Desktop" / "superask" / "opencode_ref")))

    sua_password: str = ""
    sua_auto_approve: bool = False
    sua_enabled: bool = False

    model_operator: str = "opencode"
    model_api: str = "zen"
    model_id: str = "opencode zen"

    secure_boot: bool = False
    sa_enabled: bool = True
    sa_running: bool = False

    data_dir: Path = Path(__file__).parent.parent / "data"

    def __post_init__(self):
        self.data_dir.mkdir(parents=True, exist_ok=True)

    @property
    def sua_password_path(self) -> Path:
        return self.data_dir / "sua_password.enc"

    @property
    def config_path(self) -> Path:
        return self.data_dir / "config.json"


config = Config()
