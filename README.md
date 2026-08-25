# SiC MOSFET BTI 快速栅极驱动PCB

## 项目目的
功能复现 Li et al., *Accurate Evaluation of Threshold Voltage Hysteresis in SiC MOSFET Under Switching Stress*, IEEE TPEL 2024 的 Fig. 3 测试架构。

项目重点不是单独让Si8273输出边沿小于100 ns，而是让DUT完成：

`0 V预处理 → stress → measurement`

并在stress结束后约100 ns内获得可解释、可重复的VDS测量点，最终用于MI、MP、MN和ΔVth提取。

## 汇报版项目介绍
- [中文版：项目介绍](docs/project_introduction_zh_v1.0.md)
- [English version: Project Introduction](docs/project_introduction_en_v1.0.md)

## 项目级强制规则：聊天输出文件必须同步到 GitHub

本项目每个聊天产生的用户可交付输出文件，必须在任务完成前保存到本仓库，并登记到 [`docs/chat_output_index.md`](docs/chat_output_index.md)。详细范围、路径、例外和完成条件见 [`docs/output_sync_policy.md`](docs/output_sync_policy.md)。

当前 SP1 输出已保存为 [`docs/SP1_paper_method_system_requirements_v0.1.md`](docs/SP1_paper_method_system_requirements_v0.1.md)。

无输出文件的普通讨论不要求创建空文件；无再分发权限的论文原 PDF、凭据、敏感信息和未批准的大文件不得直接提交。

## 核心项目规则
- 同一块PCB必须同时支持正BTI和负BTI；
- 正负模式只通过外部`VDDA/GNDA`电压和控制波形改变，不更换PCB元件；
- `SREF`定义为DUT Kelvin Source参考点，不默认等于实验室earth；
- Si8273 `VOA`用于stress voltage与measurement voltage之间的高速切换；
- 完整测试包括0 V precondition、stress和measurement三个状态；
- 不允许猜测器件引脚、额定值或datasheet参数；
- 在ERC、DRC、人工审核和验证矩阵通过之前，不发布最终Gerber生产文件。

## 仓库结构
- `docs/`：需求、接口、决策、风险、项目状态、Stage-Gate、验证矩阵、聊天输出准则与索引；
- `hardware/`：KiCad原理图、PCB、BOM、datasheet；
- `calculations/`：电路、功率和时序计算；
- `analysis/`：B1505和示波器数据处理脚本；
- `measurements/`：原始和处理后的实验数据；
- `references/`：论文笔记和参考文献元数据。除非具有再分发权限，否则不要把受版权保护的PDF直接提交到仓库。

## 主要软件链
1. **ChatGPT**：论文、datasheet、系统架构、电路推理、设计审核；
2. **LTspice**：栅极驱动、Rg、简化DUT Gate模型、寄生和0 V precondition等电路行为仿真；
3. **KiCad**：正式原理图、Footprint、PCB Placement、Routing、ERC/DRC；
4. **GitHub + Codex**：工程文件、版本控制、BOM、自动检查、确定性的KiCad修改和脚本；
5. **Python**：后续示波器CSV、B1505数据、tdly、MI/MP/MN和ΔVth自动分析；
6. **Keysight EasyEXPERT / B1505A**：固定VDS的IDS-VGS基准扫描和校准。

## 当前阶段
当前处于：**需求定义 + 系统架构阶段**。

详细进度与每一步PASS条件见：`docs/stage_gate.md`。

实时项目状态见：`docs/project_status.md`。

## 文档语言
面向人的项目文档默认使用中文；Net名、Pin名、公式变量、软件命令和标准缩写保留英文，避免技术歧义。Codex专用的机器约束文件`AGENTS.md`可保持英文。