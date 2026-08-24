# PCB Design Stage-Gate Plan

This file is the master stage-gate tracker for the SiC MOSFET BTI Fig. 3 reproduction PCB project. It must be updated whenever the project makes a meaningful design, verification, or implementation advance.

## Project success criterion
The PCB is not considered successful merely because the schematic is complete, DRC passes, or the Si8273 output edge is fast. The end goal is to reproduce the functional measurement architecture of Fig. 3 in Li et al., IEEE TPEL 2024, such that the DUT can move through precondition → stress → measurement states and an interpretable VDS measurement point can be obtained about 100 ns after stress removal.

## AI / human responsibility model

### Human owner
The human designer retains final responsibility for:
- final component selection approval;
- physical package and pin-1 confirmation;
- critical component placement;
- critical high-speed routing and Kelvin routing;
- laboratory grounding / floating-supply verification;
- probe connection and measurement safety;
- hardware bring-up;
- final ERC/DRC disposition;
- manufacturing approval and Gerber release.

### ChatGPT
Use ChatGPT mainly for:
- paper and datasheet interpretation;
- requirements and architecture;
- circuit reasoning and calculations;
- schematic review;
- PCB screenshot / layout review;
- failure-mode analysis;
- bring-up and validation planning;
- debugging and experiment-method review.

### Codex
Use Codex mainly for:
- repository and engineering-file maintenance;
- deterministic KiCad file edits after interfaces are approved;
- BOM generation and consistency checks;
- ERC/DRC automation and report generation;
- calculation scripts;
- oscilloscope/B1505 CSV processing;
- version control and change summaries.

Codex must not independently invent component pin numbers, ratings, frozen interfaces, safety behavior, or high-speed topology.

---

# Stage Gates

## G0 — Requirements Definition

### Purpose
Define exactly what the PCB must do before drawing the circuit.

### Learn / understand
- system input and output quantities;
- voltage, current, timing, and measurement requirements;
- positive-BTI and negative-BTI operating modes;
- meaning of SREF, GNDA, GNDI, and laboratory earth;
- precondition, stress, measurement, and safe-off states.

### Main tools
- ChatGPT
- paper / datasheets
- GitHub documentation

### AI tasks
ChatGPT:
- extract requirements from the paper;
- define states and timing;
- identify assumptions and unknowns;
- convert requirements to REQ-xxx items.

Codex:
- maintain requirements documents only after content is approved.

### Required outputs
- `docs/requirements.md`
- state table
- timing definitions
- initial verification matrix
- open-question list

### PASS criteria
- every required board function has a REQ identifier;
- positive and negative BTI operation is unambiguous;
- 0 V precondition is represented;
- SREF definition is frozen;
- the ~100 ns system-level measurement target is defined;
- unresolved items are explicitly listed rather than guessed.

### Current status
ACTIVE

---

## G1 — System Architecture

### Purpose
Split the complete experiment into functional blocks and define interfaces before selecting detailed circuits.

### Learn / understand
For each block, identify:
- signal path;
- power path;
- return path;
- voltage reference;
- control input;
- measurement output.

### Expected architecture blocks
- pulse-generator / logic input;
- Si8273 isolated gate-driver section;
- stress-to-measurement switching;
- 0 V precondition function;
- DUT gate / Kelvin-source interface;
- VDC + RL drain-load loop;
- VGS/VDS measurement interfaces;
- B1505 calibration interface / workflow.

### Main tools
- ChatGPT
- GitHub documentation

### AI tasks
ChatGPT:
- create and review block diagrams;
- define electrical interfaces;
- identify isolation and grounding risks.

Codex:
- maintain interface tables and architecture documents.

### Required outputs
- approved block diagram;
- `docs/interfaces.md` updated;
- state-to-hardware mapping;
- module ownership and boundaries.

### PASS criteria
- every connector and major net has a defined purpose;
- current return paths are understandable;
- GNDI, GNDA, SREF, and earth are not ambiguously merged;
- the boundary between PCB functions and external instruments is clear;
- SP2 and SP3 can proceed without inventing system-level interfaces.

### Current status
ACTIVE

---

## G2 — Component Selection and Circuit Calculations

### Purpose
Prove that the proposed hardware is electrically plausible before schematic capture is frozen.

