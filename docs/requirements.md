# 项目规范需求基线

- 文件状态：**FROZEN — Master approved G0 canonical requirement baseline**
- 生效日期：2026-08-25
- 规范批准来源：[G0-CRB-v1.2](G0_closing_requirements_baseline_v1.2.md)
- Master批准记录：[G0 Master Review v1.0](G0_master_review_v1.0.md)
- 唯一项目级规范需求：本文件中的65条`REQ-SYS-*`
- 需求基线状态：`FROZEN`
- G0阶段门状态：`PASS`
- 后续阶段：G1=`ACTIVE`；G3=`BLOCKED`

## 1. 基线说明

本文件正式安装Master批准的`G0-CRB-v1.2`。冻结对象是65条需求的ID、技术含义、分类、证据层级、验证概念、验证阶段、状态标签，以及SP1/legacy逐项映射和`OPEN::OI-001...022`的延期责任。

“需求基线已冻结”不等于具体验收数值已经确定。凡标有验收延期、条件未激活或后续Gate决定的条目，仍必须按批准的OPEN项关闭；不得自行补入DUT参数、电压、电流、`Rg`、电容、时序算法、容差或实现拓扑。

`PROPOSED`、`ACCEPTANCE DEFERRED`和`CONDITIONAL-INACTIVE`是v1.2获批时的需求状态标签，按Master指令原样保留。它们不影响该条需求作为冻结基线的一部分，但明确限制后续实现或验收不得越过对应OPEN项。

## 2. 冻结边界

本次冻结：

1. 65条`REQ-SYS-*`的ID、需求含义、分类和证据层级；
2. 650 V等级和3.3 kV等级DUT的低`VDS` BTI范围；
3. 约100 ns作为完整系统`tdly`设计/验证目标的性质；
4. B1505、高速PCB和外部仪器的职责边界；
5. `OPEN::OI-001...022`的owner、deadline、延期理由和验证方法；
6. canonical hierarchy及69行SP1/legacy crosswalk。

本次不冻结：

- DUT具体型号和`VGS/VGM/VDS-C/Ith/VDC/RL`数值；
- `Rg`、去耦或其他器件数值；
- 0 V预处理、`SAFE_OFF`或保护的具体拓扑与动作值；
- connector pinout、`tdly`精确算法、`VDS/IDM`数值容差；
- 原理图、PCB布局、BOM或生产文件。

## 3. 规范需求

下表的需求陈述、需求性质、来源和状态均由`G0-CRB-v1.2`原样安装。

### 3.1 功能需求（8条）

