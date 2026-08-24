# SiC MOSFET BTI Fast Gate Driver PCB / Fig. 3 Reproduction

## SP1 — 论文方法与系统需求报告

- 版本：SP1-v0.1
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

本报告不选择驱动 IC、$R_g$、电容、开关器件、继电器、0 V clamp 拓扑，不画原理图/PCB，不生成 BOM，不进行 LTspice 仿真。

## 1. Executive Summary

P1 的方法不是直接用高速示波器扫描完整的 $I_{DS}$–$V_{GS}$ 曲线，而是先用 Keysight B1505 在固定 $V_{DS-C}$ 下取得基准扫栅曲线，再用 Fig. 3 的电阻负载回路完成一个快速“点测量”。测量回路从 precondition 或 stress 栅压快速切换至接近阈值区的 measurement gate voltage；此时 DUT 处于不完全导通状态，$V_{DS}$ 的瞬时极值给出 MI、MP 或 MN。由

$$I_{DS}=\frac{V_{DC}-V_{DS}}{R_L}$$

得到测量电流，再把该电流映射回 B1505 基准曲线，获得等效栅压位置和阈值位移。

三条核心序列是：

1. Calibration：$0\ \mathrm{V}\rightarrow V_{GM-I}$，得到 MI 和测试方案自身的初始位移 $V_{th-IS}$；
2. Positive stress：$0\ \mathrm{V}\rightarrow V_{GS-P}\rightarrow V_{GM-P}$，得到 MP 和 $V_{th-PS}$；
3. Negative stress：$0\ \mathrm{V}\rightarrow V_{GS-N}\rightarrow V_{GM-N}$，得到 MN 和 $V_{th-NS}$。

$V_{GM-P}$ 与 $V_{GM-N}$ 不是必须等于 $V_{GM-I}$，也不是必须彼此相等。P1 要求分别调节它们，使 MP/MN 对应的 $I_{DM-P}$、$I_{DM-N}$ 接近校准电流 $I_{DM-I}$，同时使测量点的 $V_{DS}\approx V_{DS-C}$。

P1 对 $t_{dly}$ 的实际判定是：$V_{GS}$ 从 stress 电位切换到 measurement 电位后，直到 $V_{DS}$ 到达正应力后的最大点 MP或负应力后的最小点 MN。Fig. 6(b)/Fig. 7(b) 从 stress 结束处的 $t=0$ 标到 measured point，标称 100 ns；正文称 $t_{dly}<100$ ns。P1 没有定义 stress-removal 边沿采用哪个电压百分比，也没有定义 $V_{DS}$ 极值的 settling band、滤波、搜索窗或振铃处理，因此 PCB 工程验收中的精确定义仍须单独冻结。

## 2. Paper Method Summary

### 2.1 方法逻辑

1. 用 B1505 在固定 $V_{DS-C}$ 下做慢速阶梯式 $V_{GS}$ 扫描，获得初始 $I_{DS}$–$V_{GS}$ 曲线。
2. 定义阈值电流 $I_{th}$；基准曲线上 $I_{DS}=I_{th}$ 时的 $V_{GS}$ 是 initial $V_{th}$。
3. 在 Fig. 3 电阻负载平台上执行长时间 0 V precondition，使论文所称的 SiO$_2$/SiC interface state 被 reset，并消除前次实验的 hysteresis 影响。
4. Calibration 中将 $V_{GS}$ 快速切至 $V_{GM-I}=\text{initial }V_{th}$；DUT 进入不完全导通，记录 $V_{DS}$ 极值 MI。
5. 用 MI 对应的 $V_{DS}$ 计算 $I_{DM-I}$，再映射回 B1505 曲线得到 $V_{th-MI}$，计算 $V_{th-IS}$。
6. Positive/negative stress 测试采用相同 precondition，然后施加 $V_{GS-P}$ 或 $V_{GS-N}$，持续 $t_{str}$；stress 结束后快速切至各自的 $V_{GM-P}$ 或 $V_{GM-N}$，捕获 MP 或 MN。
7. 保持 $V_{DC}$ 和 $R_L$ 不变，分别调节 $V_{GM-P}$、$V_{GM-N}$，使 $I_{DM-P}$、$I_{DM-N}$ 接近 $I_{DM-I}$。
8. 通过与式 (3) 相同的映射方法得到包含测试方案自身初始位移的 $V_{th-PS}$、$V_{th-NS}$，再减去 $V_{th-IS}$，得到校正后的 $\Delta V_{th}$。
9. 改变 $t_{str}$ 和 $t_{dly}$，得到不同测试点/频率下的 $\Delta V_{th}$ 及 recovery。

### 2.2 P1 给出的关键实验事实

- DUT：商用 1.2 kV、TO-247 SiC MOSFET；确切型号未公开。
- $I_{th}=10$ mA，$V_{DS-C}=10$ V。
- 典型 stress：$V_{GS-P}/V_{GS-N}=20\ \mathrm{V}/-5\ \mathrm{V}$。
- 典型波形：$t_{str}=10\ \mu\mathrm{s}$，正文关联 50 kHz。
- 另一处实验：500 kHz stress 对应 $t_{str}=2\ \mu\mathrm{s}$。
- $t_{str}$ 扫描范围写为 0.2–200 $\mu$s，并关联 5 MHz–5 kHz。
- 多脉冲 gate stress 总时长为 $10^5\ \mu$s，用于恢复 premeasurement trap occupation state 并获得稳定 $\Delta V_{th}$。
- $I_{DM-P}$、$I_{DM-N}$ 相对 $I_{DM-I}$ 的偏差在论文实验中低于 $\pm20\%$，论文认为相应 $\Delta V_{th}$ 偏差可接受。
- 在 $I_{DS}$ 接近 $I_{th}$ 时，Fig. 8(a) 所示平行移位验证中 $\Delta V_{th}$ 波动在 1% 内。
- 500 kHz stress 后，以 1 $\mu$s 测得的正/负 $\Delta V_{th}$ 相比 100 ns 分别低 32%/22%。

## 3. Variable Definition Table

