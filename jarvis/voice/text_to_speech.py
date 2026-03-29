from __future__ import annotations

import threading

import pyttsx3


class TextToSpeech:
    """Simple wrapper around pyttsx3 for offline TTS."""

    def __init__(self) -> None:
        self._engine = pyttsx3.init()
        self._lock = threading.Lock()

    def speak(self, text: str) -> None:
        """Speak the given text synchronously (thread-safe)."""
        if not text:
            return

        with self._lock:
            self._engine.stop()
            self._engine.say(text)
            self._engine.runAndWait()

