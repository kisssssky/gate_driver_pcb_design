# SiC MOSFET BTI快速栅极驱动与阈值迟滞测量平台

## 项目介绍（中文版）

- 版本：`PROJECT-INTRO-ZH-v1.0`
- 日期：2026-08-25
- 适用场景：组会、博士阶段汇报、项目评审和技术交流
- GitHub：`kisssssky/gate_driver_pcb_design`

## 1. 项目概述

本项目旨在功能复现Li等人在IEEE TPEL 2024论文《Accurate Evaluation of Threshold Voltage Hysteresis in SiC MOSFET Under Switching Stress》中Fig. 3所示的快速测试架构，开发一套面向SiC MOSFET偏压温度不稳定性（BTI）和阈值电压迟滞研究的快速栅极驱动与测量平台。

SiC MOSFET在撤除栅极应力后会发生快速恢复。如果应力状态切换到测量状态所需时间过长，最早期的阈值电压变化将被遗漏。项目因此不把“驱动器输出边沿快”作为唯一目标，而把完整系统目标定义为：

> DUT完成`0 V预处理 → 栅极应力 → 快速测量`，并在应力结束后约100 ns获得可解释、可重复的`VDS`测量点。

测得的高速`VGS(t)`、`VDS(t)`和时序数据将与Keysight B1505A获得的固定`VDS-C`校准曲线结合，通过`VDS → IDS → Vth → ΔVth`处理链提取阈值电压变化。

## 2. 研究问题

传统BTI测试存在以下困难：

- 应力撤除与测量之间的延迟会掩盖快速恢复过程；
- Positive BTI和Negative BTI需要不同的栅极应力与测量电压；
- 栅极驱动、漏极偏置、探头带宽、回流路径和寄生参数会共同影响约100 ns测量结果；
- 不同额定电压和封装的SiC MOSFET具有不同的`Qg`、输入电容、允许`VGS`和公共Source寄生；
- 仅观察驱动器输出不能证明DUT端已经形成有效、可解释的测量状态。

本项目通过系统架构、接口定义、受控DUT profile、同步波形测量和阶段门验证解决这些问题。

## 3. 项目目标

1. 使用同一块Base PCB支持Positive BTI和Negative BTI，不因切换极性而更换PCB元件。
2. 使用外部`VDDA/GNDA`设定和控制波形改变应力/测量极性。
3. 使用Si8273 channel A / `VOA`完成stress-to-measurement快速切换。
4. 支持Calibration、Positive BTI和Negative BTI三条完整测试序列。
5. 在同一次事件中记录`VGS(t)`、`VDS(t)`和共同时间参考。
6. 支持650 V-class与3.3 kV-class三引脚SiC MOSFET的低`VDS` BTI测试。
7. 建立从原始波形到`MI/MP/MN`、`IDS`、`Vth`和`ΔVth`的可追溯数据链。
8. 通过需求、计算、仿真、ERC/DRC、人工审核和实验验证后再发布制造文件。

## 4. 实验流程

| 测试序列 | 状态流程 | 目的 |
|---|---|---|
| Calibration | `PRECONDITION → MEASUREMENT_I` | 获得初始测量点MI和`Vth-IS` |
| Positive BTI | `PRECONDITION → POSITIVE_STRESS → MEASUREMENT_P` | 获得正栅应力后的MP及恢复数据 |
| Negative BTI | `PRECONDITION → NEGATIVE_STRESS → MEASUREMENT_N` | 获得负栅应力后的MN及恢复数据 |

`PRECONDITION`用于建立Gate-to-`SREF`的0 V初始状态；`SAFE_OFF`是独立安全状态，用于禁止非预期应力、撤销漏极能量并锁存故障，两者不能混为同一状态。

## 5. 系统架构

| 子系统 | 主要职责 |
|---|---|
| Pulse Generator / 控制器 | 产生状态命令、`VIA`控制和共同时间参考 |
| Si8273隔离栅极驱动 | 隔离逻辑域并执行P/N stress-to-measurement快速切换 |
| Gate目标协调与安全互锁 | 管理0 V预处理、`VGM-I`、路径互斥和`SAFE_OFF` |
| 浮动栅极电源轨 | 提供相对`SREF`定义的`VDDA/GNDA` |
| 三引脚DUT adapter | 映射Gate、Drain、Source及DUT专用profile |
| `VDC + RL`漏极回路 | 提供低`VDS`测量偏置、限制电流和能量 |
| 示波器与探头 | 同步采集`VGS`、`VDS`和时序参考 |
| B1505A | 生成固定`VDS-C`的`IDS-VGS`校准曲线 |
| 后处理软件 | 计算`IDS`、`Vth`、`ΔVth`并保存metadata |

