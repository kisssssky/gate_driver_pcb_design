# PCB 设计阶段门（Stage-Gate）总计划

本文件是本项目的主进度控制文件。每当项目出现实质性的设计、验证、仿真、原理图、PCB、调试或实验进展时，都应同步更新本文件中的阶段状态和通过证据。

## 项目级输出归档规则

每个项目聊天产生的用户可交付输出文件必须按 [`docs/output_sync_policy.md`](output_sync_policy.md) 保存到 GitHub，并更新 [`docs/chat_output_index.md`](chat_output_index.md)。未完成同步时不得把该输出标记为正式完成。

## 项目最终成功标准
本项目不是“原理图画完”或“DRC通过”就算成功，也不是只要Si8273输出边沿小于100 ns就算成功。最终目标是功能复现 Li et al., IEEE TPEL 2024 Fig. 3：DUT能够完成 `0 V预处理 → stress → measurement`，并在stress结束后约100 ns内获得可解释、可重复的VDS测量点，用于后续MI/MP/MN和ΔVth提取。

项目级通用性目标：同一平台用于650 V-class与3.3 kV-class SiC MOSFET的低VDS BTI / Vth-hysteresis测试。DUT的额定blocking voltage不等于本BTI PCB必须工作在650 V或3.3 kV；实际Drain bias由calibration/measurement条件决定。

## 人与AI的职责划分

### 你（最终负责人）必须亲自确认
- 最终器件选型；
- 实物封装和Pin 1方向；
- 关键器件placement；
- 关键高速走线和三引脚Source端`SREF` Kelvin式参考走线；
- 实验室电源是否真正浮地/隔离；
- 示波器探头和接地方式；
- 实物上电调试；
- ERC/DRC警告最终处置；
- Gerber/生产文件最终批准。

### ChatGPT主要负责
- 论文和datasheet解释；
- 系统需求和架构；
- 电路原理推理与计算；
- LTspice建模思路；
- 原理图review；
- PCB截图、placement、routing review；
- 故障模式和安全风险分析；
- bring-up与验证计划；
- 波形和实验方法分析。

### Codex主要负责
- GitHub与工程文件维护；
- 在接口已经冻结后执行确定性的KiCad文件修改；
- BOM生成与一致性检查；
- ERC/DRC自动化与报告；
- 计算脚本；
- 示波器/B1505 CSV自动处理；
- 版本控制和变更摘要。

Codex不得自行猜测器件引脚、额定值、冻结接口、安全行为或高速拓扑。

---

# 阶段门

## G0 — 需求定义
### 目标
在画电路前，明确PCB到底必须实现什么。
### 需要理解
- 输入、输出、控制和测量量；
- 电压、电流、时间和测量要求；
- 正BTI与负BTI模式；
- SREF、GNDA、GNDI、实验室earth之间的区别；
- PRECONDITION、STRESS、MEASUREMENT、SAFE-OFF状态。
### 主要工具
ChatGPT、论文、datasheet、GitHub文档。
### AI负责
ChatGPT提取需求、状态、时序、未知项，并编号为`REQ-xxx`；Codex只负责在批准后维护文档。
### 必须产出
- `docs/requirements.md`
- `docs/G0_closing_requirements_baseline_v1.2.md`
- `docs/G0_master_review_v1.0.md`
- `docs/SP1_paper_method_system_requirements_v0.2.md`
- `docs/SP1_final_gate_review_v1.0.md`
- `docs/SP1_master_review_v1.0.md`
- 状态表
- 时序定义
- 初版验证矩阵
- 未解决问题清单
### PASS标准
- 所有必要功能有REQ编号；
- 正/负BTI逻辑无歧义；
- 0 V预处理已被纳入；
- SREF定义冻结；
- 系统级约100 ns测量目标被明确定义；
- 所有未解决问题明确列出，不靠猜测补全。
### 当前状态
**PASS — canonical requirement baseline FROZEN**

