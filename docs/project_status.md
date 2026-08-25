# 项目状态

版本：v0.8
当前阶段：G1系统架构

- 需求基线状态：**FROZEN — Master approved G0 canonical requirement baseline**
- G0阶段门状态：**PASS**

## 项目目标
功能复现 Li et al., IEEE TPEL 2024 Fig. 3 的SiC MOSFET快速阈值电压迟滞测试架构。重点不是单独追求Si8273输出边沿小于100 ns，而是让DUT完成`0 V预处理 → stress → measurement`，并在stress结束后约100 ns内获得可解释、可重复的VDS测量点。

项目同时要求平台能够用于 **650 V-class 与 3.3 kV-class SiC MOSFET 的低VDS BTI / Vth-hysteresis测试**。DUT额定阻断电压不等于本BTI PCB必须工作在650 V或3.3 kV；实际Drain bias由calibration/measurement条件决定。

## 当前已完成
- GitHub仓库初始化；
- 建立项目固定约束；
- 建立初版需求文档；
- 建立初版接口文档；
- 建立决策记录；
- 建立风险登记表；
- 建立验证矩阵；
- 建立`docs/stage_gate.md`作为PCB总流程和进度控制文件；
- 完成SP1-v0.2 Requirement Audit：修正2项ERROR、2项AMBIGUOUS、5项UNSUPPORTED、3项OUT_OF_SCOPE；保留36条编号需求和验证矩阵；
- 完成SP1 Final Gate Review：A-N全部PASS；
- 完成Master独立交叉审核：对照原论文、SP1-v0.2和Final Gate Review复核，结论为`SP1 MASTER APPROVED / COMPLETE`；
- 建立`docs/SP1_master_review_v1.0.md`作为Master最终审核记录；
- 将650 V-class + 3.3 kV-class低VDS BTI通用性加入项目级需求与决策；
- 建立项目级聊天输出文件GitHub同步准则与`docs/chat_output_index.md`；
- 将“每个聊天产生的输出文件必须同步到GitHub”冻结为项目基本准则；
- 确定人 / ChatGPT / Codex的职责边界；
- 确定主要软件链：ChatGPT + LTspice + KiCad + GitHub/Codex + Python + B1505/EasyEXPERT。
- Master批准`G0-CRB-v1.2`、65条`REQ-SYS-*`规范需求和69行SP1/legacy crosswalk；
- 创建`docs/G0_master_review_v1.0.md`，并以`DEC-017`记录批准与变更控制；
- 将65条需求正式安装进`docs/requirements.md`，需求基线状态为`FROZEN`；
- 重建`docs/verification_matrix.md`，覆盖65/65条需求，无孤立需求或测试；
- `OPEN::OI-000`已由Master批准并关闭；`OPEN::OI-001...022`继续按批准的owner、deadline和Gate关闭；
- 完成G0安装文件的GitHub同步、远端回读和状态一致性检查。
- `docs/G1_system_architecture_v1.0.md`与`docs/G1_final_gate_review_v1.0.md`为历史候选，已被三引脚返修版v1.1 supersede。
- `OI-012...017`均形成`G1 RESOLUTION PROPOSED — READY FOR MASTER REVIEW`，等待Master批准；未选择器件、数值、connector pinout或具体拓扑。
- `docs/interfaces.md`更新为`PROPOSED G1 INTERFACE BASELINE — READY FOR MASTER REVIEW`；接口尚未`FROZEN`。
- Master审核结论为`CHANGES REQUIRED；G1 ACTIVE`，已按三引脚DUT边界完成G1 v1.1返修。
- 创建`docs/G1_system_architecture_v1.1.md`与`docs/G1_final_gate_review_v1.1.md`：DUT只保留Gate/Drain/Source三个物理引脚；`SREF`与`DRET`在`DUT_SOURCE/SOURCE_STAR`单点汇合。
- 新增`IF-GATE-01 / CAL_GATE_TARGET`，由Gate目标协调模块向`DUT_GATE`提供相对`SREF`的`VGM-I`逻辑目标；接口总数重新计算为25。
- PRECONDITION只有在0 V Gate目标、`VDC/RL`供能、`VDS=VDC`和漏极回路全部验证有效后才开始`tpre`；fault后不得自动重启。
- 三引脚封装内部公共Source阻抗已进入DUT profile要求、RISK-007、FMEA与G11验证；未修改冻结需求。

