# Production Adapter Contract

The GitHub Actions factory must invoke the repository's real rendering engine through a stable adapter. The adapter is responsible for:

1. loading the current PawanStudio rulebook;
2. project research and official-source asset collection;
3. fresh script/storyboard generation;
4. authorized creator voice selection;
5. rendering through the existing MoneyPrinterTurbo/Extended engine;
6. forensic QC of the exact output;
7. self-healing and complete re-QC;
8. artifact publication only after PASS.

The factory may not fabricate a successful run. If any required engine or adapter is missing, the workflow must return BLOCKED with a machine-readable report.

## Free-first policy

Use open-source/local components and GitHub-hosted compute where practical. Do not require paid APIs by default. Heavy model stages must have a CPU-feasible open-source implementation or a clearly reported blocking condition.
