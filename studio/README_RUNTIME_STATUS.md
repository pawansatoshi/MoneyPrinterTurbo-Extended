# PawanStudio Runtime Status

The Studio is fail-closed: unavailable analysis is not a pass.

Implemented runtime foundations:
- resumable stage state machine
- live research adapter contract with conservative official verification
- forensic FFmpeg/FFprobe sampling and black-frame detection
- advanced mandatory QC gate contract
- self-healing controller
- originality/cliche scoring
- official-first provenance policy
- provider-neutral voice runtime

Provider adapters are explicit integration points. A missing browser/search, ASR/CV, TTS, image/video generation or rendering dependency produces `blocked`/`unavailable`, never a false `PASS`.

A production master is releasable only after all mandatory gates have executable evidence and the final review passes. Self-healing may retry targeted repairs, but it must stop and request review when a repairer or required analyzer is unavailable.