### Learn / understand
- datasheet reading;
- voltage/current ratings;
- Qg and gate-current requirements;
- Rg effects;
- decoupling requirements;
- RL, IDS, resistor pulse power, and DUT self-heating;
- timing and bandwidth margins;
- power-up, power-down, EN, and UVLO behavior.

### Main tools
- ChatGPT
- LTspice
- Python / calculation scripts
- manufacturer datasheets

### AI tasks
ChatGPT:
- datasheet review;
- component comparison;
- circuit calculations;
- failure-mode analysis;
- LTspice model simplification guidance.

Codex:
- parameter-sweep scripts;
- BOM drafts;
- calculation automation;
- datasheet-reference consistency checks.

### Human tasks
- approve exact orderable part numbers;
- verify physical parts and available laboratory supplies/instruments;
- confirm no critical value is based on an AI guess.

### Required outputs
- approved Si8273 part/package;
- gate-drive current calculation;
- initial Rg range;
- decoupling specification;
- 0 V precondition topology decision;
- VDC/RL calculation method;
- component-rating table;
- LTspice results for relevant simplified circuits where useful.

### PASS criteria
- all critical components have cited datasheet support;
- voltage/current/power margins are checked;
- the target transition is quantitatively plausible;
- negative-BTI fail-state risk is addressed;
- no critical OPEN item prevents schematic implementation.

### Current status
NOT STARTED / waiting for G0-G1 definitions to stabilize

---

## G3 — Schematic Capture

### Purpose
Create the complete electrical connectivity in KiCad.

### Learn / understand
- symbols versus physical components;
- pins and nets;
- power symbols and references;
- decoupling;
- connectors;
- no-connect and unused-pin handling;
- ERC.

### Main tools
- KiCad Schematic Editor
- ChatGPT
- Codex

### AI tasks
ChatGPT:
- module-by-module schematic design and review;
- pin-by-pin review from datasheets;
- screenshot review;
- identify grounding, isolation, and default-state errors.

Codex:
- deterministic KiCad edits from an approved connection specification;
- BOM/net consistency checks;
- ERC execution and report generation.

### Human tasks
- open and inspect the schematic visually;
- verify every critical pin against the datasheet;
- approve all ERC warning dispositions.

### Required outputs
- KiCad schematic;
- BOM draft;
- ERC report;
- schematic review checklist.

### PASS criteria
- no unresolved serious ERC errors;
- every critical IC pin manually checked;
- no floating control inputs;
- GNDI/GNDA/SREF/earth relationships are correct;
- positive and negative BTI modes follow the frozen interface table;
- 0 V precondition does not conflict with the Si8273 output.

### Current status
BLOCKED until G0-G2 pass

---

## G4 — Footprint and Physical-Part Verification

### Purpose
Map every schematic component to the correct physical package and pad numbering.

### Learn / understand
- symbol pin number versus footprint pad number;
- package variants;
- pin 1 orientation;
- mechanical drawings;
- connector orientation;
- polarity markings.

### Main tools
- KiCad
- manufacturer datasheets
- ChatGPT
- Codex

### AI tasks
ChatGPT:
- mechanical drawing review;
- package-variant comparison.

Codex:
- detect missing footprints;
- generate footprint audit lists.

### Human tasks
- final physical-package confirmation;
- pin-1 and connector-orientation confirmation.

### Required outputs
- footprint assignment table;
- footprint audit;
- package-orientation checklist.

### PASS criteria
- 100% of PCB-mounted components have verified footprints;
- symbol-pin to footprint-pad mapping is correct;
- no package selection is based on name similarity alone;
- connector polarity/orientation is explicitly reviewed.

### Current status
BLOCKED until G3 pass

---

## G5 — PCB Constraints and Board Setup

### Purpose
Define layout rules before placement and routing.

### Learn / understand
- board stackup;
- copper layers;
- trace width;
- clearance;
- vias;
- net classes;
- isolation boundary;
- current return paths.

### Suggested net classes / functional groups
- LOGIC
- GATE_FAST
- FLOATING_POWER
- DRAIN_POWER
- SENSE

### Main tools
- KiCad PCB Editor
- KiCad Calculator / Python where useful
- ChatGPT
- Codex

### AI tasks
ChatGPT:
- recommend rule principles based on actual current, voltage, and switching requirements.

Codex:
- implement approved net classes and design rules;
- check rule consistency.

