from __future__ import annotations

from typing import Optional

import speech_recognition as sr

from jarvis.config import audio_config


class SpeechToText:
    def __init__(self) -> None:
        self._recognizer = sr.Recognizer()
        self._microphone = sr.Microphone()

        self._recognizer.energy_threshold = audio_config.energy_threshold
        self._recognizer.pause_threshold = audio_config.pause_threshold

    def listen_for_command(
        self,
        prompt: Optional[str] = None,
        timeout: Optional[int] = None,
        phrase_time_limit: Optional[int] = None,
    ) -> Optional[str]:
        """
        Listen once and return recognized text (without the wake word).
        Returns None if nothing is understood.
        """
        phrase_time_limit = phrase_time_limit or audio_config.phrase_time_limit

        with self._microphone as source:
            if prompt:
                print(prompt)
            audio = self._recognizer.listen(
                source, timeout=timeout, phrase_time_limit=phrase_time_limit
            )

        try:
            text = self._recognizer.recognize_google(
                audio, language=audio_config.language
            )
            cleaned = text.lower().strip()

            wake = audio_config.wake_word.lower()
            if cleaned.startswith(wake):
                cleaned = cleaned[len(wake) :].strip()

            return cleaned or None
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            return None

