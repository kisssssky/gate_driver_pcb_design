# SiC MOSFET BTI Fast Gate Driver PCB / Fig. 3 Reproduction

## SP1 — 论文方法与系统需求报告

- 版本：SP1-v0.2
- 审计修订：Requirement Audit（2026-08-24）
- 日期：2026-08-24
- 状态：需求草案，等待 Master 冻结开放项
- 唯一证据源：Xu Li, Xiaochuan Deng, Jingyu Huang, Xuan Li, Wanjun Chen, and Bo Zhang, “Accurate Evaluation of Threshold Voltage Hysteresis in SiC MOSFET Under Switching Stress,” *IEEE Transactions on Power Electronics*, vol. 39, no. 11, pp. 14118–14121, Nov. 2024, DOI: 10.1109/TPEL.2024.3409570（下文记为 P1）。

## 0. 证据分类与工作边界

本报告采用以下标签，避免把工程常识写成论文事实：

- **PAPER FACT**：P1 正文、图、表或公式直接支持。
- **PAPER EXAMPLE VALUE**：P1 在其 1200 V、TO-247 商用 DUT 上使用或展示的数值，不自动成为其他 DUT 的通用需求。
- **ENGINEERING INFERENCE**：由 P1 拓扑、波形或公式推导，但 P1 未直接表述。
- **PROJECT DESIGN CHOICE**：本项目后续需要决定的实现方式，不属于论文结论。
- **UNKNOWN / PAPER_NOT_SPECIFIED**：P1 没有公开，禁止在 SP1 中补全。

本报告不选择驱动 IC、`Rg`、电容、开关器件、继电器、0 V clamp 拓扑，不画原理图/PCB，不生成 BOM，不进行 LTspice 仿真。

### 0.1 Requirement Audit 结论

本次审计逐页复核 P1 Fig. 2-4、Table I、式 (1)-(5)、Fig. 6-10 及相关正文。审计没有新增设计内容，也没有改动论文公式。v0.1 的方法主链正确，但有若干陈述把“实验展示”“部分定义”或“系统分工推导”写得过于确定。v0.2 已逐项修正如下。

| Audit ID | v0.1 问题 | 判定 | v0.2 修正 |
|---|---|---|---|
| AUD-001 | 把 `tdly` 起点写成确定的“stress removal / gate transition starts”。 | AMBIGUOUS | P1 定义 `tdly` 为 stress end 与 measurement 之间的 test delay；Fig. 6(b)/7(b) 以名义 `t=0` 的 stress-to-measurement switching boundary 为起点、以 measured point 为终点，但未规定控制事件或 `VGS` 电压 crossing。精确电气起点改为 PAPER_NOT_SPECIFIED。 |
| AUD-002 | 把正文的 `<100 ns` 直接写成复现系统的论文规范性 PASS。 | UNSUPPORTED | P1 报告其平台在典型波形中 `tdly<100 ns`，摘要/结论概述为 100 ns；这是 PAPER REPORTED PERFORMANCE，不是对任意复现硬件发布的规范。项目是否采用 `<100 ns`、`≤100 ns` 或“约 100 ns”由 Master 冻结。 |
| AUD-003 | REQ-MEAS-001 将“共同时间基准、deskew”混入论文直接需求。 | UNSUPPORTED | 同时观察 `VGS`/`VDS` 可由 Fig. 6/7 支持；共同时间基准是提取时间差所需的 ENGINEERING INFERENCE；deskew 规则为 PROJECT REQUIREMENT，P1 未公开。 |
| AUD-004 | PCB、pulse generator、scope 等职责分配以“必须”陈述，未统一标出分配来源。 | UNSUPPORTED | 保留用户要求的功能边界，但明确整段属于 SYSTEM INTERFACE ALLOCATION；只有 `VDC` supply、`VGS` signal generator、oscilloscope、testing board、B1505 等论文明确出现的设备事实为 PAPER FACT，具体功能归属为 ENGINEERING INFERENCE/PROJECT REQUIREMENT。 |
| AUD-005 | REQ-FUNC-002 的“每条包含 precondition/stress/measurement”可能被读成 Calibration 也含 stress。 | ERROR | 改为三条各自序列：Calibration=`PRECONDITION→MEASUREMENT_I`；Positive/Negative=`PRECONDITION→对应 STRESS→对应 MEASUREMENT`。 |
| AUD-006 | REQ-FUNC-004 可被读成 MI 后也必须出现 recovery。 | UNSUPPORTED | 改为捕获 MI/MP/MN；仅 MP/MN 后的恢复趋势是 P1 明确讨论的 stress-recovery 行为。 |
| AUD-007 | REQ-TIME-002 把“论文平台达到的结果”与“项目 requirement”混为同一分类。 | ERROR | 改为 PROJECT REQUIREMENT，来源是 PAPER PERFORMANCE REFERENCE；数值关系与事件算法均保持 OPEN。 |
| AUD-008 | REQ-MEAS-010 的验证引入温升代理、pulse energy 等未由 P1 指定的方法。 | OUT_OF_SCOPE | SP1 仅保留 P1 的功能原则“positive-stress `IDS` should be minimized”；具体热测方法和限值交由后续子项目/Master。 |
| AUD-009 | REQ-CTRL-003 可能被理解为最小 Fig. 3 功能复现的强制基线。 | OUT_OF_SCOPE | 标为 OPTIONAL PROJECT-SCOPE REQUIREMENT；仅在 Master 批准 full-paper/Fig. 10 reproduction 时生效。 |
| AUD-010 | B1505 与 EasyEXPERT 并列表述可能暗示 P1 指定了 EasyEXPERT。 | UNSUPPORTED | 明确 P1 只指定 Keysight B1505；EasyEXPERT 软件、配置和工作流全部 PAPER_NOT_SPECIFIED。 |
| AUD-011 | Negative stress 的 blocking/`IDS≈0` 容易被读成论文公式。 | AMBIGUOUS | 保持为 ENGINEERING INFERENCE；P1 只明确 `VGS-N` 导致负 `Vth` shift，并在 Fig. 3(b3) 画出高 `VDS`，没有负应力状态方程。 |
| AUD-012 | SAFE_OFF、sequencing、protection 可能被误读为 Fig. 3 复现事实。 | OUT_OF_SCOPE | 保留为明确的 PROJECT REQUIREMENT / OPEN，不进入 Confirmed paper facts；具体电路、阈值和拓扑不属于 SP1。 |

### 0.2 十二项审计问题回答

| 检查项 | 审计结果 |
|---|---|
| 1. 未明确论文信息被当作事实 | 有，主要是 `tdly` 精确起点与设备职责分配；已修正。 |
| 2. PAPER FACT / ENGINEERING INFERENCE | v0.1 局部混淆；已按 AUD-001/003/004/011 分离。 |
| 3. 论文参数 / PCB 选择 | 未发现把 Si8273 或既有 rail 方案写成论文参数；100 ns 的规范性已重新分类。 |
| 4. 具体数值依据 | 10 V、10 mA、20 V/-5 V、10 us、2 us、0.2-200 us、5 MHz-5 kHz、`10^5 us`、±20%、1%、100 ns/1 us、32%/22% 均可在 P1 找到；全部标为论文 DUT/实验值或 reported result，而非通用设计值。 |
| 5. REQ 可追溯性 | 36 个 ID 均保留；每条重新标为 PAPER REQUIREMENT、PAPER-PERFORMANCE-DERIVED PROJECT REQUIREMENT、ENGINEERING INTERFACE REQUIREMENT、PROJECT REQUIREMENT 或 OPTIONAL PROJECT-SCOPE REQUIREMENT。 |
| 6. `tdly` 起止 | 论文层面部分清楚、工程层面不完整；见 5.3。 |
| 7. MI/MP/MN | 准确：三者是 measured potential points；在高速波形中以 `VDS` 点识别，不是电流或阈值本身。 |
| 8. `VGM-I/P/N` | 准确：`VGM-I=initial Vth`；`VGM-P/N` 分别调节到 `IDM-P/N≈IDM-I`，论文未要求三者相等。 |
| 9. B1505 / 高速 PCB measurement | 已正确区分；v0.2 进一步明确 B1505 提供慢扫基准曲线，高速平台/示波器提供点测波形。 |
| 10. 设备边界 | 功能边界清楚，但属于系统分配而非全部论文事实；已加统一标签。 |
| 11. 是否提前进入 SP2 | v0.1 没有具体电路设计；热验证细节被判为 OUT_OF_SCOPE 并移除。 |
| 12. 是否提前选器件/拓扑 | 没有选择 Si8273 pin、`Rg`、电容、MOSFET、relay 或 0 V clamp 拓扑。 |

## 1. Executive Summary

P1 的方法不是直接用高速示波器扫描完整的 `IDS`–`VGS` 曲线，而是先用 Keysight B1505 在固定 `VDS-C` 下取得基准扫栅曲线，再用 Fig. 3 的电阻负载回路完成一个快速“点测量”。测量回路从 precondition 或 stress 栅压快速切换至接近阈值区的 measurement gate voltage；此时 DUT 处于不完全导通状态，`VDS` 的瞬时极值给出 MI、MP 或 MN。由

```text
IDS=(VDC - VDS) / RL
```

得到测量电流，再把该电流映射回 B1505 基准曲线，获得等效栅压位置和阈值位移。

三条核心序列是：

1. Calibration：`0 V → VGM-I`，得到 MI 和测试方案自身的初始位移 `Vth-IS`；
2. Positive stress：`0 V → VGS-P → VGM-P`，得到 MP 和 `Vth-PS`；
3. Negative stress：`0 V → VGS-N → VGM-N`，得到 MN 和 `Vth-NS`。

`VGM-P` 与 `VGM-N` 不是必须等于 `VGM-I`，也不是必须彼此相等。P1 要求分别调节它们，使 MP/MN 对应的 `IDM-P`、`IDM-N` 接近校准电流 `IDM-I`，同时使测量点的 `VDS ≈ VDS-C`。

P1 将 `tdly` 定义为 stress 结束与 measurement 之间的 test delay。Fig. 6(b)/Fig. 7(b) 进一步从名义 `t=0` 的 stress-to-measurement switching boundary 标到 `VDS` measured point，图示为 100 ns；正文称 `tdly<100 ns`，摘要/结论概述为 100 ns。终点与 MP/MN measured point 的联系得到正文支持，但 P1 没有规定起点是控制事件还是某个 `VGS` crossing，也没有定义极值算法、滤波、搜索窗或振铃处理。因此论文定义只能支持系统级事件链，不能形成无歧义的 PCB PASS/FAIL。

## 2. Paper Method Summary

### 2.1 方法逻辑

