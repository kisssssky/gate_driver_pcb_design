# 风险登记册

- 状态：`ACTIVE / OPEN`
- 更新：2026-08-25，G1三引脚DUT架构返修

| 风险ID | 风险 | 后果 | G1控制 | 需求追溯 | 后续验证Gate | 状态 |
|---|---|---|---|---|---|---|
| RISK-001 | `SREF`意外接实验室earth | 隐式电流路径、错误`VGS`、设备损坏 | 显式参考域；探头/电源/机壳资格确认 | `REQ-SYS-INTERFACE-001`、`REQ-SYS-INTERFACE-002`、`REQ-SYS-INTERFACE-003`、`REQ-SYS-MEAS-002` | G2/G3/G10 | Open |
| RISK-002 | 外部Gate rail不浮地 | rail争用、错误Gate应力 | 非浮地或rail invalid时禁止arm | `REQ-SYS-INTERFACE-002`、`REQ-SYS-INTERFACE-003`、`REQ-SYS-INTERFACE-006`、`REQ-SYS-SAFE-004` | G2/G10 | Open |
| RISK-003 | Negative BTI默认状态造成持续负应力 | 非计划BTI或DUT损伤 | default不授权stress；fault锁存`SAFE_OFF` | `REQ-SYS-SAFE-001`、`REQ-SYS-SAFE-002` | G2/G10 | Open |
| RISK-004 | 0 V、`VOA`与`CAL_GATE_TARGET`争用 | 大电流、Gate目标错误、器件损坏 | Gate路径单一获权与break-before-make | `REQ-SYS-INTERFACE-010`、`REQ-SYS-SAFE-003` | G2/G3/G10 | Open |
| RISK-005 | Gate过冲或振铃 | 超过DUT限制或应力不确定 | DUT profile、观察接口、后续动态验证 | `REQ-SYS-SAFE-003`、`REQ-SYS-SAFE-004`、`REQ-SYS-DUT-004` | G2/G11 | Open |
| RISK-006 | `VDS`测量链过慢或时间未对齐 | `tdly`与MI/MP/MN错误 | 同次事件`VGS/VDS/timing`接口 | `REQ-SYS-TIME-001`、`REQ-SYS-TIME-002`、`REQ-SYS-MEAS-001`、`REQ-SYS-VERIFY-001` | G2/G10/G11 | Open |
| RISK-007 | 三引脚DUT封装内部公共Source阻抗 | 公共Source电阻/电感造成source bounce，PCB Kelvin式布线无法完全消除，污染实际Gate电压和`VGS/VDS`解释 | `DUT_SOURCE/SOURCE_STAR`处将`SREF`与`DRET`分流；profile记录限制；FMEA和G11验证 | `REQ-SYS-INTERFACE-001`、`REQ-SYS-INTERFACE-004`、`REQ-SYS-DUT-004`、`REQ-SYS-DUT-005`、`REQ-SYS-MEAS-002` | G4/G6/G7/G11 | Open |
| RISK-008 | `VDC/RL`产生过多自热或能量 | 温度漂移或DUT损伤 | 漏极能量责任分配，fault撤销drain enable | `REQ-SYS-SAFE-003`、`REQ-SYS-SAFE-004` | G2/G10/G11 | Open |
| RISK-009 | False trigger | 非计划状态转换 | 命令valid、非法组合转`SAFE_OFF` | `REQ-SYS-INTERFACE-005`、`REQ-SYS-SAFE-002`、`REQ-SYS-SAFE-003` | G2/G10 | Open |
| RISK-010 | Control loss | Gate状态不可控或长时间应力 | 数据invalid、撤销能量并锁存`SAFE_OFF` | `REQ-SYS-SAFE-001`、`REQ-SYS-SAFE-002` | G2/G10 | Open |
| RISK-011 | UVLO/default行为未资格确认 | 输出进入未授权状态 | 未ready不得arm；datasheet核对与故障注入 | `REQ-SYS-SAFE-002`、`REQ-SYS-PROCESS-001` | G2/G10 | Open |
| RISK-012 | `SREF`与`DRET`在`SOURCE_STAR`以外二次连接 | 共阻抗、环路和功率Source压降进入Gate参考 | 只允许Source端单点汇合；连通性与layout审查 | `REQ-SYS-INTERFACE-001`、`REQ-SYS-INTERFACE-003`、`REQ-SYS-INTERFACE-004` | G3/G7/G10 | Open |
| RISK-013 | `VGS/VDS` Source sense落点离开`SOURCE_STAR` | sense包含额外功率路径压降 | 两个Source sense接口均固定为Source端局部支路 | `REQ-SYS-MEAS-001`、`REQ-SYS-MEAS-002`、`REQ-SYS-INTERFACE-004`、`REQ-SYS-INTERFACE-009` | G6/G7/G11 | Open |
| RISK-014 | DUT adapter、pin或方向接错 | 短路、错误`SREF`、DUT损伤 | Adapter属于profile；配置不匹配禁止arm | `REQ-SYS-DUT-004`、`REQ-SYS-DUT-005`、`REQ-SYS-SAFE-004` | G4/G10 | Open |
| RISK-015 | 650 V/3.3 kV profile混用 | Gate/drain条件超限或结果无效 | 受控profile和configuration-valid | `REQ-SYS-DUT-001`、`REQ-SYS-DUT-002`、`REQ-SYS-DUT-003`、`REQ-SYS-DUT-004` | G2/G10/G12 | Open |
| RISK-016 | Scope/probe/chassis建立隐藏earth路径 | `SREF/GNDA`被钳位、短路或测量失真 | earth连接受控；差分探头共模与机壳资格确认 | `REQ-SYS-INTERFACE-002`、`REQ-SYS-INTERFACE-003`、`REQ-SYS-INTERFACE-009`、`REQ-SYS-MEAS-002`、`REQ-SYS-MEAS-003` | G2/G10 | Open |
| RISK-017 | Calibration Gate逻辑责任不完整或ready/valid误用 | `MEASUREMENT_I`未达到`VGM-I`却被标为有效 | `IF-GATE-01`指定模块5、sink/reference、互斥、ready/valid与`SAFE_OFF` | `REQ-SYS-FUNC-003`、`REQ-SYS-INTERFACE-006`、`REQ-SYS-INTERFACE-010`、`REQ-SYS-SAFE-001` | G2/G3/G10/G11 | Open |
| RISK-018 | 在`VDS=VDC`建立前错误起算`tpre` | PRECONDITION无效、初始状态不可比 | 八步PRECONDITION顺序；条件失效即数据invalid和`SAFE_OFF` | `REQ-SYS-FUNC-003`、`REQ-SYS-METHOD-001`、`REQ-SYS-TIME-003`、`REQ-SYS-SAFE-001` | G10/G12 | Open |

## 状态说明

- 本轮没有关闭或退役风险。
- RISK-007已从“Kelvin Source/Power Source可能共阻抗”改为当前三引脚DUT的确定性封装限制。
- 新增RISK-012、RISK-013、RISK-017、RISK-018，用于覆盖单点汇合、sense落点、Calibration Gate目标和PRECONDITION计时。
- 详细14项简化FMEA见`docs/G1_system_architecture_v1.1.md`第10章。
- 未编造发生率、严重度或定量风险等级。

