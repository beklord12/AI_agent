from __future__ import annotations

import os
import subprocess
import sys
from typing import Optional

from jarvis.config import app_paths


class SystemController:
    """
    Windows-focused system actions for Jarvis.
    You can customize app paths/commands in config.AppPaths.
    """

    def _run(self, command: str, *, use_shell: bool = True) -> None:
        try:
            subprocess.Popen(command, shell=use_shell)
        except OSError:
            pass

    def open_chrome(self) -> None:
        self._run(app_paths.chrome)

    def open_telegram(self) -> None:
        self._run(app_paths.telegram)

    def open_vscode(self) -> None:
        self._run(app_paths.vscode)

    def open_downloads(self) -> None:
        path = app_paths.downloads_dir
        if os.path.isdir(path):
            os.startfile(path)  # type: ignore[attr-defined]

    def shutdown_pc(self) -> None:
        # Windows shutdown command
        self._run("shutdown /s /t 0")

    def restart_pc(self) -> None:
        # Windows restart command
        self._run("shutdown /r /t 0")

