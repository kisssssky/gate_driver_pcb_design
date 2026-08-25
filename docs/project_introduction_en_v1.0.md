# Fast Gate-Drive and Threshold-Hysteresis Measurement Platform for SiC MOSFET BTI

## Project Introduction (English Version)

- Version: `PROJECT-INTRO-EN-v1.0`
- Date: 25 August 2026
- Intended use: group meetings, PhD progress reviews, project reviews, and technical presentations
- GitHub: `kisssssky/gate_driver_pcb_design`

## 1. Project Overview

This project aims to reproduce the functional behaviour of the test architecture shown in Fig. 3 of Li et al., “Accurate Evaluation of Threshold Voltage Hysteresis in SiC MOSFET Under Switching Stress,” IEEE TPEL, 2024. The objective is to develop a fast gate-drive and measurement platform for investigating bias temperature instability (BTI) and threshold-voltage hysteresis in SiC MOSFETs.

A SiC MOSFET can recover rapidly after gate stress is removed. If the transition from stress to measurement is too slow, the earliest threshold-voltage shift will be missed. The project therefore does not treat a fast driver-output edge as the sole success criterion. The system-level objective is:

> The DUT shall complete `0 V preconditioning → gate stress → fast measurement` and provide an interpretable and repeatable `VDS` measurement point approximately 100 ns after the end of stress.

High-speed `VGS(t)`, `VDS(t)`, and timing data will be combined with fixed-`VDS-C` calibration curves measured using a Keysight B1505A. Threshold-voltage shift will then be extracted through the traceable chain `VDS → IDS → Vth → ΔVth`.

## 2. Research Problem

Conventional BTI measurements face several challenges:

- Delay between stress removal and measurement can conceal fast recovery.
- Positive and negative BTI require different gate-stress and measurement voltages.
- Gate drive, drain bias, probe bandwidth, return paths, and parasitics all influence the approximately 100 ns result.
- SiC MOSFETs with different voltage classes and packages have different `Qg`, input capacitance, allowable `VGS`, and common-source parasitics.
- Observing only the driver output does not prove that a valid and interpretable measurement state has been established at the DUT.

The project addresses these issues through controlled system architecture, interface definitions, DUT profiles, simultaneous waveform acquisition, and stage-gated verification.

## 3. Project Objectives

1. Support Positive BTI and Negative BTI using the same Base PCB, without replacing PCB components when polarity changes.
2. Change stress and measurement polarity through external `VDDA/GNDA` settings and the control waveform.
3. Use Si8273 channel A / `VOA` for the fast stress-to-measurement transition.
4. Support complete Calibration, Positive BTI, and Negative BTI sequences.
5. Record `VGS(t)`, `VDS(t)`, and a common timing reference during the same event.
6. Support low-`VDS` BTI testing of three-terminal 650 V-class and 3.3 kV-class SiC MOSFETs.
7. Establish a traceable data chain from raw waveforms to `MI/MP/MN`, `IDS`, `Vth`, and `ΔVth`.
8. Release manufacturing files only after requirements, calculations, simulation, ERC/DRC, manual review, and experimental verification are complete.

## 4. Experimental Sequences

| Sequence | State flow | Purpose |
|---|---|---|
| Calibration | `PRECONDITION → MEASUREMENT_I` | Obtain the initial measurement point MI and `Vth-IS` |
| Positive BTI | `PRECONDITION → POSITIVE_STRESS → MEASUREMENT_P` | Obtain MP and recovery data after positive gate stress |
| Negative BTI | `PRECONDITION → NEGATIVE_STRESS → MEASUREMENT_N` | Obtain MN and recovery data after negative gate stress |

`PRECONDITION` establishes the initial Gate-to-`SREF` voltage of 0 V. `SAFE_OFF` is a separate safety state that prevents unintended stress, removes drain energy, and latches faults. These states must not be treated as equivalent.

## 5. System Architecture

| Subsystem | Main responsibility |
|---|---|
| Pulse Generator / controller | Generate state commands, `VIA`, and the common timing reference |
| Si8273 isolated gate driver | Isolate the logic domain and perform the P/N stress-to-measurement transition |
| Gate-target coordination and safety interlock | Manage 0 V preconditioning, `VGM-I`, path arbitration, and `SAFE_OFF` |
| Floating gate rails | Provide `VDDA/GNDA` defined relative to `SREF` |
| Three-terminal DUT adapter | Map Gate, Drain, Source, and the DUT-specific profile |
| `VDC + RL` drain loop | Provide low-`VDS` measurement bias while limiting current and energy |
| Oscilloscope and probes | Acquire `VGS`, `VDS`, and timing synchronously |
| B1505A | Generate fixed-`VDS-C` `IDS-VGS` calibration curves |
| Post-processing software | Calculate `IDS`, `Vth`, and `ΔVth` and preserve metadata |

