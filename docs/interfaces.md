# Interface Definitions

Status: **draft / G1待完善**；本文件只定义逻辑职责，不是connector pin assignment，也不选择具体电平或拓扑。

G0一致性依据：`REQ-SYS-INTERFACE-001...010`。需求基线状态为`FROZEN`；接口实现仍由G1及对应OPEN项继续定义。

## Reference domains
对应需求：`REQ-SYS-INTERFACE-001`、`REQ-SYS-INTERFACE-002`、`REQ-SYS-INTERFACE-003`。

- `GNDI`: Si8273 logic-side reference. May be tied to pulse-generator ground as required by the input interface.
- `GNDA`: Si8273 channel-A output-side lower rail.
- `VDDA`: Si8273 channel-A output-side upper rail.
- `SREF`: DUT Kelvin Source reference. Not automatically tied to earth.

## Gate-drive interface
对应需求：`REQ-SYS-INTERFACE-004`、`REQ-SYS-INTERFACE-005`、`REQ-SYS-INTERFACE-006`。

- `VIA`: channel-A control input.
- `VOA`: channel-A output to gate resistor and DUT Gate.
- `DUT_GATE`: DUT gate terminal after the selected external gate resistance.
- `DUT_KS`: DUT Kelvin Source terminal; electrically defines SREF.

## Operating-mode definitions
下列内容是已冻结的逻辑真值关系，不规定电压数值、连接器或电路实现。

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
对应需求：`REQ-SYS-INTERFACE-010`和`REQ-SYS-METHOD-001`。

- 系统必须实现Gate-to-SREF的0 V预处理功能，即预处理阶段`VGS=0 V`。
- 0 V预处理路径必须与Si8273输出互斥，避免同时低阻驱动或电源争用。
- 本文件不规定独立mechanism、clamp、switch或其他具体拓扑；职责分配由`OPEN::OI-014`在G1关闭，具体实现随后按批准流程决定。

## Drain-loop interface
对应需求：`REQ-SYS-INTERFACE-007`。

Logical path:
`VDC -> RL -> DUT_DRAIN -> DUT_POWER_SOURCE -> VDC return`

Measurement nodes:
- `VDS_DRAIN_SENSE`
- `VDS_SOURCE_SENSE`
- `VGS_GATE_SENSE`
- `VGS_KS_SENSE`
- optional `TRIGGER_OUT`

对应测量需求：`REQ-SYS-INTERFACE-009`。具体探头、仪器型号、带宽和物理连接由`OPEN::OI-018`及后续阶段决定。

## Calibration-data interface

对应需求：`REQ-SYS-INTERFACE-008`。

- B1505负责提供固定`VDS-C`校准曲线、`Ith`及DUT/温度/扫描元数据。
- 高速PCB负责形成快速测试状态并提供波形测量接口，不负责生成B1505校准曲线。
- 数据格式、插值和软件数值容差由`OPEN::OI-021`在G12前关闭。

## Forbidden implicit connections
对应需求：`REQ-SYS-INTERFACE-003`。

Do not create any implicit connection between:
- GNDI and GNDA
- GNDI and SREF
- GNDI and earth/chassis
- GNDA and earth/chassis
- SREF and earth/chassis
unless explicitly approved in the master decision log.