### PASS criteria
- board stackup is defined;
- all important net classes are assigned;
- clearance and width rules are justified;
- isolation region is defined;
- placement begins only after rules exist.

### Current status
BLOCKED

---

## G6 — Critical Placement

### Purpose
Place components to minimize parasitic inductance and create correct physical current-return paths.

### Priority placement group
First place only the critical gate-drive island:
- Si8273;
- VDDA-GNDA 100 nF decoupling;
- other local decoupling;
- Rg;
- DUT Gate connector;
- DUT Kelvin Source connector.

Then add slower/control/power components.

### Learn / understand
- loop area;
- parasitic inductance;
- decoupling-loop geometry;
- Kelvin routing;
- probe access;
- connector practicality.

### Main tools
- KiCad PCB Editor
- ChatGPT screenshot review

### AI tasks
ChatGPT:
- review placement screenshots for loop geometry, return path, isolation, and probe access.

Codex:
- only deterministic placement changes when explicitly specified;
- not responsible for independent high-speed placement decisions.

### Human tasks
- perform/approve critical placement.

### PASS criteria
- VOA → Rg → Gate → Kelvin Source → GNDA loop is physically compact;
- high-frequency VDDA-GNDA decoupling is adjacent to driver supply pins;
- Kelvin and power-source paths are physically distinguishable;
- measurement probes can realistically connect;
- isolation and connector placement are practical.

### Current status
BLOCKED

---

## G7 — Routing

### Purpose
Route the board in electrical-priority order rather than convenience order.

### Routing priority
1. VOA → Rg → DUT Gate
2. Kelvin Source → driver return
3. high-frequency driver decoupling loop
4. VGS/VDS sense connections
5. power paths
6. logic paths
7. non-critical routing

### Learn / understand
- return paths;
- copper-plane continuity;
- via inductance;
- Kelvin sensing;
- high-current versus measurement paths.

### Main tools
- KiCad PCB Editor
- ChatGPT screenshot review
- Codex for rule checks / deterministic edits

### Human tasks
The human designer must perform or explicitly approve critical high-speed and Kelvin routing.

### PASS criteria
- critical loops are reviewed before non-critical routing is allowed to constrain them;
- no drain/power current shares the intended Kelvin sense path;
- no obvious discontinuous return path exists;
- routing respects all approved rules.

### Current status
BLOCKED

---

## G8 — ERC / DRC / Engineering Design Review

### Purpose
Combine machine-rule checking with engineering review.

### Important distinction
ERC/DRC passing only proves that defined CAD rules are satisfied. It does not prove that the gate loop is short, Kelvin routing is correct, decoupling is effective, or SREF is safely referenced.

### Main tools
- KiCad ERC/DRC
- ChatGPT
- Codex

### AI tasks
Codex:
- run ERC/DRC;
- collect warnings;
- generate reports;
- check BOM/footprint/net consistency.

ChatGPT:
- engineering review of schematic and PCB screenshots;
- review unresolved warnings and risk items.

### Human tasks
- final disposition of every warning;
- final visual inspection.

### PASS criteria
- zero unresolved serious ERC errors;
- zero unresolved serious DRC errors;
- every warning has a documented disposition;
- schematic, placement, routing, measurement access, isolation, and safety reviews pass.

### Current status
BLOCKED

---

## G9 — Manufacturing Release

### Purpose
Generate fabrication/assembly outputs only after design review passes.

### Main tools
- KiCad
- Codex for deterministic export/check automation

### Required outputs
- Gerbers;
- drill files;
- BOM;
- position files if assembly is required;
- fabrication notes;
- release checklist.

### Human-only approval
Manufacturing release requires explicit human approval.

### PASS criteria
- G8 passed;
- manufacturing checklist passed;
- polarity/orientation and board dimensions checked;
- final generated files independently inspected.

### Current status
BLOCKED

---

## G10 — Hardware Bring-Up

### Purpose
Power the prototype in controlled stages without risking the DUT unnecessarily.

### Bring-up order
1. visual / microscope inspection;
2. unpowered resistance and short checks;
3. logic supply only;
4. driver supply without DUT high-voltage operation;
5. dummy gate capacitor tests;
6. positive and negative gate-transition tests;
7. DUT connected with VDC = 0;
8. low VDC + conservative RL;
9. progression toward final test conditions.

