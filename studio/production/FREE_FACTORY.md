# PawanStudio Free GitHub Factory

The production path is GitHub Actions. The baseline factory is designed to work without paid APIs or paid stock providers.

## Run a video

Open **Actions -> PawanStudio Video Factory -> Run workflow** and provide:

- `project_url`: the project's official website
- `language`: English, Hindi or Hinglish
- `aspect_ratio`: 16:9, 9:16 or 1:1
- `style`: e.g. cinematic educational, documentary, finance, tech
- `duration`: target seconds

The workflow then executes:

`official research -> first-party browser capture -> evidence/script -> authorized creator voice -> word-timed subtitles -> editorial visual cards -> MoneyPrinterTurbo/PawanStudio renderer -> forensic QC -> self-healing rerender -> artifact`

## Free-first design

- GitHub-hosted standard runner
- open-source/local Python dependencies
- local XTTS v2 voice inference using the authorized reference file
- Playwright for first-party browser capture
- faster-whisper for word timing
- MoviePy/FFmpeg for rendering
- GitHub Actions artifacts for output/evidence

No paid API key is required by the baseline path.

## Voice references

`reference_audio/pawan_english_reference.mp3` and `reference_audio/pawan_hindi_reference.mp3` are authorized creator references. The sample text is never copied as the narration script. The workflow writes a fresh script from current project research and uses the reference only for voice conditioning.

## Evidence artifacts

Each run attempts to produce:

- `pawanstudio_master.mp4`
- `request.json`
- `research.json`
- `script.txt`
- `official_asset_manifest.json`
- `asset_manifest.json`
- `render_manifest.json`
- `enhanced_subtitles.json`
- `qc_report.json`
- narration/reference audio intermediates

## Fail closed

If the official source cannot be verified, the authorized voice is missing, rendering fails, or a mandatory QC gate fails, the workflow exits non-zero and reports `BLOCKED`/`FAIL`. It does not substitute generic TTS or user screenshots and it does not claim PASS.

## Resource reality

Standard GitHub-hosted runners are free for public repositories, but they are CPU-based standard runners. Heavy local voice models can be slow. The workflow therefore caches model downloads and keeps the baseline pipeline CPU-compatible. If a future feature truly requires unavailable GPU capacity, that feature must be explicitly marked optional rather than silently pretending to be free.
