import json
import os

class Localization:
    __translations: dict = {}

    @classmethod
    def __load_file(cls, file_path: str) -> dict:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"[Localization] Warning: couldn't load '{file_path}' ({e}).")
            return {}

    @classmethod
    def load(cls, lang: str = "en", path: str = "locales"):
        # Try requested language
        primary_path = os.path.join(path, f"{lang}.json")
        translations = cls.__load_file(primary_path)

        # If primary failed and isn't English, fall back
        if not translations and lang != 'en':
            fallback_path = os.path.join(path, 'en.json')
            translations = cls.__load_file(fallback_path)
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


def __(key: str, **kwargs) -> str:
    raw = Localization.translate(key)
    try:
        return raw.format(**kwargs)
    except (KeyError, AttributeError):
        return raw
