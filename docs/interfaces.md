# Interface Definitions

Status: draft; values are logical definitions, not yet connector pin assignments.

## Reference domains
- `GNDI`: Si8273 logic-side reference. May be tied to pulse-generator ground as required by the input interface.
- `GNDA`: Si8273 channel-A output-side lower rail.
- `VDDA`: Si8273 channel-A output-side upper rail.
- `SREF`: DUT Kelvin Source reference. Not automatically tied to earth.

## Gate-drive interface
- `VIA`: channel-A control input.
- `VOA`: channel-A output to gate resistor and DUT Gate.
- `DUT_GATE`: DUT gate terminal after the selected external gate resistance.
- `DUT_KS`: DUT Kelvin Source terminal; electrically defines SREF.

## Operating-mode definitions
### Positive BTI
- `VDDA = VGS-P`
- `GNDA = VGM-P`
- stress: `VIA = HIGH`
- measurement: `VIA = LOW`
- transition at stress end: `HIGH -> LOW`

### Negative BTI
- `VDDA = VGM-N`
- `GNDA = VGS-N`
- stress: `VIA = LOW`
- measurement: `VIA = HIGH`
- transition at stress end: `LOW -> HIGH`

## Precondition interface
A separate mechanism shall support `DUT_GATE = SREF` for the 0 V precondition state. Exact topology is OPEN-REQ-004 and must prevent simultaneous low-impedance drive by the precondition path and Si8273 output.

## Drain-loop interface
Logical path:
`VDC -> RL -> DUT_DRAIN -> DUT_POWER_SOURCE -> VDC return`

Measurement nodes:
- `VDS_DRAIN_SENSE`
- `VDS_SOURCE_SENSE`
- `VGS_GATE_SENSE`
- `VGS_KS_SENSE`
- optional `TRIGGER_OUT`

## Forbidden implicit connections
Do not create any implicit connection between:
- GNDI and GNDA
- GNDI and SREF
- GNDI and earth/chassis
- GNDA and earth/chassis
- SREF and earth/chassis
unless explicitly approved in the master decision log.
