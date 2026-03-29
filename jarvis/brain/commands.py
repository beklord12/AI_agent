from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional
from jarvis.voice.text_to_speech import TextToSpeech


@dataclass
class CommandResult:
    handled: bool
    response: str
    action: Optional[Callable[[], None]] = None


class CommandBrain:
    """
    Simple rule-based command parser.

    Examples:
        "open chrome" -> open_chrome()
        "open telegram" -> open_telegram()
        "open vscode" -> open_vscode()
        "shutdown pc" -> shutdown_pc()
        "restart pc" -> restart_pc()
        "open downloads" -> open_downloads()
    """

    def __init__(self, system_controller: "SystemController") -> None:
        self._system = system_controller
        self.tts = TextToSpeech()

    def handle(self, text: str) -> CommandResult:
        if not text:
            return CommandResult(False, "I did not hear any command.")

        t = text.lower()

        # open chrome
        if "chrome" in t:
            return CommandResult(
                True,
                "Opening Chrome.",

                action=self._system.open_chrome,
            )

        # open telegram
        if "telegram" in t:
            return CommandResult(
                True,
                "Opening Telegram.",
                action=self._system.open_telegram,
            )

        # open vscode
        if "code" in t or "vs code" in t or "vscode" in t:
            return CommandResult(
                True,
                "Opening Visual Studio Code.",
                action=self._system.open_vscode,
            )

        # open downloads
        if "download" in t or "downloads" in t:
            return CommandResult(
                True,
                "Opening downloads folder.",
                action=self._system.open_downloads,
            )

        # shutdown pc
        if "shutdown" in t or "power off" in t or "turn off" in t:
            return CommandResult(
                True,
                "Shutting down the computer.",
                action=self._system.shutdown_pc,
            )

        # restart pc
        if "restart" in t or "reboot" in t:
            return CommandResult(
                True,
                "Restarting the computer.",
                action=self._system.restart_pc,
            )

        return CommandResult(False, "I don't know how to do that yet.")


# Avoid circular import type checking issues
class SystemController:  # pragma: no cover - only for type hints
    def open_chrome(self) -> None: ...

    def open_telegram(self) -> None: ...

    def open_vscode(self) -> None: ...

    def open_downloads(self) -> None: ...

    def shutdown_pc(self) -> None: ...

    def restart_pc(self) -> None: ...

