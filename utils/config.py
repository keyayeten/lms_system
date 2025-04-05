import json
import os
from typing import Any, Tuple, Type

from dotenv import load_dotenv
from pydantic_settings import (
    BaseSettings,
    DotEnvSettingsSource,
    EnvSettingsSource,
    PydanticBaseSettingsSource,
)


class JsonConfigSettingsSource(PydanticBaseSettingsSource):
    def __init__(self, settings_cls: Type[BaseSettings], json_file: str):
        super().__init__(settings_cls)
        self.json_file = json_file
        self._config_data = self._load_json_config()

    def _load_json_config(self) -> dict:
        """Load and resolve JSON configuration from the file."""
        try:
            with open(self.json_file, "r") as file:
                raw_config = json.load(file)
                return self._resolve_env_variables(raw_config)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"JSON configuration file '{self.json_file}' not found."
            )

    def _resolve_env_variables(self, value: Any) -> Any:
        """Resolve placeholders like ${ENV_VAR} in the JSON values."""
        load_dotenv()

        if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
            env_var = value[2:-1]
            return os.getenv(env_var, value)
        if isinstance(value, dict):
            return {k: self._resolve_env_variables(v) for k, v in value.items()}
        if isinstance(value, list):
            return [self._resolve_env_variables(v) for v in value]
        return value

    def __call__(self) -> dict:
        """Return the entire configuration data."""
        return self._config_data

    def get_field_value(self, field: str) -> Any:
        """Get a specific field value using dot notation."""
        keys = field.split(".")
        value = self._config_data
        try:
            for key in keys:
                value = value[key]
            return value
        except KeyError:
            return None


class DefaultSettings(BaseSettings):

    @classmethod
    def settings_customise_sources(
        cls, settings_cls: Type[BaseSettings], **kwargs
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            EnvSettingsSource(settings_cls),
            JsonConfigSettingsSource(settings_cls, json_file="config.json"),
            DotEnvSettingsSource(settings_cls, env_file=".env"),
        )
