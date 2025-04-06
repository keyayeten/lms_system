from dotenv import load_dotenv
from typing import Any, Type, Tuple
from pydantic_settings import (
    BaseSettings,
    DotEnvSettingsSource,
    EnvSettingsSource,
    PydanticBaseSettingsSource,
)
import os
import json


class JsonConfigSettingsSource(PydanticBaseSettingsSource):
    def __init__(self, settings_cls: Type[BaseSettings], json_file: str):
        super().__init__(settings_cls)
        self.json_file = json_file
        self._config_data = self._load_json_config()

    def _load_json_config(self) -> dict:
        try:
            with open(self.json_file, "r") as file:
                raw_config = json.load(file)
                return self._resolve_env_variables(raw_config)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"JSON configuration file '{self.json_file}' not found."
            )

    def _resolve_env_variables(self, value: Any) -> Any:
        if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
            env_var = value[2:-1]
            return os.getenv(env_var, value)
        if isinstance(value, dict):
            return {k: self._resolve_env_variables(v) for k, v in value.items()}
        if isinstance(value, list):
            return [self._resolve_env_variables(v) for v in value]
        return value

    def __call__(self) -> dict:
        return self._config_data

    def get_field_value(self, field_name: str, field: Any) -> Any:
        return self._config_data.get(field_name, None)


class DefaultSettings(BaseSettings):
    @classmethod
    def settings_customise_sources(
        cls, settings_cls: Type[BaseSettings], **kwargs
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        env_path = getattr(settings_cls.Config, "env_path", "app/.env")
        config_path = getattr(settings_cls.Config, "config_path", "app/config.json")

        load_dotenv(env_path)

        return (
            EnvSettingsSource(settings_cls),
            DotEnvSettingsSource(settings_cls, env_file=env_path),
            JsonConfigSettingsSource(settings_cls, json_file=config_path),
        )