# 项目状态

版本：v0.5
当前阶段：G0收尾 + G1系统架构

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

## 当前Stage-Gate状态
- G0 需求定义：**ACTIVE — SP1已Master批准；等待canonical requirements合并和项目级acceptance冻结**
- G1 系统架构：**ACTIVE**
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
- SP2：Si8273栅极驱动、电源架构、0 V precondition — 可在G1接口明确后继续；
- SP3：VDC/RL漏极负载与测量回路 — 可在G1接口明确后继续；
- SP4：KiCad原理图和BOM — 等待G0-G2冻结；
- SP5：PCB placement/routing — 等待SP4和前置审核；
- SP6：硬件bring-up与验证 — 等待原型板；
- SP7：B1505/JEP184校准与数据处理 — 可根据已批准SP1方法基线并行推进算法定义。

## 当前未解决问题
1. 650 V-class和3.3 kV-class目标DUT的准确型号、封装、Qg以及是否有独立Kelvin Source；
2. 最终VGS-P、VGS-N、VGM-I、VGM-P、VGM-N范围；
3. 0 V precondition的具体硬件拓扑；
4. 各目标DUT对应的VDS-C、Ith、VDC和RL设计值；
5. Pulse Generator、示波器、差分探头的准确型号；
6. PCB上使用的Si8273完整可订购料号和封装；
7. LTspice中Si8273是否有可用厂商模型，若没有则采用什么等效模型；
8. 项目`tdly`精确PASS算法：起点、终点、extremum search、filter、ringing、deskew/de-embedding；
9. `VDS≈VDS-C`容差、`IDM-P/N`匹配容差、tpre/tmea和self-heating验收条件；
10. SAFE_OFF、上电/掉电顺序、interlock与protection最低要求；
11. 650 V/3.3 kV DUT的connector/adapter与允许更换Rg策略；
12. 将SP1批准的36-ID requirement set正式合并进canonical `docs/requirements.md`，消除旧项目REQ与SP1 REQ的编号/层级歧义；
13. 2026-08-24之前历史聊天输出文件的完整回填范围。

## 当前推荐下一步
1. 执行 **G0 Closing**：把SP1的36条requirements与当前`docs/requirements.md`合并并建立完整traceability；
2. 同时完成 **G1 System Architecture**：画清系统方框图、各模块接口、SREF/GNDA/GNDI/earth关系和关键电流返回路径；
3. 确定哪些acceptance必须在G0冻结，哪些可以明确延期到G2或prototype validation再冻结；
4. 然后进入G2：对Si8273、650 V/3.3 kV目标DUT、Rg、去耦、0 V precondition、VDC/RL进行datasheet核对、计算和必要的LTspice仿真；
5. G0-G2通过之前，不正式进入KiCad原理图。

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