1. 用 B1505 在固定 `VDS-C` 下做慢速阶梯式 `VGS` 扫描，获得初始 `IDS`–`VGS` 曲线。
2. 定义阈值电流 `Ith`；基准曲线上 `IDS=Ith` 时的 `VGS` 是 initial `Vth`。
3. 在 Fig. 3 电阻负载平台上执行长时间 0 V precondition，使论文所称的 SiO₂/SiC interface state 被 reset，并消除前次实验的 hysteresis 影响。
4. Calibration 中将 `VGS` 快速切至 `VGM-I=initial Vth`；DUT 进入不完全导通，记录 `VDS` 极值 MI。
5. 用 MI 对应的 `VDS` 计算 `IDM-I`，再映射回 B1505 曲线得到 `Vth-MI`，计算 `Vth-IS`。
6. Positive/negative stress 测试采用相同 precondition，然后施加 `VGS-P` 或 `VGS-N`，持续 `tstr`；stress 结束后快速切至各自的 `VGM-P` 或 `VGM-N`，捕获 MP 或 MN。
7. 保持 `VDC` 和 `RL` 不变，分别调节 `VGM-P`、`VGM-N`，使 `IDM-P`、`IDM-N` 接近 `IDM-I`。
8. 通过与式 (3) 相同的映射方法得到包含测试方案自身初始位移的 `Vth-PS`、`Vth-NS`，再减去 `Vth-IS`，得到校正后的 `ΔVth`。
9. 改变 `tstr` 和 `tdly`，得到不同测试点/频率下的 `ΔVth` 及 recovery。

### 2.2 P1 给出的关键实验事实

- DUT：商用 1.2 kV、TO-247 SiC MOSFET；确切型号未公开。
- `Ith=10` mA，`VDS-C=10` V。
- 典型 stress：`VGS-P/VGS-N=20 V/-5 V`。
- 典型波形：`tstr=10 µs`，正文关联 50 kHz。
- 另一处实验：500 kHz stress 对应 `tstr=2 µs`。
- `tstr` 扫描范围写为 0.2–200 µs，并关联 5 MHz–5 kHz。
- 多脉冲 gate stress 总时长为 `10^5 µs`，用于恢复 premeasurement trap occupation state 并获得稳定 `ΔVth`。
- `IDM-P`、`IDM-N` 相对 `IDM-I` 的偏差在论文实验中低于 ±20%，论文认为相应 `ΔVth` 偏差可接受。
- 在 `IDS` 接近 `Ith` 时，Fig. 8(a) 所示平行移位验证中 `ΔVth` 波动在 1% 内。
- 500 kHz stress 后，以 1 µs 测得的正/负 `ΔVth` 相比 100 ns 分别低 32%/22%。

### 2.3 Numeric Traceability Audit

| 数值 | P1 位置 | 证据分类 | v0.2 使用限制 |
|---|---|---|---|
| 1.2 kV、TO-247 | §III 首段 | PAPER EXAMPLE VALUE | 仅描述论文 DUT；型号仍未知。 |
| `Ith=10 mA` | §III 首段 | PAPER EXAMPLE VALUE | 不冻结为本项目目标 DUT 的 `Ith`。 |
| `VDS-C=10 V` | §III step 1 | PAPER EXAMPLE VALUE | 不冻结为本项目 calibration drain bias。 |
| `VGS-P/VGS-N=20 V/-5 V` | §III、Fig. 6/7 说明 | PAPER EXAMPLE VALUE | 不冻结为 PCB rail 或 stress limit。 |
| `tstr=10 us`、50 kHz | §III、Fig. 6/7 前正文 | PAPER REPORTED PAIR | P1 未给 duty-cycle/换算定义，不能自行推导。 |
| `tstr=2 us`、500 kHz | §III、Fig. 10 讨论 | PAPER REPORTED PAIR | 同上。 |
| `tstr=0.2-200 us`、5 MHz-5 kHz | §III、Fig. 10 讨论 | PAPER REPORTED RANGE | 仅为实验扫描范围；是否复现由 Master 决定。 |
| total stress duration=`10^5 us` | §III、Fig. 10 前正文 | PAPER EXAMPLE VALUE | 仅适用于论文 multiple-pulse protocol。 |
| `tdly=100 ns` / `<100 ns` | Abstract、Fig. 6/7、§III、Conclusion | PAPER REPORTED PERFORMANCE | 图示/摘要/结论为 100 ns，§III 写 `<100 ns`；不是已冻结的项目 PASS。 |
| `tdly=1 us` 与 `0.1 us (100 ns)` | Abstract、§III、Fig. 10、Conclusion | PAPER TEST CONDITIONS | 用于 delay comparison，不是 PCB 固定 delay set。 |
| positive/negative reduction 32%/22% | Abstract、§III、Conclusion | PAPER REPORTED RESULT | Abstract 使用“more than 32%/22%”，§III/Conclusion 写 32%/22%；v0.2 保留该措辞差异。 |
| `IDM-P/N` deviation lower than ±20% | §III、Fig. 8(b) 讨论 | PAPER REPORTED ACCEPTED EXPERIMENT RANGE | P1 未定义百分比公式，也未证明对其他 DUT 通用。 |
| `ΔVth` fluctuation within 1% near `Ith` | §III、Fig. 8(a) 讨论 | PAPER REPORTED RESULT | 仅是论文器件/条件下对近似平行移位的验证结果。 |

## 3. Variable Definition Table

| 量/术语 | 名称与物理意义 | 何时出现 | 类型 | P1 是否给值 | PCB 是否直接支持 | 论文依据/状态 |
|---|---|---|---|---|---|---|
| Calibration | Fig. 3 平台与 B1505 之间偏差的预校准 | 正/负 stress 测试前 | 流程 | 无单一数值 | 是，需执行 `0→ VGM-I`；B1505/软件也参与 | §II；PAPER FACT |
| Initial sweeping curve | B1505 得到的初始 `IDS`–`VGS` 基准曲线 | 所有快速测量前 | 测量数据/查找表 | 扫描细节未给；实验 `VDS-C=10` V | 否；由 B1505 完成 | Fig. 2、§II/III；PAPER FACT |
| `VDS-C` | B1505 sweep 使用的固定 drain-source calibration bias；也是快速测量点希望对齐的 `VDS` | B1505 sweep、MI/MP/MN 对齐 | 控制量/比较基准 | 10 V（论文 DUT） | PCB 不生成其定义，但测量回路须能形成并测到该 `VDS` | §II、§III step 1；PAPER EXAMPLE VALUE |
| `Ith` | 在基准 sweep 上定义 initial `Vth` 的 threshold current | 初始阈值定义 | 分析控制量 | 10 mA（论文 DUT） | 否；B1505/后处理使用 | Fig. 1、Table I、§III；PAPER EXAMPLE VALUE |
| Initial `Vth` | 基准曲线上 `IDS=Ith` 对应的 `VGS` | Calibration 前 | 计算/提取量 | 数值未给 | 间接；用于设 `VGM-I` | §I/II；PAPER FACT |
| `VGM-I` | MI 处的 gate voltage；Calibration 中设为 initial `Vth` | MEASUREMENT_I | 控制量 | 数值未给 | 是，需形成该栅压 | Table I、式 (2)；PAPER FACT |
| `VGM-P` | MP 处的 gate voltage；为电流/电压对齐而单独调节 | MEASUREMENT_P | 控制量 | 数值未给 | 是，需独立可调 | Table I、§II；PAPER FACT |
| `VGM-N` | MN 处的 gate voltage；为电流/电压对齐而单独调节 | MEASUREMENT_N | 控制量 | 数值未给 | 是，需独立可调 | Table I、§II；PAPER FACT |
| `VGS-P` | Positive gate stress voltage | POSITIVE_STRESS | 控制量 | +20 V（论文示例） | 是，需形成正应力栅压 | Table I、§III；PAPER EXAMPLE VALUE |
| `VGS-N` | Negative gate stress voltage | NEGATIVE_STRESS | 控制量 | −5 V（论文示例） | 是，需形成负应力栅压 | Table I、§III；PAPER EXAMPLE VALUE |
| MI | 无 stress 的 initial measured potential point；`VDS` 极值 | `0→ VGM-I` 后 | 直接波形特征 | 未给 | PCB 提供可探测节点；示波器采集 | Table I、§II；PAPER FACT |
| MP | Positive stress 后的 measured potential point；`VDS` 最大值 | `VGS-P→ VGM-P` 后 | 直接波形特征 | 未给 | 同上 | Fig. 3(b2)、§II；PAPER FACT |
| MN | Negative stress 后的 measured potential point；`VDS` 最小值 | `VGS-N→ VGM-N` 后 | 直接波形特征 | 未给 | 同上 | Fig. 3(b3)、§II；PAPER FACT |
| `IDM-I` | MI 处的 `IDS` | MEASUREMENT_I | 由 `VDS` 计算 | 数值未给 | 间接支持 | Table I、式 (2)；PAPER FACT |
| `IDM-P` | MP 处的 `IDS` | MEASUREMENT_P | 由 `VDS` 计算 | 数值未给；要求接近 `IDM-I` | 间接支持 | Table I、§II/III；PAPER FACT |
| `IDM-N` | MN 处的 `IDS` | MEASUREMENT_N | 由 `VDS` 计算 | 数值未给；要求接近 `IDM-I` | 间接支持 | Table I、§II/III；PAPER FACT |
| `Vth-MI` | B1505 曲线上与 `IDM-I` 对应的 gate voltage | Calibration 后处理 | 查表/插值结果 | 未给 | 否 | Table I、式 (3)；PAPER FACT |
| `Vth-MP` | B1505 曲线上与 `IDM-P` 对应的等效 gate voltage | Positive 后处理 | 查表/插值结果 | 符号未在 Table I 单列，数值未给 | 否 | “same method as (3)”；方法直接含义，符号为 ENGINEERING RESTATEMENT |
| `Vth-MN` | B1505 曲线上与 `IDM-N` 对应的等效 gate voltage | Negative 后处理 | 查表/插值结果 | 同上 | 否 | 同上；ENGINEERING RESTATEMENT |
| `Vth-IS` | 测试方案自身的 initial `Vth` shift，在 MI 得到 | Calibration | 计算量 | 未给 | 否；软件计算 | Table I、式 (3)；PAPER FACT |
| `Vth-PS` | MP 测得、包含 `Vth-IS` 的 positive-stress `Vth` shift | Positive 后处理 | 计算量 | 未给 | 否 | Table I、§II；PAPER FACT |
| `Vth-NS` | MN 测得、包含 `Vth-IS` 的 negative-stress `Vth` shift | Negative 后处理 | 计算量 | 未给 | 否 | Table I、§II；PAPER FACT |
| `ΔVth` | 扣除 `Vth-IS` 后的准确阈值位移 | 最终结果 | 计算量 | 多组结果在 Fig. 9/10，非固定值 | 否 | Table I、式 (5)；PAPER FACT |
| `tpre` | Precondition procedure 的持续时间 | 每次 calibration/stress 前 | 控制量 | “long-term”；无明确数值/判据 | 是，系统时序需支持 | Table I、§II；PAPER_NOT_SPECIFIED（数值） |
| `tstr` | Stress procedure 的持续时间 | POSITIVE/NEGATIVE_STRESS | 控制量 | 典型 10 `µs`；2 `µs`；范围 0.2–200 `µs` | 是，系统时序需支持 | Table I、§III；PAPER EXAMPLE VALUES |
| `tmea` | Measurement procedure 的时间区间 | MEASUREMENT_I/P/N | 控制/采集窗口 | 无明确时长 | 是，保持 measurement 电位并允许采集 | Table I、Fig. 3/4；PAPER_NOT_SPECIFIED（数值） |
| `tdly` | Stress end 与 measurement 之间的 test delay；Fig. 6/7 将 measured point 作为图示终点 | stress→measurement 过渡早期 | 测量性能量 | 图示 100 ns；正文称 <100 ns；摘要/结论称 100 ns | 系统级直接相关，不能只等同 gate edge | §I/III、Fig. 6/7；PAPER FACT（概念/结果）+ AMBIGUOUS（精确起点/算法） |
| Hysteresis | 界面/氧化层陷阱捕获/释放引起的快速、可恢复 `Vth` shift；也包括慢 sweep 与快点测差异形成的测试方案初始偏差 | sweep、stress、recovery | 物理效应 | 无单一数值 | PCB 只用于施加/捕获，不直接“产生需求值” | §I/II；PAPER FACT |
| Recovery | stress removal 后 `Vth` shift 随时间快速恢复；正 stress 后 `VDS` 从 MP 下降，负 stress 后从 MN 上升 | MEASUREMENT_P/N | 被测动态行为 | 1 `µs` 与 100 ns 比较给出 32%/22%低估 | PCB/示波器需足够快地捕获 | §I/II/III；PAPER FACT |
| Fixed `VDS` | B1505 扫描时 `VDS` 保持为 `VDS-C` | 初始 calibration sweep | 控制条件 | 10 V（论文示例） | 否；参数分析仪完成 | §I/II/III；PAPER FACT |
| Resistive load | `VDC→ RL→`DUT 的串联负载回路 | 所有 Fig. 3 快速测试 | 系统拓扑 | 拓扑给出；器件细节无 | PCB/外部回路共同支持 | Fig. 3(a)；PAPER FACT |
| `RL` | 控制回路 `IDS` 的负载电阻 | 所有快速测试 | 控制/硬件参数 | 数值未给 | 需由 DUT/`VDC` 回路实现，不限定必须在 PCB | §II；PAPER_NOT_SPECIFIED（值/实现） |
| `VDC` | 电阻负载回路的 DC bias | 所有快速测试 | 控制量 | 数值未给 | 由外部供电，PCB/回路需接口 | Fig. 3(a)、§II；PAPER_NOT_SPECIFIED（值） |
| `RDUT` | measurement 状态下 DUT 等效电阻，受 `Vth` shift 与 `VGS` 影响，通常大于额定 `Ron` | MEASUREMENT_I/P/N | 隐含状态量/计算模型 | 未给 | 不直接控制 | 式 (2)、§II；PAPER FACT |

