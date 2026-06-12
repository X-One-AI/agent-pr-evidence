from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

SUPPORTED_CONFIG_SCHEMA_VERSION = 1
SUPPORTED_PROFILES = {"default", "strict"}
DEFAULT_CONFIG_NAME = ".agent-pr-evidence.yml"


@dataclass(frozen=True)
class EvidenceConfig:
    profile: str = "default"
    disabled_risk_flags: tuple[str, ...] = ()

    @property
    def require_test_evidence(self) -> bool:
        return self.profile == "strict"


def load_config(path: Path | None, profile: str | None) -> EvidenceConfig:
    data: dict = {}
    if path:
        if not path.exists():
            raise ValueError(f"Config file does not exist: {path}")
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if not isinstance(raw, dict):
            raise ValueError("Config file must contain a YAML mapping")
        data = raw
    schema_version = data.get("schema_version", SUPPORTED_CONFIG_SCHEMA_VERSION)
    if schema_version != SUPPORTED_CONFIG_SCHEMA_VERSION:
        raise ValueError(f"Unsupported config schema_version: {schema_version}")
    selected_profile = profile or data.get("profile", "default")
    if selected_profile not in SUPPORTED_PROFILES:
        raise ValueError(f"Unknown profile: {selected_profile}")
    disabled = data.get("disabled_risk_flags", [])
    if disabled is None:
        disabled = ()
    if not isinstance(disabled, list):
        raise ValueError("disabled_risk_flags must be a list")
    if not all(isinstance(item, str) for item in disabled):
        raise ValueError("disabled_risk_flags entries must be strings")
    return EvidenceConfig(profile=selected_profile, disabled_risk_flags=tuple(disabled))


def resolve_config_path(repo: Path, config_path: str | None) -> Path | None:
    if config_path:
        return Path(config_path)
    candidate = repo / DEFAULT_CONFIG_NAME
    return candidate if candidate.exists() else None
