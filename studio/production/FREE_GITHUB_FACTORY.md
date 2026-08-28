# Free GitHub Video Factory

## Operating model

PawanStudio uses GitHub Actions as the orchestration layer. The repository remains the source of truth for rules, adapters, project manifests and QC. The workflow is intentionally free-first: it uses the public-repository GitHub Actions allowance and open-source dependencies where feasible; it does not assume paid APIs, paid stock libraries, or a dedicated GPU.

### Important compute rule

GitHub-hosted free CPU runners are suitable for orchestration, web research, lightweight image processing, FFmpeg editing and QC. Large local TTS/voice-cloning/video-generation models may exceed free runner CPU/RAM/time limits. Such stages must use a supported lightweight CPU model or be explicitly marked BLOCKED; they must never silently fall back to a robotic commercial TTS service.

## Voice

`reference_audio/pawan_english_reference.mp3` and `reference_audio/pawan_hindi_reference.mp3` are authorized creator references when present. They are references, not narration scripts. A production adapter must read the corresponding manifest and verify the actual file before using it.

If the reference file cannot be read by the runtime, authenticated creator-voice narration is BLOCKED. Do not substitute unrelated voices.

## Official project assets

The project URL supplied to the workflow is the first-party discovery root. The asset collector must retrieve/capture official pages and register provenance before rendering. User-uploaded screenshots are not automatic substitutes. If an official product asset cannot be verified, the relevant scene is BLOCKED.

## Production outputs

Every run should publish, when successful:

- final MP4;
- request.json;
- storyboard.json;
- claims.json;
- asset_manifest.json;
- provenance.json;
- qc_report.json;
- repair_log.json.

## Release gate

The final MP4 must be generated first and then inspected. A successful process exit is not a QC pass. Any failed visual, audio, subtitle, provenance, authenticity, pacing, repetition or technical gate triggers repair and a complete re-check. Missing analyzers are blocking conditions.

## No misleading completion

The workflow must never report PASS unless the exact final artifact was produced and all applicable gates produced evidence for that exact artifact hash/version.
