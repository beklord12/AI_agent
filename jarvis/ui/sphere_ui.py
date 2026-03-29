from __future__ import annotations

from enum import Enum
from typing import Optional

from PySide6 import QtCore, QtGui, QtWidgets

from jarvis.config import ui_config


class SphereState(str, Enum):
    IDLE = "idle"
    LISTENING = "listening"
    PROCESSING = "processing"
    SPEAKING = "speaking"


class SphereWidget(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._state: SphereState = SphereState.IDLE
        self._audio_level: float = 0.0

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_NoSystemBackground)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.WindowStaysOnTopHint
            | QtCore.Qt.WindowType.Tool
        )
        self.resize(300, 300)

        self._pulse_timer = QtCore.QTimer(self)
        self._pulse_timer.timeout.connect(self._decay_audio_level)
        self._pulse_timer.start(30)

    def set_state(self, state: SphereState) -> None:
        self._state = state
        self.update()

    def set_audio_level(self, level: float) -> None:
        # level expected in [0, 1]
        self._audio_level = max(0.0, min(1.0, level))
        self.update()

    def _decay_audio_level(self) -> None:
        if self._audio_level > 0.01:
            self._audio_level *= 0.9
            self.update()

    def _current_color(self) -> QtGui.QColor:
        if self._state == SphereState.LISTENING:
            return QtGui.QColor(ui_config.sphere_listening_color)
        if self._state == SphereState.PROCESSING:
            return QtGui.QColor(ui_config.sphere_processing_color)
        if self._state == SphereState.SPEAKING:
            return QtGui.QColor(ui_config.sphere_speaking_color)
        return QtGui.QColor(ui_config.sphere_idle_color)

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:  # type: ignore[override]
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)

        rect = self.rect()
        size = min(rect.width(), rect.height())
        base_radius = size * 0.3
        extra = self._audio_level * size * 0.2
        radius = base_radius + extra

        center = rect.center()

        gradient = QtGui.QRadialGradient(center, radius)
        color = self._current_color()
        gradient.setColorAt(0.0, color)
        gradient.setColorAt(0.7, color.lighter(150))
        gradient.setColorAt(1.0, QtGui.QColor(0, 0, 0, 0))

        brush = QtGui.QBrush(gradient)
        painter.setBrush(brush)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawEllipse(center, int(radius), int(radius))


class SphereUI:
    """
    Tiny wrapper that manages the Qt app and sphere widget.
    Main Jarvis loop can call:
        ui.set_state(SphereState.LISTENING)
        ui.set_audio_level(level)
    """

    def __init__(self) -> None:
        self.app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
        self.widget = SphereWidget()
        self.widget.show()

    def set_state(self, state: SphereState) -> None:
        self.widget.set_state(state)

    def set_audio_level(self, level: float) -> None:
        self.widget.set_audio_level(level)

    def run(self) -> None:
        self.app.exec()

