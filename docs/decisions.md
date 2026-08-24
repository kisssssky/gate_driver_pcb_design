# Decision Log

## Approved baseline decisions
- DEC-001: Use one PCB for both positive and negative BTI.
- DEC-002: Change BTI polarity only through external VDDA/GNDA voltages and VIA waveform polarity; no PCB component replacement.
- DEC-003: Define SREF as DUT Kelvin Source reference.
- DEC-004: Do not assume SREF is laboratory earth.
- DEC-005: Use Si8273 channel A / VOA for the fast stress-to-measurement transition.
- DEC-006: Positive BTI uses VDDA = VGS-P, GNDA = VGM-P, VIA HIGH -> LOW at stress end.
- DEC-007: Negative BTI uses VDDA = VGM-N, GNDA = VGS-N, VIA LOW -> HIGH at stress end.
- DEC-008: The complete reproduction must include a 0 V precondition state in addition to stress and measurement states.
- DEC-009: System success is judged by obtaining an interpretable VDS measurement point about 100 ns after stress removal, not by VOA edge speed alone.
- DEC-010: No manufacturing output before ERC, DRC, manual review, and verification-matrix approval.

## Proposed but not yet frozen
- PROP-001: Use a separate precondition clamp/switch for Gate-to-SREF 0 V state while Si8273 handles only the fast two-level stress/measurement transition.
- PROP-002: Keep PCB connector labels generic (`VDDA`, `GNDA`, `SREF`) rather than fixed voltage labels such as +18 V or -12 V.

## Decision status rules
- `DEC-*` = approved baseline.
- `PROP-*` = proposed; may not be treated as frozen by Codex.
- Any change to `DEC-*` requires master-project approval and corresponding interface/risk review.