| ID | 规范需求 | 类别 | 需求性质 | 来源 | 当前状态 |
|---|---|---|---|---|---|
| REQ-SYS-FUNC-001 | 同一块已装配的基础PCB必须同时支持正BTI和负BTI。 | 功能 | PROJECT REQUIREMENT | `DECISION::DEC-001`; `LEGACY::REQ-001` | 已确认（`CONFIRMED`） |
| REQ-SYS-FUNC-002 | 对同一个DUT和同一份已批准DUT配置档案，P/N模式切换只能改变外部`VDDA/GNDA`和控制波形；不得重新焊接或更换基础PCB元件、DUT转接板或`Rg`。只有更换DUT或更换已批准配置档案时，才可改变DUT专用配置。 | 功能 | PROJECT REQUIREMENT | `DECISION::DEC-001`, `DECISION::DEC-002`; `LEGACY::REQ-002` | 已确认（`CONFIRMED`）；DUT配置边界见`OPEN::OI-015`、`OPEN::OI-016`、`OPEN::OI-017` |
| REQ-SYS-FUNC-003 | 系统必须支持三条序列：校准=`PRECONDITION→MEASUREMENT_I`；正应力=`PRECONDITION→POSITIVE_STRESS→MEASUREMENT_P`；负应力=`PRECONDITION→NEGATIVE_STRESS→MEASUREMENT_N`。 | 功能 | PROJECT REQUIREMENT | `SP1::REQ-FUNC-002`（PAPER FACT）；`DECISION::DEC-008` | 已确认（`CONFIRMED`） |
| REQ-SYS-FUNC-004 | 系统必须支持低能量电阻负载回路：`VDC→RL→DUT Drain→DUT Power Source→return`。 | 功能 | PROJECT REQUIREMENT | `SP1::REQ-FUNC-001`（PAPER FACT）；`LEGACY::REQ-012` | 已确认（`CONFIRMED`） |
| REQ-SYS-FUNC-005 | 在`MEASUREMENT_I/P/N`状态下，DUT必须处于不完全导通状态，并产生有限且可计算的`IDS`。 | 功能 | PROJECT REQUIREMENT | `SP1::REQ-FUNC-003`（PAPER FACT） | 已确认（`CONFIRMED`）；验收条件延期（`ACCEPTANCE DEFERRED`）至G12 |
| REQ-SYS-FUNC-006 | 系统必须获得可解释、可重复的MI、MP、MN，并保留正/负应力测量点之后的恢复波形。 | 功能 | PROJECT REQUIREMENT | `SP1::REQ-FUNC-004`（PAPER FACT）；`DECISION::DEC-009` | 已确认（`CONFIRMED`）；测量点算法延期至G10/G11 |
| REQ-SYS-FUNC-007 | Si8273 channel A的`VOA`必须承担关键的应力→测量栅极电压快速转换。 | 功能 | PROJECT REQUIREMENT | `DECISION::DEC-005`; `LEGACY::REQ-005`（PROJECT DESIGN CHOICE 已由 Master 批准） | 已确认（`CONFIRMED`） |
| REQ-SYS-FUNC-008 | 正BTI模式必须实现`VDDA=VGS-P`、`GNDA=VGM-P`、`VIA HIGH→LOW`；负BTI模式必须实现`VDDA=VGM-N`、`GNDA=VGS-N`、`VIA LOW→HIGH`。 | 功能 | PROJECT REQUIREMENT | `DECISION::DEC-006`, `DECISION::DEC-007`; `LEGACY::REQ-006`, `LEGACY::REQ-007`（PROJECT DESIGN CHOICE 已由 Master 批准） | 已确认（`CONFIRMED`） |

### 3.2 方法需求（9条）

