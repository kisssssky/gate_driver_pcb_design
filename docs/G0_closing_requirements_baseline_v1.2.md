# SiC MOSFET BTI快速栅极驱动PCB / Fig. 3复现

## G0需求基线中文重构与追溯修正版

- 版本：G0-CRB-v1.2
- 日期：2026-08-25
- 文件状态：**修正提案——可重新提交Master审核（`CORRECTED PROPOSAL — READY FOR MASTER REVIEW`）**
- 当前阶段：G0仍为`ACTIVE`；G1可以继续；G3仍为`BLOCKED`
- 批准状态：`OPEN::OI-000`尚未批准；本文件未`FROZEN`；G0未`PASS`
- 修改边界：本版只改善中文可读性并修正指定追溯关系，不增加需求、不选择电路、不修改任何已批准SP1文件或既有项目基线文件。

## 1. 一页中文摘要

### 1.1 这个项目最终要做什么

本项目要制作一块SiC MOSFET BTI快速栅极驱动PCB，用来复现论文Fig. 3的测试方法。系统先对DUT做0 V预处理，再施加正或负栅极应力，最后快速切换到测量电压。示波器捕获DUT的`VDS`测量点，软件再结合B1505校准曲线计算`Vth`和修正后的`ΔVth`。

### 1.2 PCB必须实现什么

- 同一块基础PCB同时支持正BTI和负BTI。
- 对同一个DUT和同一份配置档案，正/负模式切换只能改变外部`VDDA/GNDA`和控制波形，不能更换转接板、`Rg`或PCB元件。
- 以DUT Kelvin Source作为`SREF`，并保持`GNDI`、`GNDA`、`SREF`和实验室earth明确分开。
- 支持0 V预处理，以及校准、正应力、负应力三条完整测试序列。
- 由Si8273的`VOA`完成关键的应力→测量快速切换。
- 支持低`VDS`电阻负载回路，并提供`VGS`、`VDS`和时序参考的测量接口。
- 让系统能够得到可解释、可重复的MI、MP、MN和完整系统`tdly`。

### 1.3 PCB不负责什么

- PCB不负责生成B1505的固定`VDS-C`校准曲线。
- PCB不替代脉冲发生器、外部电源、示波器、探头或后处理软件。
- PCB不单独完成`Vth/ΔVth`计算。
- 本项目不做击穿测试，也不要求PCB因为DUT标称650 V或3.3 kV就施加该电压。
- G0不决定DUT具体参数、`Rg`、电容、保护拓扑、0 V开关拓扑、连接器引脚定义、原理图或布局。

### 1.4 为什么需要三条测试序列

- 校准序列得到MI和测试系统自身引入的初始偏差`Vth-IS`。
- 正应力序列得到MP和正应力后的阈值位移。
- 负应力序列得到MN和负应力后的阈值位移。
- 只有三条序列都存在，才能从正/负应力结果中扣除系统自身偏差，得到修正后的`ΔVth`。

### 1.5 为什么约100 ns不能只看`VOA`边沿

论文中的约100 ns描述的是完整系统延迟：从应力结束，经栅极转换和DUT响应，到`VDS`出现有效测量点。即使`VOA`边沿很快，如果DUT的`VDS`测量点出现得太晚、振铃太强或无法重复，系统仍未达到目标。因此G11必须同时测时序参考、`VGS`和`VDS`，不能只测驱动器输出边沿。

### 1.6 为什么650 V/3.3 kV不是PCB实际测试电压

650 V和3.3 kV是目标DUT的额定阻断电压等级，不是本BTI测试的漏极工作电压。本项目使用低`VDS`条件；实际`VDC`和`VDS-C`由DUT配置档案和BTI测量条件决定。通用性通过“基础架构 + DUT配置档案 + 转接/配置”实现。

### 1.7 当前已经确定什么

一块基础PCB支持正/负BTI、同一DUT和同一配置档案切换时不换硬件、`SREF`定义、0 V预处理、三条测试序列、`VOA`职责、低`VDS`电阻负载原理、`VDS→IDS→Vth→ΔVth`提取链、B1505与高速PCB的职责边界、完整系统约100 ns目标，以及650 V/3.3 kV低`VDS`兼容范围均已明确。

### 1.8 当前还没有决定什么

准确DUT型号与参数、各栅极电压和漏极条件、`Rg`、连接器/转接板实现、仪器规格、`SAFE_OFF`详细行为、保护和上电时序、`tdly`精确算法、`VDS/IDM`容差、滤波、振铃、通道时间校正（deskew）以及最终实验软件规则仍按本文件第5章延期决定。

### 1.9 G0通过后下一步做什么

Master批准`OPEN::OI-000`后，才能把本文件的65条需求正式安装进`docs/requirements.md`，并重建`docs/verification_matrix.md`。完成文件更新、远端回读和一致性检查后，才能宣布G0通过和冻结。随后G1继续完成系统方框图与接口，G2再确定DUT和电路参数；G3原理图在前置条件满足前仍保持阻塞。

## 2. 如何阅读本文件

- `REQ-SYS-*`：项目级正式需求编号。例如`REQ-SYS-TIME-002`表示“系统时间需求第2条”。
- 来源（Source）：说明需求依据来自哪里。正文采用中文列名“来源”，具体ID保留英文。
- 验证（Verification）：说明以后用什么证据判断需求是否满足。正文采用中文列名“如何验证”。
- `OPEN::OI-*`：尚未决定、但已经明确负责人和截止阶段的问题。延期不等于取消。
- 已确认（`CONFIRMED`）：需求内容已有批准依据。
- 待Master批准（`PROPOSED`）：项目需要该要求，但本次候选基线仍需Master批准。
- 验收条件延期（`ACCEPTANCE DEFERRED`）：功能要求已确定，具体数值或算法到指定阶段再决定。
- 条件未激活（`CONDITIONAL-INACTIVE`）：只有Master扩大项目范围后才生效。
- `PROJECT REQUIREMENT — CONDITIONAL`：条件性项目需求；当前不属于最小Fig. 3强制范围。

治理标签首次解释如下：

- `PAPER FACT`：论文直接支持的事实。
- `PAPER EXAMPLE VALUE`：论文示例数值，不自动成为项目数值。
- `PAPER PERFORMANCE REFERENCE`：论文报告的性能参考，不自动成为项目通过判据。
- `ENGINEERING INFERENCE`：为了实现或验证论文方法而作出的工程推断。
- `PROJECT REQUIREMENT`：对本项目有约束力的需求。
- `PROJECT DESIGN CHOICE`：实现需求的具体方案。
- `OPEN ITEM`：仍需在指定阶段决定的问题。

## 3. G0已经确定的核心要求

1. 同一块基础PCB同时支持正BTI和负BTI。
2. 同一DUT和同一配置档案在正负模式间切换时，只改变外部电源轨和控制波形，不更换基础PCB元件、转接板或`Rg`。
3. `SREF`固定定义为DUT Kelvin Source参考点，并且不自动等于实验室earth。
4. 系统必须实现0 V预处理，但0 V钳位/开关拓扑尚未决定。
5. 系统必须支持校准、正应力、负应力三条测试序列。
6. Si8273 channel A的`VOA`负责关键的应力→测量快速转换。
7. 漏极侧采用低`VDS`电阻负载测量原理。
8. 数据链必须保持为`VDS→IDS→B1505曲线→Vth→修正后ΔVth`。
9. B1505负责固定`VDS-C`校准曲线；高速PCB负责产生快速状态并提供波形测量接口。
10. 约100 ns是完整系统`tdly`目标，不是单独`VOA`边沿通过判据。
11. 平台目标包括650 V等级和3.3 kV等级的DUT，但只做低`VDS` BTI，不做击穿测试。
12. 系统必须定义`SAFE_OFF`、电源时序和保护；具体实现可以延期，但不能取消。

## 4. 规范需求

本章保留全部65条项目级需求。每条先说明“系统必须做什么”，再说明来源、理由和以后如何验收。

### 4.1 功能需求（8条）