| 量/术语 | 名称与物理意义 | 何时出现 | 类型 | P1 是否给值 | PCB 是否直接支持 | 论文依据/状态 |
|---|---|---|---|---|---|---|
| Calibration | Fig. 3 平台与 B1505 之间偏差的预校准 | 正/负 stress 测试前 | 流程 | 无单一数值 | 是，需执行 $0\rightarrow V_{GM-I}$；B1505/软件也参与 | §II；PAPER FACT |
| Initial sweeping curve | B1505 得到的初始 $I_{DS}$–$V_{GS}$ 基准曲线 | 所有快速测量前 | 测量数据/查找表 | 扫描细节未给；实验 $V_{DS-C}=10$ V | 否；由 B1505 完成 | Fig. 2、§II/III；PAPER FACT |
| $V_{DS-C}$ | B1505 sweep 使用的固定 drain-source calibration bias；也是快速测量点希望对齐的 $V_{DS}$ | B1505 sweep、MI/MP/MN 对齐 | 控制量/比较基准 | 10 V（论文 DUT） | PCB 不生成其定义，但测量回路须能形成并测到该 $V_{DS}$ | §II、§III step 1；PAPER EXAMPLE VALUE |
| $I_{th}$ | 在基准 sweep 上定义 initial $V_{th}$ 的 threshold current | 初始阈值定义 | 分析控制量 | 10 mA（论文 DUT） | 否；B1505/后处理使用 | Fig. 1、Table I、§III；PAPER EXAMPLE VALUE |
| Initial $V_{th}$ | 基准曲线上 $I_{DS}=I_{th}$ 对应的 $V_{GS}$ | Calibration 前 | 计算/提取量 | 数值未给 | 间接；用于设 $V_{GM-I}$ | §I/II；PAPER FACT |
| $V_{GM-I}$ | MI 处的 gate voltage；Calibration 中设为 initial $V_{th}$ | MEASUREMENT_I | 控制量 | 数值未给 | 是，需形成该栅压 | Table I、式 (2)；PAPER FACT |
| $V_{GM-P}$ | MP 处的 gate voltage；为电流/电压对齐而单独调节 | MEASUREMENT_P | 控制量 | 数值未给 | 是，需独立可调 | Table I、§II；PAPER FACT |
| $V_{GM-N}$ | MN 处的 gate voltage；为电流/电压对齐而单独调节 | MEASUREMENT_N | 控制量 | 数值未给 | 是，需独立可调 | Table I、§II；PAPER FACT |
| $V_{GS-P}$ | Positive gate stress voltage | POSITIVE_STRESS | 控制量 | +20 V（论文示例） | 是，需形成正应力栅压 | Table I、§III；PAPER EXAMPLE VALUE |
| $V_{GS-N}$ | Negative gate stress voltage | NEGATIVE_STRESS | 控制量 | −5 V（论文示例） | 是，需形成负应力栅压 | Table I、§III；PAPER EXAMPLE VALUE |
| MI | 无 stress 的 initial measured potential point；$V_{DS}$ 极值 | $0\rightarrow V_{GM-I}$ 后 | 直接波形特征 | 未给 | PCB 提供可探测节点；示波器采集 | Table I、§II；PAPER FACT |
| MP | Positive stress 后的 measured potential point；$V_{DS}$ 最大值 | $V_{GS-P}\rightarrow V_{GM-P}$ 后 | 直接波形特征 | 未给 | 同上 | Fig. 3(b2)、§II；PAPER FACT |
| MN | Negative stress 后的 measured potential point；$V_{DS}$ 最小值 | $V_{GS-N}\rightarrow V_{GM-N}$ 后 | 直接波形特征 | 未给 | 同上 | Fig. 3(b3)、§II；PAPER FACT |
| $I_{DM-I}$ | MI 处的 $I_{DS}$ | MEASUREMENT_I | 由 $V_{DS}$ 计算 | 数值未给 | 间接支持 | Table I、式 (2)；PAPER FACT |
| $I_{DM-P}$ | MP 处的 $I_{DS}$ | MEASUREMENT_P | 由 $V_{DS}$ 计算 | 数值未给；要求接近 $I_{DM-I}$ | 间接支持 | Table I、§II/III；PAPER FACT |
| $I_{DM-N}$ | MN 处的 $I_{DS}$ | MEASUREMENT_N | 由 $V_{DS}$ 计算 | 数值未给；要求接近 $I_{DM-I}$ | 间接支持 | Table I、§II/III；PAPER FACT |
| $V_{th-MI}$ | B1505 曲线上与 $I_{DM-I}$ 对应的 gate voltage | Calibration 后处理 | 查表/插值结果 | 未给 | 否 | Table I、式 (3)；PAPER FACT |
| $V_{th-MP}$ | B1505 曲线上与 $I_{DM-P}$ 对应的等效 gate voltage | Positive 后处理 | 查表/插值结果 | 符号未在 Table I 单列，数值未给 | 否 | “same method as (3)”；方法直接含义，符号为 ENGINEERING RESTATEMENT |
| $V_{th-MN}$ | B1505 曲线上与 $I_{DM-N}$ 对应的等效 gate voltage | Negative 后处理 | 查表/插值结果 | 同上 | 否 | 同上；ENGINEERING RESTATEMENT |
| $V_{th-IS}$ | 测试方案自身的 initial $V_{th}$ shift，在 MI 得到 | Calibration | 计算量 | 未给 | 否；软件计算 | Table I、式 (3)；PAPER FACT |
| $V_{th-PS}$ | MP 测得、包含 $V_{th-IS}$ 的 positive-stress $V_{th}$ shift | Positive 后处理 | 计算量 | 未给 | 否 | Table I、§II；PAPER FACT |
| $V_{th-NS}$ | MN 测得、包含 $V_{th-IS}$ 的 negative-stress $V_{th}$ shift | Negative 后处理 | 计算量 | 未给 | 否 | Table I、§II；PAPER FACT |
| $\Delta V_{th}$ | 扣除 $V_{th-IS}$ 后的准确阈值位移 | 最终结果 | 计算量 | 多组结果在 Fig. 9/10，非固定值 | 否 | Table I、式 (5)；PAPER FACT |
| $t_{pre}$ | Precondition procedure 的持续时间 | 每次 calibration/stress 前 | 控制量 | “long-term”；无明确数值/判据 | 是，系统时序需支持 | Table I、§II；PAPER_NOT_SPECIFIED（数值） |
| $t_{str}$ | Stress procedure 的持续时间 | POSITIVE/NEGATIVE_STRESS | 控制量 | 典型 10 $\mu$s；2 $\mu$s；范围 0.2–200 $\mu$s | 是，系统时序需支持 | Table I、§III；PAPER EXAMPLE VALUES |
| $t_{mea}$ | Measurement procedure 的时间区间 | MEASUREMENT_I/P/N | 控制/采集窗口 | 无明确时长 | 是，保持 measurement 电位并允许采集 | Table I、Fig. 3/4；PAPER_NOT_SPECIFIED（数值） |
| $t_{dly}$ | Stress 结束后到 $V_{DS}$ 达到 MP/MN measured point 的 test delay | stress→measurement 过渡早期 | 测量性能量 | 100 ns 标称；正文称 <100 ns | 系统级直接相关，不能只等同 gate edge | §I/III、Fig. 6/7；PAPER FACT；精确定义部分未公开 |
| Hysteresis | 界面/氧化层陷阱捕获/释放引起的快速、可恢复 $V_{th}$ shift；也包括慢 sweep 与快点测差异形成的测试方案初始偏差 | sweep、stress、recovery | 物理效应 | 无单一数值 | PCB 只用于施加/捕获，不直接“产生需求值” | §I/II；PAPER FACT |
| Recovery | stress removal 后 $V_{th}$ shift 随时间快速恢复；正 stress 后 $V_{DS}$ 从 MP 下降，负 stress 后从 MN 上升 | MEASUREMENT_P/N | 被测动态行为 | 1 $\mu$s 与 100 ns 比较给出 32%/22%低估 | PCB/示波器需足够快地捕获 | §I/II/III；PAPER FACT |
| Fixed $V_{DS}$ | B1505 扫描时 $V_{DS}$ 保持为 $V_{DS-C}$ | 初始 calibration sweep | 控制条件 | 10 V（论文示例） | 否；参数分析仪完成 | §I/II/III；PAPER FACT |
| Resistive load | $V_{DC}\rightarrow R_L\rightarrow$DUT 的串联负载回路 | 所有 Fig. 3 快速测试 | 系统拓扑 | 拓扑给出；器件细节无 | PCB/外部回路共同支持 | Fig. 3(a)；PAPER FACT |
| $R_L$ | 控制回路 $I_{DS}$ 的负载电阻 | 所有快速测试 | 控制/硬件参数 | 数值未给 | 需由 DUT/$V_{DC}$ 回路实现，不限定必须在 PCB | §II；PAPER_NOT_SPECIFIED（值/实现） |
| $V_{DC}$ | 电阻负载回路的 DC bias | 所有快速测试 | 控制量 | 数值未给 | 由外部供电，PCB/回路需接口 | Fig. 3(a)、§II；PAPER_NOT_SPECIFIED（值） |
| $R_{DUT}$ | measurement 状态下 DUT 等效电阻，受 $V_{th}$ shift 与 $V_{GS}$ 影响，通常大于额定 $R_{on}$ | MEASUREMENT_I/P/N | 隐含状态量/计算模型 | 未给 | 不直接控制 | 式 (2)、§II；PAPER FACT |

## 4. State Table

| State | Gate target | Drain condition | $I_{DS}$ condition | 目的 | 进入条件 | 退出条件 | 持续时间 | 高速切换要求 | PCB 完成 | 外部仪器完成 | 论文依据/状态 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SAFE_OFF | PROJECT_DESIGN_CHOICE_TO_BE_DEFINED | 建议性安全状态尚未冻结 | 未定义 | 上电、故障、待机安全 | 项目状态机决定 | 安全条件满足后进入测试 | 未定义 | 未定义 | 必须预留可验证的安全状态功能，但具体电位/拓扑由后续决定 | DC supply/pulse source 的安全配合待定义 | P1 无此状态；PAPER_NOT_SPECIFIED |
| PRECONDITION | $V_{GS}=0$ V | $V_{DS}=V_{DC}$ | $I_{DS}=0$ | reset SiO$_2$/SiC interface state，消除前次实验 hysteresis | 每次 calibration/positive/negative 序列开始 | 满足 precondition 时长/重置判据后进入下一状态 | $t_{pre}$；“long-term”，数值未知 | P1 称之后“quickly switches”；只有后续 stress→measurement 与 $t_{dly}$ 直接绑定 | 形成 0 V gate target 并保持 | $V_{DC}$ 保持；控制源定时；示波器可监测 | 式 (1)、Fig. 3(b1–b3)；PAPER FACT |
| POSITIVE_STRESS | $V_{GS}=V_{GS-P}$ | $V_{DS}\approx0$ | $I_{DS}=(V_{DC}-V_{DS})/R_L\approx V_{DC}/R_L$ | 施加正栅压应力，使 $V_{th}$ 正移 | PRECONDITION 结束 | $t_{str}$ 到期，立即转 MEASUREMENT_P | $t_{str}$ | **是**；退出边沿启动 $t_{dly}$ | 形成并保持 $V_{GS-P}$，随后转 measurement level | $V_{DC}$/$R_L$ 形成低电流回路；控制源触发；示波器采集 | 式 (4)、Fig. 3(b2)；PAPER FACT |
| NEGATIVE_STRESS | $V_{GS}=V_{GS-N}$ | Fig. 3(b3) 描绘为高 $V_{DS}$、近 $V_{DC}$ | 图示/串联回路意味着近零电流，但 P1 未给负应力状态公式 | 施加负栅压应力，使 $V_{th}$ 负移 | PRECONDITION 结束 | $t_{str}$ 到期，立即转 MEASUREMENT_N | $t_{str}$ | **是**；退出边沿启动 $t_{dly}$ | 形成并保持 $V_{GS-N}$，随后转 measurement level | 同上 | Fig. 3(b3)、§II；PAPER FACT（波形）+ ENGINEERING INFERENCE（$I_{DS}\approx0$） |
| MEASUREMENT_I | $V_{GS}=V_{GM-I}=\text{initial }V_{th}$ | $V_{DS}=V_{DC}R_{DUT}/(R_L+R_{DUT})$，目标约等于 $V_{DS-C}$ | $I_{DS}=I_{DM-I}>0$ | 取得 MI，量化方案自身的 $V_{th-IS}$ | PRECONDITION 后快速切换 | 捕获 MI/完成所需 acquisition | $t_{mea}$，数值未知 | 快速切换需要，但 P1 未将此转换定义为 $t_{dly}$ | 形成 $V_{GM-I}$、提供低寄生测量节点 | scope 捕获 MI；软件计算；B1505 提供曲线 | 式 (2)/(3)、Fig. 3(b1)；PAPER FACT |
| MEASUREMENT_P | $V_{GS}=V_{GM-P}$，单独调节 | 从约 0 V 上升到最大值 MP，再因 recovery 下降；MP 目标约 $V_{DS-C}$ | $I_{DM-P}\approx I_{DM-I}$ | 快速捕获正应力后阈值位移 | POSITIVE_STRESS 结束 | 捕获 MP，或继续观察 recovery 后退出 | $t_{mea}$，数值未知 | **是**；stress removal→MP 决定 $t_{dly}$ | 快速转到并保持 $V_{GM-P}$ | scope 同时采 $V_{GS}$/$V_{DS}$；软件提取 MP | Fig. 3(b2)、Fig. 6；PAPER FACT |
| MEASUREMENT_N | $V_{GS}=V_{GM-N}$，单独调节 | 从高值下降到最小值 MN，再因 recovery 上升；MN 目标约 $V_{DS-C}$ | $I_{DM-N}\approx I_{DM-I}$ | 快速捕获负应力后阈值位移 | NEGATIVE_STRESS 结束 | 捕获 MN，或继续观察 recovery 后退出 | $t_{mea}$，数值未知 | **是**；stress removal→MN 决定 $t_{dly}$ | 快速转到并保持 $V_{GM-N}$ | 同上 | Fig. 3(b3)、Fig. 7；PAPER FACT |

