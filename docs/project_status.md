# Project Status

Version: v0.1
Phase: architecture and requirements definition

## Objective
Reproduce the functional measurement architecture of Fig. 3 in Li et al., IEEE TPEL 2024, with a custom PCB for fast SiC MOSFET BTI stress-to-measurement switching.

## Master stage-gate control
The detailed PCB development flow, AI/human responsibility split, required deliverables, and PASS criteria are maintained in:

- `docs/stage_gate.md`

Current gate state:
- G0 Requirements Definition — ACTIVE
- G1 System Architecture — ACTIVE
- G2 Component Selection & Calculations — NOT STARTED
- G3 and later — BLOCKED until upstream gates pass

`docs/stage_gate.md` must be updated whenever the project makes a meaningful design, verification, implementation, or test advance.

## Completed
- Repository initialized.
- Baseline project constraints recorded.
- Initial system requirements created.
- Initial electrical interfaces created.
- Initial decision log created.
- Initial risk register created.
- Master PCB stage-gate process created.

## Active subprojects
- SP1: paper method and system-requirement extraction — ready to start.
- SP2: Si8273 gate drive, supply architecture, and 0 V precondition — ready to start.
- SP3: drain resistive-load and measurement loop — ready to start.

## Blocked until upstream approval
- SP4: KiCad schematic and BOM.
- SP5: PCB placement/routing.
- SP6: hardware bring-up and validation execution.

## Parallel software work
- SP7: B1505/JEP184 calibration and data-analysis workflow may start after SP1 definitions are stable.

## Current open questions
1. Exact DUT model/package and Kelvin Source availability.
2. Final stress and measurement voltage ranges.
3. Exact 0 V precondition topology.
4. VDC/RL design values for the selected DUT.
5. Pulse generator, oscilloscope, and differential probe models.
6. Exact Si8273 full orderable part number/package to be used on PCB.

## Next master action
Complete G0/G1 through SP1, SP2, and SP3 definition work, then begin G2 component selection and calculations before authorizing KiCad schematic implementation.