| ID | 系统必须满足的要求 | 类别 | 需求性质 | 来源 | 为什么需要 | 如何验证 | 验证阶段 | 当前状态 |
|---|---|---|---|---|---|---|---|---|
| REQ-SYS-FUNC-001 | 同一块已装配的基础PCB必须同时支持正BTI和负BTI。 | 功能 | PROJECT REQUIREMENT | `DECISION::DEC-001`; `LEGACY::REQ-001` | 避免为正、负两种BTI分别制作两套PCB。 | 审查设计；用同一块PCB分别执行正、负BTI测试。 | G1、G11、G12 | 已确认（`CONFIRMED`） |
| REQ-SYS-FUNC-002 | 对同一个DUT和同一份已批准DUT配置档案，P/N模式切换只能改变外部`VDDA/GNDA`和控制波形；不得重新焊接或更换基础PCB元件、DUT转接板或`Rg`。只有更换DUT或更换已批准配置档案时，才可改变DUT专用配置。 | 功能 | PROJECT REQUIREMENT | `DECISION::DEC-001`, `DECISION::DEC-002`; `LEGACY::REQ-002` | 确保同一DUT切换极性时不需要改动硬件，同时保留更换DUT时的受控适配能力。 | 核对同一DUT/profile切换前后的配置，确认只改变电源轨和控制波形。 | G1、G11 | 已确认（`CONFIRMED`）；DUT配置边界见`OPEN::OI-015`、`OPEN::OI-016`、`OPEN::OI-017` |
| REQ-SYS-FUNC-003 | 系统必须支持三条序列：校准=`PRECONDITION→MEASUREMENT_I`；正应力=`PRECONDITION→POSITIVE_STRESS→MEASUREMENT_P`；负应力=`PRECONDITION→NEGATIVE_STRESS→MEASUREMENT_N`。 | 功能 | PROJECT REQUIREMENT | `SP1::REQ-FUNC-002`（PAPER FACT）；`DECISION::DEC-008` | 三条序列共同构成MI、MP、MN和`ΔVth`提取流程。 | 同步记录三条状态波形，核对状态顺序。 | G11、G12 | 已确认（`CONFIRMED`） |
| REQ-SYS-FUNC-004 | 系统必须支持低能量电阻负载回路：`VDC→RL→DUT Drain→DUT Power Source→return`。 | 功能 | PROJECT REQUIREMENT | `SP1::REQ-FUNC-001`（PAPER FACT）；`LEGACY::REQ-012` | 该回路允许通过测得的`VDS`计算`IDS`。 | 检查连通性，并在低能量条件下验证回路与计算公式一致。 | G1、G10、G12 | 已确认（`CONFIRMED`） |
| REQ-SYS-FUNC-005 | 在`MEASUREMENT_I/P/N`状态下，DUT必须处于不完全导通状态，并产生有限且可计算的`IDS`。 | 功能 | PROJECT REQUIREMENT | `SP1::REQ-FUNC-003`（PAPER FACT） | MI、MP、MN必须对应有限电流，才能映射到B1505校准曲线。 | 验证`0<VDS<VDC`且`IDS>0`；具体裕量在G12确定。 | G11、G12 | 已确认（`CONFIRMED`）；验收条件延期（`ACCEPTANCE DEFERRED`）至G12 |
| REQ-SYS-FUNC-006 | 系统必须获得可解释、可重复的MI、MP、MN，并保留正/负应力测量点之后的恢复波形。 | 功能 | PROJECT REQUIREMENT | `SP1::REQ-FUNC-004`（PAPER FACT）；`DECISION::DEC-009` | 应力撤除后的快速恢复会使阈值位移被低估。 | 重复采集波形，检查三个测量点及正/负应力后的恢复是否可识别、可重复。 | G11、G12 | 已确认（`CONFIRMED`）；测量点算法延期至G10/G11 |
| REQ-SYS-FUNC-007 | Si8273 channel A的`VOA`必须承担关键的应力→测量栅极电压快速转换。 | 功能 | PROJECT REQUIREMENT | `DECISION::DEC-005`; `LEGACY::REQ-005`（PROJECT DESIGN CHOICE 已由 Master 批准） | 保持Master已批准的关键快速切换器件职责。 | 核对原理图追溯关系，并测量`VIA/VOA/VGS`波形。 | G3、G10、G11 | 已确认（`CONFIRMED`） |
| REQ-SYS-FUNC-008 | 正BTI模式必须实现`VDDA=VGS-P`、`GNDA=VGM-P`、`VIA HIGH→LOW`；负BTI模式必须实现`VDDA=VGM-N`、`GNDA=VGS-N`、`VIA LOW→HIGH`。 | 功能 | PROJECT REQUIREMENT | `DECISION::DEC-006`, `DECISION::DEC-007`; `LEGACY::REQ-006`, `LEGACY::REQ-007`（PROJECT DESIGN CHOICE 已由 Master 批准） | 形成Master已批准的正、负BTI两级切换真值表。 | 审查模式表，并在dummy load上验证`VGS`波形。 | G1、G10、G11 | 已确认（`CONFIRMED`） |

### 4.2 方法需求（9条）

| ID | 系统必须满足的要求 | 类别 | 需求性质 | 来源 | 为什么需要 | 如何验证 | 验证阶段 | 当前状态 |
|---|---|---|---|---|---|---|---|---|
| REQ-SYS-METHOD-001 | 每条测试序列都必须支持Gate-to-SREF的`VGS=0 V`预处理；G0不规定0 V实现拓扑。 | 方法 | PROJECT REQUIREMENT | `SP1::REQ-VOLT-001`（PAPER FACT）；`DECISION::DEC-008` | 0 V预处理用于消除前次测试历史影响，同时避免在G0提前选择实现拓扑。 | 相对`SREF`测量预处理阶段的`VGS`；容差和实现方式后定。 | G10、G12 | 已确认（`CONFIRMED`）；容差和实现拓扑延期 |
| REQ-SYS-METHOD-002 | 系统必须支持`VGM-I`、`VGM-P`、`VGM-N`；`VGM-I=initial Vth`，`VGM-P/N`可分别调节，三者不要求相等。 | 方法 | PROJECT REQUIREMENT | `SP1::REQ-VOLT-003`（PAPER FACT） | 应力后DUT等效电阻会改变，需要分别调节测量栅压来对齐工作点。 | 分别设定三个测量电压并验证实际波形。 | G2、G11、G12 | 已确认（`CONFIRMED`）；范围和分辨率延期至G2 |
| REQ-SYS-METHOD-003 | B1505必须在DUT专用的固定`VDS-C`下取得初始`IDS-VGS`曲线，并用DUT专用`Ith`交点定义初始`Vth`。 | 方法 | PROJECT REQUIREMENT | `SP1::REQ-VOLT-004`, `SP1::REQ-MEAS-008`（PAPER FACT） | 为高速点测建立统一的`IDS-VGS`参考曲线和初始`Vth`定义。 | 审查B1505测试记录，并独立重算`Ith`交点。 | G2、G12 | 已确认（`CONFIRMED`）；具体数值延期至G2 |
| REQ-SYS-METHOD-004 | MI、MP、MN处的`VDS`必须在已批准容差内与对应`VDS-C`对齐。 | 方法 | PROJECT REQUIREMENT | `SP1::REQ-VOLT-005`（PAPER FACT（原则）） | 保证高速测量点与B1505校准曲线使用可比较的漏极偏压。 | 自动计算并报告各测量点与`VDS-C`的偏差。 | G12 | 原则已确认（`CONFIRMED`）；容差延期至G12 |
| REQ-SYS-METHOD-005 | 每个测量工作点必须满足`VDS-C>VGS-Vth`；所需裕量由DUT配置档案规定。 | 方法 | PROJECT REQUIREMENT | `SP1::REQ-VOLT-006`（PAPER FACT） | 保证曲线映射使用论文要求的工作区域。 | 根据记录量检查不等式并计算裕量。 | G2、G12 | 已确认（`CONFIRMED`）；裕量延期至G2 |
| REQ-SYS-METHOD-006 | 校准被接受后，正/负应力测试必须保持`VDC`和`RL`不变，只调节`VGM-P/N`完成工作点对齐。 | 方法 | PROJECT REQUIREMENT | `SP1::REQ-FUNC-005`, `SP1::REQ-CTRL-002`（PAPER FACT） | 防止正、负应力测试改变校准条件。 | 核对三组测试的配置和元数据，确认`VDC/RL`不变。 | G12 | 已确认（`CONFIRMED`） |
| REQ-SYS-METHOD-007 | `IDM-P`和`IDM-N`必须在批准容差内与`IDM-I`匹配；P1的±20%只作为`PAPER PERFORMANCE REFERENCE`。 | 方法 | PROJECT REQUIREMENT | `SP1::REQ-MEAS-007`（原则为PAPER FACT；±20%为PAPER PERFORMANCE REFERENCE） | 限制测量电流不一致给`ΔVth`带来的误差。 | 明确百分比公式，分别报告正、负应力的电流偏差。 | G12 | 原则已确认（`CONFIRMED`）；容差延期至G12 |
| REQ-SYS-METHOD-008 | 正应力期间的`IDS`和能量必须受DUT专用上限约束，避免自热使`Vth`结果无法解释。 | 方法 | PROJECT REQUIREMENT | `SP1::REQ-MEAS-010`（PAPER FACT（原则））+ ENGINEERING INFERENCE | 避免温升造成的`Vth`变化与BTI迟滞混在一起。 | G2计算电流和能量范围；G10/G11测量实际电流、能量及必要热代理。 | G2、G10、G11 | 待Master批准（`PROPOSED`）；上限延期至G2 |
| REQ-SYS-METHOD-009 | 只有Master激活完整论文/Fig. 10复现范围后，系统才需要满足批准的多脉冲应力流程。 | 方法 | PROJECT REQUIREMENT — CONDITIONAL | `SP1::REQ-CTRL-003` + `OPEN::OI-022` | 避免把Fig. 10扩展实验误写成最小Fig. 3复现的强制功能。 | 仅在Master激活后记录脉冲列、总应力时间和测试结果。 | G12 | 条件未激活（`CONDITIONAL-INACTIVE`）；仅在Master激活完整论文/Fig. 10复现范围后生效 |

### 4.3 时间需求（6条）