| ID | 规范需求 | 类别 | 需求性质 | 来源 | 当前状态 |
|---|---|---|---|---|---|
| REQ-SYS-METHOD-001 | 每条测试序列都必须支持Gate-to-SREF的`VGS=0 V`预处理；G0不规定0 V实现拓扑。 | 方法 | PROJECT REQUIREMENT | `SP1::REQ-VOLT-001`（PAPER FACT）；`DECISION::DEC-008` | 已确认（`CONFIRMED`）；容差和实现拓扑延期 |
| REQ-SYS-METHOD-002 | 系统必须支持`VGM-I`、`VGM-P`、`VGM-N`；`VGM-I=initial Vth`，`VGM-P/N`可分别调节，三者不要求相等。 | 方法 | PROJECT REQUIREMENT | `SP1::REQ-VOLT-003`（PAPER FACT） | 已确认（`CONFIRMED`）；范围和分辨率延期至G2 |
| REQ-SYS-METHOD-003 | B1505必须在DUT专用的固定`VDS-C`下取得初始`IDS-VGS`曲线，并用DUT专用`Ith`交点定义初始`Vth`。 | 方法 | PROJECT REQUIREMENT | `SP1::REQ-VOLT-004`, `SP1::REQ-MEAS-008`（PAPER FACT） | 已确认（`CONFIRMED`）；具体数值延期至G2 |
| REQ-SYS-METHOD-004 | MI、MP、MN处的`VDS`必须在已批准容差内与对应`VDS-C`对齐。 | 方法 | PROJECT REQUIREMENT | `SP1::REQ-VOLT-005`（PAPER FACT（原则）） | 原则已确认（`CONFIRMED`）；容差延期至G12 |
| REQ-SYS-METHOD-005 | 每个测量工作点必须满足`VDS-C>VGS-Vth`；所需裕量由DUT配置档案规定。 | 方法 | PROJECT REQUIREMENT | `SP1::REQ-VOLT-006`（PAPER FACT） | 已确认（`CONFIRMED`）；裕量延期至G2 |
| REQ-SYS-METHOD-006 | 校准被接受后，正/负应力测试必须保持`VDC`和`RL`不变，只调节`VGM-P/N`完成工作点对齐。 | 方法 | PROJECT REQUIREMENT | `SP1::REQ-FUNC-005`, `SP1::REQ-CTRL-002`（PAPER FACT） | 已确认（`CONFIRMED`） |
| REQ-SYS-METHOD-007 | `IDM-P`和`IDM-N`必须在批准容差内与`IDM-I`匹配；P1的±20%只作为`PAPER PERFORMANCE REFERENCE`。 | 方法 | PROJECT REQUIREMENT | `SP1::REQ-MEAS-007`（原则为PAPER FACT；±20%为PAPER PERFORMANCE REFERENCE） | 原则已确认（`CONFIRMED`）；容差延期至G12 |
| REQ-SYS-METHOD-008 | 正应力期间的`IDS`和能量必须受DUT专用上限约束，避免自热使`Vth`结果无法解释。 | 方法 | PROJECT REQUIREMENT | `SP1::REQ-MEAS-010`（PAPER FACT（原则））+ ENGINEERING INFERENCE | 待Master批准（`PROPOSED`）；上限延期至G2 |
| REQ-SYS-METHOD-009 | 只有Master激活完整论文/Fig. 10复现范围后，系统才需要满足批准的多脉冲应力流程。 | 方法 | PROJECT REQUIREMENT — CONDITIONAL | `SP1::REQ-CTRL-003` + `OPEN::OI-022` | 条件未激活（`CONDITIONAL-INACTIVE`）；仅在Master激活完整论文/Fig. 10复现范围后生效 |

### 3.3 时间需求（6条）

| ID | 规范需求 | 类别 | 需求性质 | 来源 | 当前状态 |
|---|---|---|---|---|---|
| REQ-SYS-TIME-001 | 系统必须支持正/负应力状态快速、可重复地切换到对应测量状态。 | 时间 | PROJECT REQUIREMENT | `SP1::REQ-TIME-001`（PAPER FACT） | 已确认（`CONFIRMED`） |
| REQ-SYS-TIME-002 | 项目必须以P1报告的约100 ns完整系统`tdly`作为设计和验证目标；该目标不是单独`VOA`边沿指标，也暂不等于明确的`<100 ns`或`≤100 ns`通过判据。 | 时间 | PROJECT REQUIREMENT | `SP1::REQ-TIME-002`（PAPER PERFORMANCE REFERENCE）；`DECISION::DEC-009`; `LEGACY::REQ-010` | 目标性质已确认（`CONFIRMED`）；数值通过判据延期至G10/G11 |
| REQ-SYS-TIME-003 | 系统必须支持可配置`tpre`，并允许通过MI或`Vth-IS`稳定性建立预处理完成判据。 | 时间 | PROJECT REQUIREMENT | `SP1::REQ-TIME-003`（PAPER FACT: long-term；数值未公开） | 能力已确认（`CONFIRMED`）；数值和完成判据延期至G12 |
| REQ-SYS-TIME-004 | 系统必须支持可配置`tstr`；P1给出的时间范围和示例只属于`PAPER EXAMPLE VALUE`。 | 时间 | PROJECT REQUIREMENT | `SP1::REQ-TIME-004`（PAPER FACT（能力）） | 能力已确认（`CONFIRMED`）；项目范围延期至G2/G12 |
| REQ-SYS-TIME-005 | 系统必须支持足以捕获选定测量点和所需恢复区间的`tmea`。 | 时间 | PROJECT REQUIREMENT | `SP1::REQ-TIME-005`（PAPER FACT（能力）） | 能力已确认（`CONFIRMED`）；持续时间延期至G10/G11 |
| REQ-SYS-TIME-006 | 系统必须允许改变并记录实际`tdly`，以得到恢复随延迟变化的数据；范围和步进由批准的实验流程规定。 | 时间 | PROJECT REQUIREMENT | `SP1::REQ-TIME-006`（PAPER FACT（能力）） | 能力已确认（`CONFIRMED`）；范围和步进延期至G12 |