通过证据：

1. `SP1-v0.2 + SP1-FGR-v1.0`已经Master批准；
2. `G0-CRB-v1.2`已经Master批准，批准记录为`docs/G0_master_review_v1.0.md`；
3. 65条`REQ-SYS-*`规范需求已安装进`docs/requirements.md`；
4. `docs/verification_matrix.md`覆盖65/65条需求；
5. 69行SP1/legacy crosswalk完整，正向和反向追溯均无缺失；
6. `OPEN::OI-000`已批准并关闭；
7. `OPEN::OI-001...022`均有owner、deadline和验证方法，并继续按对应Gate关闭；
8. SREF、同一DUT/profile的P/N切换限制、0 V预处理功能、约100 ns完整系统目标及650 V/3.3 kV低`VDS`边界均已明确；
9. 安装过程没有通过猜测补入数值、算法、连接器或电路拓扑；
10. `DEC-017`、GitHub远端回读和状态一致性检查均已完成。

需求基线状态为`FROZEN`；G0阶段门状态为`PASS`。这不表示G1/G2架构、器件参数或电路设计已经完成。

---

## G1 — 系统架构
### 目标
把完整实验拆成模块，并在选具体电路之前定义模块接口。
### 每个模块必须能回答
- 信号从哪里来、到哪里去；
- 电源从哪里来；
- 电流从哪里返回；
- 参考点是谁；
- 控制输入是什么；
- 测量输出是什么。
### 预期模块
- Pulse Generator / 逻辑输入；
- Si8273隔离栅极驱动；
- stress→measurement高速切换；
- 0 V precondition；
- 三引脚DUT Gate/Drain/Source接口，以及从`DUT_SOURCE/SOURCE_STAR`分出的`SREF`与`DRET`功能路径；
- VDC + RL漏极负载回路；
- VGS/VDS测量接口；
- B1505校准流程。
### 主要工具
ChatGPT、GitHub文档。
### PASS标准
- 每个连接器和主要net用途明确；
- 关键电流回路可以解释；
- GNDI、GNDA、SREF、earth没有被模糊合并；
- PCB负责什么、外部仪器负责什么已经划清；
- 650 V-class与3.3 kV-class DUT的通用/差异接口边界已定义；
- SP2和SP3无需猜系统接口即可继续。
### 当前状态
**PASS — G1 INTERFACE BASELINE FROZEN**

通过证据：

1. Master审核记录：`docs/G1_master_review_v1.0.md`；批准决策：`DEC-019`；
2. `docs/G1_system_architecture_v1.1.md`定义13个系统模块、7个状态、25个唯一逻辑接口与8幅Mermaid架构/路径图；
3. `docs/interfaces.md`已安装为G1唯一逻辑接口冻结基线，状态`FROZEN`；
4. DUT只含Gate/Drain/Source三个物理引脚；`SREF`与`DRET`在`DUT_SOURCE/SOURCE_STAR`有意单点汇合并保持功能路径分离；
5. Gate、drain和测量回流路径及各系统责任已分配；`IF-GATE-01`闭合了`MEASUREMENT_I`的`VGM-I`逻辑目标；
6. PRECONDITION起算顺序、`SAFE_OFF`、上电/掉电、失控和互锁职责均已定义到G1层；
7. `OI-012...017`已由Master批准并标记为`RESOLVED AT G1`；
8. 未选择具体器件、数值、connector pinout、保护/0 V物理拓扑或KiCad实现。

G1阶段门=`PASS`；G1接口基线=`FROZEN`。这不表示G2参数或G3电路已经批准；G3继续`BLOCKED`。

---

