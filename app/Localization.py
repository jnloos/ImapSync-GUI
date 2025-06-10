import json
import os
import sys


class Localization:
    __translations: dict = {}

    @classmethod
    def load(cls, lang: str = "en"):
        lang = lang.lower()

        # Call the static method using the class name (cls._locales_path)
        primary_file_path = cls.__locales_path(f"{lang}.json")
        translations = cls.__load_file(primary_file_path)

        if not translations and lang != 'en':
            fallback_file_path = cls.__locales_path('en.json')
            translations = cls.__load_file(fallback_file_path)
            if translations:
                print("[Localization] Info: loaded fallback 'en' translations.")

        cls.__translations = translations or {}

    @classmethod
    def translate(cls, key: str) -> str:
        parts = key.split('.')
        value = cls.__translations
        try:
            for part in parts:
                value = value[part]
            return value if isinstance(value, str) else key
        except (KeyError, TypeError):
            return key

    @classmethod
    def __load_file(cls, file_path: str) -> dict:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"[Localization] Warning: couldn't load '{file_path}' ({e}).")
            return {}

    @staticmethod
    def __locales_path(file_name: str) -> str:
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            locales_dir = "locales"
            base_path = sys._MEIPASS
        else:
            locales_dir = "../locales"
            base_path = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(base_path, locales_dir, file_name)


def __(key: str, **kwargs) -> str:
    raw = Localization.translate(key)
    try:
        return raw.format(**kwargs)
    except (KeyError, AttributeError):
        return raw