### 3.4 测量与数据需求（9条）

| ID | 规范需求 | 类别 | 需求性质 | 来源 | 当前状态 |
|---|---|---|---|---|---|
| REQ-SYS-MEAS-001 | 每次转换必须记录同一事件的`VGS(t)`、`VDS(t)`和最终`tdly`定义所需的时序参考信号，并建立明确的共同时间关系。 | 测量 | PROJECT REQUIREMENT | `SP1::REQ-MEAS-001`（PAPER FACT + ENGINEERING INFERENCE） | 已确认（`CONFIRMED`）；deskew规则延期至G10/G11 |
| REQ-SYS-MEAS-002 | `VGS`必须测为DUT Gate-to-Kelvin-Source/SREF，不得测成gate-to-earth。 | 测量 | PROJECT REQUIREMENT | `DECISION::DEC-003`, `DECISION::DEC-004`; `LEGACY::REQ-011` | 已确认（`CONFIRMED`） |
| REQ-SYS-MEAS-003 | 系统必须提供可安全探测的`VGS`、`VDS`和时序/触发观察点；具体探头和连接器由后续阶段决定。 | 测量 | PROJECT REQUIREMENT | `LEGACY::REQ-014`; ENGINEERING INFERENCE | 功能已确认（`CONFIRMED`）；物理实现延期至G6/G7 |
| REQ-SYS-MEAS-004 | 后处理必须使用`IDS=(VDC-VDS)/RL`计算测量点电流，并保存所用`VDC/RL`元数据。 | 测量 | PROJECT REQUIREMENT | `SP1::REQ-MEAS-002`（PAPER FACT） | 已确认（`CONFIRMED`） |
| REQ-SYS-MEAS-005 | 后处理必须分别由MI、MP、MN得到`IDM-I`、`IDM-P`、`IDM-N`。 | 测量 | PROJECT REQUIREMENT | `SP1::REQ-MEAS-003`（PAPER FACT） | 已确认（`CONFIRMED`）；极值算法延期至G10/G11 |
| REQ-SYS-MEAS-006 | `IDM-I/P/N`必须映射到同一DUT、同一固定`VDS-C`的B1505曲线；插值方法必须一致且可审计。 | 测量 | PROJECT REQUIREMENT | `SP1::REQ-MEAS-004`（PAPER FACT） | 已确认（`CONFIRMED`）；插值验收延期至G12 |
| REQ-SYS-MEAS-007 | 后处理必须按P1式(3)及相同方法得到`Vth-IS/PS/NS`，并按式(5)计算修正后的`ΔVth`。 | 测量 | PROJECT REQUIREMENT | `SP1::REQ-MEAS-005`, `SP1::REQ-MEAS-006`（PAPER FACT；正/负展开式为工程重述`ENGINEERING RESTATEMENT`） | 已确认（`CONFIRMED`） |
| REQ-SYS-MEAS-008 | 采用单点/平行位移映射前，必须对每个目标DUT和测试条件验证`IDS≈Ith`附近曲线是否适用；P1的1%只作为`PAPER PERFORMANCE REFERENCE`。 | 测量 | PROJECT REQUIREMENT | `SP1::REQ-MEAS-009`（原则为PAPER FACT；1%为PAPER PERFORMANCE REFERENCE） | 待Master批准（`PROPOSED`）；验收条件延期至G12 |
| REQ-SYS-MEAS-009 | 原始波形、仪器与配置元数据、DUT配置档案、B1505曲线、算法版本和最终结果必须足以独立重算MI/MP/MN、`tdly`和`ΔVth`，并报告重复性。 | 测量 | PROJECT REQUIREMENT | `SP1::REQ-VERIFY-004`; `DECISION::DEC-009`; ENGINEERING INFERENCE | 待Master批准（`PROPOSED`） |

