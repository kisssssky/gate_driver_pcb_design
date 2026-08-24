# Risk Register

Status: initial draft

| ID | Risk | Consequence | Current mitigation | Status |
|---|---|---|---|---|
| RISK-001 | SREF accidentally tied to laboratory earth | unintended short/current path; invalid VGS reference | keep SREF distinct from GNDI/GNDA/earth in schematic and labels | Open |
| RISK-002 | External supplies are not truly isolated/floating | supply shorting or incorrect rail voltages | verify supply isolation before connection; document required topology | Open |
| RISK-003 | Negative-BTI default/UVLO state drives gate to negative stress rail | unintended prolonged negative gate stress | analyze Si8273 fault states and design safe sequencing/disconnect | Open |
| RISK-004 | 0 V precondition path fights Si8273 output | destructive shoot-through between rails | require break-before-make and mutually exclusive control | Open |
| RISK-005 | Gate-loop parasitic inductance causes overshoot/ringing | VGS overstress and inaccurate timing | short VOA-Rg-Gate-Kelvin loop; adjustable Rg; scope validation | Open |
| RISK-006 | VDS measurement chain too slow | apparent tdly meets target while actual device response is unresolved | define probe/scope bandwidth and system-level timing acceptance | Open |
| RISK-007 | Power Source and Kelvin Source share excessive impedance | source bounce corrupts VGS/VDS interpretation | separate return paths at DUT where package permits | Open |
| RISK-008 | RL/VDC combination produces excess self-heating | Vth shifts due to temperature instead of intended hysteresis | calculate current, pulse energy, and thermal limits before DUT tests | Open |
| RISK-009 | Codex or automation invents pinout/rating/topology details | latent schematic or PCB error | AGENTS.md hard constraints; datasheet citations; manual review | Mitigated, monitor |
| RISK-010 | Manufacturing files produced before design review | fabricated board contains unresolved errors | explicit manufacturing hold in AGENTS.md and requirements | Mitigated, monitor |
| RISK-011 | Mandatory output synchronization causes copyrighted, secret, sensitive, or oversized files to be committed blindly | legal/privacy/security exposure or unusable repository history | `docs/output_sync_policy.md` exclusions; index blocked items; approve Git LFS/external storage before use | Mitigated, monitor |
