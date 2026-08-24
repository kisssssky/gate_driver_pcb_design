# 项目状态

版本：v0.4
当前阶段：需求定义 + 系统架构

## 项目目标
功能复现 Li et al., IEEE TPEL 2024 Fig. 3 的SiC MOSFET快速阈值电压迟滞测试架构。重点不是单独追求Si8273输出边沿小于100 ns，而是让DUT完成`0 V预处理 → stress → measurement`，并在stress结束后约100 ns内获得可解释、可重复的VDS测量点。

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
- 完成SP1 Final Gate Review：A-N全部PASS，状态为`READY FOR MASTER REVIEW`；
- 建立项目级聊天输出文件GitHub同步准则与`docs/chat_output_index.md`；
- 将“每个聊天产生的输出文件必须同步到GitHub”冻结为项目基本准则；
- 确定人 / ChatGPT / Codex的职责边界；
- 确定主要软件链：ChatGPT + LTspice + KiCad + GitHub/Codex + Python + B1505/EasyEXPERT。

## 当前Stage-Gate状态
- G0 需求定义：**ACTIVE**
- G1 系统架构：**ACTIVE**
- G2 器件选型与计算：**NOT STARTED**
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
- SP1：论文方法和系统需求提取 — **SP1 STATUS: READY FOR MASTER REVIEW；A-N全部PASS；等待Master批准/退回，OPEN验收项尚未冻结**；
- SP2：Si8273栅极驱动、电源架构、0 V precondition — 可以继续；
- SP3：VDC/RL漏极负载与测量回路 — 可以继续；
- SP4：KiCad原理图和BOM — 等待G0-G2冻结；
- SP5：PCB placement/routing — 等待SP4和前置审核；
- SP6：硬件bring-up与验证 — 等待原型板；
- SP7：B1505/JEP184校准与数据处理 — SP1定义稳定后可并行推进。

## 当前未解决问题
1. DUT准确型号、封装以及是否有独立Kelvin Source；
2. 最终VGS-P、VGS-N、VGM-I、VGM-P、VGM-N范围；
3. 0 V precondition的具体硬件拓扑；
4. 选定DUT对应的VDC和RL设计值；
5. Pulse Generator、示波器、差分探头的准确型号；
6. PCB上使用的Si8273完整可订购料号和封装；
7. LTspice中Si8273是否有可用厂商模型，若没有则采用什么等效模型；
8. 2026-08-24之前历史聊天输出文件的完整回填范围。

## 当前推荐下一步
1. Master审查SP1-v0.2与Final Gate Review；批准后再冻结G0的系统需求、三种测试时序和验收条件；
2. 完成G1：画清系统方框图、各模块接口、参考点和电流返回路径；
3. 然后进入G2：对Si8273、DUT、Rg、去耦、0 V precondition、VDC/RL进行datasheet核对、计算和必要的LTspice仿真；
4. G0-G2通过之前，不正式进入KiCad原理图。

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