### 3.5 接口需求（10条）

| ID | 规范需求 | 类别 | 需求性质 | 来源 | 当前状态 |
|---|---|---|---|---|---|
| REQ-SYS-INTERFACE-001 | `SREF`必须定义为DUT Kelvin Source参考点。 | 接口 | PROJECT REQUIREMENT | `DECISION::DEC-003`; `LEGACY::REQ-003` | 已确认（`CONFIRMED`） |
| REQ-SYS-INTERFACE-002 | `SREF`不得自动等于实验室earth或chassis。 | 接口 | PROJECT REQUIREMENT | `DECISION::DEC-004`; `LEGACY::REQ-004` | 已确认（`CONFIRMED`） |
| REQ-SYS-INTERFACE-003 | `GNDI`、`GNDA`、`SREF`、earth/chassis必须保持显式区分；任何连接都必须经过Master批准并可追溯。 | 接口 | PROJECT REQUIREMENT | `GOVERNANCE::AGENTS.md`; `INTERFACE::docs/interfaces.md`（禁止隐式连接） | 已确认（`CONFIRMED`） |
| REQ-SYS-INTERFACE-004 | DUT封装支持时，Power Source与Kelvin Source路径必须分开；不支持时必须在DUT配置档案中记录限制。 | 接口 | PROJECT REQUIREMENT | `LEGACY::REQ-013`; ENGINEERING INFERENCE | 已确认（`CONFIRMED`） |
| REQ-SYS-INTERFACE-005 | 外部脉冲/控制接口必须支持可重复的状态命令、触发参考和`tpre/tstr/tmea/tdly`配置；电平、通道和连接器由G1定义。 | 接口 | PROJECT REQUIREMENT | `SP1::REQ-CTRL-001`（序列为PAPER FACT；接口为ENGINEERING INFERENCE） | 待Master批准（`PROPOSED`） |
| REQ-SYS-INTERFACE-006 | 栅极目标接口必须允许外部设定或提供`VGS-P/N`、`VGM-I/P/N`及已批准模式真值表所需的电源轨；G0不固定数值。 | 接口 | PROJECT REQUIREMENT | `DECISION::DEC-006`, `DECISION::DEC-007`; `SP1::REQ-VOLT-002`, `SP1::REQ-VOLT-003` | 待Master批准（`PROPOSED`） |
| REQ-SYS-INTERFACE-007 | 外部漏极负载接口必须接收DUT专用`VDC/RL`，并明确施加、返回和电流路径；基础PCB不因DUT额定阻断电压而自动承担650 V或3.3 kV。 | 接口 | PROJECT REQUIREMENT | `SP1::REQ-FUNC-001`; `DECISION::DEC-016` | 待Master批准（`PROPOSED`） |
| REQ-SYS-INTERFACE-008 | 校准数据接口必须向后处理传递B1505固定`VDS-C`曲线、`Ith`以及DUT、温度和扫描元数据；高速PCB不负责生成该曲线。 | 接口 | PROJECT REQUIREMENT | `SP1::REQ-VOLT-004`, `SP1::REQ-MEAS-008`; ENGINEERING INFERENCE | 待Master批准（`PROPOSED`） |
| REQ-SYS-INTERFACE-009 | 示波器与探头接口必须允许在同一次事件中测量`VGS`、`VDS`和时序参考，并管理共模、探头负载和时序误差；具体仪器规格后定。 | 接口 | PROJECT REQUIREMENT | `SP1::REQ-MEAS-001`; ENGINEERING INFERENCE | 待Master批准（`PROPOSED`） |
| REQ-SYS-INTERFACE-010 | 0 V预处理路径与Si8273输出必须互斥，不得同时低阻驱动；是否采用独立clamp/switch属于尚未冻结的`PROJECT DESIGN CHOICE`。 | 接口 | PROJECT REQUIREMENT | `RISK::RISK-004`; `DECISION::PROP-001` 未批准 | 待Master批准（`PROPOSED`） |