## 4. State Table

State、gate/drain/`IDS` 行为和论文依据列按 P1 取证；“PCB 完成/外部仪器完成”两列是为后续系统划分建立的 **ENGINEERING INTERFACE ALLOCATION**，不是 P1 公布的硬件端口实现。

| State | Gate target | Drain condition | `IDS` condition | 目的 | 进入条件 | 退出条件 | 持续时间 | 高速切换要求 | PCB 完成 | 外部仪器完成 | 论文依据/状态 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SAFE_OFF | PROJECT_DESIGN_CHOICE_TO_BE_DEFINED | 建议性安全状态尚未冻结 | 未定义 | 上电、故障、待机安全 | 项目状态机决定 | 安全条件满足后进入测试 | 未定义 | 未定义 | 必须预留可验证的安全状态功能，但具体电位/拓扑由后续决定 | DC supply/pulse source 的安全配合待定义 | P1 无此状态；PAPER_NOT_SPECIFIED |
| PRECONDITION | `VGS=0` V | `VDS=VDC` | `IDS=0` | reset SiO₂/SiC interface state，消除前次实验 hysteresis | 每次 calibration/positive/negative 序列开始 | 满足 precondition 时长/重置判据后进入下一状态 | `tpre`；“long-term”，数值未知 | P1 称之后“quickly switches”；只有后续 stress→measurement 与 `tdly` 直接绑定 | 形成 0 V gate target 并保持 | `VDC` 保持；控制源定时；示波器可监测 | 式 (1)、Fig. 3(b1–b3)；PAPER FACT |
| POSITIVE_STRESS | `VGS=VGS-P` | `VDS≈0` | `IDS=(VDC-VDS)/RL≈ VDC/RL` | 施加正栅压应力，使 `Vth` 正移 | PRECONDITION 结束 | `tstr` 到期，转 MEASUREMENT_P | `tstr` | **是**；该边界属于 `tdly` 事件链，但精确起点未定义 | 形成并保持 `VGS-P`，随后转 measurement level | `VDC`/`RL` 形成低电流回路；控制源/示波器职责为系统分配 | 式 (4)、Fig. 3(b2)；PAPER FACT + ENGINEERING INTERFACE ALLOCATION |
| NEGATIVE_STRESS | `VGS=VGS-N` | Fig. 3(b3) 描绘为高 `VDS` | 串联回路可推得电流很小，但 P1 未给负应力状态公式 | 施加负栅压应力，使 `Vth` 负移 | PRECONDITION 结束 | `tstr` 到期，转 MEASUREMENT_N | `tstr` | **是**；该边界属于 `tdly` 事件链，但精确起点未定义 | 形成并保持 `VGS-N`，随后转 measurement level | 同上 | Fig. 3(b3)、§II；PAPER FACT（波形/效应）+ ENGINEERING INFERENCE（状态电流） |
| MEASUREMENT_I | `VGS=VGM-I=initial Vth` | `VDS=VDCRDUT/(RL+RDUT)`，目标约等于 `VDS-C` | `IDS=IDM-I>0` | 取得 MI，量化方案自身的 `Vth-IS` | PRECONDITION 后快速切换 | 捕获 MI/完成所需 acquisition | `tmea`，数值未知 | 快速切换需要，但 P1 未将此转换定义为 `tdly` | 形成 `VGM-I`、提供低寄生测量节点 | scope 捕获 MI；软件计算；B1505 提供曲线 | 式 (2)/(3)、Fig. 3(b1)；PAPER FACT |
| MEASUREMENT_P | `VGS=VGM-P`，单独调节 | 从约 0 V 上升到最大值 MP，再因 recovery 下降；MP 目标约 `VDS-C` | `IDM-P≈ IDM-I` | 快速捕获正应力后阈值位移 | POSITIVE_STRESS 结束 | 捕获 MP，或继续观察 recovery 后退出 | `tmea`，数值未知 | **是**；stress→measurement 边界到 MP 构成论文 `tdly` 事件链，精确起点未定义 | 快速转到并保持 `VGM-P` | scope 记录 `VGS`/`VDS`；软件提取 MP | Fig. 3(b2)、Fig. 6；PAPER FACT + AMBIGUOUS（起点） |
| MEASUREMENT_N | `VGS=VGM-N`，单独调节 | 从高值下降到最小值 MN，再因 recovery 上升；MN 目标约 `VDS-C` | `IDM-N≈ IDM-I` | 快速捕获负应力后阈值位移 | NEGATIVE_STRESS 结束 | 捕获 MN，或继续观察 recovery 后退出 | `tmea`，数值未知 | **是**；stress→measurement 边界到 MN 构成论文 `tdly` 事件链，精确起点未定义 | 快速转到并保持 `VGM-N` | 同上 | Fig. 3(b3)、Fig. 7；PAPER FACT + AMBIGUOUS（起点） |

### 4.1 State Table 的七个关键结论

1. **precondition 为什么是 0 V？** P1 直接说明：长时间 precondition 用于 reset SiO₂/SiC interface state，消除前次实验造成的 hysteresis；式 (1) 同时规定 `VGS=0`、`VDS=VDC`、`IDS=0`，DUT 为 blocking state。P1 未给出微观 reset 判据、持续时间或完成检测方法。
2. **positive stress 时 DUT 状态：** 完全导通，`Ron≪ RL`，所以 `VDS≈0`、`IDS≈ VDC/RL`。P1 要求尽量减小 `IDS` 以避免 self-heating 影响阈值测量。
3. **negative stress 时 DUT 状态：** Fig. 3(b3) 显示负栅压期间 `VDS` 保持高位；结合回路可推得 DUT 阻断、`IDS` 近零，但 P1 没有给出与式 (4) 对应的负应力公式。因此“阻断/近零电流”中，波形是 PAPER FACT，精确电流关系是 ENGINEERING INFERENCE。
4. **measurement 不是简单关断：** 式 (2) 明确称其为 incomplete turn-ON；`VGS` 设在测量栅压、`RDUT` 有限、`IDS` 非零，必须形成可映射到基准曲线的 `VDS`/`IDS` 点。
5. **`VGM-I`、`VGM-P`、`VGM-N` 不必相同：** `VGM-I` 设为 initial `Vth`；`VGM-P`、`VGM-N` 要分别调整，以补偿 stress 引起的 `RDUT` 变化。
6. **为什么调 measurement gate voltage：** 使 MP/MN 的 `IDM-P`、`IDM-N` 接近 `IDM-I`，并使测量点 `VDS≈ VDS-C`，从而与同一 B1505 calibration curve 对齐，降低电流不一致导致的 `ΔVth` 误差。
7. **哪次 transition 决定 `tdly`：** POSITIVE_STRESS→MEASUREMENT_P 和 NEGATIVE_STRESS→MEASUREMENT_N 是相关状态边界。Calibration 的 PRECONDITION→MEASUREMENT_I 也被 P1 描述为快速切换，但 100 ns 图示针对 stress→measurement。边界内采用哪个电气事件作为计时起点，P1 未规定。

## 5. Timing Definition

### 5.1 四个时间量

- `tpre`：0 V precondition procedure。其功能是重置界面状态并消除前次实验的 hysteresis；P1 只写“long-term”，未给统一数值和完成判据。
- `tstr`：`VGS-P` 或 `VGS-N` stress procedure 的持续时间。P1 改变 `tstr` 研究不同 stress point/frequency 下的 `ΔVth`。
- `tmea`：measurement gate level 被施加并采集 `VDS` 的 measurement procedure。MP/MN 极值和随后的 recovery 都发生在该区间；P1 未给固定长度。
- `tdly`：P1 的文字定义是 stress end 与 measurement 之间的 test delay；Fig. 6/7 的图示终点为 `VDS` measured point，正文把它与最大/最小 measurement point 联系起来。它属于 `tmea` 前部的系统级延迟，不等于整个 `tmea`。P1 没有把它定义为 driver propagation delay 或 rise/fall time，也没有给出起点 crossing。

### 5.2 ASCII timing diagrams

以下图仅表达事件顺序，不按幅值或时间比例绘制。

Calibration：

```text
                         MEASUREMENT_I
VGS      PRECONDITION       VGM-I
         0 V             +-----------
---------+---------------/             ...
         <---- tpre ----><--- tmea --->

VDS      VDC                MI = VDS extreme
---------+---------------\____*________ ...

time --------------------|-------------------->
                         fast 0 V -> VGM-I
```

Positive stress：

```text
         PRECONDITION       POSITIVE_STRESS        MEASUREMENT_P
VGS      0 V                VGS-P                  VGM-P
---------+---------------+  +-------------------+  +-------------
                         | /                    | /               ...
                         +/                     +/
         <---- tpre ---->  <------ tstr ------>  <---- tmea ---->

VDS      VDC                approximately 0        rise to MP, then recovery
---------+----------------\______________________/---*\__________ ...
                                                      MP
time ---------------------------------------------|----|--------->
                                                  nominal t=0 boundary
                                                        measurement point
                                                  <tdly>
```

Negative stress：

