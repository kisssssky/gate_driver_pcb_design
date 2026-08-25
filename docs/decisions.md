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
- DEC-011: Every project chat output file must be saved to this GitHub repository before the corresponding task is considered complete.
- DEC-012: Output files use their canonical engineering location and are registered in `docs/chat_output_index.md`; duplicate archive copies are not required.
- DEC-013: Non-redistributable source PDFs, credentials, sensitive information, and unapproved large binaries are excluded from direct commits and require an explicit recorded alternative.
- DEC-014: Master approves `SP1-v0.2 + SP1-FGR-v1.0` as the completed paper-method/system-requirement evidence baseline. SP1 is closed unless a source error is later discovered.
- DEC-015: SP1 completion does not by itself close G0. G0 remains ACTIVE until project-level acceptance definitions and the canonical requirement baseline are frozen.
- DEC-016: The platform target includes low-VDS BTI/Vth-hysteresis testing of both 650 V-class and 3.3 kV-class SiC MOSFETs. DUT blocking-voltage rating does not itself require the BTI test PCB to operate at 650 V or 3.3 kV.
- DEC-017: Master批准`G0-CRB-v1.2`、其中65条`REQ-SYS-*`规范需求、69行SP1/legacy crosswalk及`OPEN::OI-001...022`的延期控制；`OPEN::OI-000`批准并关闭（`APPROVED / RESOLVED`）。`docs/requirements.md`从本决定生效起成为唯一项目级规范需求基线，基线状态为`FROZEN`；G0阶段门状态为`PASS`；G1保持`ACTIVE`，G3保持`BLOCKED`。legacy ID仅保留历史追溯。任何改变冻结需求的ID、技术含义、分类、scope、证据层级或crosswalk，必须经过Master change approval并留下change record。`OPEN::OI-001...022`继续按批准的owner、deadline和Gate关闭。本决定不批准任何具体电路拓扑、器件数值、DUT参数、`Rg`/电容值、0 V实现、保护实现、connector pinout、原理图、PCB或BOM。

## Proposed but not yet frozen
- PROP-001: Use a separate precondition clamp/switch for Gate-to-SREF 0 V state while Si8273 handles only the fast two-level stress/measurement transition.
- PROP-002: Keep PCB connector labels generic (`VDDA`, `GNDA`, `SREF`) rather than fixed voltage labels such as +18 V or -12 V.

## Decision status rules
- `DEC-*` = approved baseline.
- `PROP-*` = proposed; may not be treated as frozen by Codex.
- Any change to `DEC-*` requires master-project approval and corresponding interface/risk review.
- DEC-011 through DEC-013 were explicitly approved by the Master on 2026-08-24.
- DEC-014 through DEC-016 were approved during the SP1 Master Review on 2026-08-24.
- DEC-017于2026-08-25的G0 Master Review和规范基线安装中生效；需求基线状态为`FROZEN`，G0阶段门状态为`PASS`。