### 3.6 DUT兼容需求（5条）

| ID | 规范需求 | 类别 | 需求性质 | 来源 | 当前状态 |
|---|---|---|---|---|---|
| REQ-SYS-DUT-001 | 平台目标必须覆盖650 V-class和3.3 kV-class SiC MOSFET的低`VDS` BTI/`Vth`迟滞测试。 | DUT兼容 | PROJECT REQUIREMENT | `DECISION::DEC-016`; `LEGACY::REQ-015` | 已确认（`CONFIRMED`） |
| REQ-SYS-DUT-002 | DUT额定阻断电压不得被解释为PCB必须施加650 V或3.3 kV；实际`VDC/VDS-C`由BTI测量条件决定，本项目不是breakdown test。 | DUT兼容 | PROJECT REQUIREMENT | `DECISION::DEC-016`; `MASTER::SP1-REVIEW-v1.0` §5 | 已确认（`CONFIRMED`） |
| REQ-SYS-DUT-003 | 栅极驱动架构、`SREF`、正/负BTI序列、测量原理和`VDS→IDS→Vth`链应与DUT额定阻断电压等级解耦。 | DUT兼容 | PROJECT REQUIREMENT | `DECISION::DEC-016`; ENGINEERING INFERENCE | 待Master批准（`PROPOSED`） |
| REQ-SYS-DUT-004 | 每个目标DUT必须建立受控配置档案，至少记录准确料号/封装、`Qg`、`Ciss/Crss`、推荐值和绝对最大`VGS`、`Vth`、`VGM`、`Ith`、`VDS-C`、Kelvin Source、`Rg`、`VDC/RL`、温度和相关时序检查。 | DUT兼容 | PROJECT REQUIREMENT | `LEGACY::REQ-016`; `MASTER::SP1-REVIEW-v1.0` §5 | 原则已确认（`CONFIRMED`）；具体数值延期至G2 |
| REQ-SYS-DUT-005 | DUT连接器/转接板和`Rg`配置必须适应封装、Kelvin Source和`Qg`差异，同时不得破坏`REQ-SYS-FUNC-001`或`REQ-SYS-FUNC-002`；具体转接方案和`Rg`策略由G1/G2决定。 | DUT兼容 | PROJECT REQUIREMENT | `LEGACY::OPEN-REQ-006`; ENGINEERING INFERENCE | 待Master批准（`PROPOSED`）；实现方式延期 |

### 3.7 安全需求（4条）

| ID | 规范需求 | 类别 | 需求性质 | 来源 | 当前状态 |
|---|---|---|---|---|---|
| REQ-SYS-SAFE-001 | 系统必须定义独立于预处理的`SAFE_OFF`逻辑状态、进入/退出条件以及栅极/漏极目标；具体电路后定。 | 安全 | PROJECT REQUIREMENT | `SP1::REQ-SAFE-001`（非P1内容）；`RISK::RISK-003` | 安全需求已确认（`CONFIRMED`）；具体定义延期至G1 |
| REQ-SYS-SAFE-002 | 系统必须定义上电、掉电、控制丢失、UVLO和默认状态流程，并防止意外长时间应力。 | 安全 | PROJECT REQUIREMENT | `SP1::REQ-SAFE-002`; `RISK::RISK-002`, `RISK::RISK-003` | 待Master批准（`PROPOSED`）；逻辑由G1决定，动作阈值由G2决定 |
| REQ-SYS-SAFE-003 | 系统必须定义栅极过压、漏极过流、误触发、驱动争用以及能量/自热保护；动作阈值和拓扑由G2决定。 | 安全 | PROJECT REQUIREMENT | `SP1::REQ-SAFE-002`; `RISK::RISK-004`, `RISK::RISK-005`, `RISK::RISK-008` | 待Master批准（`PROPOSED`） |
| REQ-SYS-SAFE-004 | 所有DUT栅极和漏极条件必须处于该DUT配置档案批准的额定值、能量和温度范围内。 | 安全 | PROJECT REQUIREMENT | `RISK::RISK-005`, `RISK::RISK-008`; ENGINEERING INFERENCE | 待Master批准（`PROPOSED`） |