```text
         PRECONDITION       NEGATIVE_STRESS        MEASUREMENT_N
VGS      0 V                VGS-N                  VGM-N
---------+---------------+                         +-------------
                         |\_______________________/                ...
         <---- tpre ---->  <------ tstr ------>  <---- tmea ---->

VDS      VDC                high / near VDC         fall to MN, then recovery
--------------------------------------------------\___*__/------- ...
                                                      MN
time ---------------------------------------------|----|--------->
                                                  nominal t=0 boundary
                                                        measurement point
                                                  <tdly>
```

### 5.3 “100 ns”原始定义与工程验收定义

**论文原始定义（PAPER FACT）：** §I 将 `tdly` 定义为 stress end 与 measurement 之间的时间间隔。Fig. 6(b)/Fig. 7(b) 把名义 `t=0` 放在 stress→measurement 转换边界，`tdly` 箭头终点是 `VDS` 的 measured point；§III 说明 `VGS` 从 stress 切到 measurement 后，`VDS` 到达最大/最小 measurement point，且 `tdly<100 ns`。摘要和结论将结果概述为 100 ns。

**论文歧义（AMBIGUOUS）：** P1 足以说明 `tdly` 是包含 gate transition 与 DUT `VDS` response 的系统级时间，而不只是孤立的 gate edge；但它不足以确定名义 `t=0` 对应控制命令、`VGS` 边沿起点或某个 crossing。因此“100 ns 从哪个可重复电气阈值算起”无法由论文唯一回答。

**PAPER_NOT_SPECIFIED：**

- stress removal 是控制命令时刻、`VGS` 边沿起点、10%/50%/90% crossing，还是离开 stress tolerance band；
- measured point 是原始波形全局极值、规定窗口内极值、滤波后极值，还是进入 settling band；
- 是否扣除 pulse generator、driver、probe、channel skew 或 cable propagation delay；
- 示波器带宽、采样率、探头带宽、deskew 和插值方式；
- 振铃导致多个局部极值时如何选择 MP/MN。

**未来 PCB engineering acceptance definition（PROJECT DESIGN CHOICE，尚未冻结）：** 必须由 Master 明确起点事件、终点算法、通道 deskew/de-embedding、搜索窗口和噪声/振铃规则，之后才能把“<100 ns”变成无歧义的 PASS/FAIL。当前状态为 **ENGINEERING_ACCEPTANCE_TO_BE_DEFINED**。

## 6. Calibration / `Vth` Extraction Flow

### 6.1 P1 原始公式

Precondition blocking state，P1 式 (1)：

```text
VGS = 0, VDS = VDC, IDS = 0.  [Eq. 1]
```

- `VGS`：gate-source voltage；此处为 0 V。
- `VDS`：drain-source voltage；阻断时等于外加 `VDC`。
- `IDS`：drain-source current；论文理想式写为 0。

Calibration measurement state，P1 式 (2)：

```text
VGS = VGM-I = Vth
VDS = (VDC × RDUT) / (RL + RDUT)
```

```text
IDS = (VDC - VDS) / RL = IDM-I.  [Eq. 2]
```

- `VGM-I`：Calibration measurement gate voltage，设为 initial `Vth`。
- `RDUT`：measurement state 下 DUT 的等效电阻。
- `RL`：串联负载电阻。
- `IDM-I`：MI 点对应的 drain current。

Initial scheme shift，P1 式 (3)：

```text
Vth-IS = VGM-I - Vth-MI.  [Eq. 3]
```

- `Vth-MI`：B1505 基准 sweep 上，与 `IDM-I` 相等的电流所对应的 gate voltage。
- `Vth-IS`：慢 sweep 与快速点测方案之间的 initial shift，用于后续校正。

Positive stress state，P1 式 (4)：

```text
VGS = VGS-P, VDS ≈ 0
IDS = (VDC - VDS) / RL ≈ VDC / RL.  [Eq. 4]
```

- `VGS-P`：positive gate stress voltage。
- `Ron≪ RL` 时，DUT fully ON，`VDS` 接近 0，电流主要由 `RL` 限制。

Corrected threshold shift，P1 式 (5)：

```text
Positive stress: ΔVth = Vth-PS - Vth-IS
Negative stress: ΔVth = Vth-NS - Vth-IS  [Eq. 5]
```

- `Vth-PS`/`Vth-NS`：在 MP/MN 测得、仍包含 scheme initial shift 的正/负应力阈值位移。
- `ΔVth`：排除 `Vth-IS` 后的最终阈值位移。

P1 没有另行印出 `Vth-PS`、`Vth-NS` 的展开公式，只写明 MP/MN “using the same method as described in (3)”。因此以下是对论文方法的 **ENGINEERING RESTATEMENT**，不是新增的论文编号公式：

```text
Vth-PS = VGM-P - Vth-MP
Vth-NS = VGM-N - Vth-MN
```

其中 `Vth-MP`/`Vth-MN` 分别是 B1505 calibration curve 上与 `IDM-P`/`IDM-N` 对应的 gate voltage。

### 6.2 为什么需要 fixed `VDS-C`、`Ith` 和 gate-voltage adjustment

1. **为什么 fixed `VDS-C`：** 基准 `IDS`–`VGS` curve 必须在固定 drain bias 下建立，快速 measurement point 也要处在相近 drain bias，才能把测得电流映射到同一曲线。P1 还要求 measurement 时 DUT 在 saturation region：`VDS-C>VGS-Vth`。
2. **`Ith` 如何定义 initial `Vth`：** 在 B1505 基准 curve 上，`IDS` crossing `Ith` 时的 `VGS` 定义为 initial `Vth`。论文 DUT 使用 `Ith=10` mA。
3. **为什么实际 `VDS≈ VDS-C`：** 若 MI/MP/MN 的 drain bias 与 calibration curve 不同，同一个 `IDS` 不再对应相同的曲线位置，会破坏直接查表/插值的可比性。
4. **为什么 MI 需要映射回 calibration curve：** B1505 的慢阶梯扫栅本身会诱发阈值 shift，而 Fig. 3 快速点测得到的 MI 会偏离慢扫曲线；这个偏差正是需要量化并扣除的 `Vth-IS`。
5. **`Vth-IS` 逻辑：** 先由 MI 算 `IDM-I`，在 curve 上找 `Vth-MI`，再用实际施加的 `VGM-I` 减去它。
6. **MP/MN 逻辑：** 由 MP/MN 的 `VDS` 计算 `IDM-P/N`，映射到相同 curve，按与式 (3) 相同的方法得到 raw `Vth-PS/NS`。
7. **为什么单独调节 `VGM-P/N`：** stress 后 `RDUT` 改变，若保持同一 measurement gate voltage，MP/MN 的 `VDS` 和 `IDS` 会偏离 calibration 条件。P1 保持 `VDC`、`RL` 不变，只调 `VGM-P/N`，直到 `IDM-P/N≈ IDM-I`。
8. **hysteresis correction：** Calibration 先测出测试方案自身的 initial shift `Vth-IS`；positive/negative raw shifts 再各自减去同一个 `Vth-IS`，得到式 (5) 的 corrected `ΔVth`。

### 6.3 Drain load 与测量链

Fig. 3(a) 的电流路径为：

```text
VDC→ RL→ DUT Drain→ DUT Source→ return.
```

串联回路中 `RL` 的压降为 `VDC-VDS`，所以

```text
IDS=(VDC - VDS) / RL.
```

高速测试中不需要让参数分析仪在 100 ns 内直接扫完整曲线；只需示波器快速捕获 `VDS`，在已知 `VDC`、`RL` 下计算一个瞬时 `IDS`，再使用预先测得的 B1505 curve 完成等效 gate-voltage 映射。

```text
Oscilloscope VDS at MI/MP/MN
              |
              v
IDS = (VDC - VDS) / RL
              |
              v
B1505 fixed-VDS-C IDS-VGS calibration curve
              |
              v
Equivalent gate-voltage coordinate Vth-MI/MP/MN
              |
              v
Raw shift Vth-IS/PS/NS
              |
              v
Equation (5) correction -> Delta Vth
```

| 数据 | 来源 | 直接测量/控制/计算 |
|---|---|---|
| 基准 `IDS`–`VGS` curve | B1505 | 直接扫描测量 |
| `VDS-C`、`Ith` | B1505 test definition | 控制/分析设定 |
| Initial `Vth` | 基准 curve | 提取量 |
| `VGS` stress/measurement waveform | Fig. 3 平台 + oscilloscope | 控制并直接测量 |
| `VDS(t)`、MI/MP/MN | Fig. 3 平台 + oscilloscope | 直接测量/波形特征提取 |
| `VDC`、`RL` | DC supply/load definition | 已知控制/硬件参数；P1 未说明是否同步记录瞬时值 |
| `IDM-I/P/N` | 后处理 | 由 `VDS`、`VDC`、`RL` 计算 |
| `Vth-MI/MP/MN` | 后处理 + B1505 curve | 查表/插值计算 |
| `Vth-IS/PS/NS`、`ΔVth` | 后处理 | 公式计算 |
| `tdly` | oscilloscope `VGS`/`VDS` 波形 | 时间差提取 |

## 7. PCB vs External Equipment Boundary

**分类说明：** P1 Fig. 5 明确展示 `VDC` power supply、`VGS` signal generator、oscilloscope、`VGS` power supply 和 testing board，正文明确 Keysight B1505 用于 sweep。以下职责拆分是为项目形成可验证接口的 **ENGINEERING INTERFACE ALLOCATION**；除逐条引用的论文功能外，不应解释为 P1 公布了端口、电平、通道、触发或 PCB 内外划分。

### A. PCB 必须实现的功能

- 接收外部时序控制，并在 DUT source reference 下形成 precondition、positive stress、negative stress、measurement-I/P/N 所需 gate target。
- 支持 `0→ VGM-I`、`0→ VGS-P→ VGM-P`、`0→ VGS-N→ VGM-N` 的功能序列。
- 允许 `VGM-I`、`VGM-P`、`VGM-N` 在系统层面独立设定/调整；具体产生方式 PAPER_NOT_SPECIFIED。
- 支持 stress→measurement 的快速转换，使系统能够面向 P1 报告的约 100 ns `tdly` 性能参考；项目 PASS 尚未冻结。
- 提供 DUT gate/source 和 drain/source 的可测接口，使 `VGS` 与 `VDS` 能被同时观察；具体 probe/connector PAPER_NOT_SPECIFIED。
- 与 `VDC`–`RL`–DUT 串联回路兼容，并维持所需电压/电流/瞬态完整性；具体器件与布局由后续子项目决定。

### B. 外部 pulse generator 必须实现的功能

- 给出可重复的 state-transition command/trigger。
- 控制或触发 `tpre`、`tstr`、`tmea`，并允许改变 `tstr`、测试点和 `tdly` 相关控制时序。
- 为示波器提供稳定触发参考。
- 输出电平、极性、通道数、同步方式、抖动上限均 PAPER_NOT_SPECIFIED。

### C. 外部 DC supply 必须实现的功能

- 提供稳定 `VDC`，使 calibration 时可通过调整 `VDC` 与 `RL` 达到 MI 的 `VDS≈ VDS-C`。
- 在 subsequent stress measurement 中保持 `VDC` 不变。
- 电压范围、动态阻抗、限流、噪声、远端感测和保护均 PAPER_NOT_SPECIFIED。

