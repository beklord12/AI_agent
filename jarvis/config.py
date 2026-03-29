import os
from dataclasses import dataclass


@dataclass
class AudioConfig:
    wake_word: str = "altron"
    language: str = "en-US"
    energy_threshold: int = 300  # for speech_recognition
    pause_threshold: float = 0.8
    phrase_time_limit: int = 5


@dataclass
class AppPaths:
    """Default app paths/commands for Windows. Adjust as needed for your machine."""

    chrome: str = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # assumes in PATH
    telegram: str = r"C:\Users\User\AppData\Roaming\Telegram Desktop\Telegram.exe"  # may need full path
    vscode: str = r"D:\Microsoft VS Code\Code.exe"  # VS Code command line
    downloads_dir: str = os.path.join(os.path.expanduser("~"), "Downloads")


@dataclass
class UiConfig:
    sphere_idle_color: str = "#00FFFF"
    sphere_listening_color: str = "#00FFAA"
    sphere_processing_color: str = "#FFCC00"
    sphere_speaking_color: str = "#FF0066"


audio_config = AudioConfig()
app_paths = AppPaths()
ui_config = UiConfig()