### 3.8 过程需求（9条）

| ID | 规范需求 | 类别 | 需求性质 | 来源 | 当前状态 |
|---|---|---|---|---|---|
| REQ-SYS-PROCESS-001 | 所有器件pin、封装、额定值和关键参数必须在原理图冻结前由官方datasheet核对。 | 过程 | PROJECT REQUIREMENT | `LEGACY::REQ-100`; `GOVERNANCE::AGENTS.md` | 已确认（`CONFIRMED`） |
| REQ-SYS-PROCESS-002 | 关键结论必须标明`PAPER FACT`、`PAPER EXAMPLE VALUE`、`PAPER PERFORMANCE REFERENCE`、`ENGINEERING INFERENCE`、`PROJECT REQUIREMENT`、`PROJECT DESIGN CHOICE`或`OPEN ITEM`，并保留来源。 | 过程 | PROJECT REQUIREMENT | `LEGACY::REQ-101`; `MASTER::SP1-REVIEW-v1.0` | 已确认（`CONFIRMED`） |
| REQ-SYS-PROCESS-003 | 未批准的`OPEN ITEM`不得被默认成数值或实现；SP2/SP3只能在相应阶段或决定批准后展开设计。 | 过程 | PROJECT REQUIREMENT | `GOVERNANCE::AGENTS.md`; `MASTER::SP1-REVIEW-v1.0` §1、§6 | 已确认（`CONFIRMED`） |
| REQ-SYS-PROCESS-004 | ERC必须通过；如有残余warning，必须在布局冻结前逐项记录并批准。 | 过程 | PROJECT REQUIREMENT | `LEGACY::REQ-102` | 已确认（`CONFIRMED`） |
| REQ-SYS-PROCESS-005 | DRC必须通过；如有残余warning，必须在制造发布前逐项记录并批准。 | 过程 | PROJECT REQUIREMENT | `LEGACY::REQ-103` | 已确认（`CONFIRMED`） |
| REQ-SYS-PROCESS-006 | 未完成ERC、DRC、人工审查、验证矩阵批准和用户最终批准，不得生成或发布生产Gerber。 | 过程 | PROJECT REQUIREMENT | `DECISION::DEC-010`; `LEGACY::REQ-104` | 已确认（`CONFIRMED`） |
| REQ-SYS-PROCESS-007 | 每个面向用户的项目交付文件都必须同步到GitHub正式路径，随后才能报告完成。 | 过程 | PROJECT REQUIREMENT | `DECISION::DEC-011`; `LEGACY::REQ-105` | 已确认（`CONFIRMED`） |
| REQ-SYS-PROCESS-008 | 每个已同步输出都必须登记到`docs/chat_output_index.md`，无需额外复制归档。 | 过程 | PROJECT REQUIREMENT | `DECISION::DEC-012`; `LEGACY::REQ-106` | 已确认（`CONFIRMED`） |
| REQ-SYS-PROCESS-009 | 不得直接提交受限版权材料、credentials、敏感数据或未批准的大文件；同步失败时必须报告`OUTPUT_SYNC_BLOCKED`及未同步文件。 | 过程 | PROJECT REQUIREMENT | `DECISION::DEC-013`; `LEGACY::REQ-107`, `LEGACY::REQ-108` | 已确认（`CONFIRMED`） |

### 3.9 验证需求（5条）