### D. DUT / `RL` 回路必须实现的功能

- 实现 `VDC→ RL→ DUT→ return` 串联路径。
- `RL` 控制 positive-stress ON-state current，并应使 `IDS` 尽可能小以抑制 self-heating。
- Calibration 调整 `VDC`/`RL` 后，positive/negative 测试保持二者不变。
- `RL` 数值、脉冲功率、寄生参数、安装位置、技术类型均 PAPER_NOT_SPECIFIED。

### E. Oscilloscope 必须测量的内容

- 同时捕获 `VGS(t)` 和 `VDS(t)`。
- 识别 MI、MP、MN 及其时刻。
- 从 stress→measurement 的 `VGS` 事件到 MP/MN 提取 `tdly`。
- 观察 measurement 后 recovery 波形。
- 带宽、采样率、探头、deskew、滤波/平均均 PAPER_NOT_SPECIFIED。

### F. B1505 calibration 必须完成的内容

- 在固定 `VDS-C` 下获得 initial `IDS`–`VGS` sweep curve。
- 用 `Ith` 定义 initial `Vth`。
- 导出可用于 `IDM-I/P/N→ Vth-MI/MP/MN` 映射的数据。
- sweep range、step、rate、方向、hold time、温度与 compliance 除论文所述条件外均 PAPER_NOT_SPECIFIED。
- P1 未提及 EasyEXPERT；若项目使用该软件，其 test definition、导出格式和自动化均为 PROJECT DESIGN CHOICE。

### G. 后处理软件必须完成的内容

- 从 `VDS` 极值和已知 `VDC`/`RL` 计算 `IDM-I/P/N`。
- 对 B1505 curve 进行一致的查找/插值，得到等效 gate-voltage coordinate。
- 计算 `Vth-IS`、`Vth-PS`、`Vth-NS` 和式 (5) 的 `ΔVth`。
- 检查 `VDS≈ VDS-C`、`IDM-P/N≈ IDM-I`、saturation condition 和 current-deviation 条件。
- 保存原始波形、元数据和计算过程；文件格式/算法/不确定度方法 PAPER_NOT_SPECIFIED。

## 8. Requirements List

“Status=CONFIRMED”只表示 P1 直接支持所述功能或条件；“OPEN”表示项目验收、数值、接口分配或范围尚未冻结。Classification 明确区分 PAPER REQUIREMENT、PAPER-PERFORMANCE-DERIVED PROJECT REQUIREMENT、ENGINEERING MEASUREMENT/INTERFACE REQUIREMENT、PROJECT REQUIREMENT 和 OPTIONAL PROJECT-SCOPE REQUIREMENT。

| ID | Requirement | Source | Reason | Verification | Status / Classification |
|---|---|---|---|---|---|
| REQ-FUNC-001 | 系统必须实现 Fig. 3(a) 的串联电阻负载测试功能：`VDC→ RL→ DUT→ return`。 | Fig. 3(a), §II | 通过 `VDS` 间接获得 `IDS`。 | 连通性检查 + 低能量功能测试，核对 `IDS=(VDC-VDS)/RL`。 | CONFIRMED / PAPER REQUIREMENT |
| REQ-FUNC-002 | 系统必须支持三条各自定义的序列：Calibration=`PRECONDITION→MEASUREMENT_I`；Positive=`PRECONDITION→POSITIVE_STRESS→MEASUREMENT_P`；Negative=`PRECONDITION→NEGATIVE_STRESS→MEASUREMENT_N`。 | Fig. 3(b1–b3), Fig. 4 | 这是论文完整提取流程。 | 记录三条完整状态波形。 | CONFIRMED / PAPER REQUIREMENT |
| REQ-FUNC-003 | Measurement state 必须使 DUT 进入不完全导通并产生有限、可计算的 `IDS`，不能仅实现关断。 | 式 (2), §II | MI/MP/MN 必须映射到 calibration curve。 | 测得 `0<VDS<VDC` 且计算 `IDS>0`；具体容差待定。 | CONFIRMED；PASS=ENGINEERING_ACCEPTANCE_TO_BE_DEFINED |
| REQ-FUNC-004 | 系统必须支持在 measurement 区间捕获 `VDS` 的 MI、MP、MN；对 MP/MN 还应保留 measured point 后的 recovery 波形。 | Fig. 3(b), §II, Fig. 6/7 | MP/MN 后快速恢复会导致阈值位移被低估。 | 示波器波形可识别三个 measured points，并对 P/N 保留后续恢复。 | CONFIRMED；极值算法 OPEN |
| REQ-FUNC-005 | Calibration 完成后，stress 测试必须保持 `VDC` 与 `RL` 不变，只通过调节 `VGM-P/N` 完成对齐。 | §III step 3 | 保持 measurement circuit 条件一致。 | 记录配置/波形，确认 stress 测试未改变 `VDC`、`RL`。 | CONFIRMED / PAPER REQUIREMENT |
| REQ-VOLT-001 | PRECONDITION gate target 必须为 `VGS=0` V。 | 式 (1) | reset interface state 并阻断 DUT。 | 测量 precondition `VGS`；容差待定。 | CONFIRMED；tolerance OPEN |
| REQ-VOLT-002 | 系统必须支持独立的 positive 和 negative stress gate targets `VGS-P`、`VGS-N`。 | Table I, Fig. 3 | 复现 bipolar switching gate bias stress。 | 测量两种 stress level。 | CONFIRMED；论文示例 +20/−5 V，不是通用冻结值 |
| REQ-VOLT-003 | 系统必须支持 `VGM-I`、`VGM-P`、`VGM-N` 三个 measurement gate targets，并允许 `VGM-P/N` 分别调节。 | Table I, §II | 补偿 stress 后 `RDUT` 改变。 | 扫描/设定三个 level，验证可独立达到目标。 | CONFIRMED；范围/分辨率 OPEN |
| REQ-VOLT-004 | B1505 initial curve 必须在固定 `VDS-C` 下取得；论文复现实验值为 10 V。 | §II, §III step 1 | 为高速点测提供同一参考曲线。 | B1505 test record。 | CONFIRMED / PAPER REQUIREMENT；10 V 为 PAPER EXAMPLE VALUE |
| REQ-VOLT-005 | MI、MP、MN 的 `VDS` 必须约等于 `VDS-C`。 | §II, §III step 2 | 保持与 calibration curve 的 drain-bias 对齐。 | 比较各 measured point 与 `VDS-C`。 | CONFIRMED；PASS tolerance=ENGINEERING_ACCEPTANCE_TO_BE_DEFINED |
| REQ-VOLT-006 | Measurement operating point 必须满足论文给出的 saturation condition：`VDS-C>VGS-Vth`。 | §II | 保持 curve mapping 的工作区条件。 | 用各点记录量计算/检查不等式。 | CONFIRMED；margin OPEN |
| REQ-TIME-001 | 系统必须支持从 positive/negative stress state 快速切换到相应 measurement state。 | Abstract, Fig. 3, §III | 抑制 stress removal 后 recovery 导致的低估。 | Scope 记录 `VGS`/`VDS`；是否增加 control reference 由 `tdly` 工程定义决定。 | CONFIRMED / PAPER REQUIREMENT |
| REQ-TIME-002 | 项目应以 P1 报告的约 100 ns 系统级 `tdly` 作为性能参考；精确起点、终点算法及采用 `<100 ns`、`≤100 ns` 或其他表述，必须由 Master 冻结后才能形成 PASS。 | Fig. 6(b), Fig. 7(b), Abstract, §III, Conclusion | 防止把 reported performance 误写成无定义的硬件规范。 | Scope 依据冻结后的事件定义提取名义 switching boundary→measured point 时间。 | OPEN / PAPER-PERFORMANCE-DERIVED PROJECT REQUIREMENT |
| REQ-TIME-003 | 系统必须支持“long-term” `tpre`，以在每次序列前执行相同 precondition。 | §II | 消除 previous-experiment hysteresis。 | 时序记录 + 重复性/重置效果测试。 | OPEN；duration/PASS PAPER_NOT_SPECIFIED |
| REQ-TIME-004 | 系统必须允许编程 `tstr`；P1 展示 0.2–200 `µs`，并使用 10 `µs` 与 2 `µs` 示例。 | §III, Fig. 6/7/10 | 测试不同 stress point/frequency。 | scope 测各 programmed duration。 | CONFIRMED capability；frequency mapping 有论文歧义 |
| REQ-TIME-005 | 系统必须提供足够的 `tmea` 捕获 MP/MN 和其 recovery。 | Fig. 3/4, §II | 极值与恢复均是提取对象。 | scope 检查 acquisition window 覆盖极值/恢复。 | OPEN；duration PAPER_NOT_SPECIFIED |
| REQ-TIME-006 | 系统必须允许改变 test delay，以取得不同 `tdly` 下的 `ΔVth` recovery 数据。 | §III step 5, Fig. 10 | 验证 delay 对测量的影响。 | 多组时序测试，确认目标 delay 可重复。 | CONFIRMED capability；范围/步进 OPEN |
| REQ-MEAS-001 | 测量记录必须包含同一次转换的 `VGS(t)` 和 `VDS(t)`；若项目用二者计算 `tdly`，两信号必须置于已定义的共同时间关系中。 | Fig. 6/7；时间关系为工程推导 | P1 图示同时呈现 gate transition 与 drain measured point。 | 检查同次事件的两信号记录；deskew/时延校正规则待定义。 | PAPER FACT（波形信号）+ ENGINEERING MEASUREMENT REQUIREMENT（共同时间关系） |
| REQ-MEAS-002 | 后处理必须使用 P1 式 (2) 计算 `IDS=(VDC-VDS)/RL`。 | 式 (2)/(4) | 将高速电压点转换为 curve lookup current。 | 用已知测试向量做计算单元测试。 | CONFIRMED / PAPER REQUIREMENT |
| REQ-MEAS-003 | 后处理必须从 MI、MP、MN 分别得到 `IDM-I`、`IDM-P`、`IDM-N`。 | Table I, §II | 三个阈值位移的输入。 | 对带已知极值的波形做回放。 | CONFIRMED；extremum algorithm OPEN |
| REQ-MEAS-004 | 后处理必须把 `IDM-I/P/N` 映射到同一 fixed-`VDS-C` B1505 curve。 | Fig. 2, 式 (3), §II | 获得等效 gate-voltage coordinate。 | curve lookup/interpolation 单元测试。 | CONFIRMED；interpolation method OPEN |
| REQ-MEAS-005 | 后处理必须按 P1 式 (3) 计算 `Vth-IS`，并按与式 (3) 相同的方法取得 `Vth-PS/NS`。 | 式 (3), §II | 量化 raw shift。 | 对论文逻辑构造的数值用例复算。 | CONFIRMED；P/N 展开式为 ENGINEERING RESTATEMENT |
| REQ-MEAS-006 | 后处理必须按 P1 式 (5) 从 positive/negative raw shift 中减去 `Vth-IS`。 | 式 (5) | 排除测试方案自身 hysteresis。 | 公式单元测试 + 数据追溯。 | CONFIRMED / PAPER REQUIREMENT |
| REQ-MEAS-007 | `IDM-P`、`IDM-N` 必须接近 `IDM-I`；P1 实验将低于 `±20%` 的偏差视为可接受。 | §II/III, Fig. 8(b) | 限制 operating-current 不一致造成的 `ΔVth` 偏差。 | 比较三者并报告相对偏差。 | CONFIRMED principle；百分比定义/是否采纳 ±20% 为项目 PASS 待 Master 决定 |
| REQ-MEAS-008 | B1505 必须通过 `Ith` crossing 提取 initial `Vth`；P1 DUT 使用 `Ith=10` mA。 | §I/II/III | 决定 `VGM-I` 和 curve reference。 | B1505 数据重算 crossing。 | CONFIRMED；10 mA 为 PAPER EXAMPLE VALUE |
| REQ-MEAS-009 | 在依赖平行位移法之前，目标 DUT/条件应验证 sweep curves 在 `IDS≈ Ith` 附近近似平行。 | Fig. 2, Fig. 8(a), §III | 平行 shift 是点测量映射的理论基础。 | stress 前后 B1505 curve 对比。 | OPEN project verification；P1 报告波动在 1% 内 |
| REQ-MEAS-010 | Positive-stress 回路电流必须尽量小，以避免 DUT self-heating 影响 `Vth`。 | 式 (4) 后正文 | 论文明确提出该原则。 | 记录/计算 positive-stress `IDS`；“minimized”的项目判据待 Master 定义。 | CONFIRMED principle；具体热测方法与限值 OUT_OF_SCOPE / OPEN |
| REQ-CTRL-001 | 控制系统必须按确定顺序生成 PRECONDITION→STRESS→MEASUREMENT，并给示波器提供可重复触发。 | Fig. 3/4 支持 sequence；触发接口未公开 | 支持状态对齐和波形比较。 | 重复 N 次波形，检查顺序和 jitter。 | OPEN / ENGINEERING INTERFACE REQUIREMENT；sequence 为 PAPER FACT |
| REQ-CTRL-002 | 系统必须允许在 calibration 中调 `VDC`/`RL`，在 stress test 中固定二者并调 `VGM-P/N`。 | §III steps 2–3 | 按论文迭代达到 `VDS`/`IDS` 对齐。 | 配置审查 + 波形验证。 | CONFIRMED / PAPER REQUIREMENT |
| REQ-CTRL-003 | 若 Master 批准 full-paper/Fig. 10 reproduction，系统应支持 multiple-pulse gate stress；P1 的实验总 stress duration 为 `10^5 µs`。 | §III, Fig. 10 前正文 | 这是扩展实验流程，不是最小 Fig. 3 功能复现的已冻结基线。 | 对批准的扩展流程记录 pulse train 和总 stress duration。 | OPTIONAL PROJECT-SCOPE REQUIREMENT；当前不生效 |
| REQ-SAFE-001 | 项目必须定义一个独立于 PRECONDITION 的 SAFE_OFF 状态及其进入/退出逻辑。 | 非 P1 | 上电、故障、探测连接时需要可验证安全行为。 | 故障注入/上电关断测试。 | OPEN / PROJECT REQUIREMENT；具体 gate/drain target 未定义 |
| REQ-SAFE-002 | 项目必须定义 power sequencing、过压/过流/误触发保护和能量限制。 | 非 P1 | P1 未公开实现，原型验证需要安全边界。 | 设计审查 + 保护触发测试。 | OPEN / PROJECT REQUIREMENT |
| REQ-VERIFY-001 | 原型必须依据冻结后的事件定义记录所需 timing-reference signal(s)、`VGS`、`VDS`，并提取完整 system `tdly`；是否需要独立 control signal 由该定义决定。 | Fig. 6/7 + PROJECT VERIFICATION REQUIREMENT | 防止把孤立的 driver edge time 误当完整 test delay。 | Prototype oscilloscope validation。 | OPEN / ENGINEERING VERIFICATION REQUIREMENT；acceptance definition 待冻结 |
| REQ-VERIFY-002 | 原型必须验证 MI/MP/MN 均满足 `VDS≈ VDS-C`，并记录偏差。 | §II/III | 验证 calibration compatibility。 | measured-point comparison。 | OPEN；tolerance 待冻结 |
| REQ-VERIFY-003 | 原型必须验证 `IDM-P/N` 与 `IDM-I` 的匹配，并记录调整后的 `VGM-P/N`。 | §II/III | 控制 current mismatch error。 | current calculation report。 | CONFIRMED method；project PASS 待 Master 决定 |
| REQ-VERIFY-004 | 软件必须保留从 raw `VGS/VDS`、`VDC/RL`、B1505 curve 到最终 `ΔVth` 的可追溯链。 | 式 (2)–(5) | 防止 correction/映射不可审计。 | 数据包审查 + 重算。 | OPEN / ENGINEERING REQUIREMENT |

