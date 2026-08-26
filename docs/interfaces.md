# 系统接口控制文件

- 状态：**FROZEN — MASTER APPROVED G1 INTERFACE BASELINE**
- G1阶段门：`PASS`
- 版本：`G1-ICD-v1.1`
- 日期：2026-08-26
- 上游需求：65条`REQ-SYS-*`规范需求，状态`FROZEN`

本文件是Master批准并冻结的G1逻辑接口基线，不是connector pinout、原理图或PCB netlist。批准记录：`docs/G1_master_review_v1.0.md`、`DEC-019`。后续修改必须经过Master变更批准。

## 1. 三引脚DUT与Source接口规则

当前650 V-class和3.3 kV-class DUT均只有Gate、Drain、Source三个物理引脚。

| 名称 | 定义 |
|---|---|
| `DUT_SOURCE` | 三引脚DUT唯一Source物理引脚。 |
| `SOURCE_STAR` | `DUT_SOURCE`引脚或焊盘处，`SREF`和`DRET`的有意单点汇合位置。 |
| `SREF` | 从`SOURCE_STAR`引出的Gate回流和`VGS`测量Kelvin式参考路径；不是第四个引脚。 |
| `DRET` | 从同一`SOURCE_STAR`引出的漏极功率返回路径；不是独立电气域。 |

`SREF`与`DRET`在Source端导通，但除`SOURCE_STAR`外不得在上游再次连接。三引脚封装内部公共Source电阻/电感无法由PCB完全消除，必须写入DUT profile并在G11验证。未来四引脚器件必须重新进行接口和adapter审核。

## 2. 参考域与rail关系

| 名称 | 定义 |
|---|---|
| `GNDI` | Si8273逻辑输入侧参考。 |
| `GNDA` | Si8273 channel A输出侧低rail；不是0 V、`SREF`或earth的别名。 |
| `VDDA` | Si8273 channel A输出侧高rail；不是固定正电压或earth。 |
| `SREF` | 三引脚Source端Kelvin式Gate驱动和`VGS`测量参考。 |
| earth/chassis | 实验室保护地或仪器机壳参考；不得默认连接任一信号reference。 |

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

公式不表示`GNDA=SREF`、`GNDA=earth`或`SREF=earth`，也不批准rail生成或回流拓扑。禁止隐式连接`GNDI↔GNDA/SREF/earth`、`GNDA/VDDA↔earth`、`SREF↔earth`；`SREF`和`DRET`只允许在`SOURCE_STAR`汇合。

## 3. 接口总表（25个逻辑接口）

