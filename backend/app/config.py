import os
import platform
import ctypes
from pydantic import BaseModel

class Settings(BaseModel):
    APP_NAME: str = "OmniHeal Endpoint Engine"
    VERSION: str = "2.4.0"
    HOST: str = "127.0.0.1"
    PORT: int = 8765
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"
    ]
    DRY_RUN_DEFAULT: bool = False

settings = Settings()

def is_admin() -> bool:
    """Checks if the script is running with administrative / root privileges."""
    try:
        if platform.system() == "Windows":
            return bool(ctypes.windll.shell32.IsUserAnAdmin())
        else:
            return os.geteuid() == 0
    except Exception:
        return False

def get_os_family() -> str:
    """Returns 'windows', 'linux', or 'darwin'"""
    system = platform.system().lower()
    if "windows" in system:
        return "windows"
    elif "darwin" in system:
        return "darwin"
    return "linux"
