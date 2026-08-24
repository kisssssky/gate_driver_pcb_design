# SiC BTI Gate Driver PCB

Purpose: reproduce the measurement architecture of Fig. 3 in Li et al., *Accurate Evaluation of Threshold Voltage Hysteresis in SiC MOSFET Under Switching Stress*, IEEE TPEL 2024.

Core project rules:
- One PCB must support both positive and negative BTI.
- Positive/negative mode is changed only by external VDDA/GNDA voltages and control waveform.
- SREF is the DUT Kelvin Source reference and is not assumed to equal laboratory earth.
- Si8273 VOA performs the fast stress-to-measurement voltage transition.
- Full measurement sequence includes 0 V precondition, stress, and measurement states.
- The system target is not merely a <100 ns driver edge; the goal is an interpretable VDS measurement point about 100 ns after stress removal.
- Do not generate manufacturing files until ERC, DRC, manual review, and the verification matrix pass.

Repository structure:
- `docs/` — requirements, interfaces, decisions, risks, project status, verification matrix.
- `hardware/` — KiCad schematic, PCB, BOM, datasheets.
- `calculations/` — electrical and timing calculations.
- `analysis/` — B1505 / oscilloscope data processing scripts.
- `measurements/` — raw and processed experimental data.
- `references/` — paper notes and reference metadata. Do not commit copyrighted PDFs unless redistribution is permitted.

Current phase: architecture and requirements definition before KiCad schematic capture.
