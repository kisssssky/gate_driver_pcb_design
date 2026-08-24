# SP1 Master 最终审核

- 审核版本：MASTER-SP1-REVIEW-v1.0
- 被审核基线：`SP1-v0.2 + SP1-FGR-v1.0`
- 日期：2026-08-24
- 审核角色：Master
- 结论：**SP1 MASTER APPROVED**

## 1. 最终结论

Master 已对 SP1-v0.2、SP1 Final Gate Review 以及原始论文进行交叉核对。SP1 的任务边界是“把论文方法转换为可追溯的系统需求”，而不是完成项目级参数冻结或具体电路设计。

结论：

- SP1 的论文方法理解主链正确；
- A-N 十四项交付条件全部成立；
- v0.2 对 v0.1 中 `tdly`、设备职责、negative-stress 状态、EasyEXPERT、100 ns 性质等过强表述的修正是合理的；
- 没有发现必须退回 SP1 继续修改的技术错误；
- `SP1-v0.2 + SP1-FGR-v1.0` 从本次审核起成为 **Master 批准的论文方法/系统需求证据基线**。

因此：

**SP1 STATUS: MASTER APPROVED / COMPLETE**

但要特别区分：

**SP1 完成 ≠ G0 需求定义已经 PASS。**

G0 还包含本项目自己的工程验收条件、目标 DUT 范围、安全要求以及 canonical `docs/requirements.md` 的合并冻结，这些不是论文能够替我们决定的。

## 2. Master 独立核对结果

### A. Calibration / Positive / Negative 方法链

通过。

SP1 对三条序列的定义正确：

- Calibration：`PRECONDITION → MEASUREMENT_I`
- Positive：`PRECONDITION → POSITIVE_STRESS → MEASUREMENT_P`
- Negative：`PRECONDITION → NEGATIVE_STRESS → MEASUREMENT_N`

论文明确给出 precondition 时 `VGS=0`、`VDS=VDC`、`IDS=0`；Calibration 将 `VGM-I` 设为 initial `Vth`；positive stress 时 DUT fully ON，`VDS≈0`、`IDS≈VDC/RL`；positive/negative stress 后分别由 MP/MN 获取快速测量点。

### B. `MI / MP / MN` 与 `VDS → IDS → Vth` 链

通过。

SP1 正确区分：

- MI / MP / MN 是高速 `VDS` 波形上的 measured potential points；
- 它们不是 `IDS` 本身，也不是 `Vth` 本身；
- 使用 `IDS=(VDC-VDS)/RL` 得到对应测量电流；
- 再映射至 B1505 在 fixed `VDS-C` 下取得的 `IDS-VGS` 基准曲线；
- 最后按论文方法得到 `Vth-IS`、`Vth-PS`、`Vth-NS` 和校正后的 `ΔVth`。

### C. `VGM-I / VGM-P / VGM-N`

通过。

SP1 没有错误地要求三者相等。论文明确规定 `VGM-I=initial Vth`，而 `VGM-P`、`VGM-N` 需要分别调整，使 `IDM-P/IDM-N` 接近 `IDM-I`，并使 measured-point `VDS` 与 calibration 的 `VDS-C` 对齐。

### D. `tdly` 与约 100 ns

通过，且 v0.2 的保守处理是正确的。

论文把 `tdly` 定义为 stress end 与 measurement 之间的 test delay；典型波形中报告 `tdly<100 ns`，摘要/结论概述为 100 ns。但论文没有给出工程复现所需的精确 crossing、滤波、极值搜索窗、ringing 处理或 deskew 算法。

因此 SP1 将“约 100 ns / <100 ns”分类为论文报告性能，而不是直接写成一个无歧义的 PCB PASS 算法，这是正确的。

### E. 论文事实与工程选择的边界

通过。

SP1 已将以下内容保留为 `PAPER_NOT_SPECIFIED` / 后续工程决策：

- multistage driver 的具体 schematic；
- driver IC；
- `Rg`；
- decoupling；
- rail generation；
- 0 V precondition 具体实现；
- exact state-control circuit；
- PCB stackup/layout/parasitics；
- probe/oscilloscope 细节；
- power sequencing / interlock / protection；
- EasyEXPERT 具体工作流。

这满足 SP1 的关键边界要求。

