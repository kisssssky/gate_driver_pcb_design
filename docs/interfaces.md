# Interface Definitions

Status: **PROPOSED G1 INTERFACE BASELINE — READY FOR MASTER REVIEW**

- 版本：`G1-ICD-v1.0`
- 日期：2026-08-25
- 需求基线：65条`REQ-SYS-*`保持`FROZEN`
- 详细架构与接口责任：[`G1_system_architecture_v1.0.md`](G1_system_architecture_v1.0.md)
- 本文件只定义逻辑接口，不是connector pin assignment，也不选择具体电平、器件或拓扑。

## 1. Reference domains

| Domain | 受控定义 |
|---|---|
| `GNDI` | Si8273 logic-side reference；可作为Pulse Generator输入接口参考，但不跨越隔离边界。 |
| `GNDA` | Si8273 channel A output-side lower rail；不是0 V、`SREF`或earth的别名。 |
| `VDDA` | Si8273 channel A output-side upper rail；不是固定正电压或earth的别名。 |
| `SREF` | DUT Kelvin Source reference；是`VGS`驱动和测量参考。 |
| `DRET` | G1提出的`VDC return`/Power Source回路返回域；不是`SREF`或earth。 |
| earth/chassis | 实验室保护地或仪器机壳；任何信号域连接均须显式批准和资格确认。 |

Isolation boundary位于`GNDI`与Si8273 channel A output domain之间。禁止隐式连接：`GNDI↔GNDA/SREF/earth`、`GNDA↔SREF/DRET/earth`、`VDDA↔earth`、`SREF↔DRET/earth`。三端DUT导致KS/Power Source不可物理分开的情况只能作为DUT profile限制记录，不得成为Base PCB默认连接。

## 2. 冻结P/N逻辑关系

Positive BTI：

- `V(VDDA)-V(SREF)=VGS-P`
- `V(GNDA)-V(SREF)=VGM-P`
- stress：`VIA=HIGH`
- measurement：`VIA=LOW`

Negative BTI：

- `V(VDDA)-V(SREF)=VGM-N`
- `V(GNDA)-V(SREF)=VGS-N`
- stress：`VIA=LOW`
- measurement：`VIA=HIGH`

公式不代表`GNDA=SREF`、`GNDA=earth`、`SREF=earth`，也不批准rail generation/return拓扑。

## 3. ICD总表（24个逻辑接口）