| ID | 系统必须满足的要求 | 类别 | 需求性质 | 来源 | 为什么需要 | 如何验证 | 验证阶段 | 当前状态 |
|---|---|---|---|---|---|---|---|---|
| REQ-SYS-TIME-001 | 系统必须支持正/负应力状态快速、可重复地切换到对应测量状态。 | 时间 | PROJECT REQUIREMENT | `SP1::REQ-TIME-001`（PAPER FACT） | 减少应力撤除后恢复造成的测量低估。 | 在同一次事件中记录时序参考、`VGS`和`VDS`。 | G11 | 已确认（`CONFIRMED`） |
| REQ-SYS-TIME-002 | 项目必须以P1报告的约100 ns完整系统`tdly`作为设计和验证目标；该目标不是单独`VOA`边沿指标，也暂不等于明确的`<100 ns`或`≤100 ns`通过判据。 | 时间 | PROJECT REQUIREMENT | `SP1::REQ-TIME-002`（PAPER PERFORMANCE REFERENCE）；`DECISION::DEC-009`; `LEGACY::REQ-010` | 保留论文报告的性能方向，同时避免在事件算法未定义时给出虚假的硬通过判据。 | 按G10/G11批准的事件定义提取完整系统`tdly`。 | G11 | 目标性质已确认（`CONFIRMED`）；数值通过判据延期至G10/G11 |
| REQ-SYS-TIME-003 | 系统必须支持可配置`tpre`，并允许通过MI或`Vth-IS`稳定性建立预处理完成判据。 | 时间 | PROJECT REQUIREMENT | `SP1::REQ-TIME-003`（PAPER FACT: long-term；数值未公开） | 控制前次测试历史对当前结果的影响。 | 改变`tpre`并检查MI或`Vth-IS`的稳定性和重复性。 | G12 | 能力已确认（`CONFIRMED`）；数值和完成判据延期至G12 |
| REQ-SYS-TIME-004 | 系统必须支持可配置`tstr`；P1给出的时间范围和示例只属于`PAPER EXAMPLE VALUE`。 | 时间 | PROJECT REQUIREMENT | `SP1::REQ-TIME-004`（PAPER FACT（能力）） | 支持研究不同应力持续时间下的BTI响应。 | 比较设定值与示波器实测`tstr`。 | G11、G12 | 能力已确认（`CONFIRMED`）；项目范围延期至G2/G12 |
| REQ-SYS-TIME-005 | 系统必须支持足以捕获选定测量点和所需恢复区间的`tmea`。 | 时间 | PROJECT REQUIREMENT | `SP1::REQ-TIME-005`（PAPER FACT（能力）） | 防止采集窗口截断测量点或恢复波形。 | 检查采集窗口是否完整覆盖选定测量点和恢复区间。 | G10、G11、G12 | 能力已确认（`CONFIRMED`）；持续时间延期至G10/G11 |
| REQ-SYS-TIME-006 | 系统必须允许改变并记录实际`tdly`，以得到恢复随延迟变化的数据；范围和步进由批准的实验流程规定。 | 时间 | PROJECT REQUIREMENT | `SP1::REQ-TIME-006`（PAPER FACT（能力）） | 支持获得`ΔVth`随测量延迟变化的数据。 | 执行延迟扫描，核对实际`tdly`、重复性和元数据。 | G11、G12 | 能力已确认（`CONFIRMED`）；范围和步进延期至G12 |

### 4.4 测量与数据需求（9条）

| ID | 系统必须满足的要求 | 类别 | 需求性质 | 来源 | 为什么需要 | 如何验证 | 验证阶段 | 当前状态 |
|---|---|---|---|---|---|---|---|---|
| REQ-SYS-MEAS-001 | 每次转换必须记录同一事件的`VGS(t)`、`VDS(t)`和最终`tdly`定义所需的时序参考信号，并建立明确的共同时间关系。 | 测量 | PROJECT REQUIREMENT | `SP1::REQ-MEAS-001`（PAPER FACT + ENGINEERING INFERENCE） | 完整系统时序需要把控制事件、栅极响应和漏极测量点放在同一时间关系中。 | 核对通道、触发和时间对齐；deskew规则在G10/G11确定。 | G10、G11 | 已确认（`CONFIRMED`）；deskew规则延期至G10/G11 |
| REQ-SYS-MEAS-002 | `VGS`必须测为DUT Gate-to-Kelvin-Source/SREF，不得测成gate-to-earth。 | 测量 | PROJECT REQUIREMENT | `DECISION::DEC-003`, `DECISION::DEC-004`; `LEGACY::REQ-011` | 避免参考点错误和危险的接地回路。 | 采用差分方式测量，并审查实际接线。 | G1、G10、G11 | 已确认（`CONFIRMED`） |
| REQ-SYS-MEAS-003 | 系统必须提供可安全探测的`VGS`、`VDS`和时序/触发观察点；具体探头和连接器由后续阶段决定。 | 测量 | PROJECT REQUIREMENT | `LEGACY::REQ-014`; ENGINEERING INFERENCE | 关键功能必须有实际可接入的测量证据。 | 审查接口和探头接入空间；G6/G7核对物理实现。 | G1、G6/G7、G10 | 功能已确认（`CONFIRMED`）；物理实现延期至G6/G7 |
| REQ-SYS-MEAS-004 | 后处理必须使用`IDS=(VDC-VDS)/RL`计算测量点电流，并保存所用`VDC/RL`元数据。 | 测量 | PROJECT REQUIREMENT | `SP1::REQ-MEAS-002`（PAPER FACT） | 建立从`VDS`到`IDS`的可重算链。 | 用已知输入做计算单元测试，并重算样例数据。 | G12 | 已确认（`CONFIRMED`） |
| REQ-SYS-MEAS-005 | 后处理必须分别由MI、MP、MN得到`IDM-I`、`IDM-P`、`IDM-N`。 | 测量 | PROJECT REQUIREMENT | `SP1::REQ-MEAS-003`（PAPER FACT） | 为三条阈值位移提取流程提供对应电流。 | 用带已知测量点的参考波形回放算法。 | G10/G11、G12 | 已确认（`CONFIRMED`）；极值算法延期至G10/G11 |
| REQ-SYS-MEAS-006 | `IDM-I/P/N`必须映射到同一DUT、同一固定`VDS-C`的B1505曲线；插值方法必须一致且可审计。 | 测量 | PROJECT REQUIREMENT | `SP1::REQ-MEAS-004`（PAPER FACT） | 保证三个测量电流都使用同一条校准曲线。 | 对查表和插值算法做单元测试。 | G12 | 已确认（`CONFIRMED`）；插值验收延期至G12 |
| REQ-SYS-MEAS-007 | 后处理必须按P1式(3)及相同方法得到`Vth-IS/PS/NS`，并按式(5)计算修正后的`ΔVth`。 | 测量 | PROJECT REQUIREMENT | `SP1::REQ-MEAS-005`, `SP1::REQ-MEAS-006`（PAPER FACT；正/负展开式为工程重述`ENGINEERING RESTATEMENT`） | 完成从原始测量量到修正后`ΔVth`的计算链。 | 用构造数据做公式单元测试，并独立重算结果。 | G12 | 已确认（`CONFIRMED`） |
| REQ-SYS-MEAS-008 | 采用单点/平行位移映射前，必须对每个目标DUT和测试条件验证`IDS≈Ith`附近曲线是否适用；P1的1%只作为`PAPER PERFORMANCE REFERENCE`。 | 测量 | PROJECT REQUIREMENT | `SP1::REQ-MEAS-009`（原则为PAPER FACT；1%为PAPER PERFORMANCE REFERENCE） | 防止把论文DUT的平行位移特性直接外推到其他DUT。 | 比较应力前后曲线，检查`IDS≈Ith`附近的位移一致性。 | G12 | 待Master批准（`PROPOSED`）；验收条件延期至G12 |
| REQ-SYS-MEAS-009 | 原始波形、仪器与配置元数据、DUT配置档案、B1505曲线、算法版本和最终结果必须足以独立重算MI/MP/MN、`tdly`和`ΔVth`，并报告重复性。 | 测量 | PROJECT REQUIREMENT | `SP1::REQ-VERIFY-004`; `DECISION::DEC-009`; ENGINEERING INFERENCE | 保证结果可解释、可重复并能由第三方重算。 | 审查完整数据包，并用独立软件回放。 | G11、G12 | 待Master批准（`PROPOSED`） |

### 4.5 接口需求（10条）