## G2 — 器件选型与电路计算
### 目标
在冻结原理图前，证明方案在电气上合理。
### 需要学习
- datasheet读法；
- 电压/电流额定值；
- Qg与栅极驱动电流；
- Rg对速度和振铃的影响；
- 去耦；
- RL、IDS、脉冲功率和DUT自热；
- 时序与带宽裕量；
- 上电、掉电、EN、UVLO状态。
### 主要工具
ChatGPT、LTspice、Python、厂商datasheet。
### AI负责
ChatGPT做datasheet review、计算、失效状态分析和LTspice模型简化；Codex做参数扫描、BOM草案和计算脚本。
### 你负责
确认准确料号、实物器件、实验室现有电源/仪器，并确认所有关键数值都有来源。
### 必须产出
- Si8273准确料号和封装；
- 650 V-class与3.3 kV-class目标DUT的Qg/栅极接口/允许VGS核对；
- 栅极驱动电流计算；
- 初始Rg范围；
- 去耦规格；
- 0 V precondition拓扑决定；
- VDC/RL选择方法；
- 器件额定值表；
- 必要的LTspice仿真结果。
### PASS标准
- 所有关键器件都有datasheet依据；
- 电压、电流、功率裕量完成检查；
- 对两类目标DUT的目标切换速度均有定量依据；
- 负BTI默认状态风险得到处理；
- 没有阻止原理图实现的关键OPEN问题。
### 当前状态
**ACTIVE — datasheet核对、电气计算、DUT profile、候选拓扑和LTspice输入deck已完成；等待用户本地LTspice实跑、B1505目标值与Master批准。Final Gate Review仍有H/I/K/N/O/P/Q FAIL，因此未READY、未PASS。**

---

## G3 — KiCad原理图
### 目标
把完整电气连接关系正式画入KiCad。
### 需要学习
- Symbol与真实器件的区别；
- Pin与Net；
- 电源符号与参考点；
- 去耦；
- Connector；
- 未使用引脚处理；
- ERC。
### 主要工具
KiCad Schematic Editor、ChatGPT、Codex。
### AI负责
ChatGPT逐模块设计和逐pin review；Codex按已批准连接表修改KiCad、跑ERC和生成报告。
### 你负责
视觉检查原理图、对照datasheet核对关键pin、批准所有ERC warning。
### PASS标准
- 无未解决严重ERC；
- 关键IC逐pin人工核对；
- 无悬空控制输入；
- GNDI/GNDA/SREF/earth关系正确；
- 正负BTI满足冻结的接口表；
- 0 V precondition不与Si8273输出冲突。
### 当前状态
**BLOCKED，直到G1和G2通过**

---

## G4 — Footprint与实物封装核对
### 目标
把每个原理图器件映射到正确的真实焊盘与机械封装。
### 需要学习
- Symbol pin号与Footprint pad号；
- 同名封装的不同变体；
- Pin 1方向；
- 机械尺寸图；
- Connector方向和极性。
### AI负责
ChatGPT检查机械图和封装变体；Codex检查缺失footprint并生成审计表。
### 你负责
最终确认实物封装、Pin 1和Connector方向。
### PASS标准
- 100%板载器件有已验证footprint；
- Symbol pin到pad映射正确；
- 不根据“名字看起来像”选封装；
- Connector极性和方向已人工review。
### 当前状态
**BLOCKED**

---

## G5 — PCB规则与板级设置
### 目标
在placement和routing之前先定义设计规则。
### 需要学习
- 层叠；
- 铜层；
- 线宽；
- clearance；
- via；
- net class；
- 隔离区；
- return path。
### 建议功能组
`LOGIC`、`GATE_FAST`、`FLOATING_POWER`、`DRAIN_POWER`、`SENSE`。
### AI负责
ChatGPT根据实际电压、电流、速度提出规则原则；Codex实现已批准的net class和规则。
### PASS标准
- stackup确定；
- 重要net class全部分配；
- 线宽和间距有理由；
- 隔离区域确定；
- 规则存在后才开始placement。
### 当前状态
**BLOCKED**

---