## 6. Three-Terminal DUT and Source Reference

The current 650 V-class and 3.3 kV-class target DUTs have only Gate, Drain, and Source terminals. They do not provide a separate fourth Kelvin-source terminal.

A `SOURCE_STAR` is therefore defined at the DUT Source lead or pad:

- `SREF`: a Kelvin-style path from `SOURCE_STAR` for gate-current return and the negative reference of the `VGS` measurement;
- `DRET`: the drain-power return path from the same `SOURCE_STAR`.

The two paths intentionally meet at `SOURCE_STAR` and shall not be reconnected upstream. Common Source resistance and inductance inside a three-terminal package cannot be eliminated by PCB routing, so these limitations must be recorded in the DUT profile and evaluated during high-speed waveform verification.

## 7. Compatibility Boundary for 650 V and 3.3 kV DUTs

Compatibility means that both DUT classes use the same logical architecture, state machine, measurement chain, and Base PCB concept. It does not mean that the PCB applies 650 V or 3.3 kV to the DUT.

This is a low-`VDS` BTI and threshold-hysteresis platform, not a breakdown-test system. DUT-specific profiles and adapters manage differences in:

- package and pin mapping;
- `VGS-P/N` and `VGM-I/P/N`;
- `Qg/Ciss/Crss` and gate-driver loading;
- `Rg`;
- `VDS-C`, `VDC`, and `RL`;
- common-source parasitics;
- probe common-mode range, bandwidth, and physical access.

## 8. Current Status

As of 25 August 2026:

| Stage | Status |
|---|---|
| SP1 Paper method and system requirements | `MASTER APPROVED / COMPLETE` |
| G0 Canonical requirements | `PASS` |
| Canonical requirement baseline | `FROZEN`, 65 `REQ-SYS-*` requirements |
| G1 System architecture | `ACTIVE — READY FOR MASTER REVIEW`, three-terminal revision candidate v1.1 |
| G2 Component selection and calculations | `NOT STARTED`; datasheet preparation and calculations may begin |
| G3 KiCad schematic | `BLOCKED` |

The current G1 candidate contains 13 modules, seven logical states, 25 interfaces, eight architecture/path diagrams, and 14 FMEA items. This status does not mean that G1 has passed or that the interfaces are frozen.

## 9. Next Steps

1. Complete the G1 Master review and freeze the system interfaces.
2. In G2, confirm the exact Si8273 part, target DUTs, gate voltages, `Qg`, `Rg`, decoupling, `VDC/RL`, and protection requirements.
3. Use LTspice to evaluate gate drive, preconditioning, fast transitions, parasitics, and fault states.
4. Complete the KiCad schematic, footprints, PCB rules, placement, routing, and ERC/DRC reviews in G3–G8.
5. Complete bring-up, fault tests, approximately 100 ns transition verification, and measurement-chain qualification in G10–G11.
6. Execute the full Fig. 3 experiment and produce `MI/MP/MN → IDS → Vth → ΔVth` results in G12.

## 10. Expected Outcomes

- A fast gate-drive Base PCB supporting Positive and Negative BTI;
- interchangeable adapters and controlled profiles for three-terminal 650 V-class and 3.3 kV-class SiC MOSFETs;
- verified approximately 100 ns stress-to-measurement capability;
- an integrated workflow for B1505 calibration and high-speed oscilloscope data;
- traceable requirements, design decisions, verification evidence, risks, and experimental records;
- an experimental platform supporting SiC MOSFET BTI, threshold-hysteresis research, and TCAD model calibration.

## 11. Short Presentation Introduction

This project is developing a fast gate-drive and measurement platform for investigating BTI and threshold-voltage hysteresis in SiC MOSFETs, with the goal of reproducing the functional behaviour of Fig. 3 in Li et al., 2024. Conventional measurements can miss rapid recovery immediately after gate stress is removed. The proposed platform therefore uses a Si8273 driver to switch quickly from stress voltage to measurement voltage and targets an interpretable DUT-side `VDS` measurement point approximately 100 ns after stress. The same Base PCB will support both positive and negative BTI, while B1505 calibration curves and synchronised `VGS/VDS` waveforms will be combined to extract `IDS`, `Vth`, and `ΔVth`. The canonical requirement baseline is frozen and G0 has passed; the revised three-terminal DUT architecture is currently awaiting G1 Master review.