| ID | 系统必须满足的要求 | 类别 | 需求性质 | 来源 | 为什么需要 | 如何验证 | 验证阶段 | 当前状态 |
|---|---|---|---|---|---|---|---|---|
| REQ-SYS-INTERFACE-001 | `SREF`必须定义为DUT Kelvin Source参考点。 | 接口 | PROJECT REQUIREMENT | `DECISION::DEC-003`; `LEGACY::REQ-003` | 固定栅极驱动和`VGS`测量的共同参考点。 | 审查net和接口，并做连通性测试。 | G1、G3、G10 | 已确认（`CONFIRMED`） |
| REQ-SYS-INTERFACE-002 | `SREF`不得自动等于实验室earth或chassis。 | 接口 | PROJECT REQUIREMENT | `DECISION::DEC-004`; `LEGACY::REQ-004` | 避免意外短路、共模错误和无效`VGS`测量。 | 做绝缘与连通性测试。 | G1、G3、G10 | 已确认（`CONFIRMED`） |
| REQ-SYS-INTERFACE-003 | `GNDI`、`GNDA`、`SREF`、earth/chassis必须保持显式区分；任何连接都必须经过Master批准并可追溯。 | 接口 | PROJECT REQUIREMENT | `GOVERNANCE::AGENTS.md`; `INTERFACE::docs/interfaces.md`（禁止隐式连接） | 防止不同参考域在设计中被隐式合并。 | 审查系统架构、net关系和任何批准的跨域连接。 | G1、G3、G8、G10 | 已确认（`CONFIRMED`） |
| REQ-SYS-INTERFACE-004 | DUT封装支持时，Power Source与Kelvin Source路径必须分开；不支持时必须在DUT配置档案中记录限制。 | 接口 | PROJECT REQUIREMENT | `LEGACY::REQ-013`; ENGINEERING INFERENCE | 降低Power Source压降和source bounce对驱动与测量的影响。 | 审查连接器、net和layout，并进行动态波形验证。 | G1、G6/G7、G11 | 已确认（`CONFIRMED`） |
| REQ-SYS-INTERFACE-005 | 外部脉冲/控制接口必须支持可重复的状态命令、触发参考和`tpre/tstr/tmea/tdly`配置；电平、通道和连接器由G1定义。 | 接口 | PROJECT REQUIREMENT | `SP1::REQ-CTRL-001`（序列为PAPER FACT；接口为ENGINEERING INFERENCE） | 保证状态切换与示波器采集能够同步。 | 审查接口控制文件，并重复采集触发波形。 | G1、G11 | 待Master批准（`PROPOSED`） |
| REQ-SYS-INTERFACE-006 | 栅极目标接口必须允许外部设定或提供`VGS-P/N`、`VGM-I/P/N`及已批准模式真值表所需的电源轨；G0不固定数值。 | 接口 | PROJECT REQUIREMENT | `DECISION::DEC-006`, `DECISION::DEC-007`; `SP1::REQ-VOLT-002`, `SP1::REQ-VOLT-003` | 让通用架构适配不同DUT所需的栅极电压。 | 审查接口范围，并使用批准的DUT配置档案验证。 | G1、G2、G11 | 待Master批准（`PROPOSED`） |
| REQ-SYS-INTERFACE-007 | 外部漏极负载接口必须接收DUT专用`VDC/RL`，并明确施加、返回和电流路径；基础PCB不因DUT额定阻断电压而自动承担650 V或3.3 kV。 | 接口 | PROJECT REQUIREMENT | `SP1::REQ-FUNC-001`; `DECISION::DEC-016` | 防止把DUT额定阻断电压错误地当成BTI测试偏压。 | 审查架构和额定值，并在低能量条件下测试漏极回路。 | G1、G2、G10 | 待Master批准（`PROPOSED`） |
| REQ-SYS-INTERFACE-008 | 校准数据接口必须向后处理传递B1505固定`VDS-C`曲线、`Ith`以及DUT、温度和扫描元数据；高速PCB不负责生成该曲线。 | 接口 | PROJECT REQUIREMENT | `SP1::REQ-VOLT-004`, `SP1::REQ-MEAS-008`; ENGINEERING INFERENCE | 明确B1505负责校准曲线，高速PCB只负责快速波形测试。 | 审查数据格式，并从B1505数据到最终结果做端到端回放。 | G1、G12 | 待Master批准（`PROPOSED`） |
| REQ-SYS-INTERFACE-009 | 示波器与探头接口必须允许在同一次事件中测量`VGS`、`VDS`和时序参考，并管理共模、探头负载和时序误差；具体仪器规格后定。 | 接口 | PROJECT REQUIREMENT | `SP1::REQ-MEAS-001`; ENGINEERING INFERENCE | 保证测量点和`tdly`不被仪器共模、负载或时序误差破坏。 | 制定仪器资格确认计划并用实测波形验证。 | G1、G2、G10/G11 | 待Master批准（`PROPOSED`） |
| REQ-SYS-INTERFACE-010 | 0 V预处理路径与Si8273输出必须互斥，不得同时低阻驱动；是否采用独立clamp/switch属于尚未冻结的`PROJECT DESIGN CHOICE`。 | 接口 | PROJECT REQUIREMENT | `RISK::RISK-004`; `DECISION::PROP-001` 未批准 | 冻结“不得争用”的安全功能，同时不提前选择0 V实现拓扑。 | 审查状态转换和FMEA，并在G10做故障测试。 | G1、G2、G10 | 待Master批准（`PROPOSED`） |

### 4.6 DUT兼容需求（5条）

| ID | 系统必须满足的要求 | 类别 | 需求性质 | 来源 | 为什么需要 | 如何验证 | 验证阶段 | 当前状态 |
|---|---|---|---|---|---|---|---|---|
| REQ-SYS-DUT-001 | 平台目标必须覆盖650 V-class和3.3 kV-class SiC MOSFET的低`VDS` BTI/`Vth`迟滞测试。 | DUT兼容 | PROJECT REQUIREMENT | `DECISION::DEC-016`; `LEGACY::REQ-015` | 明确平台必须覆盖两类目标DUT。 | 分别审查两类DUT配置档案并完成实验资格验证。 | G1、G2、G12 | 已确认（`CONFIRMED`） |
| REQ-SYS-DUT-002 | DUT额定阻断电压不得被解释为PCB必须施加650 V或3.3 kV；实际`VDC/VDS-C`由BTI测量条件决定，本项目不是breakdown test。 | DUT兼容 | PROJECT REQUIREMENT | `DECISION::DEC-016`; `MASTER::SP1-REVIEW-v1.0` §5 | 避免形成错误的高压绝缘要求或危险测试。 | 审查需求、额定值和实际测试配置。 | G1、G2、G12 | 已确认（`CONFIRMED`） |
| REQ-SYS-DUT-003 | 栅极驱动架构、`SREF`、正/负BTI序列、测量原理和`VDS→IDS→Vth`链应与DUT额定阻断电压等级解耦。 | DUT兼容 | PROJECT REQUIREMENT | `DECISION::DEC-016`; ENGINEERING INFERENCE | 最大化平台复用，同时把器件差异留在DUT配置档案中。 | 审查系统架构，并比较两类DUT的配置差异。 | G1、G2 | 待Master批准（`PROPOSED`） |
| REQ-SYS-DUT-004 | 每个目标DUT必须建立受控配置档案，至少记录准确料号/封装、`Qg`、`Ciss/Crss`、推荐值和绝对最大`VGS`、`Vth`、`VGM`、`Ith`、`VDS-C`、Kelvin Source、`Rg`、`VDC/RL`、温度和相关时序检查。 | DUT兼容 | PROJECT REQUIREMENT | `LEGACY::REQ-016`; `MASTER::SP1-REVIEW-v1.0` §5 | 把所有不能通用的参数集中到受控DUT配置档案。 | 核对datasheet、计算依据和配置档案完整性。 | G2 | 原则已确认（`CONFIRMED`）；具体数值延期至G2 |
| REQ-SYS-DUT-005 | DUT连接器/转接板和`Rg`配置必须适应封装、Kelvin Source和`Qg`差异，同时不得破坏`REQ-SYS-FUNC-001`或`REQ-SYS-FUNC-002`；具体转接方案和`Rg`策略由G1/G2决定。 | DUT兼容 | PROJECT REQUIREMENT | `LEGACY::OPEN-REQ-006`; ENGINEERING INFERENCE | 明确“不更换基础PCB”和“允许DUT专用适配”之间的边界。 | G1审查转接和`Rg`策略；G2计算驱动要求；G6/G7审查物理实现。 | G1、G2、G6/G7 | 待Master批准（`PROPOSED`）；实现方式延期 |

### 4.7 安全需求（4条）

| ID | 系统必须满足的要求 | 类别 | 需求性质 | 来源 | 为什么需要 | 如何验证 | 验证阶段 | 当前状态 |
|---|---|---|---|---|---|---|---|---|
| REQ-SYS-SAFE-001 | 系统必须定义独立于预处理的`SAFE_OFF`逻辑状态、进入/退出条件以及栅极/漏极目标；具体电路后定。 | 安全 | PROJECT REQUIREMENT | `SP1::REQ-SAFE-001`（非P1内容）；`RISK::RISK-003` | 覆盖上电、故障、待机和连接操作时的安全状态。 | G1审查状态表和FMEA；G10执行故障测试。 | G1、G10 | 安全需求已确认（`CONFIRMED`）；具体定义延期至G1 |
| REQ-SYS-SAFE-002 | 系统必须定义上电、掉电、控制丢失、UVLO和默认状态流程，并防止意外长时间应力。 | 安全 | PROJECT REQUIREMENT | `SP1::REQ-SAFE-002`; `RISK::RISK-002`, `RISK::RISK-003` | 防止默认状态损坏DUT或短接外部电源。 | 审查时序，并在G10进行受控故障注入。 | G1、G2、G10 | 待Master批准（`PROPOSED`）；逻辑由G1决定，动作阈值由G2决定 |
| REQ-SYS-SAFE-003 | 系统必须定义栅极过压、漏极过流、误触发、驱动争用以及能量/自热保护；动作阈值和拓扑由G2决定。 | 安全 | PROJECT REQUIREMENT | `SP1::REQ-SAFE-002`; `RISK::RISK-004`, `RISK::RISK-005`, `RISK::RISK-008` | 论文没有给出原型系统的完整保护边界。 | 完成危险分析、计算和故障测试。 | G1、G2、G10 | 待Master批准（`PROPOSED`） |
| REQ-SYS-SAFE-004 | 所有DUT栅极和漏极条件必须处于该DUT配置档案批准的额定值、能量和温度范围内。 | 安全 | PROJECT REQUIREMENT | `RISK::RISK-005`, `RISK::RISK-008`; ENGINEERING INFERENCE | 防止通用平台被误用到DUT允许范围之外。 | 核对datasheet和计算，并审查实测波形。 | G2、G10、G11 | 待Master批准（`PROPOSED`） |

### 4.8 过程需求（9条）