### Main tools
- DMM
- current-limited supplies
- oscilloscope / differential probes
- pulse generator
- ChatGPT for test planning and debugging
- Codex for data logging/analysis

### PASS criteria
- every staged test passes before progressing;
- no unexpected rail short or grounding path;
- positive/negative gate transitions are correct;
- no unsafe VGS overshoot;
- fail states and power sequencing behave as designed.

### Current status
BLOCKED

---

## G11 — Fast-Switching and Measurement Validation

### Purpose
Prove the PCB meets the actual Fig. 3 timing objective.

### Measurements
At minimum capture:
- VIA or equivalent control edge;
- VGS referenced to Kelvin Source;
- VDS.

Evaluate:
- transition time;
- overshoot;
- ringing;
- settling;
- stress-end timestamp;
- VDS measurement point timestamp;
- tdly;
- repeatability.

### Main tools
- oscilloscope
- Python
- Codex data-analysis scripts
- ChatGPT waveform review

### PASS criteria
- VGS remains within approved DUT limits;
- measurement voltage is reached reproducibly;
- MP/MN/MI measurement behavior is interpretable;
- stress removal → valid VDS measurement point is approximately 100 ns or otherwise meets the approved timing requirement;
- result is repeatable across repeated acquisitions.

### Current status
BLOCKED

---

## G12 — Fig. 3 Experimental Reproduction

### Purpose
Run the complete method rather than only proving that the PCB switches.

### Required test sequences
Calibration:
- 0 V → VGM-I → measure MI.

Positive stress:
- 0 V → VGS-P → VGM-P → measure MP.

Negative stress:
- 0 V → VGS-N → VGM-N → measure MN.

Combine the fast VDS measurement with the B1505 fixed-VDS IDS-VGS calibration to derive the threshold-voltage shift according to the approved analysis method.

### Main tools
- PCB test platform
- B1505 / EasyEXPERT
- pulse generator
- oscilloscope
- Python
- ChatGPT
- Codex

### PASS criteria
- calibration workflow passes;
- positive and negative stress workflows pass on the same PCB;
- VGM-P and VGM-N can be adjusted as required without hardware modification;
- MI, MP, MN and tdly are extracted reliably;
- ΔVth calculation pipeline is validated;
- test results are reproducible.

### Current status
BLOCKED

---

## G13 — Revision / V2 Decision

### Purpose
Convert prototype observations into controlled design changes.

### Required process
Every hardware problem must be mapped to:
- observed symptom;
- evidence;
- root-cause hypothesis;
- validation test;
- design change;
- regression test.

### AI use
ChatGPT:
- root-cause reasoning and design-review support.

Codex:
- change implementation, versioning, automated regression/reporting.

### PASS criteria
- all V1 critical issues have documented dispositions;
- V2 changes are traceable to measured evidence;
- no unreviewed change is introduced.

### Current status
BLOCKED

---

# Current Master Gate Summary

| Gate | Name | Status |
|---|---|---|
| G0 | Requirements Definition | ACTIVE |
| G1 | System Architecture | ACTIVE |
| G2 | Component Selection & Calculations | NOT STARTED |
| G3 | Schematic Capture | BLOCKED |
| G4 | Footprint Verification | BLOCKED |
| G5 | PCB Constraints | BLOCKED |
| G6 | Placement | BLOCKED |
| G7 | Routing | BLOCKED |
| G8 | ERC/DRC & Engineering Review | BLOCKED |
| G9 | Manufacturing Release | BLOCKED |
| G10 | Hardware Bring-Up | BLOCKED |
| G11 | Fast-Switching Validation | BLOCKED |
| G12 | Fig. 3 Experimental Reproduction | BLOCKED |
| G13 | Revision / V2 | BLOCKED |

## Update rule
Whenever a meaningful project advance occurs, update this file before declaring the corresponding stage complete. For each update:
1. change the relevant gate status;
2. add or update required outputs;
3. record newly discovered blockers;
4. only mark a gate `PASS` when every PASS criterion has explicit evidence;
5. do not unlock a downstream gate whose upstream prerequisite has not passed.

Allowed status values:
- NOT STARTED
- ACTIVE
- BLOCKED
- REVIEW
- PASS
- REWORK

Last updated: 2026-08-24