## 9. Verification Matrix

| Requirement ID | Requirement | Verification method | Instrument | Measured quantity | Pass condition | Design stage |
|---|---|---|---|---|---|---|
| REQ-FUNC-001 | 电阻负载串联回路 | Inspection + low-energy functional test | DMM/scope/DC supply | `VDC`、`VDS`、`RL`、回路电流 | 拓扑正确且式 (2) 一致；数值误差限待定义 | Bring-up |
| REQ-FUNC-002 | 三条测试序列 | Waveform review | Pulse source + scope | state order、gate level、duration | Calibration/P/N 三条序列均与 Fig. 3(b) 顺序一致 | Bring-up |
| REQ-FUNC-003 | 不完全导通 measurement | Operating-point test | Scope | `VGS`、`VDS`、computed `IDS` | `0<VDS<VDC` 且 `IDS>0`；margin 待定义 | Functional prototype |
| REQ-FUNC-004 | 捕获极值和 recovery | Transient capture | Scope + software | MI/MP/MN、post-extremum trend | 极值和后续恢复可区分；算法 acceptance 待定义 | Prototype validation |
| REQ-FUNC-005 | Calibration 后固定 `VDC`/`RL` | Configuration audit | DC supply + test record | `VDC`、`RL` config | P/N 测试与已接受 calibration 配置相同 | Experiment setup |
| REQ-VOLT-001 | 0 V precondition | Static/dynamic measurement | Scope/DMM | precondition `VGS` | Target=0 V；tolerance=ENGINEERING_ACCEPTANCE_TO_BE_DEFINED | Bring-up |
| REQ-VOLT-002 | 正/负 stress levels | Dynamic measurement | Scope | `VGS-P`、`VGS-N` | 达到已批准实验 profile；P1 示例 +20/−5 V | Functional prototype |
| REQ-VOLT-003 | 三个 measurement levels 可独立调 | Parameter sweep | Scope + controller | `VGM-I/P/N` | 三者能独立达到已批准 target；范围/分辨率待定 | Functional prototype |
| REQ-VOLT-004 | B1505 fixed `VDS-C` curve | Calibration record review | B1505 | `VDS` during sweep | 固定于批准的 `VDS-C`；论文复现实验为 10 V | Calibration |
| REQ-VOLT-005 | MI/MP/MN 对齐 `VDS-C` | Point comparison | Scope + software | `VDS, MI/MP/MN-VDS-C` | ENGINEERING_ACCEPTANCE_TO_BE_DEFINED | Calibration/prototype |
| REQ-VOLT-006 | Saturation condition | Calculation | B1505 + scope + software | `VDS-C`、`VGS`、`Vth` | 每个 measurement point 满足 `VDS-C>VGS-Vth`；margin 待定 | Data acceptance |
| REQ-TIME-001 | stress→measurement 快切换 | Time-domain measurement | Scope | control、`VGS`、`VDS` | 状态转换可重复且产生 MP/MN；速度由 REQ-TIME-002 判定 | Prototype validation |
| REQ-TIME-002 | 约 100 ns 的论文性能参考 | Synchronous transient measurement | Scope + probes | frozen start event→measured point time | 数值关系和事件算法均为 ENGINEERING_ACCEPTANCE_TO_BE_DEFINED；不得直接宣称 `<100 ns` PASS | Prototype validation |
| REQ-TIME-003 | long-term `tpre` | Duration + reset-repeatability study | Controller + B1505/scope | `tpre`、重复 MI/`Vth-IS` | Duration/stability criterion=ENGINEERING_ACCEPTANCE_TO_BE_DEFINED | Method validation |
| REQ-TIME-004 | 可编程 `tstr` | Timing sweep | Pulse source + scope | stress width | 覆盖批准 protocol；full paper reproduction 候选 0.2–200 `µs` | Controller validation |
| REQ-TIME-005 | 足够 `tmea` | Acquisition-window review | Scope | measurement window、extremum/recovery coverage | 覆盖选定极值与 recovery interval；数值待定义 | Experiment setup |
| REQ-TIME-006 | 可变 `tdly` | Delay sweep | Controller + scope | programmed/measured `tdly` | 覆盖批准的 delay set；P1 对比含 0.1/1 `µs` | Method validation |
| REQ-MEAS-001 | 同次事件记录 `VGS`/`VDS` | Signal-time relationship check | Scope + probes | two waveforms and relative timing | 两信号属于同次转换；共同时间关系/允许 skew 为 ENGINEERING_ACCEPTANCE_TO_BE_DEFINED | Instrument qualification |
| REQ-MEAS-002 | 式 (2) 电流计算 | Software unit test | Software | known `VDC, VDS, RL` vectors | 与解析结果一致；数值精度待软件规范 | Software verification |
| REQ-MEAS-003 | MI/MP/MN 到三电流 | Waveform replay | Software | extrema、`IDM-I/P/N` | 对 reference waveform 输出正确；极值规则待冻结 | Software verification |
| REQ-MEAS-004 | 映射到同一 B1505 curve | Lookup/interpolation test | Software + B1505 export | input current、mapped gate voltage | 使用同一 approved curve；插值误差限待定义 | Software verification |
| REQ-MEAS-005 | raw shifts | Formula test | Software | `VGM`、mapped voltage、raw shift | 式 (3) 与相同方法的 P/N 结果可重算 | Software verification |
| REQ-MEAS-006 | scheme-shift correction | Formula test | Software | `Vth-IS/PS/NS`、`ΔVth` | 精确实现式 (5) | Software verification |
| REQ-MEAS-007 | `IDM` 匹配 | Current-consistency report | Scope + software | `IDM-P/N` vs `IDM-I` | P1 报告低于 ±20%；项目是否沿用及百分比定义待 Master 批准 | Method validation |
| REQ-MEAS-008 | `Ith` crossing 初始阈值 | Independent re-extraction | B1505 + software | `IDS`–`VGS`、crossing | 在批准的 `Ith` 得到一致 initial `Vth`；论文值 10 mA | Calibration |
| REQ-MEAS-009 | 平行移位假设 | Pre/post-stress curve comparison | B1505 + software | `ΔVth` vs `IDS` near `Ith` | P1 结果为 1% 内；项目 acceptance/window 待定义 | Method qualification |
| REQ-MEAS-010 | 尽量减小 positive-stress `IDS` | Current record/calculation | Scope + DC supply | positive-stress `IDS` | “minimized”判据=ENGINEERING_ACCEPTANCE_TO_BE_DEFINED；热测方法不在 SP1 冻结 | Method/design verification |
| REQ-CTRL-001 | 状态顺序和触发可重复 | Repetition/jitter test | Pulse source + scope | order、period、jitter | 顺序正确；允许 jitter 和重复次数待定义 | Controller validation |
| REQ-CTRL-002 | 调参边界正确 | Procedure audit | Test record + instruments | `VDC`/`RL`/`VGM` changes | Calibration 调 `VDC/RL`；stress test 固定二者、只调 `VGM-P/N` | Experiment qualification |
| REQ-CTRL-003 | Optional multiple-pulse stress | Pulse-train verification | Pulse source + scope/counter | pulse count、width、total duration | 仅在 Master 激活 full-paper/Fig. 10 scope 后：按批准流程验证；P1 reported total=`10^5 µs` | Extended-method validation |
| REQ-SAFE-001 | SAFE_OFF | State/fault test | Scope + supplies | gate/drain state、stored energy | ENGINEERING_ACCEPTANCE_TO_BE_DEFINED | Architecture/prototype safety |
| REQ-SAFE-002 | Sequencing/protection | Design review + fault injection | Supplies/scope/protection monitor | overvoltage/current/false trigger response | ENGINEERING_ACCEPTANCE_TO_BE_DEFINED | Architecture/prototype safety |
| REQ-VERIFY-001 | 完整 system `tdly` 验证 | Transient capture using frozen event definition | Scope | required timing-reference signal(s)、`VGS`、`VDS` | 不以单独 gate edge 代替；事件与数值 PASS 待冻结 | Prototype validation |
| REQ-VERIFY-002 | `VDS` 对齐报告 | Automated comparison | Scope + software | MI/MP/MN vs `VDS-C` | ENGINEERING_ACCEPTANCE_TO_BE_DEFINED | Prototype validation |
| REQ-VERIFY-003 | Current match 报告 | Automated comparison | Scope + software | `IDM-P/N` vs `IDM-I` | Master 批准的 tolerance；P1 参考低于 ±20% | Prototype validation |
| REQ-VERIFY-004 | 全链可追溯 | Dataset audit/recompute | B1505 + scope + software | raw/calibration/config/results | 独立重算得到相同 `ΔVth`；数值 tolerance 待定 | Experiment release |