### 4.1 State Table 的七个关键结论

1. **precondition 为什么是 0 V？** P1 直接说明：长时间 precondition 用于 reset SiO$_2$/SiC interface state，消除前次实验造成的 hysteresis；式 (1) 同时规定 $V_{GS}=0$、$V_{DS}=V_{DC}$、$I_{DS}=0$，DUT 为 blocking state。P1 未给出微观 reset 判据、持续时间或完成检测方法。
2. **positive stress 时 DUT 状态：** 完全导通，$R_{on}\ll R_L$，所以 $V_{DS}\approx0$、$I_{DS}\approx V_{DC}/R_L$。P1 要求尽量减小 $I_{DS}$ 以避免 self-heating 影响阈值测量。
3. **negative stress 时 DUT 状态：** Fig. 3(b3) 显示负栅压期间 $V_{DS}$ 保持高位；结合回路可推得 DUT 阻断、$I_{DS}$ 近零，但 P1 没有给出与式 (4) 对应的负应力公式。因此“阻断/近零电流”中，波形是 PAPER FACT，精确电流关系是 ENGINEERING INFERENCE。
4. **measurement 不是简单关断：** 式 (2) 明确称其为 incomplete turn-ON；$V_{GS}$ 设在测量栅压、$R_{DUT}$ 有限、$I_{DS}$ 非零，必须形成可映射到基准曲线的 $V_{DS}$/$I_{DS}$ 点。
5. **$V_{GM-I}$、$V_{GM-P}$、$V_{GM-N}$ 不必相同：** $V_{GM-I}$ 设为 initial $V_{th}$；$V_{GM-P}$、$V_{GM-N}$ 要分别调整，以补偿 stress 引起的 $R_{DUT}$ 变化。
6. **为什么调 measurement gate voltage：** 使 MP/MN 的 $I_{DM-P}$、$I_{DM-N}$ 接近 $I_{DM-I}$，并使测量点 $V_{DS}\approx V_{DS-C}$，从而与同一 B1505 calibration curve 对齐，降低电流不一致导致的 $\Delta V_{th}$ 误差。
7. **哪次 transition 决定 $t_{dly}$：** POSITIVE_STRESS→MEASUREMENT_P 和 NEGATIVE_STRESS→MEASUREMENT_N。Calibration 的 PRECONDITION→MEASUREMENT_I 也要求快速，但 P1 的 $t_{dly}$ 定义与 100 ns 结果针对 stress removal 后到 MP/MN。

## 5. Timing Definition

### 5.1 四个时间量

- $t_{pre}$：0 V precondition procedure。其功能是重置界面状态并消除前次实验的 hysteresis；P1 只写“long-term”，未给统一数值和完成判据。
- $t_{str}$：$V_{GS-P}$ 或 $V_{GS-N}$ stress procedure 的持续时间。P1 改变 $t_{str}$ 研究不同 stress point/frequency 下的 $\Delta V_{th}$。
- $t_{mea}$：measurement gate level 被施加并采集 $V_{DS}$ 的 measurement procedure。MP/MN 极值和随后的 recovery 都发生在该区间；P1 未给固定长度。
- $t_{dly}$：stress 结束、$V_{GS}$ 切向 measurement state 后，到 $V_{DS}$ 到达 MP（最大）或 MN（最小）measurement point 的时间间隔。它位于 $t_{mea}$ 的最前部，不等于整个 $t_{mea}$，也不等于 gate-driver 自身的 propagation delay 或 rise/fall time。

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
                                                  t=0  measurement point
                                                  stress removal
                                                  gate transition starts
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
                                                  t=0  measurement point
                                                  stress removal
                                                  gate transition starts
                                                  <tdly>