| ID | 系统必须满足的要求 | 类别 | 需求性质 | 来源 | 为什么需要 | 如何验证 | 验证阶段 | 当前状态 |
|---|---|---|---|---|---|---|---|---|
| REQ-SYS-PROCESS-001 | 所有器件pin、封装、额定值和关键参数必须在原理图冻结前由官方datasheet核对。 | 过程 | PROJECT REQUIREMENT | `LEGACY::REQ-100`; `GOVERNANCE::AGENTS.md` | 禁止根据名称或记忆猜测硬件事实。 | 完成datasheet核对表。 | G2/G3 | 已确认（`CONFIRMED`） |
| REQ-SYS-PROCESS-002 | 关键结论必须标明`PAPER FACT`、`PAPER EXAMPLE VALUE`、`PAPER PERFORMANCE REFERENCE`、`ENGINEERING INFERENCE`、`PROJECT REQUIREMENT`、`PROJECT DESIGN CHOICE`或`OPEN ITEM`，并保留来源。 | 过程 | PROJECT REQUIREMENT | `LEGACY::REQ-101`; `MASTER::SP1-REVIEW-v1.0` | 保持论文证据、工程推断和项目选择分层。 | 在每个阶段审查需求来源和分类。 | 各阶段 | 已确认（`CONFIRMED`） |
| REQ-SYS-PROCESS-003 | 未批准的`OPEN ITEM`不得被默认成数值或实现；SP2/SP3只能在相应阶段或决定批准后展开设计。 | 过程 | PROJECT REQUIREMENT | `GOVERNANCE::AGENTS.md`; `MASTER::SP1-REVIEW-v1.0` §1、§6 | 防止用未经批准的猜测填补需求空白。 | 使用阶段检查表审查。 | G1至G3 | 已确认（`CONFIRMED`） |
| REQ-SYS-PROCESS-004 | ERC必须通过；如有残余warning，必须在布局冻结前逐项记录并批准。 | 过程 | PROJECT REQUIREMENT | `LEGACY::REQ-102` | 保证原理图机器检查问题全部闭环。 | 审查ERC报告和每一条残余warning。 | G3/G8 | 已确认（`CONFIRMED`） |
| REQ-SYS-PROCESS-005 | DRC必须通过；如有残余warning，必须在制造发布前逐项记录并批准。 | 过程 | PROJECT REQUIREMENT | `LEGACY::REQ-103` | 保证PCB规则检查问题全部闭环。 | 审查DRC报告和每一条残余warning。 | G8 | 已确认（`CONFIRMED`） |
| REQ-SYS-PROCESS-006 | 未完成ERC、DRC、人工审查、验证矩阵批准和用户最终批准，不得生成或发布生产Gerber。 | 过程 | PROJECT REQUIREMENT | `DECISION::DEC-010`; `LEGACY::REQ-104` | 防止未经审核的设计进入制造。 | 执行制造暂停检查表。 | G9 | 已确认（`CONFIRMED`） |
| REQ-SYS-PROCESS-007 | 每个面向用户的项目交付文件都必须同步到GitHub正式路径，随后才能报告完成。 | 过程 | PROJECT REQUIREMENT | `DECISION::DEC-011`; `LEGACY::REQ-105` | 保持工程输出可长期追溯。 | 完成GitHub远端文件回读。 | 每次交付 | 已确认（`CONFIRMED`） |
| REQ-SYS-PROCESS-008 | 每个已同步输出都必须登记到`docs/chat_output_index.md`，无需额外复制归档。 | 过程 | PROJECT REQUIREMENT | `DECISION::DEC-012`; `LEGACY::REQ-106` | 建立唯一的输出索引和正式路径。 | 核对索引记录与实际文件路径。 | 每次交付 | 已确认（`CONFIRMED`） |
| REQ-SYS-PROCESS-009 | 不得直接提交受限版权材料、credentials、敏感数据或未批准的大文件；同步失败时必须报告`OUTPUT_SYNC_BLOCKED`及未同步文件。 | 过程 | PROJECT REQUIREMENT | `DECISION::DEC-013`; `LEGACY::REQ-107`, `LEGACY::REQ-108` | 防止同步规则造成版权、安全或仓库体积问题。 | 审查仓库内容和任何`OUTPUT_SYNC_BLOCKED`记录。 | 每次交付 | 已确认（`CONFIRMED`） |

### 4.9 验证需求（5条）

| ID | 系统必须满足的要求 | 类别 | 需求性质 | 来源 | 为什么需要 | 如何验证 | 验证阶段 | 当前状态 |
|---|---|---|---|---|---|---|---|---|
| REQ-SYS-VERIFY-001 | 原型必须按批准的事件定义同时记录时序参考、`VGS`和`VDS`，并提取完整系统`tdly`；不得用单独`VOA`边沿代替。 | 验证 | PROJECT REQUIREMENT | `SP1::REQ-VERIFY-001`; `DECISION::DEC-009` | 直接证明核心完整系统时序目标。 | 用示波器同步采集时序参考、`VGS`和`VDS`。 | G11 | 已确认（`CONFIRMED`）；算法延期至G10/G11 |
| REQ-SYS-VERIFY-002 | 原型和方法验证必须报告MI/MP/MN相对`VDS-C`的偏差及通过判定。 | 验证 | PROJECT REQUIREMENT | `SP1::REQ-VERIFY-002` | 证明高速测量点与B1505校准偏压兼容。 | 自动比较MI、MP、MN与`VDS-C`。 | G12 | 已确认（`CONFIRMED`）；容差延期至G12 |
| REQ-SYS-VERIFY-003 | 原型和方法验证必须报告`IDM-P/N`相对`IDM-I`的偏差公式、结果、调节后的`VGM-P/N`及通过判定。 | 验证 | PROJECT REQUIREMENT | `SP1::REQ-VERIFY-003` | 控制测量电流不匹配造成的误差。 | 生成电流一致性报告。 | G12 | 已确认（`CONFIRMED`）；容差延期至G12 |
| REQ-SYS-VERIFY-004 | 发布的数据集必须能够独立重算原始波形→`IDS`→B1505映射→原始位移→修正后`ΔVth`的完整链。 | 验证 | PROJECT REQUIREMENT | `SP1::REQ-VERIFY-004` | 证明最终结果能够从原始数据独立重算。 | 用独立软件回放完整数据链。 | G12 | 已确认（`CONFIRMED`）；软件数值容差延期至G12 |
| REQ-SYS-VERIFY-005 | 平台通用性声明必须分别用至少一个已批准650 V-class配置档案和一个3.3 kV-class配置档案完成资格验证；不要求施加额定阻断电压。 | 验证 | PROJECT REQUIREMENT | `DECISION::DEC-016`; ENGINEERING INFERENCE | 防止只凭架构推测就宣称平台兼容两类DUT。 | 分别审查两类配置档案，并完成低`VDS`功能和方法验证。 | G2、G11、G12 | 待Master批准（`PROPOSED`） |

## 5. 哪些问题允许延期

延期的含义是“现在不猜数值或实现，但必须在指定阶段前作出决定”。每个开放项仍有负责人、最迟决定时间和验证方法。

### 5.1 按阶段分组

| 必须决定的阶段 | 对应问题 |
|---|---|
| G0必须批准 | `OPEN::OI-000` |
| G1必须决定 | `OPEN::OI-012`至`OPEN::OI-017`：安全状态、电源时序、保护职责、兼容架构、DUT转接和`Rg`配置策略。 |
| G2必须决定 | `OPEN::OI-011`、`OPEN::OI-018`、`OPEN::OI-019`：自热上限、仪器要求和DUT专用参数。 |
| G6/G7必须决定 | `OPEN::OI-020`：探测焊盘、连接器机械条件、Kelvin走线和物理隔离。 |
| G10/G11原型验证前必须决定 | `OPEN::OI-001`、`OPEN::OI-002`、`OPEN::OI-006`至`OPEN::OI-010`：`tdly`定义、约100 ns通过规则、采集窗口、极值、滤波、振铃和deskew。 |
| G12完整实验前必须决定 | `OPEN::OI-003`至`OPEN::OI-005`、`OPEN::OI-021`、`OPEN::OI-022`：`VDS/IDM`容差、`tpre`、软件规则和是否扩展到Fig. 10。 |

只有`OPEN::OI-000`必须由G0 Master批准。其余22项允许延期，但都必须在表中规定的阶段前关闭。

### 5.2 完整开放项表