| 接口ID | 名称 | Source | Sink | 类型/方向 | 参考 | 正常含义 | `SAFE_OFF`含义 | 后续Gate | 需求追溯 |
|---|---|---|---|---|---|---|---|---|---|
| IF-CTRL-01 | `VIA` | Pulse Generator | Si8273输入 | 控制→ | `GNDI` | 执行P/N真值 | 不得产生stress | G2/G10/G11 | `REQ-SYS-FUNC-007`、`REQ-SYS-FUNC-008`、`REQ-SYS-INTERFACE-005` |
| IF-CTRL-02 | `TRIGGER_TIMING_REF` | Pulse Generator | 示波器/软件 | 时序→ | 接收端资格确认 | 共同时间关系 | 仅记录fault/stop | G2/G10/G11 | `REQ-SYS-TIME-002`、`REQ-SYS-MEAS-001`、`REQ-SYS-VERIFY-001` |
| IF-CTRL-03 | `STATE_COMMAND` | Sequence controller | 协调/安全模块 | 控制→ | `GNDI`/隔离状态域 | 选择Calibration/P/N和状态 | 仅stop/reset/re-arm | G10/G12 | `REQ-SYS-FUNC-003`、`REQ-SYS-TIME-003`、`REQ-SYS-TIME-004`、`REQ-SYS-TIME-005`、`REQ-SYS-TIME-006` |
| IF-PWR-I-01 | `VDDI_GNDI` | 逻辑电源 | Si8273输入侧 | 能量↔ | `GNDI` | 逻辑供电 | 未ready不得arm | G2/G3/G10 | `REQ-SYS-INTERFACE-003`、`REQ-SYS-SAFE-002` |
| IF-PWR-A-01 | `VDDA_GNDA` | 浮动rail | Si8273输出侧 | 能量↔ | 输出rail域 | 提供profile rail | disabled/非应力 | G2/G3/G10 | `REQ-SYS-FUNC-002`、`REQ-SYS-INTERFACE-006`、`REQ-SYS-SAFE-004` |
| IF-PWR-A-02 | `RAIL_SREF_PROFILE` | profile/`SREF`接口 | 浮动rail | 目标/参考↔ | `SREF`边界 | 定义rail相对`SREF`目标 | 不借earth闭合 | G2/G3/G10 | `REQ-SYS-INTERFACE-001`、`REQ-SYS-INTERFACE-002`、`REQ-SYS-INTERFACE-003`、`REQ-SYS-INTERFACE-006` |
| IF-DRV-01 | `VOA` | Si8273 channel A | `Rg`/DUT Gate接口 | Gate能量↔ | 相对`SREF` | P/N快速切换 | inhibited | G2/G3/G11 | `REQ-SYS-FUNC-006`、`REQ-SYS-FUNC-007`、`REQ-SYS-TIME-001`、`REQ-SYS-TIME-002` |
| IF-GATE-01 | `CAL_GATE_TARGET` | Gate目标协调模块 | `DUT_GATE` | 逻辑目标→ | `SREF` | `MEASUREMENT_I`保证`VGS=VGM-I` | invalid并移交安全目标 | G2/G3/G10/G11 | `REQ-SYS-FUNC-003`、`REQ-SYS-METHOD-001`、`REQ-SYS-METHOD-002`、`REQ-SYS-INTERFACE-006`、`REQ-SYS-INTERFACE-010`、`REQ-SYS-SAFE-001` |
| IF-DUT-01 | `DUT_GATE` | 获权Gate功能 | DUT Gate | Gate能量↔ | `SREF` | 当前Gate目标 | 安全目标 | G2/G4/G6/G7 | `REQ-SYS-METHOD-001`、`REQ-SYS-METHOD-002`、`REQ-SYS-DUT-005` |
| IF-DUT-02 | `DUT_SOURCE_SREF` | `DUT_SOURCE/SOURCE_STAR` | driver与`VGS`测量 | 参考/低电流回流↔ | `SREF` | Source端Kelvin式路径 | 受控且不接earth | G4/G6/G7/G11 | `REQ-SYS-INTERFACE-001`、`REQ-SYS-INTERFACE-002`、`REQ-SYS-INTERFACE-004`、`REQ-SYS-MEAS-002` |
| IF-DUT-03 | `DUT_SOURCE_POWER_RETURN` | `DUT_SOURCE/SOURCE_STAR` | `DRET/VDC return` | 功率电流→ | `DRET`路径 | 漏极功率回流 | drain去能量 | G2/G4/G6/G7/G11 | `REQ-SYS-FUNC-004`、`REQ-SYS-INTERFACE-004`、`REQ-SYS-INTERFACE-007` |
| IF-DUT-04 | `DUT_DRAIN` | `RL` | DUT Drain | 功率电流→ | 漏极回路 | 接收低能量电流 | de-energized | G2/G4 | `REQ-SYS-FUNC-004`、`REQ-SYS-INTERFACE-007` |
| IF-DRAIN-01 | `VDC` | 漏极电源 | `RL` | 能量→ | `DRET`回流 | 低`VDS`偏置 | disabled | G2/G10 | `REQ-SYS-METHOD-003`、`REQ-SYS-METHOD-004`、`REQ-SYS-METHOD-005`、`REQ-SYS-INTERFACE-007`、`REQ-SYS-SAFE-003`、`REQ-SYS-SAFE-004` |
| IF-DRAIN-02 | `RL` | 负载模块 | DUT Drain | 能量→ | `DRET`回流 | 限流并支持`IDS`计算 | 回路disabled | G2/G6/G7 | `REQ-SYS-FUNC-004`、`REQ-SYS-FUNC-005`、`REQ-SYS-MEAS-004` |
| IF-MEAS-01 | `VGS_GATE_SENSE` | DUT Gate | `VGS`探头 | 测量→ | 与Source sense成对 | `VGS`正端 | 数据无效 | G2/G6/G7/G10 | `REQ-SYS-MEAS-001`、`REQ-SYS-MEAS-002`、`REQ-SYS-MEAS-003`、`REQ-SYS-INTERFACE-009` |
| IF-MEAS-02 | `VGS_SOURCE_SENSE` | `SOURCE_STAR`局部sense | `VGS`探头 | 测量→ | `SREF` | `VGS`负端 | 不接earth，数据无效 | G2/G6/G7/G10/G11 | `REQ-SYS-MEAS-001`、`REQ-SYS-MEAS-002`、`REQ-SYS-MEAS-003`、`REQ-SYS-INTERFACE-009` |
| IF-MEAS-03 | `VDS_DRAIN_SENSE` | DUT Drain局部sense | `VDS`探头 | 测量→ | 与Source sense成对 | `VDS`正端 | 仅确认去能量 | G2/G6/G7/G10 | `REQ-SYS-MEAS-001`、`REQ-SYS-MEAS-003`、`REQ-SYS-INTERFACE-009` |
| IF-MEAS-04 | `VDS_SOURCE_SENSE` | `SOURCE_STAR`局部sense | `VDS`探头 | 测量→ | Source局部参考 | `VDS`负端 | 数据无效 | G2/G6/G7/G10/G11 | `REQ-SYS-MEAS-001`、`REQ-SYS-MEAS-003`、`REQ-SYS-INTERFACE-004`、`REQ-SYS-INTERFACE-009`、`REQ-SYS-VERIFY-001` |
| IF-DATA-01 | `WAVEFORM_DATA` | 示波器 | 软件 | 数据→ | 数据域 | 波形与时序 | invalid/fault | G10/G11/G12 | `REQ-SYS-MEAS-001`、`REQ-SYS-MEAS-009`、`REQ-SYS-VERIFY-001` |
| IF-DATA-02 | `B1505_CAL_DATA` | B1505 | 软件 | 数据→ | 数据域 | 曲线、`Ith`、metadata | 不用不匹配数据 | G12 | `REQ-SYS-INTERFACE-008`、`REQ-SYS-MEAS-006`、`REQ-SYS-MEAS-007`、`REQ-SYS-MEAS-008`、`REQ-SYS-MEAS-009` |
| IF-DATA-03 | `RESULT_DATA` | 软件 | 报告/存储 | 数据→ | 数据域 | `IDS/Vth/ΔVth`审计链 | 不发布合格结论 | G12 | `REQ-SYS-MEAS-004`、`REQ-SYS-MEAS-005`、`REQ-SYS-MEAS-006`、`REQ-SYS-MEAS-007`、`REQ-SYS-MEAS-009`、`REQ-SYS-VERIFY-004` |
| IF-SAFE-01 | `PROTECTION_INTERLOCK_STATUS` | 检测者/User | 安全协调 | 状态→ | 各源域/隔离接口 | valid/fault组合 | fault锁存 | G2/G10 | `REQ-SYS-SAFE-001`、`REQ-SYS-SAFE-002`、`REQ-SYS-SAFE-003`、`REQ-SYS-SAFE-004` |
| IF-SAFE-02 | `GATE_POWER_ENABLE_DISABLE` | 安全协调 | rails/driver/Gate协调 | 控制→ | 隔离控制域 | 顺序允许Gate功能 | inhibit | G2/G10 | `REQ-SYS-SAFE-001`、`REQ-SYS-SAFE-002` |
| IF-SAFE-03 | `DRAIN_POWER_ENABLE_DISABLE` | 安全协调 | `VDC/RL` | 控制→ | 隔离控制域 | Gate和PRECONDITION条件有效后供能 | disable/去能量 | G2/G10 | `REQ-SYS-SAFE-001`、`REQ-SYS-SAFE-002`、`REQ-SYS-SAFE-003` |
| IF-PROFILE-01 | `DUT_PROFILE_CONFIG` | 受控配置 | 控制/rails/adapter/软件 | 配置→ | 数据/配置域 | 包含三引脚公共Source限制 | invalid禁止arm | G2/G4/G10/G12 | `REQ-SYS-DUT-001`、`REQ-SYS-DUT-002`、`REQ-SYS-DUT-003`、`REQ-SYS-DUT-004`、`REQ-SYS-DUT-005`、`REQ-SYS-SAFE-004` |