## 当前Stage-Gate状态
- G0 需求定义：**PASS — canonical requirement baseline FROZEN**
- G1 系统架构：**ACTIVE — READY FOR MASTER REVIEW（返修候选，等待Master复审）**
- G2 器件选型与计算：**NOT STARTED / 可开始准备datasheet与DUT参数**
- G3 KiCad原理图：**BLOCKED**
- G4 Footprint验证：**BLOCKED**
- G5 PCB规则：**BLOCKED**
- G6 Placement：**BLOCKED**
- G7 Routing：**BLOCKED**
- G8 ERC/DRC/工程审核：**BLOCKED**
- G9 制造发布：**BLOCKED**
- G10 Bring-up：**BLOCKED**
- G11 高速切换/测量验证：**BLOCKED**
- G12 Fig. 3完整实验复现：**BLOCKED**
- G13 V2改版：**BLOCKED**

## 当前子项目
- SP1：论文方法和系统需求提取 — **MASTER APPROVED / COMPLETE**；后续工程选择不再回填为论文事实；
- SP2：Si8273栅极驱动、电源架构、0 V precondition与Calibration Gate目标 — v1.1候选接口已明确，可准备G2 datasheet和计算；具体rail、mux、clamp、器件与拓扑仍待Master/G2/G3批准；
- SP3：VDC/RL漏极负载与测量回路 — 三引脚`SOURCE_STAR/SREF/DRET`候选职责已明确，可准备G2参数计算；具体数值仍待批准；
- SP4：KiCad原理图和BOM — 等待G0-G2冻结；
- SP5：PCB placement/routing — 等待SP4和前置审核；
- SP6：硬件bring-up与验证 — 等待原型板；
- SP7：B1505/JEP184校准与数据处理 — 可根据已批准SP1方法基线并行推进算法定义。

## 当前未解决问题
1. 650 V-class和3.3 kV-class目标DUT的准确型号、三引脚封装、`Qg`及封装公共Source阻抗验证资料；
2. 最终VGS-P、VGS-N、VGM-I、VGM-P、VGM-N范围；
3. 0 V precondition的具体硬件拓扑；
4. 各目标DUT对应的VDS-C、Ith、VDC和RL设计值；
5. Pulse Generator、示波器、差分探头的准确型号；
6. PCB上使用的Si8273完整可订购料号和封装；
7. LTspice中Si8273是否有可用厂商模型，若没有则采用什么等效模型；
8. 项目`tdly`精确PASS算法：起点、终点、extremum search、filter、ringing、deskew/de-embedding；
9. `VDS≈VDS-C`容差、`IDM-P/N`匹配容差、tpre/tmea和self-heating验收条件；
10. SAFE_OFF、上电/掉电顺序、interlock与protection最低要求；
11. 650 V/3.3 kV三引脚DUT的connector/adapter、`SOURCE_STAR`落点与允许更换`Rg`策略；
12. 2026-08-24之前历史聊天输出文件的完整回填范围。

上述技术问题均已纳入`OPEN::OI-001...022`控制；需求基线冻结不表示这些后续参数或实现已经确定。

## 当前推荐下一步
1. Master复审`G1_system_architecture_v1.1.md`、25接口G1 ICD和`OI-012...017` proposals；
2. G1在Master批准前不得标记`PASS`或`FROZEN`；
3. G2可准备Si8273和目标DUT的datasheet核对与计算，所有具体数值必须来自批准的DUT配置档案；
4. G1与G2均通过之前，G3 KiCad原理图保持`BLOCKED`；
5. 后续Gate不会因G0或G1候选基线就自动通过。

## 文档语言规则
面向人的项目文档默认使用中文，以便快速理解；器件Pin名、Net名、文件名、公式变量、标准名称、软件命令和必要的专业缩写保留英文，例如`VDDA`、`GNDA`、`SREF`、`VGS-P`、`VGM-P`、`ERC`、`DRC`。Codex专用的机器约束文件如`AGENTS.md`可以保留英文，以减少执行歧义。

## 进度更新规则
每次出现实质性项目进展，都同时检查并更新：
- `docs/project_status.md`
- `docs/stage_gate.md`
- 如涉及需求、接口、决策或风险，再同步更新对应文档；
- 每个聊天产生的输出文件必须保存到其正式仓库路径，并更新`docs/chat_output_index.md`；
- 具体执行与例外遵守`docs/output_sync_policy.md`。

任何Gate只有满足其PASS标准并有证据后，才可标记为`PASS`。