| OI ID | 尚未决定的问题 | 负责人/阶段 | 最迟决定时间 | 为什么可以延期 | 如何验证 |
|---|---|---|---|---|---|
| OI-000 | 是否批准本文件的规范需求层级、历史映射和新增项目需求 | **G0必须决定（`MUST_FREEZE_G0`）/ Master** | G0最终批准时 | 它决定项目正式需求的唯一基线；这是唯一仍需G0 Master处理的事项。 | Master审查本版差异；批准后再更新`requirements.md`。 |
| OI-001 | `tdly`的精确起点、交越点和终点定义 | **延期至G10/G11（`DEFER_TO_G10_G11`）/ SP6测量负责人** | G11测试计划冻结前 | G1只需保证控制、`VGS`和`VDS`可同时观察；精确算法必须根据真实波形确定。 | 同步采集时序参考、`VGS`和`VDS`，再回放候选算法。 |
| OI-002 | 约100 ns最终采用`<100 ns`、`≤100 ns`、区间还是统计判据 | **延期至G10/G11（`DEFER_TO_G10_G11`）/ Master与SP6** | G11验收规则冻结前 | 完整系统目标已经确定；最终通过判据还需要重复性和噪声证据。 | 重复测量`tdly`，报告分布和不确定度。 |
| OI-003 | `VDS≈VDS-C`的允许容差 | **延期至G12（`DEFER_TO_G12`）/ SP7方法负责人** | 首次G12数据集验收前 | 它不改变G1架构；容差需结合校准曲线灵敏度和DUT配置确定。 | 做灵敏度分析，并比较实测点与`VDS-C`。 |
| OI-004 | `IDM-P/N≈IDM-I`的百分比公式和允许容差 | **延期至G12（`DEFER_TO_G12`）/ SP7** | 首次G12方法资格确认前 | 论文的±20%不能直接成为项目判据；该数值不影响G1接口。 | 明确分母和符号约定，完成误差与灵敏度分析。 |
| OI-005 | `tpre`最小值和预处理完成判据 | **延期至G12（`DEFER_TO_G12`）/ SP7** | 正式BTI流程发布前 | 论文没有给出可直接采用的数值；必须用目标DUT验证历史效应是否消除。 | 扫描`tpre`，检查MI或`Vth-IS`的稳定性和重复性。 |
| OI-006 | `tmea`长度、退出条件和恢复观察窗口 | **延期至G10/G11（`DEFER_TO_G10_G11`）/ SP6** | G11采集计划冻结前 | G1只需保证窗口可配置、波形可采集；具体长度取决于真实波形和示波器存储能力。 | 改变采集窗口，确认测量点和恢复波形均未被截断。 |
| OI-007 | MI/MP/MN极值提取算法和搜索窗口 | **延期至G10/G11（`DEFER_TO_G10_G11`）/ SP6与SP7** | G11算法冻结前 | 真实振铃和噪声尚未知；现在只需保留原始信号。 | 用已标注波形集回放算法并做单元测试。 |
| OI-008 | 波形处理中的滤波、平均和插值规则 | **延期至G10/G11（`DEFER_TO_G10_G11`）/ SP6与SP7** | G11算法冻结前 | 现在规定数值会变成对仪器噪声的猜测。 | 比较原始和处理后波形，检查相位与幅值偏差。 |
| OI-009 | 振铃处理和多个局部极值的选择规则 | **延期至G10/G11（`DEFER_TO_G10_G11`）/ SP6与SP7** | G11算法冻结前 | 规则必须基于原型实测波形；G1/G2仍应尽量降低振铃。 | 对合成及实测振铃波形运行算法，并进行人工交叉核对。 |
| OI-010 | 通道时间校正、电缆延迟和去嵌入规则 | **延期至G10/G11（`DEFER_TO_G10_G11`）/ SP6** | G11仪器资格确认前 | G1只需提供共同时间关系；校正量取决于最终探头和电缆。 | 使用校准夹具或已知边沿验证通道时间校正。 |
| OI-011 | 自热以及正应力电流/能量上限 | **延期至G2（`DEFER_TO_G2`）/ SP3与DUT负责人** | G2电气范围冻结前 | 上限需要DUT热数据和电气数据；G0已经要求必须设置限制。 | 计算`IDS`、脉冲能量、占空比和温升，并在G10/G11实测验证。 |
| OI-012 | `SAFE_OFF`的栅极/漏极目标和进入/退出逻辑 | **延期至G1（`DEFER_TO_G1`）/ G1架构负责人** | G1状态/接口冻结前 | 架构必须先定义故障状态，但G0不必选择具体器件或拓扑。 | 审查状态表和FMEA；G10执行故障测试。 |
| OI-013 | 上电、掉电、控制丢失、UVLO和默认状态流程 | **延期至G1（`DEFER_TO_G1`）/ G1架构负责人** | G1控制/电源接口冻结前 | G1必须先分配模块职责；阈值和器件可在G2确定。 | 审查时序图和FMEA；G10分阶段上电验证。 |
| OI-014 | 保护功能、0 V预处理争用/互锁及能量限制的职责分配 | **延期至G1（`DEFER_TO_G1`）/ G1架构负责人** | G1安全接口冻结前 | G1必须说明由谁检测和切断；动作值与拓扑不必在G0决定。 | 审查危险分析和接口分配；G2计算，G10做故障测试。 |
| OI-015 | 650 V/3.3 kV兼容架构和配置边界 | **延期至G1（`DEFER_TO_G1`）/ G1架构负责人** | G1方框图/ICD冻结前 | 低`VDS`和基础架构解耦原则已定；模块边界仍需在方框图中明确。 | 用两类DUT配置逐项演练接口和职责。 |
| OI-016 | DUT连接器和转接板策略 | **延期至G1（`DEFER_TO_G1`）/ G1接口负责人** | G1 DUT接口冻结前 | 它不改变测试方法，但会影响后续封装适配和回流路径。 | 审查接口控制文件和转接矩阵；G6/G7检查物理实现。 |
| OI-017 | 是否以及如何允许DUT专用`Rg`更换或选择 | **延期至G1（`DEFER_TO_G1`）/ G1接口负责人** | G1配置策略冻结前；数值在G2决定 | G1必须明确它属于DUT配置，不得把它作为同一DUT正/负模式切换的一部分；具体阻值依赖`Qg`。 | 审查配置规则；G2计算驱动要求；G11检查波形。 |
| OI-018 | 仪器准确型号、最小带宽、采样率、共模和负载要求 | **延期至G2（`DEFER_TO_G2`）/ 测量负责人** | G2仪器需求冻结前 | 规格应从约100 ns目标和预估边沿、振铃反推；不妨碍G1定义信号接口。 | 建立带宽与误差预算；G10/G11完成仪器资格确认。 |
| OI-019 | 准确DUT、封装、`Qg/Ciss/Crss`、`VGS/VGM`、`Ith`、`VDS-C`、`VDC/RL`和温度 | **延期至G2（`DEFER_TO_G2`）/ DUT、SP2与SP3负责人** | 对应DUT配置档案在G2冻结前 | 这些都是DUT专用参数；G0只冻结参数类别，不猜具体数值。 | 核对datasheet并完成必要计算；按需进行LTspice或台架验证。 |
| OI-020 | 探测焊盘、连接器机械条件、Kelvin走线和物理隔离 | **延期至G6/G7（`DEFER_TO_G6_G7`）/ PCB负责人** | 器件放置和布线冻结前 | G1先定义逻辑网络；物理实现依赖封装和层叠。 | 审查器件放置、布线、连通性和寄生影响。 |
| OI-021 | B1505曲线插值、软件数值容差和文件格式 | **延期至G12（`DEFER_TO_G12`）/ SP7** | G12软件发布前 | 公式链已经确定；软件实现细节不影响G1硬件架构。 | 使用单元测试、标准向量和独立回放验证。 |
| OI-022 | 是否激活多脉冲/Fig. 10复现范围 | **延期至G12（`DEFER_TO_G12`）/ Master** | G12复现范围冻结前 | 最小Fig. 3复现不需要该扩展；硬件只在已批准接口能力内评估。 | 由Master作范围决定；激活后再验证相应实验流程。 |

## 6. 650 V/3.3 kV兼容边界

本项目是低`VDS` BTI测试，不是breakdown test。DUT额定阻断电压不等于PCB工作电压。通用性通过“基础架构 + DUT配置档案 + 转接/配置”实现。

| 应保持通用的系统部分 | 必须按DUT单独确定的部分 |
|---|---|
| `VGS`控制概念 | `Qg`、`Ciss`、`Crss` |
| `SREF=DUT Kelvin Source` | 推荐值和绝对最大`VGS` |
| 正/负BTI测试序列 | `Vth`、`VGM-I/P/N`、`Ith` |
| 0 V预处理功能 | `VDS-C`、`VDC`、`RL` |
| `VOA`应力→测量职责 | 准确封装和pinout |
| `VDS→IDS→Vth→ΔVth`提取链 | Kelvin Source是否存在及转接方式 |
| B1505与高速PCB职责边界 | `Rg`、驱动电流和去耦范围 |
| 完整系统`tdly`概念和数据追溯 | 实际波形对应的仪器共模、带宽和探头负载要求 |

## 7. G0关闭条件

1. v1.2目前只是Master候选基线，不是已冻结需求。
2. Master必须先批准`OPEN::OI-000`。
3. 批准后才可把65条`REQ-SYS-*`安装进`docs/requirements.md`。
4. `docs/verification_matrix.md`随后必须按65条需求重建。
5. 必须更新相关状态文件和输出索引，并完成GitHub远端回读。
6. 必须再次检查需求数量、ID唯一性、正向/反向追溯和OPEN项完整性。
7. 以上安装与检查全部通过后，Master才能宣布G0 `PASS/FROZEN`。

当前状态保持：G0=`ACTIVE`；G1可以继续；G3=`BLOCKED`。

## 附录A：逐项来源到规范需求映射

本附录用于机器检查和历史追溯。正文审批时不需要逐行阅读。每个SP1或旧项目ID只出现一次，所有目标ID都必须真实存在。