## 10. OPEN / PAPER_NOT_SPECIFIED List

| 项目 | 状态 | P1 实际公开到什么程度 |
|---|---|---|
| Fig. 3(a) 电阻负载系统拓扑 | PAPER_SPECIFIED | 给出 `VDC`、`RL`、DUT、VGS driver 的功能连接。 |
| Fig. 3(b) 三类 gate/drain 波形与状态顺序 | PAPER_SPECIFIED | 给出 b1/b2/b3 的目标电位和 MI/MP/MN 行为。 |
| Multistage adjustable gate driver 具体 schematic | PAPER_NOT_SPECIFIED | 仅给功能名称和硬件照片。 |
| Driver IC 型号 | PAPER_NOT_SPECIFIED | 未公开。 |
| Driver output impedance/source-sink current | PAPER_NOT_SPECIFIED | 未公开。 |
| Gate resistor `Rg` | PAPER_NOT_SPECIFIED | 未公开。 |
| Gate-loop decoupling/rail capacitor | PAPER_NOT_SPECIFIED | 未公开。 |
| 0 V precondition 的具体电路/0 V clamp 拓扑 | PAPER_NOT_SPECIFIED | 仅规定 gate target=0 V。 |
| Positive/negative/measurement rail 的产生方式 | PAPER_NOT_SPECIFIED | 仅规定功能电位。 |
| `VGM-I/P/N` 数值、范围、分辨率、调节算法 | PAPER_PARTIALLY_SPECIFIED | `VGM-I` 的逻辑和 P/N 独立调节原则已给；实现及数值未给。 |
| Exact state-control circuit/logic levels/truth table | PAPER_NOT_SPECIFIED | 只有波形级策略。 |
| Pulse generator 型号、通道、输出电平、抖动 | PAPER_NOT_SPECIFIED | Fig. 5 只标功能设备。 |
| `tpre` 数值与 reset-complete 判据 | PAPER_NOT_SPECIFIED | 仅称 long-term precondition。 |
| `tmea` 长度与退出条件 | PAPER_NOT_SPECIFIED | 只给 measurement procedure。 |
| `tdly` 精确起止百分比、settling/filter/window | PAPER_PARTIALLY_SPECIFIED | stress→measurement 后到 `VDS` 最大/最小 measured point；精确算法未给。 |
| `tstr` 与“switching frequency”的严格换算/占空比 | PAPER_PARTIALLY_SPECIFIED | 给了多个数值映射，但未给统一时序公式，且示例存在表面不一致。 |
| `VDC` 数值 | PAPER_NOT_SPECIFIED | 只说明是 DC voltage bias。 |
| `RL` 数值、技术、功率、脉冲额定、寄生 | PAPER_NOT_SPECIFIED | 只说明用于控制 `IDS`。 |
| 目标 DUT 的确切型号/栅电荷/电容参数 | PAPER_PARTIALLY_SPECIFIED | 只给商用 1.2 kV、TO-247。 |
| Negative-stress 状态的明确 `VDS`/`IDS` 公式 | PAPER_PARTIALLY_SPECIFIED | Fig. 3(b3) 给波形，正文无对应方程。 |
| B1505 型号类别 | PAPER_SPECIFIED | 明确 Keysight B1505。 |
| EasyEXPERT 的具体 test definition/workflow | PAPER_NOT_SPECIFIED | P1 只明确 B1505 仪器，没有说明 EasyEXPERT 配置。 |
| B1505 sweep range/step/rate/direction/hold/compliance | PAPER_NOT_SPECIFIED | 仅称较慢 staircase increasing scan；Fig. 1 讨论 up/down sweep。 |
| 实验温度、温控与温度稳定判据 | PAPER_NOT_SPECIFIED | 本文方法段未公开。 |
| `VDS≈ VDS-C` 的允许误差 | PAPER_NOT_SPECIFIED | 只有“approx/align”。 |
| `IDM-P/N≈ IDM-I` 的项目 PASS | PAPER_PARTIALLY_SPECIFIED | P1 实验偏差低于 ±20% 并认为可接受；百分比定义与通用性未给。 |
| self-heating 的最大允许 `IDS`/能量/温升 | PAPER_NOT_SPECIFIED | 只要求 `IDS` should be minimized。 |
| MI/MP/MN 极值检测、滤波、振铃处理 | PAPER_NOT_SPECIFIED | 只定义极值点。 |
| Oscilloscope 型号/带宽/采样率 | PAPER_NOT_SPECIFIED | Fig. 5 标注 oscilloscope，正文未给规格。 |
| `VGS`/`VDS` probe 型号、带宽、输入电容、接法 | PAPER_NOT_SPECIFIED | 未公开。 |
| Channel deskew/cable-delay correction | PAPER_NOT_SPECIFIED | 未公开。 |
| Kelvin-source 测量/驱动参考 | PAPER_NOT_SPECIFIED | 未公开，不能作为论文事实。 |
| Connector/test point 类型 | PAPER_NOT_SPECIFIED | 未公开。 |
| PCB schematic/layout/层数/stackup/copper/return path | PAPER_NOT_SPECIFIED | 只有 testing board 照片。 |
| Gate/power-loop parasitic inductance/capacitance | PAPER_NOT_SPECIFIED | 未量化。 |
| Power sequencing、UVLO、interlock、fault response | PAPER_NOT_SPECIFIED | 未公开。 |
| Gate overvoltage、drain overcurrent、short-circuit 保护 | PAPER_NOT_SPECIFIED | 未公开。 |
| DC supply 动态阻抗、噪声、限流、remote sense | PAPER_NOT_SPECIFIED | 未公开。 |
| `RL` 与 supply 的物理位置/回路去耦 | PAPER_NOT_SPECIFIED | 未公开。 |
| Measurement uncertainty/error budget | PAPER_NOT_SPECIFIED | 未给完整不确定度传播。 |
| 后处理插值、数据格式、自动化与版本控制 | PAPER_NOT_SPECIFIED | 未公开。 |

## 11. Risks / Ambiguities

1. **`tdly` 可重复性风险：** 论文有系统级语义但无工程阈值定义；不同 edge crossing、filter 或 extremum 搜索窗可能得到不同“100 ns”。
2. **振铃/探头负载风险：** MP/MN 被定义为极值，任何 parasitic 或 probe-induced overshoot 都可能被误识别为物理 measurement point；P1 无排除规则。
3. **`VDS` 对齐风险：** “`VDS≈ VDS-C`”没有容差；即使 current 匹配，drain-bias mismatch 仍可能影响 curve mapping。
4. **Current matching 风险：** P1 报告 ±20% 内可接受，但未明确百分比计算式、是否对 P/N 使用相同容差、是否适用于不同 DUT。
5. **平行移位假设风险：** 点测方法依赖 sweep curve 近似平行移动；P1 在同型号器件、`IDS≈ Ith` 附近验证 1% 内，不保证本项目目标 DUT/温度/stress 条件相同。
6. **Precondition 不确定性：** “long-term”没有时间或状态完成判据，MI/`Vth-IS` 可能随测试历史漂移。
7. **Self-heating 混杂风险：** Positive stress 时存在 `VDC/RL` 电流，但 P1 不提供最大能量/温升；热引起的阈值变化可能与 hysteresis 混合。
8. **频率定义歧义：** P1 同时给出 `tstr=10 µs`↔50 kHz、`tstr=2 µs`↔500 kHz、0.2–200 `µs`↔5 MHz–5 kHz，未给 duty-cycle/period 的统一定义；不能由 SP1 自行修正。
9. **“constant rated `VDS`”措辞歧义：** 论文随后对 1.2 kV DUT 使用 `VDS-C=10` V，因此此处不能解释为器件额定耐压；本报告只把它作为固定 calibration drain bias。
10. **负应力状态方程缺失：** Fig. 3(b3) 显示高 `VDS`，但 P1 未像 positive stress 那样给出明确回路公式。
11. **调整迭代风险：** `VGM-P/N`、`VDC`、`RL` 的调节步长/收敛算法未给，可能导致不同操作者得到不同 operating point。
12. **测量链误差风险：** scope/probe bandwidth、channel skew、probe capacitance、cable delay 都会直接影响 `tdly` 和极值，但 P1 未公开。
13. **安全边界风险：** Fig. 3 是方法示意图，不含上电顺序、互锁、故障态和保护；不可直接据此进入硬件实现。

## 12. Items Requiring Master Decision

1. 冻结复现范围：只复现 Fig. 3 的 functional architecture，还是还要复现 Fig. 6/7 的 <100 ns 波形和 Fig. 10 的 delay/frequency sweep。
2. 冻结 `tdly` 工程定义：起点 crossing、终点 extremum 算法、search window、filter、deskew/de-embedding、<100 ns 或 ≤100 ns。
3. 为目标 DUT 选择 `VDS-C` 与 `Ith`；P1 的 10 V/10 mA 只能视为论文示例。
4. 冻结 `VDS≈ VDS-C` 的误差带。
5. 冻结 `IDM-P/N` 相对 `IDM-I` 的偏差定义与 PASS；决定是否沿用 P1 的 ±20%实验标准或采用更严标准。
6. 冻结 `tpre` 的最低时长及“reset complete”重复性判据。
7. 冻结 `tmea`、recovery observation window 与 MI/MP/MN 选择算法。
8. 澄清 `tstr`、正/负半周期、占空比与 switching frequency 的项目定义。
9. 冻结“`IDS` should be minimized”的项目 acceptance criterion；具体热验证方法不在 SP1 冻结。
10. 冻结 SAFE_OFF、上电/掉电顺序、interlock 和 protection requirements。
11. 冻结系统接口：pulse source control/trigger、gate-level programming、scope probe/trigger、`VDC`/`RL`/DUT 连接。
12. 决定目标 DUT 是否先做平行曲线验证；若不满足，是否继续使用 P1 的单点映射方法。

