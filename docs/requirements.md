# System Requirements

Status: draft baseline — SP1 Master approved; canonical SP1 requirement merge still pending

## Output persistence requirements

- REQ-105: Every project chat that produces a user-facing output file shall synchronize that file to this GitHub repository before the task is marked complete.
- REQ-106: Every synchronized output file shall be stored at its canonical engineering path and registered in `docs/chat_output_index.md`.
- REQ-107: Outputs containing non-redistributable copyrighted material, credentials, secrets, personal sensitive information, or unapproved large binaries shall not be committed directly; the block and approved alternative shall be recorded.
- REQ-108: If GitHub synchronization cannot be completed, the task shall report `OUTPUT_SYNC_BLOCKED` and identify every unsynchronized file.

Detailed policy: [`output_sync_policy.md`](output_sync_policy.md).

## Functional requirements
- REQ-001: A single PCB shall support both positive and negative BTI operation.
- REQ-002: Switching between positive and negative BTI modes shall require only changes to external VDDA/GNDA voltages and the VIA control waveform, not PCB component changes.
- REQ-003: SREF shall be the DUT Kelvin Source reference.
- REQ-004: SREF shall not be assumed to equal laboratory earth.
- REQ-005: Si8273 VOA shall provide the fast stress-to-measurement gate-voltage transition.
- REQ-006: Positive BTI mode shall use VDDA = VGS-P and GNDA = VGM-P, with VIA HIGH during stress and LOW during measurement.
- REQ-007: Negative BTI mode shall use VDDA = VGM-N and GNDA = VGS-N, with VIA LOW during stress and HIGH during measurement.
- REQ-008: The complete measurement sequence shall support 0 V precondition, stress, and measurement states.
- REQ-009: The system shall support calibration, positive-stress, and negative-stress sequences corresponding to MI, MP, and MN extraction.
- REQ-010: The target system-level test delay shall be approximately 100 ns from stress removal to an interpretable VDS measurement point. The exact electrical start/end algorithm remains an OPEN project acceptance item.
- REQ-011: VGS shall be measured relative to DUT Kelvin Source, not gate-to-earth.
- REQ-012: The drain loop shall support a resistive-load measurement architecture consistent with Fig. 3 of the reference paper.
- REQ-013: Power Source and Kelvin Source paths shall be separated where the DUT/package permits.
- REQ-014: The design shall expose measurement points for VGS, VDS, and timing/trigger observation.
- REQ-015: The platform shall support low-VDS BTI / Vth-hysteresis testing of both 650 V-class and 3.3 kV-class SiC MOSFETs. DUT blocking-voltage rating shall not by itself be treated as the required operating voltage of this BTI PCB.
- REQ-016: DUT-specific gate levels, `VDS-C`, `Ith`, load conditions, gate-drive-current sizing, package/interface details, and timing checks shall be defined per target DUT. Numerical values from the reference paper are examples for its 1.2 kV DUT unless separately adopted by the project.

## Process requirements
- REQ-100: All component pin assignments and electrical ratings shall be verified from authoritative datasheets before schematic freeze.
- REQ-101: All critical design decisions shall be tagged as paper-derived, datasheet-derived, calculated, or engineering assumption.
- REQ-102: ERC shall pass or all residual warnings shall be explicitly reviewed before PCB layout freeze.
- REQ-103: DRC shall pass or all residual warnings shall be explicitly reviewed before manufacturing output.
- REQ-104: Gerbers and production files shall not be generated until ERC, DRC, manual review, and verification-matrix approval are complete.

## Open requirement items
- OPEN-REQ-001: Exact DUT model and package.
- OPEN-REQ-002: Final VGS-P, VGS-N, VGM-I, VGM-P, and VGM-N ranges.
- OPEN-REQ-003: Exact VDS-C, Ith, VDC, and RL targets for the selected DUT.
- OPEN-REQ-004: Exact implementation of the 0 V precondition state.
- OPEN-REQ-005: Instrument models and bandwidth requirements for VGS/VDS capture.
- OPEN-REQ-006: Exact adaptation policy for supporting 650 V-class and 3.3 kV-class DUTs: connector/adapter strategy, permitted Rg changes, and Kelvin-Source/package variants.
- OPEN-REQ-007: Exact project `tdly` PASS definition, including electrical start event, measured-point/extremum algorithm, search window, filtering, ringing treatment, and deskew/de-embedding policy.
- OPEN-REQ-008: Merge and reconcile the approved SP1 36-ID requirement set into this canonical project requirement baseline with full traceability and no ID ambiguity.

## Approved SP1 evidence baseline

The paper-derived method baseline is now Master-approved at:
- `docs/SP1_paper_method_system_requirements_v0.2.md`
- `docs/SP1_final_gate_review_v1.0.md`
- `docs/SP1_master_review_v1.0.md`

Until OPEN-REQ-008 is closed, this file remains a project-level draft and must not be treated as a fully frozen G0 canonical baseline.