## 3. Master 对 A-N Gate 的最终判定

| Gate | Master 判定 |
|---|---|
| A. Fig. 3测试状态完整定义 | PASS |
| B. calibration / positive / negative流程完整定义 | PASS |
| C. `tpre / tstr / tmea / tdly` 已定义 | PASS |
| D. 约100 ns论文含义明确 | PASS |
| E. MI / MP / MN 已定义 | PASS |
| F. `VDS → IDS → Vth` 链明确 | PASS |
| G. B1505与高速测试职责分开 | PASS |
| H. PCB与外部仪器边界已定义，并正确标为工程分配 | PASS |
| I. 关键需求有REQ编号 | PASS |
| J. 每个关键REQ有verification思路 | PASS |
| K. 论文未公开内容已列出 | PASS |
| L. 未擅自进入SP2/SP3电路设计 | PASS |
| M. 未猜测未公开参数 | PASS |
| N. `PAPER FACT / ENGINEERING INFERENCE / PROJECT DESIGN CHOICE` 分离 | PASS |

## 4. 不阻止 SP1 完成、但阻止 G0 直接 PASS 的项目级 OPEN 项

以下项目不是 SP1 缺陷，而是必须由 Master / G1 / G2 冻结的工程内容：

1. 项目 `tdly` 的精确验收定义：起点、终点、search window、filter、ringing、deskew/de-embedding，以及最终采用 `<100 ns`、`≤100 ns` 还是其他表达；
2. `VDS≈VDS-C` 的允许误差带；
3. `IDM-P/N` 相对 `IDM-I` 的项目 PASS 范围；
4. `tpre` 最低时长 / reset complete 判据；
5. `tmea` 和 MI/MP/MN extremum extraction 算法；
6. self-heating 的项目级限制；
7. SAFE_OFF、上电/掉电顺序、interlock、protection；
8. 目标 DUT 的 `VDS-C`、`Ith`、stress 电压、measurement 电压和温度；
9. canonical `docs/requirements.md` 需要与 SP1 的 36 条分类需求做一次正式合并/追溯，避免旧的项目设计选择与论文需求混在同一层级。

## 5. 新增的项目范围约束：650 V + 3.3 kV DUT

Master 记录后续项目讨论形成的新项目要求：本平台目标是用于 **650 V-class 和 3.3 kV-class SiC MOSFET 的低 `VDS` BTI / Vth hysteresis 测试**。

这不要求测试 PCB 承受 DUT 的 650 V 或 3.3 kV blocking rating，因为当前实验不是 breakdown test；实际 drain bias 由 BTI measurement / calibration 条件决定。

不同 DUT 的 `Qg`、推荐 `VGS`、`Vth`、`VGM`、`Ith`、`VDS-C`、封装和 Kelvin Source 条件仍需在 G1/G2 分别验证。

该要求属于 **PROJECT REQUIREMENT**，不是 P1 的 PAPER FACT，因此不回写为 SP1 论文结论。

## 6. Master 决策

- **DECISION 1：批准 SP1-v0.2 + SP1-FGR-v1.0。**
- **DECISION 2：SP1 关闭，不再继续增加论文方法内容；后续新增工程内容进入 G0/G1/G2，而不是回填 SP1。**
- **DECISION 3：G0 暂时保持 ACTIVE，直到项目级 acceptance 与 canonical requirements 合并完成。**
- **DECISION 4：允许 G1 系统架构继续推进；G2 可开始 datasheet/计算准备，但 G3 KiCad 原理图仍保持 BLOCKED。**

## 7. 下一步

下一步不是继续读 P1，而是执行 **G0 Closing + G1 System Architecture**：

1. 把 SP1 的 36 条需求与当前 `docs/requirements.md` 合并成一个 canonical requirement baseline；
2. 加入 650 V / 3.3 kV low-VDS BTI 通用性项目需求；
3. 画完整系统方框图；
4. 冻结 PCB 与 pulse generator / DC supply / DUT / RL / scope / B1505 的接口；
5. 列出 G0 中仍必须在 G2 前决定和可以延后到 prototype validation 决定的 acceptance items。

---

**MASTER FINAL VERDICT: SP1 APPROVED AND COMPLETE; G0 REMAINS ACTIVE.**