## G6 — 关键器件Placement
### 目标
通过物理摆放降低寄生电感并建立正确回流路径。
### 第一轮只优先放
- Si8273；
- VDDA-GNDA 100 nF；
- 其他本地去耦；
- Rg；
- DUT Gate connector；
- 三引脚DUT Source接口和`SOURCE_STAR`，不得增加未批准的第四个Source参考connector。
### 需要学习
- loop area；
- parasitic inductance；
- 去耦回路几何；
- 从`SOURCE_STAR`引出的`SREF` Kelvin式参考routing与`DRET`功率routing；
- probe access；
- connector可操作性。
### AI负责
ChatGPT根据PCB截图review回路、回流、隔离和探头空间；Codex只做明确指定的坐标/批量修改。
### 你负责
关键器件的placement和最终批准。
### PASS标准
- `VOA → Rg → Gate → Gate/Source电容 → DUT_SOURCE/SOURCE_STAR → SREF → 已批准rail return`物理回路紧凑；
- 高频去耦紧贴驱动器供电pin；
- `SREF`与`DRET`在PCB上作为不同功能路径可区分，且只在`SOURCE_STAR`汇合；
- 探头实际能够接入；
- 隔离和Connector布局合理。
### 当前状态
**BLOCKED**

---

## G7 — Routing
### 目标
按电气重要性顺序走线，而不是按“哪里好走”来走。
### 路由优先级
1. VOA → Rg → DUT Gate
2. `DUT_SOURCE/SOURCE_STAR → SREF → driver return`
3. 高频驱动去耦回路
4. VGS/VDS sense
5. Power
6. Logic
7. 非关键线
### 需要学习
- return path；
- ground/copper plane连续性；
- via电感；
- 三引脚Source端Kelvin式sensing；
- 功率回路与测量回路分离。
### AI负责
ChatGPT逐段截图review；Codex做规则检查和明确的机械修改。
### 你负责
关键高速与三引脚Source端`SREF` Kelvin式routing。
### PASS标准
- 关键回路先完成并通过review；
- Drain功率电流不使用`SREF` sense路径；`SREF`与`DRET`仅在`SOURCE_STAR`汇合；
- 没有明显断裂的return path；
- 所有routing满足批准规则。
### 当前状态
**BLOCKED**

---

## G8 — ERC / DRC / 工程审核
### 目标
把机器规则检查和工程判断结合起来。
### 重要原则
ERC/DRC通过只能证明“符合已经写入CAD的规则”，不能证明Gate loop短、Kelvin正确、去耦有效或SREF安全。
### AI负责
Codex跑ERC/DRC、收集warning、检查BOM/footprint/net一致性；ChatGPT做系统级工程review。
### 你负责
所有warning最终处置和完整视觉检查。
### PASS标准
- 0个未解决严重ERC；
- 0个未解决严重DRC；
- 每个warning都有记录；
- 原理图、placement、routing、测量接口、隔离和安全review通过。
### 当前状态
**BLOCKED**

---

## G9 — 制造发布
### 目标
只有设计审核通过后才生成正式制造文件。
### 主要输出
- Gerber；
- Drill；
- BOM；
- Position files（如需要装配）；
- Fabrication notes；
- Release checklist。
### 规则
生产发布必须由你明确批准。
### PASS标准
- G8通过；
- 制造checklist通过；
- 极性、方向、板框尺寸检查完成；
- 最终输出文件再次独立检查。
### 当前状态
**BLOCKED**

---

## G10 — 实物Bring-up
### 目标
以受控步骤第一次给PCB上电，避免直接损坏DUT。
### 建议顺序
1. 目检/显微镜检查；
2. 断电电阻与短路检查；
3. 只上逻辑电源；
4. 上driver电源但不进行DUT高压运行；
5. Dummy gate capacitor测试；
6. 正/负栅极切换测试；
7. 接DUT但`VDC=0`；
8. 低VDC + 保守RL；
9. 逐步接近正式实验条件。
### 主要工具
万用表、限流电源、示波器/差分探头、Pulse Generator、ChatGPT、Codex。
### PASS标准
- 每一级通过后才进入下一级；
- 无异常短路或意外ground路径；
- 正/负栅极切换正确；
- 无不安全VGS过冲；
- fail state与power sequence符合设计。
### 当前状态
**BLOCKED**