```

### 5.3 “100 ns”原始定义与工程验收定义

**论文原始定义（PAPER FACT）：** Fig. 6(b)/Fig. 7(b) 把 $t=0$ 放在 stress→measurement 转换处，$t_{dly}$ 箭头终点是 $V_{DS}$ 的 measured point；正文写“After $V_{GS}$ switching from stress to measurement, $V_{DS}$ rapidly reaches its maximum and minimum values … and $t_{dly}$ is less than 100 ns.”因此 P1 的 100 ns 是 stress-to-valid-$V_{DS}$-extremum 的系统级时间，不只是 $V_{GS}$ edge time。

**PAPER_NOT_SPECIFIED：**

- stress removal 是控制命令时刻、$V_{GS}$ 边沿起点、10%/50%/90% crossing，还是离开 stress tolerance band；
- measured point 是原始波形全局极值、规定窗口内极值、滤波后极值，还是进入 settling band；
- 是否扣除 pulse generator、driver、probe、channel skew 或 cable propagation delay；
- 示波器带宽、采样率、探头带宽、deskew 和插值方式；
- 振铃导致多个局部极值时如何选择 MP/MN。

**未来 PCB engineering acceptance definition（PROJECT DESIGN CHOICE，尚未冻结）：** 必须由 Master 明确起点事件、终点算法、通道 deskew/de-embedding、搜索窗口和噪声/振铃规则，之后才能把“<100 ns”变成无歧义的 PASS/FAIL。当前状态为 **ENGINEERING_ACCEPTANCE_TO_BE_DEFINED**。

## 6. Calibration / $V_{th}$ Extraction Flow

### 6.1 P1 原始公式

Precondition blocking state，P1 式 (1)：

$$V_{GS}=0,\qquad V_{DS}=V_{DC},\qquad I_{DS}=0. \tag{1}$$

- $V_{GS}$：gate-source voltage；此处为 0 V。
- $V_{DS}$：drain-source voltage；阻断时等于外加 $V_{DC}$。
- $I_{DS}$：drain-source current；论文理想式写为 0。

Calibration measurement state，P1 式 (2)：

$$V_{GS}=V_{GM-I}=V_{th},\qquad V_{DS}=\frac{V_{DC}\times R_{DUT}}{R_L+R_{DUT}},$$

$$I_{DS}=\frac{V_{DC}-V_{DS}}{R_L}=I_{DM-I}. \tag{2}$$

- $V_{GM-I}$：Calibration measurement gate voltage，设为 initial $V_{th}$。
- $R_{DUT}$：measurement state 下 DUT 的等效电阻。
- $R_L$：串联负载电阻。
- $I_{DM-I}$：MI 点对应的 drain current。

Initial scheme shift，P1 式 (3)：

$$V_{th-IS}=V_{GM-I}-V_{th-MI}. \tag{3}$$

- $V_{th-MI}$：B1505 基准 sweep 上，与 $I_{DM-I}$ 相等的电流所对应的 gate voltage。
- $V_{th-IS}$：慢 sweep 与快速点测方案之间的 initial shift，用于后续校正。

Positive stress state，P1 式 (4)：

$$V_{GS}=V_{GS-P},\qquad V_{DS}\approx0,\qquad I_{DS}=\frac{V_{DC}-V_{DS}}{R_L}\approx\frac{V_{DC}}{R_L}. \tag{4}$$

- $V_{GS-P}$：positive gate stress voltage。
- $R_{on}\ll R_L$ 时，DUT fully ON，$V_{DS}$ 接近 0，电流主要由 $R_L$ 限制。

Corrected threshold shift，P1 式 (5)：

$$
\Delta V_{th}=\begin{cases}
V_{th-PS}-V_{th-IS}, & \text{positive stress},\\
V_{th-NS}-V_{th-IS}, & \text{negative stress}.
\end{cases}\tag{5}
$$

- $V_{th-PS}$/$V_{th-NS}$：在 MP/MN 测得、仍包含 scheme initial shift 的正/负应力阈值位移。
- $\Delta V_{th}$：排除 $V_{th-IS}$ 后的最终阈值位移。

P1 没有另行印出 $V_{th-PS}$、$V_{th-NS}$ 的展开公式，只写明 MP/MN “using the same method as described in (3)”。因此以下是对论文方法的 **ENGINEERING RESTATEMENT**，不是新增的论文编号公式：

$$V_{th-PS}=V_{GM-P}-V_{th-MP},\qquad V_{th-NS}=V_{GM-N}-V_{th-MN},$$

其中 $V_{th-MP}$/$V_{th-MN}$ 分别是 B1505 calibration curve 上与 $I_{DM-P}$/$I_{DM-N}$ 对应的 gate voltage。

### 6.2 为什么需要 fixed $V_{DS-C}$、$I_{th}$ 和 gate-voltage adjustment

1. **为什么 fixed $V_{DS-C}$：** 基准 $I_{DS}$–$V_{GS}$ curve 必须在固定 drain bias 下建立，快速 measurement point 也要处在相近 drain bias，才能把测得电流映射到同一曲线。P1 还要求 measurement 时 DUT 在 saturation region：$V_{DS-C}>V_{GS}-V_{th}$。
2. **$I_{th}$ 如何定义 initial $V_{th}$：** 在 B1505 基准 curve 上，$I_{DS}$ crossing $I_{th}$ 时的 $V_{GS}$ 定义为 initial $V_{th}$。论文 DUT 使用 $I_{th}=10$ mA。
3. **为什么实际 $V_{DS}\approx V_{DS-C}$：** 若 MI/MP/MN 的 drain bias 与 calibration curve 不同，同一个 $I_{DS}$ 不再对应相同的曲线位置，会破坏直接查表/插值的可比性。
4. **为什么 MI 需要映射回 calibration curve：** B1505 的慢阶梯扫栅本身会诱发阈值 shift，而 Fig. 3 快速点测得到的 MI 会偏离慢扫曲线；这个偏差正是需要量化并扣除的 $V_{th-IS}$。
5. **$V_{th-IS}$ 逻辑：** 先由 MI 算 $I_{DM-I}$，在 curve 上找 $V_{th-MI}$，再用实际施加的 $V_{GM-I}$ 减去它。
6. **MP/MN 逻辑：** 由 MP/MN 的 $V_{DS}$ 计算 $I_{DM-P/N}$，映射到相同 curve，按与式 (3) 相同的方法得到 raw $V_{th-PS/NS}$。
7. **为什么单独调节 $V_{GM-P/N}$：** stress 后 $R_{DUT}$ 改变，若保持同一 measurement gate voltage，MP/MN 的 $V_{DS}$ 和 $I_{DS}$ 会偏离 calibration 条件。P1 保持 $V_{DC}$、$R_L$ 不变，只调 $V_{GM-P/N}$，直到 $I_{DM-P/N}\approx I_{DM-I}$。
8. **hysteresis correction：** Calibration 先测出测试方案自身的 initial shift $V_{th-IS}$；positive/negative raw shifts 再各自减去同一个 $V_{th-IS}$，得到式 (5) 的 corrected $\Delta V_{th}$。

### 6.3 Drain load 与测量链

Fig. 3(a) 的电流路径为：

$$V_{DC}\rightarrow R_L\rightarrow \text{DUT Drain}\rightarrow \text{DUT Source}\rightarrow \text{return}.$$

串联回路中 $R_L$ 的压降为 $V_{DC}-V_{DS}$，所以

$$I_{DS}=\frac{V_{DC}-V_{DS}}{R_L}.$$

高速测试中不需要让参数分析仪在 100 ns 内直接扫完整曲线；只需示波器快速捕获 $V_{DS}$，在已知 $V_{DC}$、$R_L$ 下计算一个瞬时 $I_{DS}$，再使用预先测得的 B1505 curve 完成等效 gate-voltage 映射。

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
| 基准 $I_{DS}$–$V_{GS}$ curve | B1505 | 直接扫描测量 |
| $V_{DS-C}$、$I_{th}$ | B1505 test definition | 控制/分析设定 |
| Initial $V_{th}$ | 基准 curve | 提取量 |
| $V_{GS}$ stress/measurement waveform | Fig. 3 平台 + oscilloscope | 控制并直接测量 |
| $V_{DS}(t)$、MI/MP/MN | Fig. 3 平台 + oscilloscope | 直接测量/波形特征提取 |
| $V_{DC}$、$R_L$ | DC supply/load definition | 已知控制/硬件参数；P1 未说明是否同步记录瞬时值 |
| $I_{DM-I/P/N}$ | 后处理 | 由 $V_{DS}$、$V_{DC}$、$R_L$ 计算 |
| $V_{th-MI/MP/MN}$ | 后处理 + B1505 curve | 查表/插值计算 |
| $V_{th-IS/PS/NS}$、$\Delta V_{th}$ | 后处理 | 公式计算 |
| $t_{dly}$ | oscilloscope $V_{GS}$/$V_{DS}$ 波形 | 时间差提取 |

## 7. PCB vs External Equipment Boundary

### A. PCB 必须实现的功能

- 接收外部时序控制，并在 DUT source reference 下形成 precondition、positive stress、negative stress、measurement-I/P/N 所需 gate target。
- 支持 $0\rightarrow V_{GM-I}$、$0\rightarrow V_{GS-P}\rightarrow V_{GM-P}$、$0\rightarrow V_{GS-N}\rightarrow V_{GM-N}$ 的功能序列。
- 允许 $V_{GM-I}$、$V_{GM-P}$、$V_{GM-N}$ 在系统层面独立设定/调整；具体产生方式 PAPER_NOT_SPECIFIED。
- 支持 stress→measurement 的快速转换，使整个系统有可能达到论文的 <100 ns $t_{dly}$。
- 提供 DUT gate/source 和 drain/source 的可测接口，使 $V_{GS}$ 与 $V_{DS}$ 能被同时观察；具体 probe/connector PAPER_NOT_SPECIFIED。
- 与 $V_{DC}$–$R_L$–DUT 串联回路兼容，并维持所需电压/电流/瞬态完整性；具体器件与布局由后续子项目决定。

### B. 外部 pulse generator 必须实现的功能

- 给出可重复的 state-transition command/trigger。
- 控制或触发 $t_{pre}$、$t_{str}$、$t_{mea}$，并允许改变 $t_{str}$、测试点和 $t_{dly}$ 相关控制时序。
- 为示波器提供稳定触发参考。
- 输出电平、极性、通道数、同步方式、抖动上限均 PAPER_NOT_SPECIFIED。

### C. 外部 DC supply 必须实现的功能

- 提供稳定 $V_{DC}$，使 calibration 时可通过调整 $V_{DC}$ 与 $R_L$ 达到 MI 的 $V_{DS}\approx V_{DS-C}$。
- 在 subsequent stress measurement 中保持 $V_{DC}$ 不变。
- 电压范围、动态阻抗、限流、噪声、远端感测和保护均 PAPER_NOT_SPECIFIED。

### D. DUT / $R_L$ 回路必须实现的功能

- 实现 $V_{DC}\rightarrow R_L\rightarrow DUT\rightarrow return$ 串联路径。
- $R_L$ 控制 positive-stress ON-state current，并应使 $I_{DS}$ 尽可能小以抑制 self-heating。
- Calibration 调整 $V_{DC}$/$R_L$ 后，positive/negative 测试保持二者不变。
- $R_L$ 数值、脉冲功率、寄生参数、安装位置、技术类型均 PAPER_NOT_SPECIFIED。

### E. Oscilloscope 必须测量的内容

- 同时捕获 $V_{GS}(t)$ 和 $V_{DS}(t)$。
- 识别 MI、MP、MN 及其时刻。
- 从 stress→measurement 的 $V_{GS}$ 事件到 MP/MN 提取 $t_{dly}$。
- 观察 measurement 后 recovery 波形。
- 带宽、采样率、探头、deskew、滤波/平均均 PAPER_NOT_SPECIFIED。

### F. B1505 / EasyEXPERT calibration 必须完成的内容

- 在固定 $V_{DS-C}$ 下获得 initial $I_{DS}$–$V_{GS}$ sweep curve。
- 用 $I_{th}$ 定义 initial $V_{th}$。
- 导出可用于 $I_{DM-I/P/N}\rightarrow V_{th-MI/MP/MN}$ 映射的数据。
- sweep range、step、rate、方向、hold time、温度与 compliance 除论文所述条件外均 PAPER_NOT_SPECIFIED。

### G. 后处理软件必须完成的内容

- 从 $V_{DS}$ 极值和已知 $V_{DC}$/$R_L$ 计算 $I_{DM-I/P/N}$。
- 对 B1505 curve 进行一致的查找/插值，得到等效 gate-voltage coordinate。
- 计算 $V_{th-IS}$、$V_{th-PS}$、$V_{th-NS}$ 和式 (5) 的 $\Delta V_{th}$。
- 检查 $V_{DS}\approx V_{DS-C}$、$I_{DM-P/N}\approx I_{DM-I}$、saturation condition 和 current-deviation 条件。
- 保存原始波形、元数据和计算过程；文件格式/算法/不确定度方法 PAPER_NOT_SPECIFIED。

## 8. Requirements List

“Status=CONFIRMED”表示论文直接支持需求的功能或条件；“OPEN”表示论文目标明确但工程验收/数值/实现尚未冻结。Classification 明确它是 paper requirement、paper example，还是 project requirement。

| ID | Requirement | Source | Reason | Verification | Status / Classification |
|---|---|---|---|---|---|
| REQ-FUNC-001 | 系统必须实现 Fig. 3(a) 的串联电阻负载测试功能：$V_{DC}\rightarrow R_L\rightarrow DUT\rightarrow return$。 | Fig. 3(a), §II | 通过 $V_{DS}$ 间接获得 $I_{DS}$。 | 连通性检查 + 低能量功能测试，核对 $I_{DS}=(V_{DC}-V_{DS})/R_L$。 | CONFIRMED / PAPER REQUIREMENT |
| REQ-FUNC-002 | 系统必须支持 Calibration、Positive stress、Negative stress 三条序列，每条包含规定的 precondition/stress/measurement 状态。 | Fig. 3(b1–b3), Fig. 4 | 这是论文完整提取流程。 | 示波器记录三条完整状态波形。 | CONFIRMED / PAPER REQUIREMENT |
| REQ-FUNC-003 | Measurement state 必须使 DUT 进入不完全导通并产生有限、可计算的 $I_{DS}$，不能仅实现关断。 | 式 (2), §II | MI/MP/MN 必须映射到 calibration curve。 | 测得 $0<V_{DS}<V_{DC}$ 且计算 $I_{DS}>0$；具体容差待定。 | CONFIRMED；PASS=ENGINEERING_ACCEPTANCE_TO_BE_DEFINED |
| REQ-FUNC-004 | 系统必须支持在 measurement 早期捕获 $V_{DS}$ 的 MI/MP/MN 极值及随后 recovery。 | Fig. 3(b), §II, Fig. 6/7 | 快恢复会导致阈值位移被低估。 | 示波器波形能区分极值和后续单调恢复趋势。 | CONFIRMED；极值算法 OPEN |
| REQ-FUNC-005 | Calibration 完成后，stress 测试必须保持 $V_{DC}$ 与 $R_L$ 不变，只通过调节 $V_{GM-P/N}$ 完成对齐。 | §III step 3 | 保持 measurement circuit 条件一致。 | 记录配置/波形，确认 stress 测试未改变 $V_{DC}$、$R_L$。 | CONFIRMED / PAPER REQUIREMENT |
| REQ-VOLT-001 | PRECONDITION gate target 必须为 $V_{GS}=0$ V。 | 式 (1) | reset interface state 并阻断 DUT。 | 测量 precondition $V_{GS}$；容差待定。 | CONFIRMED；tolerance OPEN |
| REQ-VOLT-002 | 系统必须支持独立的 positive 和 negative stress gate targets $V_{GS-P}$、$V_{GS-N}$。 | Table I, Fig. 3 | 复现 bipolar switching gate bias stress。 | 测量两种 stress level。 | CONFIRMED；论文示例 +20/−5 V，不是通用冻结值 |
| REQ-VOLT-003 | 系统必须支持 $V_{GM-I}$、$V_{GM-P}$、$V_{GM-N}$ 三个 measurement gate targets，并允许 $V_{GM-P/N}$ 分别调节。 | Table I, §II | 补偿 stress 后 $R_{DUT}$ 改变。 | 扫描/设定三个 level，验证可独立达到目标。 | CONFIRMED；范围/分辨率 OPEN |
| REQ-VOLT-004 | B1505 initial curve 必须在固定 $V_{DS-C}$ 下取得；论文复现实验值为 10 V。 | §II, §III step 1 | 为高速点测提供同一参考曲线。 | B1505 test record。 | CONFIRMED / PAPER REQUIREMENT；10 V 为 PAPER EXAMPLE VALUE |
| REQ-VOLT-005 | MI、MP、MN 的 $V_{DS}$ 必须约等于 $V_{DS-C}$。 | §II, §III step 2 | 保持与 calibration curve 的 drain-bias 对齐。 | 比较各 measured point 与 $V_{DS-C}$。 | CONFIRMED；PASS tolerance=ENGINEERING_ACCEPTANCE_TO_BE_DEFINED |
| REQ-VOLT-006 | Measurement operating point 必须满足论文给出的 saturation condition：$V_{DS-C}>V_{GS}-V_{th}$。 | §II | 保持 curve mapping 的工作区条件。 | 用各点记录量计算/检查不等式。 | CONFIRMED；margin OPEN |
| REQ-TIME-001 | 系统必须支持从 positive/negative stress state 快速切换到相应 measurement state。 | Abstract, Fig. 3, §III | 抑制 stress removal 后 recovery 导致的低估。 | scope 同时测 control/$V_{GS}$/$V_{DS}$。 | CONFIRMED / PAPER REQUIREMENT |
| REQ-TIME-002 | Fig. 3 功能复现应达到 stress→MP/MN 的 $t_{dly}<100$ ns；在精确事件定义冻结前不得仅以 gate edge 判定通过。 | Fig. 6(b), Fig. 7(b), §III | 论文核心性能目标。 | scope 提取 start event→$V_{DS}$ extremum。 | OPEN；数值来自 PAPER FACT，PASS=ENGINEERING_ACCEPTANCE_TO_BE_DEFINED |
| REQ-TIME-003 | 系统必须支持“long-term” $t_{pre}$，以在每次序列前执行相同 precondition。 | §II | 消除 previous-experiment hysteresis。 | 时序记录 + 重复性/重置效果测试。 | OPEN；duration/PASS PAPER_NOT_SPECIFIED |
| REQ-TIME-004 | 系统必须允许编程 $t_{str}$；P1 展示 0.2–200 $\mu$s，并使用 10 $\mu$s 与 2 $\mu$s 示例。 | §III, Fig. 6/7/10 | 测试不同 stress point/frequency。 | scope 测各 programmed duration。 | CONFIRMED capability；frequency mapping 有论文歧义 |
| REQ-TIME-005 | 系统必须提供足够的 $t_{mea}$ 捕获 MP/MN 和其 recovery。 | Fig. 3/4, §II | 极值与恢复均是提取对象。 | scope 检查 acquisition window 覆盖极值/恢复。 | OPEN；duration PAPER_NOT_SPECIFIED |
| REQ-TIME-006 | 系统必须允许改变 test delay，以取得不同 $t_{dly}$ 下的 $\Delta V_{th}$ recovery 数据。 | §III step 5, Fig. 10 | 验证 delay 对测量的影响。 | 多组时序测试，确认目标 delay 可重复。 | CONFIRMED capability；范围/步进 OPEN |
| REQ-MEAS-001 | 示波器测量必须同时包含 $V_{GS}(t)$ 和 $V_{DS}(t)$，并具有共同时间基准。 | Fig. 6/7 | $t_{dly}$ 起点来自 gate transition，终点来自 drain response。 | 两通道同步波形 + deskew 记录。 | CONFIRMED functional need；instrument specs OPEN |
| REQ-MEAS-002 | 后处理必须使用 P1 式 (2) 计算 $I_{DS}=(V_{DC}-V_{DS})/R_L$。 | 式 (2)/(4) | 将高速电压点转换为 curve lookup current。 | 用已知测试向量做计算单元测试。 | CONFIRMED / PAPER REQUIREMENT |
| REQ-MEAS-003 | 后处理必须从 MI、MP、MN 分别得到 $I_{DM-I}$、$I_{DM-P}$、$I_{DM-N}$。 | Table I, §II | 三个阈值位移的输入。 | 对带已知极值的波形做回放。 | CONFIRMED；extremum algorithm OPEN |
| REQ-MEAS-004 | 后处理必须把 $I_{DM-I/P/N}$ 映射到同一 fixed-$V_{DS-C}$ B1505 curve。 | Fig. 2, 式 (3), §II | 获得等效 gate-voltage coordinate。 | curve lookup/interpolation 单元测试。 | CONFIRMED；interpolation method OPEN |
| REQ-MEAS-005 | 后处理必须按 P1 式 (3) 计算 $V_{th-IS}$，并按与式 (3) 相同的方法取得 $V_{th-PS/NS}$。 | 式 (3), §II | 量化 raw shift。 | 对论文逻辑构造的数值用例复算。 | CONFIRMED；P/N 展开式为 ENGINEERING RESTATEMENT |
| REQ-MEAS-006 | 后处理必须按 P1 式 (5) 从 positive/negative raw shift 中减去 $V_{th-IS}$。 | 式 (5) | 排除测试方案自身 hysteresis。 | 公式单元测试 + 数据追溯。 | CONFIRMED / PAPER REQUIREMENT |
| REQ-MEAS-007 | $I_{DM-P}$、$I_{DM-N}$ 必须接近 $I_{DM-I}$；P1 实验将低于 $\pm20\%$ 的偏差视为可接受。 | §II/III, Fig. 8(b) | 限制 operating-current 不一致造成的 $\Delta V_{th}$ 偏差。 | 比较三者并报告相对偏差。 | CONFIRMED principle；百分比定义/是否采纳 ±20% 为项目 PASS 待 Master 决定 |
| REQ-MEAS-008 | B1505 必须通过 $I_{th}$ crossing 提取 initial $V_{th}$；P1 DUT 使用 $I_{th}=10$ mA。 | §I/II/III | 决定 $V_{GM-I}$ 和 curve reference。 | B1505 数据重算 crossing。 | CONFIRMED；10 mA 为 PAPER EXAMPLE VALUE |
| REQ-MEAS-009 | 在依赖平行位移法之前，目标 DUT/条件应验证 sweep curves 在 $I_{DS}\approx I_{th}$ 附近近似平行。 | Fig. 2, Fig. 8(a), §III | 平行 shift 是点测量映射的理论基础。 | stress 前后 B1505 curve 对比。 | OPEN project verification；P1 报告波动在 1% 内 |
| REQ-MEAS-010 | Positive-stress 回路电流必须尽量小以避免 DUT self-heating 影响 $V_{th}$。 | 式 (4) 后正文 | 隔离电荷俘获效应与热效应。 | 测/算 $I_{DS}$、功耗和温升代理量。 | CONFIRMED principle；最大电流/温升 PASS 未定义 |
| REQ-CTRL-001 | 控制系统必须按确定顺序生成 PRECONDITION→STRESS→MEASUREMENT，并给示波器提供可重复触发。 | Fig. 3/4 支持 sequence；触发接口未公开 | 支持状态对齐和波形比较。 | 重复 N 次波形，检查顺序和 jitter。 | OPEN / ENGINEERING INTERFACE REQUIREMENT；sequence 为 PAPER FACT |
| REQ-CTRL-002 | 系统必须允许在 calibration 中调 $V_{DC}$/$R_L$，在 stress test 中固定二者并调 $V_{GM-P/N}$。 | §III steps 2–3 | 按论文迭代达到 $V_{DS}$/$I_{DS}$ 对齐。 | 配置审查 + 波形验证。 | CONFIRMED / PAPER REQUIREMENT |
| REQ-CTRL-003 | 系统应支持 multiple-pulse gate stress；P1 使用总时长 $10^5\ \mu$s 的 pulse train 获得稳定 premeasurement trap occupation。 | §III, Fig. 10 前正文 | 复现 P1 稳定 acquisition protocol。 | pulse count/总时长记录。 | CONFIRMED for full paper reproduction；最小 Fig. 3 功能范围可由 Master裁剪 |
| REQ-SAFE-001 | 项目必须定义一个独立于 PRECONDITION 的 SAFE_OFF 状态及其进入/退出逻辑。 | 非 P1 | 上电、故障、探测连接时需要可验证安全行为。 | 故障注入/上电关断测试。 | OPEN / PROJECT REQUIREMENT；具体 gate/drain target 未定义 |
| REQ-SAFE-002 | 项目必须定义 power sequencing、过压/过流/误触发保护和能量限制。 | 非 P1 | P1 未公开实现，原型验证需要安全边界。 | 设计审查 + 保护触发测试。 | OPEN / PROJECT REQUIREMENT |
| REQ-VERIFY-001 | 原型必须用同一时间基准同时验证 control、$V_{GS}$、$V_{DS}$，并提取完整 system $t_{dly}$。 | Fig. 6/7 | 防止把 driver edge time 误当 test delay。 | Prototype oscilloscope validation。 | OPEN；acceptance definition 待冻结 |
| REQ-VERIFY-002 | 原型必须验证 MI/MP/MN 均满足 $V_{DS}\approx V_{DS-C}$，并记录偏差。 | §II/III | 验证 calibration compatibility。 | measured-point comparison。 | OPEN；tolerance 待冻结 |
| REQ-VERIFY-003 | 原型必须验证 $I_{DM-P/N}$ 与 $I_{DM-I}$ 的匹配，并记录调整后的 $V_{GM-P/N}$。 | §II/III | 控制 current mismatch error。 | current calculation report。 | CONFIRMED method；project PASS 待 Master 决定 |
| REQ-VERIFY-004 | 软件必须保留从 raw $V_{GS}/V_{DS}$、$V_{DC}/R_L$、B1505 curve 到最终 $\Delta V_{th}$ 的可追溯链。 | 式 (2)–(5) | 防止 correction/映射不可审计。 | 数据包审查 + 重算。 | OPEN / ENGINEERING REQUIREMENT |

## 9. Verification Matrix

| Requirement ID | Requirement | Verification method | Instrument | Measured quantity | Pass condition | Design stage |
|---|---|---|---|---|---|---|
| REQ-FUNC-001 | 电阻负载串联回路 | Inspection + low-energy functional test | DMM/scope/DC supply | $V_{DC}$、$V_{DS}$、$R_L$、回路电流 | 拓扑正确且式 (2) 一致；数值误差限待定义 | Bring-up |
| REQ-FUNC-002 | 三条测试序列 | Waveform review | Pulse source + scope | state order、gate level、duration | Calibration/P/N 三条序列均与 Fig. 3(b) 顺序一致 | Bring-up |
| REQ-FUNC-003 | 不完全导通 measurement | Operating-point test | Scope | $V_{GS}$、$V_{DS}$、computed $I_{DS}$ | $0<V_{DS}<V_{DC}$ 且 $I_{DS}>0$；margin 待定义 | Functional prototype |
| REQ-FUNC-004 | 捕获极值和 recovery | Transient capture | Scope + software | MI/MP/MN、post-extremum trend | 极值和后续恢复可区分；算法 acceptance 待定义 | Prototype validation |
| REQ-FUNC-005 | Calibration 后固定 $V_{DC}$/$R_L$ | Configuration audit | DC supply + test record | $V_{DC}$、$R_L$ config | P/N 测试与已接受 calibration 配置相同 | Experiment setup |
| REQ-VOLT-001 | 0 V precondition | Static/dynamic measurement | Scope/DMM | precondition $V_{GS}$ | Target=0 V；tolerance=ENGINEERING_ACCEPTANCE_TO_BE_DEFINED | Bring-up |
| REQ-VOLT-002 | 正/负 stress levels | Dynamic measurement | Scope | $V_{GS-P}$、$V_{GS-N}$ | 达到已批准实验 profile；P1 示例 +20/−5 V | Functional prototype |
| REQ-VOLT-003 | 三个 measurement levels 可独立调 | Parameter sweep | Scope + controller | $V_{GM-I/P/N}$ | 三者能独立达到已批准 target；范围/分辨率待定 | Functional prototype |
| REQ-VOLT-004 | B1505 fixed $V_{DS-C}$ curve | Calibration record review | B1505 | $V_{DS}$ during sweep | 固定于批准的 $V_{DS-C}$；论文复现实验为 10 V | Calibration |
| REQ-VOLT-005 | MI/MP/MN 对齐 $V_{DS-C}$ | Point comparison | Scope + software | $V_{DS,MI/MP/MN}-V_{DS-C}$ | ENGINEERING_ACCEPTANCE_TO_BE_DEFINED | Calibration/prototype |
| REQ-VOLT-006 | Saturation condition | Calculation | B1505 + scope + software | $V_{DS-C}$、$V_{GS}$、$V_{th}$ | 每个 measurement point 满足 $V_{DS-C}>V_{GS}-V_{th}$；margin 待定 | Data acceptance |
| REQ-TIME-001 | stress→measurement 快切换 | Time-domain measurement | Scope | control、$V_{GS}$、$V_{DS}$ | 状态转换可重复且产生 MP/MN；速度由 REQ-TIME-002 判定 | Prototype validation |
| REQ-TIME-002 | $t_{dly}<100$ ns | Synchronous transient measurement | Scope + probes | start event→MP/MN time | 事件定义冻结后 $t_{dly}<100$ ns；当前 ENGINEERING_ACCEPTANCE_TO_BE_DEFINED | Prototype validation |
| REQ-TIME-003 | long-term $t_{pre}$ | Duration + reset-repeatability study | Controller + B1505/scope | $t_{pre}$、重复 MI/$V_{th-IS}$ | Duration/stability criterion=ENGINEERING_ACCEPTANCE_TO_BE_DEFINED | Method validation |
| REQ-TIME-004 | 可编程 $t_{str}$ | Timing sweep | Pulse source + scope | stress width | 覆盖批准 protocol；full paper reproduction 候选 0.2–200 $\mu$s | Controller validation |
| REQ-TIME-005 | 足够 $t_{mea}$ | Acquisition-window review | Scope | measurement window、extremum/recovery coverage | 覆盖选定极值与 recovery interval；数值待定义 | Experiment setup |
| REQ-TIME-006 | 可变 $t_{dly}$ | Delay sweep | Controller + scope | programmed/measured $t_{dly}$ | 覆盖批准的 delay set；P1 对比含 0.1/1 $\mu$s | Method validation |
| REQ-MEAS-001 | 同时采 $V_{GS}$/$V_{DS}$ | Channel synchronization/deskew | Scope + two probes | relative time skew | 通道同一时基；允许 skew=ENGINEERING_ACCEPTANCE_TO_BE_DEFINED | Instrument qualification |
| REQ-MEAS-002 | 式 (2) 电流计算 | Software unit test | Software | known $V_{DC},V_{DS},R_L$ vectors | 与解析结果一致；数值精度待软件规范 | Software verification |
| REQ-MEAS-003 | MI/MP/MN 到三电流 | Waveform replay | Software | extrema、$I_{DM-I/P/N}$ | 对 reference waveform 输出正确；极值规则待冻结 | Software verification |
| REQ-MEAS-004 | 映射到同一 B1505 curve | Lookup/interpolation test | Software + B1505 export | input current、mapped gate voltage | 使用同一 approved curve；插值误差限待定义 | Software verification |
| REQ-MEAS-005 | raw shifts | Formula test | Software | $V_{GM}$、mapped voltage、raw shift | 式 (3) 与相同方法的 P/N 结果可重算 | Software verification |
| REQ-MEAS-006 | scheme-shift correction | Formula test | Software | $V_{th-IS/PS/NS}$、$\Delta V_{th}$ | 精确实现式 (5) | Software verification |
| REQ-MEAS-007 | $I_{DM}$ 匹配 | Current-consistency report | Scope + software | $I_{DM-P/N}$ vs $I_{DM-I}$ | P1 报告低于 ±20%；项目是否沿用及百分比定义待 Master 批准 | Method validation |
| REQ-MEAS-008 | $I_{th}$ crossing 初始阈值 | Independent re-extraction | B1505 + software | $I_{DS}$–$V_{GS}$、crossing | 在批准的 $I_{th}$ 得到一致 initial $V_{th}$；论文值 10 mA | Calibration |
| REQ-MEAS-009 | 平行移位假设 | Pre/post-stress curve comparison | B1505 + software | $\Delta V_{th}$ vs $I_{DS}$ near $I_{th}$ | P1 结果为 1% 内；项目 acceptance/window 待定义 | Method qualification |
| REQ-MEAS-010 | 限制 self-heating | Electrical/thermal assessment | Scope + DC supply + temperature method TBD | $I_{DS}$、$V_{DS}$、pulse energy、temperature proxy | 最大电流/能量/温升=ENGINEERING_ACCEPTANCE_TO_BE_DEFINED | Design verification |
| REQ-CTRL-001 | 状态顺序和触发可重复 | Repetition/jitter test | Pulse source + scope | order、period、jitter | 顺序正确；允许 jitter 和重复次数待定义 | Controller validation |
| REQ-CTRL-002 | 调参边界正确 | Procedure audit | Test record + instruments | $V_{DC}$/$R_L$/$V_{GM}$ changes | Calibration 调 $V_{DC}/R_L$；stress test 固定二者、只调 $V_{GM-P/N}$ | Experiment qualification |
| REQ-CTRL-003 | Multiple-pulse stress | Pulse-train verification | Pulse source + scope/counter | pulse count、width、total duration | 若 full reproduction：总 stress duration 达 $10^5\ \mu$s；其他 profile 由 Master 定义 | Controller validation |
| REQ-SAFE-001 | SAFE_OFF | State/fault test | Scope + supplies | gate/drain state、stored energy | ENGINEERING_ACCEPTANCE_TO_BE_DEFINED | Architecture/prototype safety |
| REQ-SAFE-002 | Sequencing/protection | Design review + fault injection | Supplies/scope/protection monitor | overvoltage/current/false trigger response | ENGINEERING_ACCEPTANCE_TO_BE_DEFINED | Architecture/prototype safety |
| REQ-VERIFY-001 | 完整 system $t_{dly}$ 验证 | Three-signal transient capture | Scope | control/$V_{GS}$/$V_{DS}$ timing | 不以单独 gate edge 代替；具体 <100 ns 判据待冻结 | Prototype validation |
| REQ-VERIFY-002 | $V_{DS}$ 对齐报告 | Automated comparison | Scope + software | MI/MP/MN vs $V_{DS-C}$ | ENGINEERING_ACCEPTANCE_TO_BE_DEFINED | Prototype validation |
| REQ-VERIFY-003 | Current match 报告 | Automated comparison | Scope + software | $I_{DM-P/N}$ vs $I_{DM-I}$ | Master 批准的 tolerance；P1 参考低于 ±20% | Prototype validation |
| REQ-VERIFY-004 | 全链可追溯 | Dataset audit/recompute | B1505 + scope + software | raw/calibration/config/results | 独立重算得到相同 $\Delta V_{th}$；数值 tolerance 待定 | Experiment release |

## 10. OPEN / PAPER_NOT_SPECIFIED List

| 项目 | 状态 | P1 实际公开到什么程度 |
|---|---|---|
| Fig. 3(a) 电阻负载系统拓扑 | PAPER_SPECIFIED | 给出 $V_{DC}$、$R_L$、DUT、VGS driver 的功能连接。 |
| Fig. 3(b) 三类 gate/drain 波形与状态顺序 | PAPER_SPECIFIED | 给出 b1/b2/b3 的目标电位和 MI/MP/MN 行为。 |
| Multistage adjustable gate driver 具体 schematic | PAPER_NOT_SPECIFIED | 仅给功能名称和硬件照片。 |
| Driver IC 型号 | PAPER_NOT_SPECIFIED | 未公开。 |
| Driver output impedance/source-sink current | PAPER_NOT_SPECIFIED | 未公开。 |
| Gate resistor $R_g$ | PAPER_NOT_SPECIFIED | 未公开。 |
| Gate-loop decoupling/rail capacitor | PAPER_NOT_SPECIFIED | 未公开。 |
| 0 V precondition 的具体电路/0 V clamp 拓扑 | PAPER_NOT_SPECIFIED | 仅规定 gate target=0 V。 |
| Positive/negative/measurement rail 的产生方式 | PAPER_NOT_SPECIFIED | 仅规定功能电位。 |
| $V_{GM-I/P/N}$ 数值、范围、分辨率、调节算法 | PAPER_PARTIALLY_SPECIFIED | $V_{GM-I}$ 的逻辑和 P/N 独立调节原则已给；实现及数值未给。 |
| Exact state-control circuit/logic levels/truth table | PAPER_NOT_SPECIFIED | 只有波形级策略。 |
| Pulse generator 型号、通道、输出电平、抖动 | PAPER_NOT_SPECIFIED | Fig. 5 只标功能设备。 |
| $t_{pre}$ 数值与 reset-complete 判据 | PAPER_NOT_SPECIFIED | 仅称 long-term precondition。 |
| $t_{mea}$ 长度与退出条件 | PAPER_NOT_SPECIFIED | 只给 measurement procedure。 |
| $t_{dly}$ 精确起止百分比、settling/filter/window | PAPER_PARTIALLY_SPECIFIED | stress→measurement 后到 $V_{DS}$ 最大/最小 measured point；精确算法未给。 |
| $t_{str}$ 与“switching frequency”的严格换算/占空比 | PAPER_PARTIALLY_SPECIFIED | 给了多个数值映射，但未给统一时序公式，且示例存在表面不一致。 |
| $V_{DC}$ 数值 | PAPER_NOT_SPECIFIED | 只说明是 DC voltage bias。 |
| $R_L$ 数值、技术、功率、脉冲额定、寄生 | PAPER_NOT_SPECIFIED | 只说明用于控制 $I_{DS}$。 |
| 目标 DUT 的确切型号/栅电荷/电容参数 | PAPER_PARTIALLY_SPECIFIED | 只给商用 1.2 kV、TO-247。 |
| Negative-stress 状态的明确 $V_{DS}$/$I_{DS}$ 公式 | PAPER_PARTIALLY_SPECIFIED | Fig. 3(b3) 给波形，正文无对应方程。 |
| B1505 型号类别 | PAPER_SPECIFIED | 明确 Keysight B1505。 |
| EasyEXPERT 的具体 test definition/workflow | PAPER_NOT_SPECIFIED | P1 只明确 B1505 仪器，没有说明 EasyEXPERT 配置。 |
| B1505 sweep range/step/rate/direction/hold/compliance | PAPER_NOT_SPECIFIED | 仅称较慢 staircase increasing scan；Fig. 1 讨论 up/down sweep。 |
| 实验温度、温控与温度稳定判据 | PAPER_NOT_SPECIFIED | 本文方法段未公开。 |
| $V_{DS}\approx V_{DS-C}$ 的允许误差 | PAPER_NOT_SPECIFIED | 只有“approx/align”。 |
| $I_{DM-P/N}\approx I_{DM-I}$ 的项目 PASS | PAPER_PARTIALLY_SPECIFIED | P1 实验偏差低于 ±20% 并认为可接受；百分比定义与通用性未给。 |
| self-heating 的最大允许 $I_{DS}$/能量/温升 | PAPER_NOT_SPECIFIED | 只要求 $I_{DS}$ should be minimized。 |
| MI/MP/MN 极值检测、滤波、振铃处理 | PAPER_NOT_SPECIFIED | 只定义极值点。 |
| Oscilloscope 型号/带宽/采样率 | PAPER_NOT_SPECIFIED | Fig. 5 标注 oscilloscope，正文未给规格。 |
| $V_{GS}$/$V_{DS}$ probe 型号、带宽、输入电容、接法 | PAPER_NOT_SPECIFIED | 未公开。 |
| Channel deskew/cable-delay correction | PAPER_NOT_SPECIFIED | 未公开。 |
| Kelvin-source 测量/驱动参考 | PAPER_NOT_SPECIFIED | 未公开，不能作为论文事实。 |
| Connector/test point 类型 | PAPER_NOT_SPECIFIED | 未公开。 |
| PCB schematic/layout/层数/stackup/copper/return path | PAPER_NOT_SPECIFIED | 只有 testing board 照片。 |
| Gate/power-loop parasitic inductance/capacitance | PAPER_NOT_SPECIFIED | 未量化。 |
| Power sequencing、UVLO、interlock、fault response | PAPER_NOT_SPECIFIED | 未公开。 |
| Gate overvoltage、drain overcurrent、short-circuit 保护 | PAPER_NOT_SPECIFIED | 未公开。 |
| DC supply 动态阻抗、噪声、限流、remote sense | PAPER_NOT_SPECIFIED | 未公开。 |
| $R_L$ 与 supply 的物理位置/回路去耦 | PAPER_NOT_SPECIFIED | 未公开。 |
| Measurement uncertainty/error budget | PAPER_NOT_SPECIFIED | 未给完整不确定度传播。 |
| 后处理插值、数据格式、自动化与版本控制 | PAPER_NOT_SPECIFIED | 未公开。 |

## 11. Risks / Ambiguities

1. **$t_{dly}$ 可重复性风险：** 论文有系统级语义但无工程阈值定义；不同 edge crossing、filter 或 extremum 搜索窗可能得到不同“100 ns”。
2. **振铃/探头负载风险：** MP/MN 被定义为极值，任何 parasitic 或 probe-induced overshoot 都可能被误识别为物理 measurement point；P1 无排除规则。
3. **$V_{DS}$ 对齐风险：** “$V_{DS}\approx V_{DS-C}$”没有容差；即使 current 匹配，drain-bias mismatch 仍可能影响 curve mapping。
4. **Current matching 风险：** P1 报告 ±20% 内可接受，但未明确百分比计算式、是否对 P/N 使用相同容差、是否适用于不同 DUT。
5. **平行移位假设风险：** 点测方法依赖 sweep curve 近似平行移动；P1 在同型号器件、$I_{DS}\approx I_{th}$ 附近验证 1% 内，不保证本项目目标 DUT/温度/stress 条件相同。
6. **Precondition 不确定性：** “long-term”没有时间或状态完成判据，MI/$V_{th-IS}$ 可能随测试历史漂移。
7. **Self-heating 混杂风险：** Positive stress 时存在 $V_{DC}/R_L$ 电流，但 P1 不提供最大能量/温升；热引起的阈值变化可能与 hysteresis 混合。
8. **频率定义歧义：** P1 同时给出 $t_{str}=10\ \mu$s↔50 kHz、$t_{str}=2\ \mu$s↔500 kHz、0.2–200 $\mu$s↔5 MHz–5 kHz，未给 duty-cycle/period 的统一定义；不能由 SP1 自行修正。
9. **“constant rated $V_{DS}$”措辞歧义：** 论文随后对 1.2 kV DUT 使用 $V_{DS-C}=10$ V，因此此处不能解释为器件额定耐压；本报告只把它作为固定 calibration drain bias。
10. **负应力状态方程缺失：** Fig. 3(b3) 显示高 $V_{DS}$，但 P1 未像 positive stress 那样给出明确回路公式。
11. **调整迭代风险：** $V_{GM-P/N}$、$V_{DC}$、$R_L$ 的调节步长/收敛算法未给，可能导致不同操作者得到不同 operating point。
12. **测量链误差风险：** scope/probe bandwidth、channel skew、probe capacitance、cable delay 都会直接影响 $t_{dly}$ 和极值，但 P1 未公开。
13. **安全边界风险：** Fig. 3 是方法示意图，不含上电顺序、互锁、故障态和保护；不可直接据此进入硬件实现。

## 12. Items Requiring Master Decision

1. 冻结复现范围：只复现 Fig. 3 的 functional architecture，还是还要复现 Fig. 6/7 的 <100 ns 波形和 Fig. 10 的 delay/frequency sweep。
2. 冻结 $t_{dly}$ 工程定义：起点 crossing、终点 extremum 算法、search window、filter、deskew/de-embedding、<100 ns 或 ≤100 ns。
3. 为目标 DUT 选择 $V_{DS-C}$ 与 $I_{th}$；P1 的 10 V/10 mA 只能视为论文示例。
4. 冻结 $V_{DS}\approx V_{DS-C}$ 的误差带。
5. 冻结 $I_{DM-P/N}$ 相对 $I_{DM-I}$ 的偏差定义与 PASS；决定是否沿用 P1 的 ±20%实验标准或采用更严标准。
6. 冻结 $t_{pre}$ 的最低时长及“reset complete”重复性判据。
7. 冻结 $t_{mea}$、recovery observation window 与 MI/MP/MN 选择算法。
8. 澄清 $t_{str}$、正/负半周期、占空比与 switching frequency 的项目定义。
9. 冻结 self-heating 上限：允许 $I_{DS}$、pulse energy、结温/壳温变化或其他 proxy。
10. 冻结 SAFE_OFF、上电/掉电顺序、interlock 和 protection requirements。
11. 冻结系统接口：pulse source control/trigger、gate-level programming、scope probe/trigger、$V_{DC}$/$R_L$/DUT 连接。
12. 决定目标 DUT 是否先做平行曲线验证；若不满足，是否继续使用 P1 的单点映射方法。

## 13. Recommended Next Step

Master 先审查并冻结以下六个 SP1 gate：

1. 三条 sequence 与七个 state 的系统定义；
2. $t_{dly}$ 工程起止事件；
3. 目标 DUT 的 $V_{DS-C}$/$I_{th}$；
4. $V_{DS}$ alignment 与 $I_{DM}$ matching acceptance；
5. $t_{pre}$/$t_{mea}$ 与 extremum extraction；
6. SAFE_OFF/protection 的项目级最低需求。

冻结后，SP2 可在不选择具体器件的前提下建立系统 architecture/interface control document；SP3 再把已批准的电压、时间、负载、探测和安全需求转换为电路级约束。任何 Si8273 rail、$R_g$、电容、0 V clamp 或 layout 选择都应在该需求基线之后进行，且标为 PROJECT DESIGN CHOICE。

---

HANDOFF_PACKET

Subproject:
SP1 — 论文方法与系统需求

Version:
SP1-v0.1

Source:
Xu Li, Xiaochuan Deng, Jingyu Huang, Xuan Li, Wanjun Chen, Bo Zhang, “Accurate Evaluation of Threshold Voltage Hysteresis in SiC MOSFET Under Switching Stress,” IEEE Transactions on Power Electronics, vol. 39, no. 11, pp. 14118–14121, Nov. 2024, DOI 10.1109/TPEL.2024.3409570.

Completed:
- 完整阅读 P1 四页正文并核对 Fig. 2、Fig. 3、Fig. 4、Table I、式 (1)–(5)。
- 提取 calibration、positive stress、negative stress 的方法链。
- 建立变量定义表、七状态表和三条 ASCII timing diagram。
- 定义 $t_{pre}$、$t_{str}$、$t_{mea}$、$t_{dly}$，分离论文定义与工程 acceptance definition。
- 建立 B1505 curve→$V_{DS}$ point→$I_{DS}$→等效 gate voltage→raw shift→corrected $\Delta V_{th}$ 流程。
- 划分 PCB、pulse generator、DC supply、DUT/$R_L$、oscilloscope、B1505、software 的功能边界。
- 提出 36 条编号需求并建立对应 verification matrix。
- 建立 PAPER_NOT_SPECIFIED、风险和 Master 决策清单。

Confirmed paper facts:
- 方法使用电阻负载回路与 multistage adjustable gate driver，从 bipolar gate stress 快速切换到 $V_{th}$ measurement。
- B1505 在 fixed $V_{DS-C}$ 下取得 initial $I_{DS}$–$V_{GS}$ curve；论文 DUT 使用 $V_{DS-C}=10$ V、$I_{th}=10$ mA。
- Precondition 为 $V_{GS}=0$、$V_{DS}=V_{DC}$、$I_{DS}=0$，用于 reset interface state 和消除前次 hysteresis。
- Calibration 使用 $V_{GM-I}=\text{initial }V_{th}$，以 MI 得到 $V_{th-IS}$。
- Positive stress 时 DUT fully ON，$V_{DS}\approx0$、$I_{DS}\approx V_{DC}/R_L$，并应尽量减小电流避免 self-heating。
- Positive/negative stress 后分别从 $V_{DS}$ maximum MP 和 minimum MN 获取测量点。
- $V_{GM-P/N}$ 分别调节，使 $I_{DM-P/N}\approx I_{DM-I}$，并使 measured-point $V_{DS}\approx V_{DS-C}$。
- Corrected $\Delta V_{th}$ 由 $V_{th-PS/NS}$ 减去 $V_{th-IS}$。
- $t_{dly}$ 是 stress→measurement 后到 $V_{DS}$ measured extremum 的时间；P1 平台正文报告 <100 ns。
- 500 kHz stress 后，1 $\mu$s delay 相对 100 ns 使正/负 shift 分别低估 32%/22%。

Engineering interpretations:
- Negative stress 期间 $I_{DS}\approx0$ 是依据 Fig. 3(b3) 高 $V_{DS}$ 与串联回路作出的 ENGINEERING INFERENCE；P1 无对应方程。
- $V_{th-PS}=V_{GM-P}-V_{th-MP}$、$V_{th-NS}=V_{GM-N}-V_{th-MN}$ 是对“same method as (3)”的 ENGINEERING RESTATEMENT，不是论文另列公式。
- 为可验证硬件增加 SAFE_OFF 是 PROJECT REQUIREMENT，不是论文状态。
- PCB 的核心时间指标必须按 control/$V_{GS}$/$V_{DS}$ 的系统链验证，不能用单一 driver rise/fall time 替代。

Requirements proposed:
- REQ-FUNC-001…005
- REQ-VOLT-001…006
- REQ-TIME-001…006
- REQ-MEAS-001…010
- REQ-CTRL-001…003
- REQ-SAFE-001…002
- REQ-VERIFY-001…004

Interfaces proposed:
- Pulse/control interface：state command、timing、trigger；电气实现待定。
- Gate-target interface：0 V、$V_{GS-P}$、$V_{GS-N}$、$V_{GM-I/P/N}$；具体 rail/driver 待定。
- Drain-load interface：$V_{DC}$、$R_L$、DUT drain/source return；具体连接/额定待定。
- Measurement interface：同步 $V_{GS}$/$V_{DS}$ 探测与 scope trigger；probe/connector 待定。
- Calibration-data interface：B1505 fixed-$V_{DS-C}$ curve 和 $I_{th}$ metadata。
- Post-processing interface：raw waveform + $V_{DC}$/$R_L$ + calibration curve → traceable $\Delta V_{th}$。

Unknown / paper not specified:
- Multistage driver schematic、driver IC、output impedance、source/sink current、$R_g$、decoupling。
- Positive/negative/measurement rail 生成方法和 exact 0 V implementation/clamp。
- State-control circuit、logic levels、pulse-generator channels/jitter/trigger implementation。
- $V_{GM-I/P/N}$ 数值/范围/分辨率与调节算法。
- $V_{DC}$、$R_L$ 数值及 $R_L$ 技术/功率/寄生/物理位置。
- $t_{pre}$ 数值/reset 判据、$t_{mea}$ 长度/退出条件。
- $t_{dly}$ edge percentage、extremum filter/window、settling、deskew/de-embedding。
- $t_{str}$ 与 bipolar frequency/duty-cycle 的统一定义。
- DUT exact part number；B1505 sweep step/rate/range/hold/compliance；test temperature。
- $V_{DS}\approx V_{DS-C}$ tolerance；$I_{DM}$ matching 的通用 PASS；self-heating limit。
- Scope/probe model、bandwidth、sample rate、probe loading、cable delay、Kelvin reference。
- PCB schematic/layout/stackup/connector/test point/parasitics。
- Power sequencing、interlock、protection、fault state、SAFE_OFF target。
- Measurement uncertainty、extremum algorithm、interpolation/data format。

Risks:
- 100 ns 无统一工程事件定义，可能产生不可比结果。
- 振铃/探头负载可能伪造 MP/MN 极值。
- Curve mapping 依赖 $V_{DS}$ 和 $I_{DS}$ 对齐及平行移位假设。
- 未定义 precondition 和 thermal limit 可能使 history/temperature 与 hysteresis 混杂。
- P1 的 $t_{str}$–frequency 叙述存在歧义。
- 论文没有安全与电路实现信息，不能直接据 Fig. 3 下板。

Open questions:
- Master 是否要求 full paper reproduction，还是只做 Fig. 3 functional reproduction？
- $t_{dly}$ 起止事件和 <100 ns PASS 如何冻结？
- 目标 DUT 的 $V_{DS-C}$、$I_{th}$、stress level 和 operating temperature 是什么？
- $V_{DS}$ alignment、$I_{DM}$ matching、parallel-shift validation 采用什么 tolerance？
- $t_{pre}$、$t_{mea}$、extremum/recovery window 如何定义？
- SAFE_OFF、sequencing、interlock、protection 由哪个子项目冻结？

Items requiring master approval:
- State table 与 sequence baseline。
- $t_{dly}$ engineering acceptance definition。
- Target-DUT calibration profile：$V_{DS-C}$、$I_{th}$。
- $V_{DS}$/$I_{DM}$ alignment tolerance。
- Precondition/measurement timing 与 measurement-point algorithm。
- Full-reproduction scope、frequency definition、multiple-pulse requirement。
- Thermal limit、SAFE_OFF、power sequencing、protection baseline。
- 系统级 control/gate/drain/measurement/data interfaces。

Recommended next action:
Master 先对上述八类 approval item 作出冻结决定；随后交由 SP2 生成系统 architecture/interface control document，再由 SP3 把冻结后的需求转成电路级约束。不得在 $t_{dly}$、measurement-point、calibration profile 和安全基线未冻结前，把任何具体 Si8273 rail、$R_g$、电容、0 V clamp 或 layout 方案标为论文复现需求。

END_HANDOFF_PACKET
