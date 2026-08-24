# Verification Matrix

Status: draft; acceptance limits must be refined by SP1/SP2/SP3.

The complete SP1-v0.1 requirement/verification matrix is maintained in [`SP1_paper_method_system_requirements_v0.1.md`](SP1_paper_method_system_requirements_v0.1.md). This file retains the cross-project implementation checks.

| Test ID | Requirement | Verification method | Acceptance criterion | Phase |
|---|---|---|---|---|
| TEST-001 | REQ-001/002 | Review schematic and mode table | Same assembled PCB supports both polarities using external supply/control changes only | Design review |
| TEST-002 | REQ-003/004 | Continuity/isolation test | SREF connects to DUT Kelvin Source and has no unintended earth/GNDI connection | Bring-up |
| TEST-003 | REQ-006 | Oscilloscope VGS test | Positive mode produces stress-to-measure transition with specified rail values | Dummy load/DUT |
| TEST-004 | REQ-007 | Oscilloscope VGS test | Negative mode produces stress-to-measure transition with specified rail values | Dummy load/DUT |
| TEST-005 | REQ-008 | State-sequence capture | 0 V precondition, stress, and measurement states are all achieved without driver contention | Dummy load/DUT |
| TEST-006 | REQ-010 | Simultaneous VGS/VDS timing capture | Interpretable VDS measurement point is obtained at approximately 100 ns target delay after stress removal | System validation |
| TEST-007 | REQ-011 | Differential VGS measurement | VGS is measured Gate-to-Kelvin-Source with acceptable ringing/settling | System validation |
| TEST-008 | REQ-012 | Drain-loop functional test | VDS and IDS behavior agrees with resistive-load equations within defined tolerance | Low-voltage/system |
| TEST-009 | REQ-013 | Layout/continuity review | Power Source and Kelvin Source paths are separated as designed | PCB review/bring-up |
| TEST-010 | REQ-100 | Datasheet audit | All pin numbers, ratings, packages, and critical component values have cited sources | Schematic freeze |
| TEST-011 | REQ-102 | ERC | Pass or all remaining warnings individually approved | Schematic freeze |
| TEST-012 | REQ-103 | DRC | Pass or all remaining warnings individually approved | PCB freeze |
| TEST-013 | REQ-104 | Manufacturing hold review | Gerbers released only after ERC, DRC, manual review, and matrix approval | Release |
| TEST-014 | REQ-105/106 | GitHub file and output-index audit | Every chat deliverable exists at its canonical repository path and is registered before task completion | Every deliverable |
| TEST-015 | REQ-107/108 | Repository-content and blocked-state audit | No prohibited content is committed; blocked outputs are explicitly reported and recorded | Every deliverable |