## 13. Recommended Next Step

Master 先审查并冻结以下六个 SP1 gate：

1. 三条 sequence 与七个 state 的系统定义；
2. `tdly` 工程起止事件；
3. 目标 DUT 的 `VDS-C`/`Ith`；
4. `VDS` alignment 与 `IDM` matching acceptance；
5. `tpre`/`tmea` 与 extremum extraction；
6. SAFE_OFF/protection 的项目级最低需求。

冻结后，SP2 可在不选择具体器件的前提下建立系统 architecture/interface control document；SP3 再把已批准的电压、时间、负载、探测和安全需求转换为电路级约束。任何 Si8273 rail、`Rg`、电容、0 V clamp 或 layout 选择都应在该需求基线之后进行，且标为 PROJECT DESIGN CHOICE。

---

HANDOFF_PACKET

Subproject:
SP1 — 论文方法与系统需求

Version:
SP1-v0.2

Source:
Xu Li, Xiaochuan Deng, Jingyu Huang, Xuan Li, Wanjun Chen, Bo Zhang, “Accurate Evaluation of Threshold Voltage Hysteresis in SiC MOSFET Under Switching Stress,” IEEE Transactions on Power Electronics, vol. 39, no. 11, pp. 14118–14121, Nov. 2024, DOI 10.1109/TPEL.2024.3409570.

Completed:
- 对 SP1-v0.1 完成 12 项严格 Requirement Audit，分类为 2 项 ERROR、2 项 AMBIGUOUS、5 项 UNSUPPORTED、3 项 OUT_OF_SCOPE，并逐项修正。
- 重新核对 P1 四页正文、Fig. 2-4、Table I、式 (1)-(5) 以及 Fig. 6-10 中与数值和 `tdly` 有关的证据。
- 完成所有具体数值的来源与适用性审计，区分 PAPER EXAMPLE VALUE、PAPER REPORTED PAIR/RANGE/PERFORMANCE/RESULT。
- 修正 `tdly`：保留 stress-end-to-measurement 的论文概念和 measured-point 图示终点，将精确电气起点/极值算法标为 AMBIGUOUS / PAPER_NOT_SPECIFIED。
- 确认 MI/MP/MN、`VGM-I/P/N`、B1505 calibration 与高速点测主链准确。
- 重新分类全部 36 个 requirement，未新增 requirement ID。
- 修正 Verification Matrix 中把 `<100 ns`、deskew、热测方法等写得过度确定的问题。
- 明确 PCB 与外部设备职责表属于 ENGINEERING INTERFACE ALLOCATION，不是完整的论文硬件公开信息。
- 确认文档未选择 Si8273 pin、`Rg`、电容、MOSFET、relay、0 V clamp 或其他具体拓扑。

Confirmed paper facts:
- 方法使用电阻负载回路与 multistage adjustable gate driver，从 bipolar gate stress 快速切换到 `Vth` measurement。
- B1505 在 fixed `VDS-C` 下取得 initial `IDS`–`VGS` curve；论文 DUT 使用 `VDS-C=10` V、`Ith=10` mA。
- Precondition 为 `VGS=0`、`VDS=VDC`、`IDS=0`，用于 reset interface state 和消除前次 hysteresis。
- Calibration 使用 `VGM-I=initial Vth`，以 MI 得到 `Vth-IS`。
- Positive stress 时 DUT fully ON，`VDS≈0`、`IDS≈ VDC/RL`，并应尽量减小电流避免 self-heating。
- Positive stress 后 `VDS` 到达 maximum MP 后因 recovery 下降；negative stress 后 `VDS` 具有 minimum MN 后继续上升。
- MI、MP、MN 是 measured potential points；`IDM-I/P/N` 是相应点的 `IDS`。
- `VGM-P/N` 分别调节，使 `IDM-P/N≈IDM-I`；P1 同时要求 measured-point `VDS≈VDS-C`。
- Corrected `ΔVth` 由 `Vth-PS/NS` 减去 `Vth-IS`。
- P1 将 `tdly` 定义为 stress end 与 measurement 之间的 test delay；Fig. 6/7 以 stress-to-measurement 名义边界到 measured point 图示 100 ns，§III 报告 `<100 ns`。
- P1 的论文 DUT/实验使用 20 V/-5 V stress；`tstr` 示例和扫描值详见 Numeric Traceability Audit。
- 500 kHz stress 后，1 us delay 相对 0.1 us (100 ns) 的正/负 shift 在 §III/Conclusion 中分别低 32%/22%；Abstract 写“more than”该比例。

Engineering interpretations:
- Negative stress 期间 `IDS≈0` 是依据 Fig. 3(b3) 高 `VDS` 与串联回路作出的 ENGINEERING INFERENCE；P1 无对应方程。
- `Vth-PS=VGM-P-Vth-MP`、`Vth-NS=VGM-N-Vth-MN` 是对“same method as (3)”的 ENGINEERING RESTATEMENT，不是论文另列公式。
- PCB、pulse generator、DC supply、DUT/`RL`、scope、B1505、software 的职责拆分属于 ENGINEERING INTERFACE ALLOCATION；P1 未给出完整端口分工。
- 同次事件下建立 `VGS`/`VDS` 的共同时间关系，是为了计算系统 `tdly` 的 ENGINEERING MEASUREMENT REQUIREMENT；deskew 方法未由论文规定。
- 系统 `tdly` 不能由单一 driver rise/fall time 代替，是由 P1 的 gate transition→drain measured-point 事件链得出的 ENGINEERING INFERENCE。
- 为可验证硬件增加 SAFE_OFF、sequencing、protection 是 PROJECT REQUIREMENT，不是论文状态或论文电路。
- REQ-CTRL-003 仅是 full-paper/Fig. 10 reproduction 的 OPTIONAL PROJECT-SCOPE REQUIREMENT，当前未激活。

Requirements proposed:
- REQ-FUNC-001…005
- REQ-VOLT-001…006
- REQ-TIME-001…006
- REQ-MEAS-001…010
- REQ-CTRL-001…003
- REQ-SAFE-001…002
- REQ-VERIFY-001…004
- 合计 36 个既有 ID；v0.2 未新增 ID，只修正 wording、classification 和 verification。

Interfaces proposed:
- 以下仅为系统级 ENGINEERING INTERFACE ALLOCATION，不是 P1 原理图细节。
- Pulse/control interface：sequence command、timing、trigger reference；电气实现待定。
- Gate-target interface：0 V、`VGS-P`、`VGS-N`、`VGM-I/P/N`；具体 rail/driver 待定。
- Drain-load interface：`VDC`、`RL`、DUT drain/source return；具体连接/额定待定。
- Measurement interface：同次事件的 `VGS`/`VDS` 探测及时间参考；probe/connector/deskew 待定。
- Calibration-data interface：B1505 fixed-`VDS-C` curve 和 `Ith` metadata。
- Post-processing interface：raw waveform + `VDC`/`RL` + calibration curve → traceable `ΔVth`。

Unknown / paper not specified:
- Multistage driver schematic、driver IC、output impedance、source/sink current、`Rg`、decoupling。
- Positive/negative/measurement rail 生成方法和 exact 0 V implementation/clamp。
- State-control circuit、logic levels、pulse-generator channels/jitter/trigger implementation。
- `VGM-I/P/N` 数值/范围/分辨率与调节算法。
- `VDC`、`RL` 数值及 `RL` 技术/功率/寄生/物理位置。
- `tpre` 数值/reset 判据、`tmea` 长度/退出条件。
- `tdly` 的控制/电气起点、edge percentage、extremum filter/window、settling、deskew/de-embedding。
- `tstr` 与 bipolar frequency/duty-cycle 的统一定义。
- DUT exact part number；B1505 sweep step/rate/range/hold/compliance；test temperature。
- `VDS≈ VDS-C` tolerance；`IDM` matching 的通用 PASS；self-heating limit。
- Scope/probe model、bandwidth、sample rate、probe loading、cable delay、Kelvin reference。
- PCB schematic/layout/stackup/connector/test point/parasitics。
- Power sequencing、interlock、protection、fault state、SAFE_OFF target。
- Measurement uncertainty、extremum algorithm、interpolation/data format。
- EasyEXPERT 是否使用及其全部配置/流程。

Risks:
- P1 的 100 ns 是 reported performance，但没有统一工程事件定义；直接写成 `<100 ns` 硬 PASS 会产生不可比结果。
- 振铃/探头负载可能伪造 MP/MN 极值。
- Curve mapping 依赖 `VDS` 和 `IDS` 对齐及平行移位假设。
- 未定义 precondition 和 thermal limit 可能使 history/temperature 与 hysteresis 混杂。
- P1 的 `tstr`–frequency 叙述存在歧义。
- 将工程接口分配误当论文硬件架构，会导致 PCB 与外部仪器边界被错误冻结。
- 论文没有安全与电路实现信息，不能直接据 Fig. 3 下板。

Open questions:
- Master 是否要求 full paper reproduction，还是只做 Fig. 3 functional reproduction？
- `tdly` 精确起止事件以及 `<100 ns`、`≤100 ns` 或“约 100 ns”哪一种项目 PASS 如何冻结？
- 目标 DUT 的 `VDS-C`、`Ith`、stress level 和 operating temperature 是什么？
- `VDS` alignment、`IDM` matching、parallel-shift validation 采用什么 tolerance？
- `tpre`、`tmea`、extremum/recovery window 如何定义？
- SAFE_OFF、sequencing、interlock、protection 由哪个子项目冻结？
- PCB 与外部 signal generator/power supplies/scope 之间的接口分配由谁批准？

Items requiring master approval:
- State table 与 sequence baseline。
- `tdly` engineering acceptance definition。
- Target-DUT calibration profile：`VDS-C`、`Ith`。
- `VDS`/`IDM` alignment tolerance。
- Precondition/measurement timing 与 measurement-point algorithm。
- Full-reproduction scope、frequency definition，以及是否激活 REQ-CTRL-003 multiple-pulse requirement。
- Thermal limit、SAFE_OFF、power sequencing、protection baseline。
- 系统级 control/gate/drain/measurement/data interfaces。

Recommended next action:
Master 先审阅并批准 SP1-v0.2 的审计分类，尤其冻结 `tdly` 工程定义、复现范围、目标 DUT calibration profile、`VDS`/`IDM` tolerance 和系统接口分配。批准前不得把约 100 ns reported performance、20 V/-5 V、10 V/10 mA、±20% 或任何具体 Si8273 rail、`Rg`、电容、0 V clamp、MOSFET/relay、layout 方案标为已冻结的论文复现需求。

END_HANDOFF_PACKET
