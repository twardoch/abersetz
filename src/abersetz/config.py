"""Configuration helpers for abersetz."""
# this_file: src/abersetz/config.py

from __future__ import annotations

import json
import os
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from platformdirs import user_config_dir

CONFIG_FILENAME = "config.json"


@dataclass(slots=True)
class Defaults:
    """Runtime defaults for translation."""

    engine: str = "translators/google"
    from_lang: str = "auto"
    to_lang: str = "en"
    chunk_size: int = 1200
    html_chunk_size: int = 1800

    def to_dict(self) -> dict[str, Any]:
        return {
            "engine": self.engine,
            "from_lang": self.from_lang,
            "to_lang": self.to_lang,
            "chunk_size": self.chunk_size,
            "html_chunk_size": self.html_chunk_size,
        }

    @classmethod
    def from_dict(cls, raw: Mapping[str, Any] | None) -> Defaults:
        if raw is None:
            return cls()
        return cls(
            engine=str(raw.get("engine", cls.engine)),
            from_lang=str(raw.get("from_lang", cls.from_lang)),
            to_lang=str(raw.get("to_lang", cls.to_lang)),
            chunk_size=int(raw.get("chunk_size", cls.chunk_size)),
            html_chunk_size=int(raw.get("html_chunk_size", cls.html_chunk_size)),
        )


@dataclass(slots=True)
class Credential:
    """Represents an API credential reference."""

    name: str | None = None
    env: str | None = None
    value: str | None = None

    def to_dict(self) -> dict[str, str]:
        data: dict[str, str] = {}
        if self.name:
            data["name"] = self.name
        if self.env:
            data["env"] = self.env
        if self.value:
            data["value"] = self.value
        return data

    @classmethod
    def from_any(cls, raw: CredentialLike | None) -> Credential | None:
        if raw is None:
            return None
        if isinstance(raw, Credential):
            return raw
        if isinstance(raw, str):
            return cls(name=raw)
        if isinstance(raw, Mapping):
            return cls(
                name=raw.get("name"),
                env=raw.get("env"),
                value=raw.get("value"),
            )
        raise TypeError(f"Unsupported credential payload: {type(raw)!r}")


CredentialLike = Credential | Mapping[str, Any] | str | None


@dataclass(slots=True)
class EngineConfig:
    """Engine specific configuration block."""

    name: str
    chunk_size: int | None = None
    html_chunk_size: int | None = None
    credential: Credential | None = None
    options: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {"name": self.name, "options": self.options}
        if self.chunk_size is not None:
            data["chunk_size"] = self.chunk_size
        if self.html_chunk_size is not None:
            data["html_chunk_size"] = self.html_chunk_size
        if self.credential:
            data["credential"] = self.credential.to_dict()
        return data

    @classmethod
    def from_dict(cls, name: str, raw: Mapping[str, Any] | None) -> EngineConfig:
        if raw is None:
            return cls(name=name)
        return cls(
            name=name,
            chunk_size=raw.get("chunk_size"),
            html_chunk_size=raw.get("html_chunk_size"),
            credential=Credential.from_any(raw.get("credential")),
            options=dict(raw.get("options", {})),
        )


@dataclass(slots=True)
class AbersetzConfig:
    """Aggregate configuration for the toolkit."""

    defaults: Defaults = field(default_factory=Defaults)
    credentials: dict[str, Credential] = field(default_factory=dict)
    engines: dict[str, EngineConfig] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "defaults": self.defaults.to_dict(),
            "credentials": {key: cred.to_dict() for key, cred in self.credentials.items()},
            "engines": {key: engine.to_dict() for key, engine in self.engines.items()},
        }

    @classmethod
    def from_dict(cls, raw: Mapping[str, Any]) -> AbersetzConfig:
        defaults = Defaults.from_dict(raw.get("defaults"))
        credentials = {
            key: Credential.from_any(value) or Credential(name=key)
            for key, value in dict(raw.get("credentials", {})).items()
        }
        engines = {
            key: EngineConfig.from_dict(key, value)
            for key, value in dict(raw.get("engines", {})).items()
        }
        return cls(defaults=defaults, credentials=credentials, engines=engines)


DEFAULT_CONFIG_DICT: dict[str, Any] = {
    "defaults": Defaults().to_dict(),
    "credentials": {
        "siliconflow": {"name": "siliconflow", "env": "SILICONFLOW_API_KEY"},
    },
    "engines": {
        "translators": {
            "name": "translators",
            "chunk_size": 800,
            "options": {"provider": "google"},
        },
        "deep-translator": {
            "name": "deep-translator",
            "chunk_size": 800,
            "options": {"provider": "google"},
        },
        "hysf": {
            "name": "hysf",
            "chunk_size": 2400,
            "credential": {"name": "siliconflow"},
            "options": {
                "model": "tencent/Hunyuan-MT-7B",
                "base_url": "https://api.siliconflow.com/v1",
                "temperature": 0.3,
            },
        },
        "ullm": {
            "name": "ullm",
            "chunk_size": 2400,
            "credential": {"name": "siliconflow"},
            "options": {
                "profiles": {
                    "default": {
                        "base_url": "https://api.siliconflow.com/v1",
                        "model": "tencent/Hunyuan-MT-7B",
                        "temperature": 0.3,
                        "max_input_tokens": 32000,
                        "prolog": {},
                    }
                }
            },
        },
    },
}


def _default_dict() -> dict[str, Any]:
    """Return a deep copy of the default config mapping."""
    return json.loads(json.dumps(DEFAULT_CONFIG_DICT))


def _default_config() -> AbersetzConfig:
    """Return a fresh ``AbersetzConfig`` with defaults."""
    return AbersetzConfig.from_dict(_default_dict())


def config_dir() -> Path:
    """Return directory holding the configuration file."""
    custom = os.getenv("ABERSETZ_CONFIG_DIR")
    if custom:
        return Path(custom)
    return Path(user_config_dir(appname="abersetz", appauthor="twardoch"))


def config_path() -> Path:
    """Return absolute path to the configuration file."""
    return config_dir() / CONFIG_FILENAME


def load_config() -> AbersetzConfig:
    """Load configuration from disk, creating defaults if needed."""
    path = config_path()
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        save_config(_default_config())
        return _default_config()
    return AbersetzConfig.from_dict(json.loads(path.read_text()))


def save_config(config: AbersetzConfig) -> None:
    """Persist configuration to ``config.json``."""
    path = config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(config.to_dict(), indent=2, sort_keys=True))


def resolve_credential(
    config: AbersetzConfig,
    reference: CredentialLike,
) -> str | None:
    """Resolve a credential reference to a usable secret."""
    credential = Credential.from_any(reference)
    if credential is None:
        return None
    if credential.name:
        stored = config.credentials.get(credential.name)
        if stored and stored != credential:
            return resolve_credential(config, stored)
    if credential.env:
        env_value = os.getenv(credential.env)
        if env_value:
            return env_value
    if credential.value:
        return credential.value
    if credential.name and credential.name in config.credentials:
        return resolve_credential(config, config.credentials[credential.name])
    return None


__all__ = [
    "AbersetzConfig",
    "Credential",
    "CredentialLike",
    "Defaults",
    "EngineConfig",
    "config_dir",
    "config_path",
    "load_config",
    "resolve_credential",
    "save_config",
]
