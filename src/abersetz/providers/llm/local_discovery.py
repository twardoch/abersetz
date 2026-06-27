# this_file: src/abersetz/providers/llm/local_discovery.py
from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

import fire


@dataclass
class LocalModel:
    """Represents a discovered local AI model."""

    path: Path
    name: str
    app: str
    format: str
    size: int


class LocalModelFinder:
    """Discovers downloaded LLM and AI models across standard directories on macOS and Windows."""

    def __init__(self) -> None:
        self.home = Path.home()

        # Extensions to look for
        self.target_extensions = {
            "GGUF": [".gguf"],
            "Safetensors": [".safetensors"],
            "PyTorch": [".bin", ".pt", ".pth"],
            "ONNX": [".onnx"],
        }

        # Bundle formats (directories)
        self.target_bundles = {"CoreML": [".mlpackage"]}

    def _get_lmstudio_path(self) -> Path:
        """Determine LM Studio models path gracefully."""
        pointer_path = self.home / ".lmstudio-home-pointer"
        if pointer_path.exists():
            try:
                target_dir = pointer_path.read_text(encoding="utf-8").strip()
                return Path(target_dir) / "models"
            except Exception:
                pass

        # Fallbacks for standard directories
        paths = [self.home / ".cache" / "lm-studio" / "models", self.home / ".lmstudio" / "models"]
        for p in paths:
            if p.exists():
                return p
        return paths[0]

    def _get_search_paths(self) -> dict[str, Path]:
        """Return a dictionary of apps and their expected model directories."""
        paths = {
            "HuggingFace": self.home / ".cache" / "huggingface" / "hub",
            "Ollama": self.home / ".ollama" / "models",
            "LMStudio": self._get_lmstudio_path(),
            "Pinokio": self.home / "pinokio",
            "GPT4All": self.home / "AppData" / "Local" / "nomic.ai" / "GPT4All"
            if os.name == "nt"
            else self.home / "Library" / "Application Support" / "nomic.ai" / "GPT4All",
        }
        # Only return paths that actually exist on this system
        return {app: path for app, path in paths.items() if path.exists()}

    def _get_dir_size(self, path: Path) -> int:
        """Calculate total size of a directory recursively."""
        try:
            return sum(f.stat().st_size for f in path.rglob("*") if f.is_file())
        except Exception:
            return 0

    def _format_matches(self, format_name: str, format_filter: str | None) -> bool:
        """Return whether a discovered model format passes the CLI filter."""
        if not format_filter:
            return True
        return format_name.lower().replace(".", "") == format_filter.lower().replace(".", "")

    def _format_label(self, format_name: str) -> str:
        """Normalize raw format names for display."""
        labels = {
            "gguf": "GGUF",
            "safetensors": "Safetensors",
            "pytorch": "PyTorch",
            "onnx": "ONNX",
            "coreml": "CoreML",
        }
        return labels.get(format_name.lower(), format_name)

    def _discover_lmstudio_cli_models(
        self, format_filter: str | None, min_size_bytes: int
    ) -> list[LocalModel]:
        """Use `lms ls --json` so LM Studio models are grouped like LM Studio reports them."""
        lms_path = shutil.which("lms")
        if not lms_path:
            return []

        try:
            with tempfile.NamedTemporaryFile(mode="w+", encoding="utf-8") as output:
                subprocess.run(
                    [lms_path, "ls", "--json"],
                    check=True,
                    stderr=subprocess.PIPE,
                    stdout=output,
                    text=True,
                    timeout=30,
                )
                output.seek(0)
                raw_models = json.load(output)
        except (OSError, subprocess.SubprocessError, json.JSONDecodeError):
            return []

        if not isinstance(raw_models, list):
            return []

        lmstudio_root = self._get_lmstudio_path()
        models: list[LocalModel] = []
        for item in raw_models:
            if not isinstance(item, Mapping):
                continue

            size = item.get("sizeBytes", 0)
            model_format = str(item.get("format") or "unknown")
            relative_path = str(item.get("path") or "")
            if not isinstance(size, int) or size < min_size_bytes:
                continue
            if not self._format_matches(model_format, format_filter):
                continue

            name = str(item.get("modelKey") or item.get("displayName") or relative_path)
            models.append(
                LocalModel(
                    path=lmstudio_root / relative_path if relative_path else lmstudio_root,
                    name=name,
                    app="LMStudio",
                    format=self._format_label(model_format),
                    size=size,
                )
            )
        return models

    def discover_models(
        self, format_filter: str | None = None, min_size_mb: float = 100.0
    ) -> list[LocalModel]:
        """Scan for AI models on disk.

        Args:
            format_filter: (Optional) Filter by a specific extension, e.g. 'gguf' or 'safetensors'.
            min_size_mb: Minimum file size in MB to filter out small configs (default: 100.0).
        """
        search_paths = self._get_search_paths()
        min_size_bytes = int(min_size_mb * 1024 * 1024)
        discovered: list[LocalModel] = []

        for app_name, app_path in search_paths.items():
            if app_name == "LMStudio":
                lmstudio_models = self._discover_lmstudio_cli_models(format_filter, min_size_bytes)
                if lmstudio_models:
                    discovered.extend(lmstudio_models)
                    continue

            for root, dirs, files in os.walk(app_path):
                root_path = Path(root)

                # 1. Check for Directory Bundles (like CoreML .mlpackage)
                # We iterate backwards to safely remove items from the list during iteration
                for i in range(len(dirs) - 1, -1, -1):
                    d = dirs[i]
                    if any(d.endswith(ext) for ext in self.target_bundles["CoreML"]):
                        bundle_path = root_path / d

                        if format_filter and format_filter.lower() != "coreml":
                            del dirs[i]
                            continue

                        size = self._get_dir_size(bundle_path)
                        if size >= min_size_bytes:
                            discovered.append(
                                LocalModel(
                                    path=bundle_path,
                                    name=d,
                                    app=app_name,
                                    format="CoreML",
                                    size=size,
                                )
                            )
                        # Don't recurse into the mlpackage bundle
                        del dirs[i]

                # 2. Check for Standard Model Files
                for f in files:
                    file_path = root_path / f

                    # Special handling for Ollama (stored as extensionless sha256 blobs)
                    if (
                        app_name == "Ollama"
                        and root_path.name == "blobs"
                        and f.startswith("sha256-")
                    ):
                        if format_filter and format_filter.lower() != "gguf":
                            continue
                        try:
                            size = file_path.stat().st_size
                            if size >= min_size_bytes:
                                discovered.append(
                                    LocalModel(
                                        path=file_path,
                                        name=f,
                                        app=app_name,
                                        format="GGUF",
                                        size=size,
                                    )
                                )
                        except OSError:
                            pass
                        continue

                    # General extension matching
                    ext = file_path.suffix.lower()
                    if format_filter:
                        fmt_clean = format_filter.lower().replace(".", "")
                        if f".{fmt_clean}" != ext:
                            continue

                    # Identify the format label
                    matched_format = None
                    for fmt_label, extensions in self.target_extensions.items():
                        if ext in extensions:
                            matched_format = fmt_label
                            break

                    if matched_format:
                        try:
                            size = file_path.stat().st_size
                            if size >= min_size_bytes:
                                discovered.append(
                                    LocalModel(
                                        path=file_path,
                                        name=f,
                                        app=app_name,
                                        format=matched_format,
                                        size=size,
                                    )
                                )
                        except OSError:
                            pass

        return discovered

    def scan(self, format: str | None = None, min_size_mb: float = 100.0) -> None:
        """CLI wrapper for scan visualization."""
        models = self.discover_models(format_filter=format, min_size_mb=min_size_mb)

        if not models:
            print("No local models found with matching filters.")
            return

        print(f"[*] Discovered {len(models)} local models:\n")
        total_size = 0
        for m in models:
            size_gb = m.size / (1024 * 1024 * 1024)
            print(f"[{m.app} - {m.format}] {m.name} ({size_gb:.2f} GB)")
            print(f"  Path: {m.path}\n")
            total_size += m.size

        total_size_gb = total_size / (1024 * 1024 * 1024)
        print(f"[*] Summary: Total size of discovered models: {total_size_gb:.2f} GB")


if __name__ == "__main__":
    fire.Fire(LocalModelFinder)