| 来源命名空间 | 来源ID | 来源内容摘要 | 对应canonical ID | 映射类型 | 处置说明 |
|---|---|---|---|---|---|
| SP1 | REQ-FUNC-001 | Fig. 3电阻负载回路 | REQ-SYS-FUNC-004; REQ-SYS-INTERFACE-007 | 1:N（一对多） | 拆分到多个项目级需求，分别约束不同职责。 |
| SP1 | REQ-FUNC-002 | 校准、正应力和负应力三条序列 | REQ-SYS-FUNC-003 | 1:1（一对一） | 技术含义保持不变。 |
| SP1 | REQ-FUNC-003 | 测量时DUT不完全导通 | REQ-SYS-FUNC-005 | 1:1（一对一） | 技术含义保持不变。 |
| SP1 | REQ-FUNC-004 | 捕获MI/MP/MN及正/负应力后的恢复 | REQ-SYS-FUNC-006 | 1:1（一对一） | 技术含义保持不变。 |
| SP1 | REQ-FUNC-005 | 校准后固定`VDC/RL`，只调`VGM-P/N` | REQ-SYS-METHOD-006 | 1:1（一对一） | 技术含义保持不变。 |
| SP1 | REQ-VOLT-001 | 0 V预处理目标 | REQ-SYS-METHOD-001 | 1:1（一对一） | 技术含义保持不变。 |
| SP1 | REQ-VOLT-002 | 独立的正/负应力栅极目标 | REQ-SYS-FUNC-008; REQ-SYS-INTERFACE-006 | 1:N（一对多） | 拆分到多个项目级需求，分别约束不同职责。 |
| SP1 | REQ-VOLT-003 | 支持`VGM-I/P/N`并可分别调节 | REQ-SYS-METHOD-002; REQ-SYS-INTERFACE-006 | 1:N（一对多） | 拆分到多个项目级需求，分别约束不同职责。 |
| SP1 | REQ-VOLT-004 | B1505固定`VDS-C`校准曲线 | REQ-SYS-METHOD-003; REQ-SYS-INTERFACE-008 | 1:N（一对多） | 拆分到多个项目级需求，分别约束不同职责。 |
| SP1 | REQ-VOLT-005 | MI/MP/MN的`VDS`与`VDS-C`对齐 | REQ-SYS-METHOD-004; REQ-SYS-VERIFY-002 | 1:N（一对多） | 拆分到多个项目级需求，分别约束不同职责。 |
| SP1 | REQ-VOLT-006 | 测量工作点的饱和区条件 | REQ-SYS-METHOD-005 | 1:1（一对一） | 技术含义保持不变。 |
| SP1 | REQ-TIME-001 | 应力→测量快速切换 | REQ-SYS-TIME-001 | 1:1（一对一） | 技术含义保持不变。 |
| SP1 | REQ-TIME-002 | 论文报告的约100 ns性能参考 | REQ-SYS-TIME-002 | 1:1（一对一） | 技术含义保持不变。 |
| SP1 | REQ-TIME-003 | 可配置的长时间`tpre` | REQ-SYS-TIME-003 | 1:1（一对一） | 技术含义保持不变。 |
| SP1 | REQ-TIME-004 | 可编程`tstr` | REQ-SYS-TIME-004 | 1:1（一对一） | 技术含义保持不变。 |
| SP1 | REQ-TIME-005 | `tmea`覆盖测量点与恢复 | REQ-SYS-TIME-005 | 1:1（一对一） | 技术含义保持不变。 |
| SP1 | REQ-TIME-006 | 可变测试延迟 | REQ-SYS-TIME-006 | 1:1（一对一） | 技术含义保持不变。 |
| SP1 | REQ-MEAS-001 | 同次事件记录`VGS/VDS`并定义时间关系 | REQ-SYS-MEAS-001; REQ-SYS-INTERFACE-009 | 1:N（一对多） | 拆分到多个项目级需求，分别约束不同职责。 |
| SP1 | REQ-MEAS-002 | 用`IDS=(VDC-VDS)/RL`计算电流 | REQ-SYS-MEAS-004 | 1:1（一对一） | 技术含义保持不变。 |
| SP1 | REQ-MEAS-003 | 由MI/MP/MN得到`IDM-I/P/N` | REQ-SYS-MEAS-005 | 1:1（一对一） | 技术含义保持不变。 |
| SP1 | REQ-MEAS-004 | 所有电流映射到同一B1505曲线 | REQ-SYS-MEAS-006 | 1:1（一对一） | 技术含义保持不变。 |
| SP1 | REQ-MEAS-005 | 计算原始`Vth`位移 | REQ-SYS-MEAS-007 | MERGED（合并） | 与相关旧需求合并，原技术含义仍保留。 |
| SP1 | REQ-MEAS-006 | 减去`Vth-IS`得到修正`ΔVth` | REQ-SYS-MEAS-007 | MERGED（合并） | 与相关旧需求合并，原技术含义仍保留。 |
| SP1 | REQ-MEAS-007 | `IDM-P/N`与`IDM-I`匹配 | REQ-SYS-METHOD-007; REQ-SYS-VERIFY-003 | 1:N（一对多） | 拆分到多个项目级需求，分别约束不同职责。 |
| SP1 | REQ-MEAS-008 | 用`Ith`交点定义初始`Vth` | REQ-SYS-METHOD-003; REQ-SYS-INTERFACE-008 | 1:N（一对多） | 拆分到多个项目级需求，分别约束不同职责。 |
| SP1 | REQ-MEAS-009 | 验证平行位移方法是否适用 | REQ-SYS-MEAS-008 | 1:1（一对一） | 技术含义保持不变。 |
| SP1 | REQ-MEAS-010 | 减小正应力电流和自热影响 | REQ-SYS-METHOD-008 | 1:1（一对一） | 技术含义保持不变。 |
| SP1 | REQ-CTRL-001 | 状态顺序和可重复触发 | REQ-SYS-FUNC-003; REQ-SYS-INTERFACE-005 | SPLIT（拆分） | 拆分为职责更清楚的多个项目级需求。 |
| SP1 | REQ-CTRL-002 | 校准与应力测试的调参边界 | REQ-SYS-METHOD-006 | MERGED（合并） | 与相关旧需求合并，原技术含义仍保留。 |
| SP1 | REQ-CTRL-003 | 可选的多脉冲应力 | REQ-SYS-METHOD-009 | 1:1（一对一） | 技术含义保持不变。 |
| SP1 | REQ-SAFE-001 | 独立`SAFE_OFF`状态 | REQ-SYS-SAFE-001 | 1:1（一对一） | 技术含义保持不变。 |
| SP1 | REQ-SAFE-002 | 电源时序和保护 | REQ-SYS-SAFE-002; REQ-SYS-SAFE-003 | SPLIT（拆分） | 拆分为职责更清楚的多个项目级需求。 |
| SP1 | REQ-VERIFY-001 | 完整系统`tdly`验证 | REQ-SYS-VERIFY-001 | 1:1（一对一） | 技术含义保持不变。 |
| SP1 | REQ-VERIFY-002 | `VDS`对齐报告 | REQ-SYS-VERIFY-002 | 1:1（一对一） | 技术含义保持不变。 |
| SP1 | REQ-VERIFY-003 | `IDM`匹配报告 | REQ-SYS-VERIFY-003 | 1:1（一对一） | 技术含义保持不变。 |
| SP1 | REQ-VERIFY-004 | 原始数据到`ΔVth`的追溯链 | REQ-SYS-VERIFY-004; REQ-SYS-MEAS-009 | 1:N（一对多） | 拆分到多个项目级需求，分别约束不同职责。 |
| LEGACY | REQ-001 | 同一PCB支持正/负BTI | REQ-SYS-FUNC-001 | 1:1（一对一） | 技术含义保持不变。 |
| LEGACY | REQ-002 | 正/负模式只通过外部电源轨和控制改变 | REQ-SYS-FUNC-002 | 1:1（一对一） | 技术含义保持不变。 |
| LEGACY | REQ-003 | `SREF`是DUT Kelvin Source | REQ-SYS-INTERFACE-001 | 1:1（一对一） | 技术含义保持不变。 |
| LEGACY | REQ-004 | `SREF`不默认等于earth | REQ-SYS-INTERFACE-002 | 1:1（一对一） | 技术含义保持不变。 |
| LEGACY | REQ-005 | Si8273 `VOA`完成快速转换 | REQ-SYS-FUNC-007 | 1:1（一对一） | 技术含义保持不变。 |
| LEGACY | REQ-006 | 正BTI电源轨和真值表 | REQ-SYS-FUNC-008 | MERGED（合并） | 与相关旧需求合并，原技术含义仍保留。 |
| LEGACY | REQ-007 | 负BTI电源轨和真值表 | REQ-SYS-FUNC-008 | MERGED（合并） | 与相关旧需求合并，原技术含义仍保留。 |
| LEGACY | REQ-008 | 完整序列包括0 V预处理、应力和测量 | REQ-SYS-FUNC-003; REQ-SYS-METHOD-001 | SPLIT（拆分） | 拆分为职责更清楚的多个项目级需求。 |
| LEGACY | REQ-009 | 用于MI/MP/MN的校准、正应力和负应力序列 | REQ-SYS-FUNC-003; REQ-SYS-FUNC-006 | SPLIT（拆分） | 拆分为职责更清楚的多个项目级需求。 |
| LEGACY | REQ-010 | 约100 ns完整系统延迟目标 | REQ-SYS-TIME-002; REQ-SYS-VERIFY-001 | SPLIT（拆分） | 拆分为职责更清楚的多个项目级需求。 |
| LEGACY | REQ-011 | 相对Kelvin Source测量`VGS` | REQ-SYS-MEAS-002 | 1:1（一对一） | 技术含义保持不变。 |
| LEGACY | REQ-012 | Fig. 3电阻负载漏极回路 | REQ-SYS-FUNC-004 | MERGED（合并） | 与相关旧需求合并，原技术含义仍保留。 |
| LEGACY | REQ-013 | 条件允许时分开Power Source与Kelvin Source | REQ-SYS-INTERFACE-004 | 1:1（一对一） | 技术含义保持不变。 |
| LEGACY | REQ-014 | 提供`VGS/VDS`及时序观察点 | REQ-SYS-MEAS-003; REQ-SYS-INTERFACE-009 | SPLIT（拆分） | 拆分为职责更清楚的多个项目级需求。 |
| LEGACY | REQ-015 | 650 V/3.3 kV低`VDS` BTI范围 | REQ-SYS-DUT-001; REQ-SYS-DUT-002 | SPLIT（拆分） | 拆分为职责更清楚的多个项目级需求。 |
| LEGACY | REQ-016 | DUT专用电气参数和接口参数 | REQ-SYS-DUT-003; REQ-SYS-DUT-004; REQ-SYS-DUT-005 | SPLIT（拆分） | 拆分为职责更清楚的多个项目级需求。 |
| LEGACY | REQ-100 | datasheet核对 | REQ-SYS-PROCESS-001 | 1:1（一对一） | 技术含义保持不变。 |
| LEGACY | REQ-101 | 标注关键设计依据 | REQ-SYS-PROCESS-002 | 1:1（一对一） | 技术含义保持不变。 |
| LEGACY | REQ-102 | ERC闭环 | REQ-SYS-PROCESS-004 | 1:1（一对一） | 技术含义保持不变。 |
| LEGACY | REQ-103 | DRC闭环 | REQ-SYS-PROCESS-005 | 1:1（一对一） | 技术含义保持不变。 |
| LEGACY | REQ-104 | 制造暂停条件 | REQ-SYS-PROCESS-006 | 1:1（一对一） | 技术含义保持不变。 |
| LEGACY | REQ-105 | 同步项目输出 | REQ-SYS-PROCESS-007 | 1:1（一对一） | 技术含义保持不变。 |
| LEGACY | REQ-106 | 正式路径和输出索引 | REQ-SYS-PROCESS-008 | 1:1（一对一） | 技术含义保持不变。 |
| LEGACY | REQ-107 | 禁止提交受限制内容 | REQ-SYS-PROCESS-009 | MERGED（合并） | 与相关旧需求合并，原技术含义仍保留。 |
| LEGACY | REQ-108 | 报告`OUTPUT_SYNC_BLOCKED` | REQ-SYS-PROCESS-009 | MERGED（合并） | 与相关旧需求合并，原技术含义仍保留。 |
| LEGACY | OPEN-REQ-001 | 准确DUT型号和封装 | REQ-SYS-DUT-004 | DEFERRED-TO-OI（延期至开放项） | 技术要求保留，具体决定延期至`OPEN::OI-019`。 |
| LEGACY | OPEN-REQ-002 | 最终栅极电压范围 | REQ-SYS-METHOD-002; REQ-SYS-INTERFACE-006; REQ-SYS-DUT-004 | DEFERRED-TO-OI（延期至开放项） | 技术要求保留，具体决定延期至`OPEN::OI-019`。 |
| LEGACY | OPEN-REQ-003 | 准确`VDS-C/Ith/VDC/RL` | REQ-SYS-METHOD-003; REQ-SYS-METHOD-004; REQ-SYS-METHOD-006; REQ-SYS-DUT-004 | DEFERRED-TO-OI（延期至开放项） | 技术要求保留，具体决定延期至`OPEN::OI-019`、`OPEN::OI-003`。 |
| LEGACY | OPEN-REQ-004 | 0 V预处理的准确实现 | REQ-SYS-METHOD-001; REQ-SYS-INTERFACE-010 | DEFERRED-TO-OI（延期至开放项） | 技术要求保留，具体决定延期至`OPEN::OI-014`。 |
| LEGACY | OPEN-REQ-005 | 仪器型号和带宽 | REQ-SYS-INTERFACE-009 | DEFERRED-TO-OI（延期至开放项） | 技术要求保留，具体决定延期至`OPEN::OI-018`。 |
| LEGACY | OPEN-REQ-006 | 650 V/3.3 kV转接板和`Rg`策略 | REQ-SYS-DUT-003; REQ-SYS-DUT-005 | DEFERRED-TO-OI（延期至开放项） | 技术要求保留，具体决定延期至`OPEN::OI-015`。 |
| LEGACY | OPEN-REQ-007 | 准确`tdly`通过算法 | REQ-SYS-TIME-002; REQ-SYS-MEAS-001; REQ-SYS-MEAS-005; REQ-SYS-VERIFY-001 | DEFERRED-TO-OI（延期至开放项） | 技术要求保留，具体决定延期至`OPEN::OI-001`。 |
| LEGACY | OPEN-REQ-008 | 合并SP1与项目需求 | REQ-SYS-PROCESS-002; REQ-SYS-PROCESS-003 | RESOLVED-BY-MERGE（通过合并解决） | v1.2已完成技术合并；正式生效仍等待`OPEN::OI-000`批准。 |