## 6. 三引脚DUT与Source参考

当前650 V-class和3.3 kV-class目标DUT均只有Gate、Drain和Source三个物理引脚，不具有独立第四个Kelvin Source引脚。

项目在DUT Source引脚或焊盘处定义`SOURCE_STAR`：

- `SREF`：从`SOURCE_STAR`引出的Gate回流和`VGS`测量Kelvin式参考路径；
- `DRET`：从同一`SOURCE_STAR`引出的漏极功率返回路径。

两条路径在`SOURCE_STAR`有意汇合，但不得在上游再次连接。三引脚封装内部公共Source电阻和电感无法由PCB完全消除，因此必须记录在DUT profile中，并在高速波形验证阶段评估其影响。

## 7. 650 V与3.3 kV兼容边界

平台兼容性指使用同一套逻辑架构、状态机、测量链和Base PCB概念测试两类DUT，并不意味着PCB向DUT施加650 V或3.3 kV。

本项目研究的是低`VDS`条件下的BTI和阈值电压迟滞，不是击穿测试。不同DUT通过受控profile和adapter管理以下差异：

- 封装和引脚映射；
- `VGS-P/N`与`VGM-I/P/N`；
- `Qg/Ciss/Crss`及Gate driver负载；
- `Rg`；
- `VDS-C`、`VDC`和`RL`；
- 公共Source寄生；
- 探头共模、带宽和接入方式。

## 8. 当前进度

截至2026-08-25：

| 阶段 | 状态 |
|---|---|
| SP1 论文方法与系统需求 | `MASTER APPROVED / COMPLETE` |
| G0 规范需求定义 | `PASS` |
| Canonical requirement baseline | `FROZEN`，65条`REQ-SYS-*` |
| G1 系统架构 | `ACTIVE — READY FOR MASTER REVIEW`，三引脚返修候选v1.1 |
| G2 器件选型与计算 | `NOT STARTED`，可准备datasheet和计算 |
| G3 KiCad原理图 | `BLOCKED` |

G1候选架构现包含13个模块、7个逻辑状态、25个接口、8幅架构/路径图和14项FMEA。该状态不表示G1已经PASS或接口已经FROZEN。

## 9. 下一步计划

1. 完成G1 Master复审并冻结系统接口。
2. 在G2确认Si8273准确料号、目标DUT、栅极电压、`Qg`、`Rg`、去耦、`VDC/RL`和保护要求。
3. 使用LTspice验证栅极驱动、预处理、快速切换、寄生和故障状态。
4. 在G3–G8完成KiCad原理图、footprint、PCB规则、placement、routing及ERC/DRC审核。
5. 在G10–G11完成bring-up、故障测试、约100 ns切换和测量链验证。
6. 在G12执行完整Fig. 3实验复现，并输出`MI/MP/MN → IDS → Vth → ΔVth`结果。

## 10. 预期成果

- 一块支持Positive/Negative BTI的快速栅极驱动Base PCB；
- 面向650 V-class与3.3 kV-class三引脚SiC MOSFET的可更换adapter/profile体系；
- 经过验证的约100 ns stress-to-measurement测试能力；
- B1505校准与高速示波器数据的统一处理流程；
- 可追溯的需求、设计、验证、风险和实验记录；
- 支持SiC MOSFET BTI、阈值迟滞和TCAD模型校准的实验平台。

## 11. 汇报用简短介绍

本项目正在开发一套用于SiC MOSFET BTI和阈值电压迟滞研究的快速栅极驱动与测量平台，目标是复现Li等人2024年论文Fig. 3的功能。在传统测试中，器件撤除应力后的快速恢复容易被测量延迟掩盖，因此本平台通过Si8273实现应力电压到测量电压的快速切换，并争取在应力结束后约100 ns获得可解释的DUT端`VDS`测量点。平台使用同一块Base PCB支持正、负BTI，通过B1505校准曲线和同步`VGS/VDS`波形提取`IDS`、`Vth`与`ΔVth`。当前需求基线已经冻结，G0已经通过，三引脚DUT系统架构正在等待G1 Master复审。