---

## G11 — 高速切换与测量验证
### 目标
证明PCB真正满足Fig. 3要求，而不仅是“能切换”。
### 至少测量
- VIA或等效控制边沿；
- 相对三引脚`DUT_SOURCE/SOURCE_STAR` Kelvin式取点的`VGS`；
- VDS。
### 评估
- transition time；
- overshoot；
- ringing；
- settling；
- stress结束时刻；
- VDS有效测量点时刻；
- tdly；
- repeatability。
### PASS标准
- VGS始终在DUT允许范围；
- measurement voltage可重复到达；
- MI/MP/MN行为可解释；
- stress removal → valid VDS point约100 ns，或满足最终批准的时序指标；
- 多次采集结果可重复。
### 当前状态
**BLOCKED**

---

## G12 — Fig. 3完整实验复现
### 目标
执行完整论文方法，而不仅验证PCB波形。
### 三类测试
**Calibration**：`0 V → VGM-I → MI`

**Positive stress**：`0 V → VGS-P → VGM-P → MP`

**Negative stress**：`0 V → VGS-N → VGM-N → MN`

然后将高速VDS测量与B1505固定VDS的IDS-VGS基准曲线结合，按批准的数据流程得到ΔVth。
### 主要工具
自制PCB、B1505/EasyEXPERT、Pulse Generator、示波器、Python、ChatGPT、Codex。
### PASS标准
- calibration通过；
- 同一块PCB完成正/负stress；
- VGM-P、VGM-N可通过外部设置调整，无需换PCB元件；
- MI、MP、MN和tdly可靠提取；
- ΔVth计算链路验证；
- 实验结果可重复。
### 当前状态
**BLOCKED**

---

## G13 — V2改版决定
### 目标
把V1实测问题转化成受控的V2修改，而不是凭感觉改板。
### 每个问题都必须记录
- 现象；
- 证据；
- 根因假设；
- 验证测试；
- 设计修改；
- 回归测试。
### AI负责
ChatGPT做根因分析和改版方案；Codex维护change list、KiCad确定性修改和版本diff。
### PASS标准
- 每项V2修改都有证据来源；
- 不引入无关改动；
- 修改后对应回归测试明确。
### 当前状态
**BLOCKED**

---

# 当前总进度
- G0 需求定义：**PASS — canonical requirement baseline FROZEN**
- G1 系统架构：**PASS — G1 interface baseline FROZEN**
- G2 器件选型与计算：**ACTIVE — 工程输入已准备；等待本地LTspice/B1505/Master动作**
- G3 原理图：**BLOCKED**
- G4 Footprint：**BLOCKED**
- G5 PCB规则：**BLOCKED**
- G6 Placement：**BLOCKED**
- G7 Routing：**BLOCKED**
- G8 ERC/DRC/工程审核：**BLOCKED**
- G9 制造发布：**BLOCKED**
- G10 Bring-up：**BLOCKED**
- G11 高速验证：**BLOCKED**
- G12 Fig. 3实验复现：**BLOCKED**
- G13 V2改版：**BLOCKED**

## 更新规则
每次项目出现实质性进展后：
1. 更新对应Gate的`当前状态`；
2. 在该Gate下补充通过证据或未通过原因；
3. 同步更新`docs/project_status.md`；
4. 只有满足PASS标准后，才能把状态改成`PASS`；
5. 任何关键假设都必须有来源：论文、datasheet、计算或明确标注的工程假设；
6. 每个聊天产生的输出文件保存到GitHub并更新`docs/chat_output_index.md`。