## 附录B：自动检查结果

| 检查项目 | 要求 | v1.2结果 |
|---|---|---|
| 规范需求总数 | 65 | PASS — 65 |
| 分类数量 | 8/9/6/9/10/5/4/9/5 | PASS — 8/9/6/9/10/5/4/9/5 |
| 规范需求唯一数量 | 65 | PASS — 65 |
| 规范需求重复数量 | 0 | PASS — 0 |
| 规范需求与SP1同名冲突 | 0 | PASS — 0 |
| 规范需求与旧项目ID同名冲突 | 0 | PASS — 0 |
| 映射表来源行数 | 69 | PASS — 69，来源ID重复0 |
| SP1覆盖 | 36/36 | PASS — 36/36 |
| 旧项目REQ覆盖 | 25/25 | PASS — 25/25 |
| 旧OPEN覆盖 | 8/8 | PASS — 8/8 |
| 正向缺失目标 | 0 | PASS — 0 |
| 反向缺失关系 | 0 | PASS — 0 |
| 模糊或未限定来源 | 0 | PASS — 0；每条需求均有带命名空间的来源 |
| 需求空字段 | 0 | PASS — 0 |
| OI数量/重复 | 23/0 | PASS — 23/0 |
| OI负责人、截止时间、延期理由或验证方法缺失 | 0 | PASS — 0 |
| `MUST_FREEZE_G0`数量 | 1，仅`OI-000` | PASS — 1，仅`OI-000` |
| 完整英文说明句 | 0 | PASS — 0；英文仅用于必要名称、变量和固定治理标签 |
| 新增设计值、拓扑、原理图或布局 | 0 | PASS — 0；保留的0 V、约100 ns、650 V/3.3 kV及论文数值均按原分类呈现 |

### B.1 Final Gate Review

| Gate | 结果 | 证据 |
|---|---|---|
| A. 中文项目摘要清楚 | PASS | 第1章直接回答项目目标、职责边界、已定/未定事项和下一步。 |
| B. 非PCB背景用户能够理解文件用途 | PASS | 第1章使用通俗摘要，第2章解释编号、来源、验证和状态。 |
| C. 正文以中文为主 | PASS | 标题、说明、需求、理由、验证和状态均以中文表达。 |
| D. 逐项映射表已移至附录 | PASS | 69行映射只在附录A出现。 |
| E. 65条规范需求数量正确 | PASS | 自动检查为65，分类数量符合要求。 |
| F. 规范需求ID唯一且全仓库零冲突 | PASS | 唯一65、重复0；与SP1和旧项目ID冲突均为0。 |
| G. 69个来源ID逐项映射完整 | PASS | SP1 36/36、旧项目REQ 25/25、旧OPEN 8/8。 |
| H. 正向追溯完整 | PASS | 来源ID重复0，缺失来源0，缺失目标0。 |
| I. 反向追溯完整 | PASS | 每个需求来源字段中的`SP1::*`和`LEGACY::*`均有对应映射，缺失关系0。 |
| J. 不存在模糊或未限定来源 | PASS | `Section 7`、`boundary`、`approved SP1`等模糊来源均为0。 |
| K. 3条接口需求来源已修正 | PASS | `REQ-SYS-INTERFACE-007/008/009`均使用明确来源，对应映射同步更新。 |
| L. `REQ-SYS-SAFE-004`来源已修正 | PASS | 来源改为`RISK::RISK-005`、`RISK::RISK-008`和ENGINEERING INFERENCE；不再引用`LEGACY::REQ-100`。 |
| M. 23个OPEN项完整 | PASS | 数量23、重复0、必填字段缺失0。 |
| N. 只有`OI-000`等待G0 Master批准 | PASS | `MUST_FREEZE_G0`数量为1，仅`OI-000`。 |
| O. 约100 ns和650 V/3.3 kV边界未改变 | PASS | 约100 ns仍是完整系统目标；650 V/3.3 kV仍只表示低`VDS` DUT兼容范围。 |
| P. 未增加技术需求或设计假设 | PASS | v1.1→v1.2只做中文重构和指定追溯修正。 |
| Q. 未进入G1/G2具体电路设计 | PASS | 未新增器件值、拓扑、连接器引脚、原理图、布局、BOM或仿真结果。 |
| R. 未修改禁止修改的项目文件 | PASS | 提交后逐项比较GitHub blob SHA，均与本轮开始时一致。 |
| S. GitHub文件和索引已同步并远端回读 | PASS | v1.2与本地定稿逐字一致；索引条目和技术状态已回读确认。 |

# G0 STATUS: READY FOR MASTER REVIEW

> `G0-CRB-v1.2`只是具备Master审核条件；`OI-000`尚未批准，requirements尚未`FROZEN`，G0仍为`ACTIVE`。

HANDOFF_PACKET

- 子项目：G0中文可读性与追溯修正
- 版本：G0-CRB-v1.2
- 输入文件：15个必需文件已完整读取，缺失0
- 中文可读性修正：中文摘要、阅读说明、核心要求、中文需求表、按阶段开放项、crosswalk移至附录
- 追溯修正：3条Interface来源、`REQ-SYS-SAFE-004`来源及对应crosswalk目标
- 需求数量：65；分类8/9/6/9/10/5/4/9/5；ID重复0；与SP1/旧项目ID冲突0
- 映射覆盖：69行；SP1 36/36；旧项目REQ 25/25；旧OPEN 8/8；正向缺失目标0；反向缺失关系0
- OPEN状态：23项；重复0；必填字段缺失0；仅`OI-000`为`MUST_FREEZE_G0`
- 创建文件：`docs/G0_closing_requirements_baseline_v1.2.md`
- 更新文件：`docs/chat_output_index.md`
- 明确不修改文件：`docs/requirements.md`、`docs/verification_matrix.md`、`docs/decisions.md`、`docs/interfaces.md`、`docs/risk_register.md`、`docs/project_status.md`、`docs/stage_gate.md`、所有已批准SP1文件、v1.0、v1.1
- 电气行为变更：无
- 新增技术需求：无
- 新增设计假设：无
- ERC/DRC：未涉及
- Gate结果：`READY FOR MASTER REVIEW`；G0仍为`ACTIVE`；G1可以继续；G3仍为`BLOCKED`
- 待Master批准：仅`OPEN::OI-000`

END_HANDOFF_PACKET
