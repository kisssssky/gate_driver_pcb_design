# AGENTS.md

## Project scope
Reproduce the functional behavior of Fig. 3 in Li et al., IEEE TPEL 2024, for fast SiC MOSFET BTI threshold-voltage-shift measurement.

## Hard constraints
1. One PCB must support both positive and negative BTI.
2. Positive/negative mode changes only through external VDDA/GNDA voltages and control waveform; do not require PCB component replacement.
3. SREF is the DUT Kelvin Source reference. Do not connect SREF to laboratory earth unless explicitly approved.
4. Si8273 channel A / VOA is the fast stress-to-measurement switching element.
5. Positive BTI: VDDA = VGS-P, GNDA = VGM-P, VIA transitions HIGH -> LOW at stress end.
6. Negative BTI: VDDA = VGM-N, GNDA = VGS-N, VIA transitions LOW -> HIGH at stress end.
7. The complete experiment requires 0 V precondition, stress, and measurement states.
8. The primary timing requirement is an interpretable VDS measurement point about 100 ns after stress ends, not merely a fast VOA edge.
9. Never invent component pin numbers, ratings, package data, or datasheet parameters.
10. Critical design choices must identify their basis: paper, datasheet, calculation, or engineering assumption.
11. Unresolved items must stay explicitly unresolved.
12. Do not generate Gerbers or production files until ERC, DRC, manual review, and the verification matrix are approved.
13. Do not silently connect GNDI, GNDA, SREF, chassis ground, or earth.
14. Do not change frozen interfaces without master-project approval.

## Required change report
For every engineering change, report:
- files changed
- electrical behavior changed
- calculations performed
- assumptions introduced
- unresolved ERC/DRC warnings
- risks introduced or retired
- items requiring approval

## Preferred workflow
1. Read `docs/requirements.md`, `docs/interfaces.md`, `docs/decisions.md`, and `docs/project_status.md` before modifying hardware files.
2. Work on a branch for nontrivial changes.
3. Keep schematic, PCB, BOM, calculations, and documentation consistent.
4. Run available checks after changes.
5. Do not proceed to manufacturing outputs without explicit approval.