## 4. Calibration Gate接口语义

`STATE_COMMAND=CALIBRATION`请求完成有效PRECONDITION后进入`MEASUREMENT_I`。Gate目标协调模块通过`IF-GATE-01`保证sink=`DUT_GATE`达到相对`SREF`的`VGM-I`逻辑目标。Ready要求profile/control/rails/interlock有效、0 V路径可释放且其他Gate路径可互斥；valid要求目标被接受并验证有效。MI还要求漏极回路与采集条件有效。进入`SAFE_OFF`时接口立即invalid并移交安全目标。

`IF-GATE-01`不选择具体rail、mux、clamp、器件或拓扑；物理实现延期至G2/G3。P/N的`VIA`真值表不得被用来猜测Calibration的物理实现。

## 5. PRECONDITION接口约束

有效顺序为：所有配置和interlock有效→Gate相对`SREF`为0 V并验证→允许`VDC/RL`→验证`VDS=VDC`与漏极回路→开始`tpre`。任何条件失效均使数据无效并进入锁存`SAFE_OFF`；fault后不得自动重启。

## 6. 延期边界

- `VGM-I`的具体rail、mux、clamp、器件与拓扑：G2/G3。
- connector型号、pin number、Source焊盘和sense落点：G4/G6/G7。
- 三引脚公共Source阻抗的动态影响：G11。
- 四引脚Kelvin Source DUT：不属于本基线，未来需重新审核。

**G1 INTERFACE BASELINE: FROZEN — MASTER APPROVED**

接口数量：25；唯一接口ID：25；未知canonical REQ ID：0。G1阶段门=`PASS`；接口基线=`FROZEN`。