| Interface ID | 逻辑名称 | Source → Sink | 方向/类型 | Reference | 正常责任 | `SAFE_OFF`责任 | 可配置项/延期 | 对应REQ |
|---|---|---|---|---|---|---|---|---|
| IF-CTRL-01 | `VIA` | Pulse Generator → Si8273 input | 控制→ | `GNDI` | P/N真值命令 | stress无效/屏蔽 | 电平/边沿：G2 | `REQ-SYS-FUNC-008`; `REQ-SYS-INTERFACE-005` |
| IF-CTRL-02 | `TRIGGER_TIMING_REF` | Pulse Generator → scope/software | 时序→ | source=`GNDI`，接收域待资格确认 | 同次事件时间参考 | 只记录fault | 通道/deskew：G2/G10/G11 | `REQ-SYS-MEAS-001`; `REQ-SYS-INTERFACE-005/009`; `REQ-SYS-VERIFY-001` |
| IF-CTRL-03 | `STATE_COMMAND` | controller → interlock/state functions | 控制→ | 控制域 | 选择Calibration/P/N和状态 | 只允许stop/reset/re-arm | timing：G10/G12 | `REQ-SYS-FUNC-003`; `REQ-SYS-TIME-003...006` |
| IF-PWR-I-01 | `VDDI/GNDI` | logic supply → Si8273 input | 能量/return | `GNDI` | 逻辑供电 | 维持fault记录或受控关断 | 数值：G2 | `REQ-SYS-INTERFACE-003`; `REQ-SYS-SAFE-002` |
| IF-PWR-A-01 | `VDDA/GNDA` | floating rails → Si8273 output | 能量/return | output rail domain | 提供P/N rails | disable或批准safe行为 | 数值：G2 | `REQ-SYS-FUNC-008`; `REQ-SYS-INTERFACE-006` |
| IF-PWR-A-02 | `RAIL_SREF_PROFILE` | SREF/profile ↔ floating rails | reference/return↔ | `SREF`边界 | 定义rail相对SREF并闭合gate电流 | 不得借earth闭合 | 拓扑：G2/Master | `REQ-SYS-INTERFACE-001...003/006`; `REQ-SYS-SAFE-004` |
| IF-DRV-01 | `VOA` | Si8273 A → `Rg`/Gate | gate energy↔ | output domain，相对`SREF` | stress→measurement快切换 | inhibited/non-stress | 动态：G2/G11 | `REQ-SYS-FUNC-007/008`; `REQ-SYS-TIME-001/002` |
| IF-DUT-01 | `DUT_GATE` | driver/PRECONDITION → DUT | gate energy↔ | `SREF` | 承载目标VGS | `VGS_SAFE` | `Rg`/物理：G2/G4/G6/G7 | `REQ-SYS-METHOD-001/002`; `REQ-SYS-DUT-005` |
| IF-DUT-02 | `DUT_KS/SREF` | DUT KS ↔ driver/measurement | reference/return | `SREF` | gate和VGS参考 | 保持受控、不接earth | KS存在性：G2/G4 | `REQ-SYS-INTERFACE-001...004`; `REQ-SYS-MEAS-002` |
| IF-DUT-03 | `DUT_POWER_SOURCE` | DUT → `DRET` | drain current→ | `DRET` | 漏极回流 | 去能量 | package：G4 | `REQ-SYS-FUNC-004`; `REQ-SYS-INTERFACE-004/007` |
| IF-DUT-04 | `DUT_DRAIN` | `RL` → DUT | drain current→ | `DRET` | 接收低能量电流 | de-energized | profile：G2 | `REQ-SYS-FUNC-004`; `REQ-SYS-INTERFACE-007` |
| IF-DRAIN-01 | `VDC` | drain supply → `RL` | 能量→ | `DRET` | 低`VDS`偏置 | disabled | 数值/限流：G2 | `REQ-SYS-METHOD-003...008`; `REQ-SYS-INTERFACE-007`; `REQ-SYS-SAFE-003/004` |
| IF-DRAIN-02 | `RL` | load → DUT Drain | 能量→ | `DRET` | 限流并支持IDS计算 | 回路disabled | 数值/额定：G2 | `REQ-SYS-FUNC-004/005`; `REQ-SYS-MEAS-004` |
| IF-MEAS-01 | `VGS_GATE_SENSE` | DUT Gate → VGS probe | 测量→ | 与SREF成对 | VGS正端 | 不作有效measurement | probe：G2/G6/G10 | `REQ-SYS-MEAS-001...003`; `REQ-SYS-INTERFACE-009` |
| IF-MEAS-02 | `VGS_KS_SENSE` | DUT KS → VGS probe | 测量→ | `SREF` | VGS负端 | 不接earth | KS/adapter：G4/G6 | `REQ-SYS-MEAS-002/003`; `REQ-SYS-INTERFACE-009` |
| IF-MEAS-03 | `VDS_DRAIN_SENSE` | DUT Drain → VDS probe | 测量→ | 与Power Source成对 | VDS正端 | 确认去能量 | 共模/带宽：G2/G10 | `REQ-SYS-MEAS-001/003`; `REQ-SYS-INTERFACE-009` |
| IF-MEAS-04 | `VDS_SOURCE_SENSE` | DUT Power Source → VDS probe | 测量→ | `DRET`局部source | VDS负端 | 确认去能量 | source点：G4/G6 | `REQ-SYS-INTERFACE-004/009`; `REQ-SYS-VERIFY-001` |
| IF-DATA-01 | `B1505_CAL_DATA` | B1505 → software | 数据→ | data domain | curve、Ith、VDS-C、metadata | 保持只读追溯 | 格式/插值：G12 | `REQ-SYS-METHOD-003`; `REQ-SYS-MEAS-006...009`; `REQ-SYS-INTERFACE-008` |
| IF-DATA-02 | `WAVEFORM_DATA` | scope → software | 数据→ | data domain | raw VGS/VDS/timing/metadata | fault波形标invalid | 格式/deskew：G10/G11/G12 | `REQ-SYS-MEAS-001/005/009`; `REQ-SYS-VERIFY-001/004` |
| IF-CFG-01 | `DUT_PROFILE_CONFIG` | controlled record/User → system | 数据/许可→ | configuration domain | 绑定DUT/adapter/`Rg`/参数 | mismatch禁止arm | 具体数据：G2/G4/G12 | `REQ-SYS-FUNC-002`; `REQ-SYS-DUT-001...005`; `REQ-SYS-SAFE-004` |
| IF-SAFE-01 | `PROTECTION_INTERLOCK_STATUS` | detectors/user → SAFE_OFF control | 状态→ | 各source域 | all-valid才arm | 任一invalid强制safe | 阈值：G2 | `REQ-SYS-SAFE-001...003`; `REQ-SYS-INTERFACE-005/010` |
| IF-SAFE-02 | `GATE_POWER_ENABLE_DISABLE` | SAFE_OFF control → rails/driver | 控制→ | 隔离控制域 | 受控gate enable | inhibit/保持必要safe能量 | default：G2/G10 | `REQ-SYS-SAFE-001/002` |
| IF-SAFE-03 | `DRAIN_ENABLE_DISABLE` | SAFE_OFF control/user → VDC | 控制→ | 外部电源域 | precondition valid后供能 | disable优先 | 响应：G2/G10 | `REQ-SYS-SAFE-001...004`; `REQ-SYS-INTERFACE-007` |
| IF-SAFE-04 | `FAULT_LOG_STATUS` | controller/instruments → software/User | 数据→ | data domain | 保存cause/state/profile/time | 锁存并阻止自动re-arm | 格式：G10/G12 | `REQ-SYS-MEAS-009`; `REQ-SYS-SAFE-002/003`; `REQ-SYS-VERIFY-004` |

## 4. 状态接口约束

- `PRECONDITION`：Gate-to-SREF=`0 V`，0 V路径独占；`VIA`不得使`VOA`与其争用。
- `SAFE_OFF`：Gate为符号化`VGS_SAFE`非应力目标、drain disabled；与PRECONDITION不同。
- P/N stress→measurement关系严格按第2章；同一DUT/profile切换P/N不得换Base PCB元件、adapter或`Rg`。
- Calibration的`VIA_CAL`与rail assignment不是P/N表的自然推论，保持受控配置并延期至G2/Master。
- 0 V路径与`VOA`必须break-before-make；实现拓扑和时间值延期至G2。
- 任何跨domain连接、connector pinout或instrument earth关系均不得由本候选基线默示建立。

## 5. OPEN状态

`OI-012...017`均已在`G1_system_architecture_v1.0.md`提出resolution proposal，状态统一为：

**G1 RESOLUTION PROPOSED — READY FOR MASTER REVIEW**

本文件在Master批准前不得标记`FROZEN`。

