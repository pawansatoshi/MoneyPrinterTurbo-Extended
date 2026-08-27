"""Provider-neutral local TTS runtime.

The Studio never hard-codes a paid vendor. Providers are selected from
providers.json and invoked through a configurable command template. This keeps
natural-voice generation optional and reproducible while allowing Chatterbox,
Kokoro, Piper, or another locally installed adapter.
"""
from __future__ import annotations

import argparse
import json
import shlex
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROVIDERS = ROOT / "providers.json"


def load_config() -> dict:
    return json.loads(PROVIDERS.read_text(encoding="utf-8"))


def build_command(provider: str, text_file: str, output_file: str, extra: list[str] | None = None) -> list[str]:
    data = load_config()
    item = data["providers"].get(provider)
    if not item:
        raise ValueError(f"Unknown voice provider: {provider}")
    template = item.get("command_template") or item.get("command")
    if not template:
        raise ValueError(f"Provider {provider} has no command configured")
    command = template.format(text=shlex.quote(text_file), output=shlex.quote(output_file))
    return shlex.split(command) + (extra or [])


def synthesize(provider: str, text: str, output: str, *, consented: bool = False, extra: list[str] | None = None) -> str:
    data = load_config()
    if provider not in data["providers"]:
        raise ValueError(f"Unknown voice provider: {provider}")
    if provider == "external":
        raise ValueError("External provider requires a project-specific adapter")
    text_path = Path(output).with_suffix(".txt")
    text_path.parent.mkdir(parents=True, exist_ok=True)
    text_path.write_text(text, encoding="utf-8")
    cmd = build_command(provider, str(text_path), output, extra)
    subprocess.run(cmd, check=True)
    if not Path(output).exists():
        raise RuntimeError(f"Voice provider completed without creating {output}")
    provenance = Path(output).with_suffix(Path(output).suffix + ".provenance.json")
    provenance.write_text(json.dumps({
        "provider": provider,
        "consented_voice": bool(consented),
        "voice_cloning_policy": data["policy"],
    }, indent=2), encoding="utf-8")
    return output


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Pawan Video Studio TTS runtime")
    ap.add_argument("provider")
    ap.add_argument("text")
    ap.add_argument("output")
    ap.add_argument("--consented", action="store_true")
    args = ap.parse_args()
    synthesize(args.provider, args.text, args.output, consented=args.consented)
