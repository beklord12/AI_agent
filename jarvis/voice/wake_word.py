from __future__ import annotations

import time
from typing import Callable, Optional

import speech_recognition as sr

from jarvis.config import audio_config


class WakeWordDetector:
    """
    Very simple wake word detector using speech_recognition.

    It continuously listens in short chunks and looks for the word "jarvis"
    (or whatever is configured in AudioConfig.wake_word) in the recognized text.
    """

    def __init__(self, on_detect: Optional[Callable[[], None]] = None) -> None:
        self._recognizer = sr.Recognizer()
        self._microphone = sr.Microphone()
        self._on_detect = on_detect
        self._running = False

        self._recognizer.energy_threshold = audio_config.energy_threshold
        self._recognizer.pause_threshold = audio_config.pause_threshold

    def start_listening(self) -> None:
        """Blocking loop that waits until the wake word is heard."""
        self._running = True
        wake = audio_config.wake_word.lower()

        with self._microphone as source:
            self._recognizer.adjust_for_ambient_noise(source, duration=1)

        while self._running:
            try:
                with self._microphone as source:
                    audio = self._recognizer.listen(
                        source, phrase_time_limit=audio_config.phrase_time_limit
                    )

                text = self._recognizer.recognize_google(
                    audio, language=audio_config.language
                ).lower()

                if wake in text:
                    if self._on_detect:
                        self._on_detect()
                    break
            except sr.UnknownValueError:
                # nothing understood in this chunk, keep listening
                pass
            except sr.RequestError:
                # network error – avoid tight loop
                time.sleep(1)

    def stop(self) -> None:
        self._running = False