| ID | 规范需求 | 类别 | 需求性质 | 来源 | 当前状态 |
|---|---|---|---|---|---|
| REQ-SYS-VERIFY-001 | 原型必须按批准的事件定义同时记录时序参考、`VGS`和`VDS`，并提取完整系统`tdly`；不得用单独`VOA`边沿代替。 | 验证 | PROJECT REQUIREMENT | `SP1::REQ-VERIFY-001`; `DECISION::DEC-009` | 已确认（`CONFIRMED`）；算法延期至G10/G11 |
| REQ-SYS-VERIFY-002 | 原型和方法验证必须报告MI/MP/MN相对`VDS-C`的偏差及通过判定。 | 验证 | PROJECT REQUIREMENT | `SP1::REQ-VERIFY-002` | 已确认（`CONFIRMED`）；容差延期至G12 |
| REQ-SYS-VERIFY-003 | 原型和方法验证必须报告`IDM-P/N`相对`IDM-I`的偏差公式、结果、调节后的`VGM-P/N`及通过判定。 | 验证 | PROJECT REQUIREMENT | `SP1::REQ-VERIFY-003` | 已确认（`CONFIRMED`）；容差延期至G12 |
| REQ-SYS-VERIFY-004 | 发布的数据集必须能够独立重算原始波形→`IDS`→B1505映射→原始位移→修正后`ΔVth`的完整链。 | 验证 | PROJECT REQUIREMENT | `SP1::REQ-VERIFY-004` | 已确认（`CONFIRMED`）；软件数值容差延期至G12 |
| REQ-SYS-VERIFY-005 | 平台通用性声明必须分别用至少一个已批准650 V-class配置档案和一个3.3 kV-class配置档案完成资格验证；不要求施加额定阻断电压。 | 验证 | PROJECT REQUIREMENT | `DECISION::DEC-016`; ENGINEERING INFERENCE | 待Master批准（`PROPOSED`） |

## 4. OPEN控制

### 4.1 G0批准项

- `OPEN::OI-000`：**已批准并关闭（`APPROVED / RESOLVED`）**。
- 批准人：Master。
- 批准内容：65条规范需求、69行crosswalk、`OPEN::OI-001...022`的延期控制和正式安装授权。

### 4.2 仍按后续Gate关闭的OPEN项

下表逐项保留v1.2批准的owner、deadline、延期理由和验证方法。延期不等于关闭。

| OI ID | 尚未决定的问题 | 负责人/阶段 | 最迟决定时间 | 为什么可以延期 | 如何验证 |
|---|---|---|---|---|---|
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

## 5. 历史ID与追溯

- `LEGACY::REQ-001...REQ-016`和`LEGACY::REQ-100...REQ-108`只作为历史来源ID，不再是项目级规范需求。
- `LEGACY::OPEN-REQ-001...OPEN-REQ-007`已由新的OPEN控制体系替代。
- `LEGACY::OPEN-REQ-008`已通过需求合并解决。
- SP1的36个批准ID继续作为论文方法证据ID，不作为本文件的项目级规范ID。
- 69行完整逐项映射见[G0-CRB-v1.2附录A](G0_closing_requirements_baseline_v1.2.md#附录a逐项来源到规范需求映射)。

## 6. 验证控制

65条需求的受控验证行见[verification_matrix.md](verification_matrix.md)。具体验收数值延期不会阻止需求基线冻结，但必须满足：

1. 每条需求至少有一条验证行；
2. 延期验收明确引用对应`OPEN::OI-*`；
3. 未批准的数值不得作为通过条件；
4. 条件需求`REQ-SYS-METHOD-009`在Master激活前保持`CONDITIONAL-INACTIVE`。

## 7. 变更控制

以后如需改变任何冻结需求的ID、技术含义、分类、scope、证据层级或crosswalk，必须：

1. 提交明确的change record；
2. 说明受影响需求、接口、验证、风险和阶段门；
3. 获得Master批准；
4. 同步更新`requirements.md`、`verification_matrix.md`及相关状态文件；
5. 完成GitHub提交和远端一致性回读后方可生效。

