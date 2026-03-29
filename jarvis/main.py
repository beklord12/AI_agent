from __future__ import annotations

import threading
from typing import Optional

from jarvis.brain.commands import CommandBrain
from jarvis.system.computer_control import SystemController
from jarvis.ui.sphere_ui import SphereState, SphereUI
from jarvis.voice.speech_to_text import SpeechToText
from jarvis.voice.text_to_speech import TextToSpeech
from jarvis.voice.wake_word import WakeWordDetector


class JarvisApp:
    def __init__(self, ui: Optional[SphereUI] = None) -> None:
        self.ui = ui
        self.system = SystemController()
        self.brain = CommandBrain(self.system)
        self.stt = SpeechToText()
        self.tts = TextToSpeech()
        self.wake = WakeWordDetector(on_detect=self._on_wake_detected)

        self._wake_event = threading.Event()

    def _on_wake_detected(self) -> None:
        self._wake_event.set()
        if self.ui:
            self.ui.set_state(SphereState.LISTENING)
        self.tts.speak("sir?")

    def run(self) -> None:
        while True:
            if self.ui:
                self.ui.set_state(SphereState.IDLE)

            self._wake_event.clear()
            self.wake.start_listening()  # blocks until wake word

            self._wake_event.wait()

            if self.ui:
                self.ui.set_state(SphereState.LISTENING)

            command = self.stt.listen_for_command(prompt="Listening for command...")

            if self.ui:
                self.ui.set_state(SphereState.PROCESSING)

            result = self.brain.handle(command or "")

            if result.handled and result.action:
                result.action()

            if self.ui:
                self.ui.set_state(SphereState.SPEAKING)

            self.tts.speak(result.response)

    @staticmethod
    def start_with_ui() -> None:
        ui = SphereUI()

        def jarvis_loop() -> None:
            app = JarvisApp(ui=ui)
            app.run()

        t = threading.Thread(target=jarvis_loop, daemon=True)
        t.start()
        ui.run()


if __name__ == "__main__":
    JarvisApp.start_with_ui()

