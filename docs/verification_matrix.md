# 规范需求验证矩阵

- 文件状态：**ACTIVE CONTROLLED MATRIX — aligned with frozen G0 baseline**
- 需求基线状态：`FROZEN`
- 对齐基线：[requirements.md](requirements.md)
- 批准来源：[G0-CRB-v1.2](G0_closing_requirements_baseline_v1.2.md)
- 论文方法证据：[SP1-v0.2](SP1_paper_method_system_requirements_v0.2.md)
- 覆盖状态：65/65
- 未覆盖需求：0
- 无效需求引用：0
- G0阶段门状态：`PASS`
- 后续阶段：G1=`ACTIVE`；G3=`BLOCKED`

## 1. 使用规则

1. 每个`REQ-SYS-*`在本矩阵中恰好对应一条唯一验证行。
2. 需求基线冻结不表示所有验收值已经确定。OPEN依赖不为空时，先验证需求中的功能或原则，最终数值、算法或实现按对应`OPEN::OI-*`的批准结果判定。
3. 本矩阵不得用论文示例值替代项目验收值。
4. `REQ-SYS-METHOD-009`在Master通过`OPEN::OI-022`激活完整论文/Fig. 10范围前不执行。
5. 验证完成后应附上可审计证据；本文件的“需求已冻结”不等于该验证已经执行通过。

## 2. 验证矩阵

| Test ID | Requirement ID | 验证目标 | 验证方法 | 验收条件 | 验证阶段 | OPEN依赖 | 当前状态 |
|---|---|---|---|---|---|---|---|
| TEST-SYS-FUNC-001 | REQ-SYS-FUNC-001 | 证明：同一块已装配的基础PCB必须同时支持正BTI和负BTI。 | 审查设计；用同一块PCB分别执行正、负BTI测试。 | 需求陈述全部成立，并形成可审计证据。 | G1、G11、G12 | 无 | 需求已冻结，待相应阶段验证 |
| TEST-SYS-FUNC-002 | REQ-SYS-FUNC-002 | 证明：对同一个DUT和同一份已批准DUT配置档案，P/N模式切换只能改变外部`VDDA/GNDA`和控制波形；不得重新焊接或更换基础PCB元件、DUT转接板或`Rg`。只有更换DUT或更换已批准配置档案时，才可改变DUT专用配置。 | 核对同一DUT/profile切换前后的配置，确认只改变电源轨和控制波形。 | 需求中的功能或原则成立；涉及数值、算法或实现的最终判定按`OPEN::OI-015`、`OPEN::OI-016`、`OPEN::OI-017`批准结果执行，不得预填数值。 | G1、G11 | `OPEN::OI-015`、`OPEN::OI-016`、`OPEN::OI-017` | 需求已冻结，验收值或实现延期 |
| TEST-SYS-FUNC-003 | REQ-SYS-FUNC-003 | 证明：系统必须支持三条序列：校准=`PRECONDITION→MEASUREMENT_I`；正应力=`PRECONDITION→POSITIVE_STRESS→MEASUREMENT_P`；负应力=`PRECONDITION→NEGATIVE_STRESS→MEASUREMENT_N`。 | 同步记录三条状态波形，核对状态顺序。 | 需求陈述全部成立，并形成可审计证据。 | G11、G12 | 无 | 需求已冻结，待相应阶段验证 |
| TEST-SYS-FUNC-004 | REQ-SYS-FUNC-004 | 证明：系统必须支持低能量电阻负载回路：`VDC→RL→DUT Drain→DUT Power Source→return`。 | 检查连通性，并在低能量条件下验证回路与计算公式一致。 | 需求陈述全部成立，并形成可审计证据。 | G1、G10、G12 | 无 | 需求已冻结，待相应阶段验证 |
| TEST-SYS-FUNC-005 | REQ-SYS-FUNC-005 | 证明：在`MEASUREMENT_I/P/N`状态下，DUT必须处于不完全导通状态，并产生有限且可计算的`IDS`。 | 验证`0<VDS<VDC`且`IDS>0`；具体裕量在G12确定。 | 需求中的功能或原则成立；涉及数值、算法或实现的最终判定按`OPEN::OI-003`、`OPEN::OI-004`批准结果执行，不得预填数值。 | G11、G12 | `OPEN::OI-003`、`OPEN::OI-004` | 需求已冻结，验收值或实现延期 |
| TEST-SYS-FUNC-006 | REQ-SYS-FUNC-006 | 证明：系统必须获得可解释、可重复的MI、MP、MN，并保留正/负应力测量点之后的恢复波形。 | 重复采集波形，检查三个测量点及正/负应力后的恢复是否可识别、可重复。 | 需求中的功能或原则成立；涉及数值、算法或实现的最终判定按`OPEN::OI-007`、`OPEN::OI-008`、`OPEN::OI-009`批准结果执行，不得预填数值。 | G11、G12 | `OPEN::OI-007`、`OPEN::OI-008`、`OPEN::OI-009` | 需求已冻结，验收值或实现延期 |
| TEST-SYS-FUNC-007 | REQ-SYS-FUNC-007 | 证明：Si8273 channel A的`VOA`必须承担关键的应力→测量栅极电压快速转换。 | 核对原理图追溯关系，并测量`VIA/VOA/VGS`波形。 | 需求陈述全部成立，并形成可审计证据。 | G3、G10、G11 | 无 | 需求已冻结，待相应阶段验证 |
| TEST-SYS-FUNC-008 | REQ-SYS-FUNC-008 | 证明：正BTI模式必须实现`VDDA=VGS-P`、`GNDA=VGM-P`、`VIA HIGH→LOW`；负BTI模式必须实现`VDDA=VGM-N`、`GNDA=VGS-N`、`VIA LOW→HIGH`。 | 审查模式表，并在dummy load上验证`VGS`波形。 | 需求陈述全部成立，并形成可审计证据。 | G1、G10、G11 | 无 | 需求已冻结，待相应阶段验证 |
| TEST-SYS-METHOD-001 | REQ-SYS-METHOD-001 | 证明：每条测试序列都必须支持Gate-to-SREF的`VGS=0 V`预处理；G0不规定0 V实现拓扑。 | 相对`SREF`测量预处理阶段的`VGS`；容差和实现方式后定。 | 需求中的功能或原则成立；涉及数值、算法或实现的最终判定按`OPEN::OI-005`、`OPEN::OI-014`批准结果执行，不得预填数值。 | G10、G12 | `OPEN::OI-005`、`OPEN::OI-014` | 需求已冻结，验收值或实现延期 |
| TEST-SYS-METHOD-002 | REQ-SYS-METHOD-002 | 证明：系统必须支持`VGM-I`、`VGM-P`、`VGM-N`；`VGM-I=initial Vth`，`VGM-P/N`可分别调节，三者不要求相等。 | 分别设定三个测量电压并验证实际波形。 | 需求中的功能或原则成立；涉及数值、算法或实现的最终判定按`OPEN::OI-019`批准结果执行，不得预填数值。 | G2、G11、G12 | `OPEN::OI-019` | 需求已冻结，验收值或实现延期 |
| TEST-SYS-METHOD-003 | REQ-SYS-METHOD-003 | 证明：B1505必须在DUT专用的固定`VDS-C`下取得初始`IDS-VGS`曲线，并用DUT专用`Ith`交点定义初始`Vth`。 | 审查B1505测试记录，并独立重算`Ith`交点。 | 需求中的功能或原则成立；涉及数值、算法或实现的最终判定按`OPEN::OI-019`批准结果执行，不得预填数值。 | G2、G12 | `OPEN::OI-019` | 需求已冻结，验收值或实现延期 |
| TEST-SYS-METHOD-004 | REQ-SYS-METHOD-004 | 证明：MI、MP、MN处的`VDS`必须在已批准容差内与对应`VDS-C`对齐。 | 自动计算并报告各测量点与`VDS-C`的偏差。 | 需求中的功能或原则成立；涉及数值、算法或实现的最终判定按`OPEN::OI-003`批准结果执行，不得预填数值。 | G12 | `OPEN::OI-003` | 需求已冻结，验收值或实现延期 |
| TEST-SYS-METHOD-005 | REQ-SYS-METHOD-005 | 证明：每个测量工作点必须满足`VDS-C>VGS-Vth`；所需裕量由DUT配置档案规定。 | 根据记录量检查不等式并计算裕量。 | 需求中的功能或原则成立；涉及数值、算法或实现的最终判定按`OPEN::OI-019`批准结果执行，不得预填数值。 | G2、G12 | `OPEN::OI-019` | 需求已冻结，验收值或实现延期 |
| TEST-SYS-METHOD-006 | REQ-SYS-METHOD-006 | 证明：校准被接受后，正/负应力测试必须保持`VDC`和`RL`不变，只调节`VGM-P/N`完成工作点对齐。 | 核对三组测试的配置和元数据，确认`VDC/RL`不变。 | 需求陈述全部成立，并形成可审计证据。 | G12 | 无 | 需求已冻结，待相应阶段验证 |
| TEST-SYS-METHOD-007 | REQ-SYS-METHOD-007 | 证明：`IDM-P`和`IDM-N`必须在批准容差内与`IDM-I`匹配；P1的±20%只作为`PAPER PERFORMANCE REFERENCE`。 | 明确百分比公式，分别报告正、负应力的电流偏差。 | 需求中的功能或原则成立；涉及数值、算法或实现的最终判定按`OPEN::OI-004`批准结果执行，不得预填数值。 | G12 | `OPEN::OI-004` | 需求已冻结，验收值或实现延期 |
| TEST-SYS-METHOD-008 | REQ-SYS-METHOD-008 | 证明：正应力期间的`IDS`和能量必须受DUT专用上限约束，避免自热使`Vth`结果无法解释。 | G2计算电流和能量范围；G10/G11测量实际电流、能量及必要热代理。 | 需求中的功能或原则成立；涉及数值、算法或实现的最终判定按`OPEN::OI-011`批准结果执行，不得预填数值。 | G2、G10、G11 | `OPEN::OI-011` | 需求已冻结，验收值或实现延期 |
| TEST-SYS-METHOD-009 | REQ-SYS-METHOD-009 | 证明：只有Master激活完整论文/Fig. 10复现范围后，系统才需要满足批准的多脉冲应力流程。 | 仅在Master激活后记录脉冲列、总应力时间和测试结果。 | 当前不作功能通过判定；仅在Master激活完整论文/Fig. 10范围后，按批准流程验证。 | G12 | `OPEN::OI-022` | 条件未激活（`CONDITIONAL-INACTIVE`） |
| TEST-SYS-TIME-001 | REQ-SYS-TIME-001 | 证明：系统必须支持正/负应力状态快速、可重复地切换到对应测量状态。 | 在同一次事件中记录时序参考、`VGS`和`VDS`。 | 需求陈述全部成立，并形成可审计证据。 | G11 | 无 | 需求已冻结，待相应阶段验证 |
| TEST-SYS-TIME-002 | REQ-SYS-TIME-002 | 证明：项目必须以P1报告的约100 ns完整系统`tdly`作为设计和验证目标；该目标不是单独`VOA`边沿指标，也暂不等于明确的`<100 ns`或`≤100 ns`通过判据。 | 按G10/G11批准的事件定义提取完整系统`tdly`。 | 需求中的功能或原则成立；涉及数值、算法或实现的最终判定按`OPEN::OI-001`、`OPEN::OI-002`、`OPEN::OI-007`、`OPEN::OI-008`、`OPEN::OI-009`、`OPEN::OI-010`批准结果执行，不得预填数值。 | G11 | `OPEN::OI-001`、`OPEN::OI-002`、`OPEN::OI-007`、`OPEN::OI-008`、`OPEN::OI-009`、`OPEN::OI-010` | 需求已冻结，验收值或实现延期 |
| TEST-SYS-TIME-003 | REQ-SYS-TIME-003 | 证明：系统必须支持可配置`tpre`，并允许通过MI或`Vth-IS`稳定性建立预处理完成判据。 | 改变`tpre`并检查MI或`Vth-IS`的稳定性和重复性。 | 需求中的功能或原则成立；涉及数值、算法或实现的最终判定按`OPEN::OI-005`批准结果执行，不得预填数值。 | G12 | `OPEN::OI-005` | 需求已冻结，验收值或实现延期 |
| TEST-SYS-TIME-004 | REQ-SYS-TIME-004 | 证明：系统必须支持可配置`tstr`；P1给出的时间范围和示例只属于`PAPER EXAMPLE VALUE`。 | 比较设定值与示波器实测`tstr`。 | 需求中的功能或原则成立；涉及数值、算法或实现的最终判定按`OPEN::OI-019`、`OPEN::OI-022`批准结果执行，不得预填数值。 | G11、G12 | `OPEN::OI-019`、`OPEN::OI-022` | 需求已冻结，验收值或实现延期 |
| TEST-SYS-TIME-005 | REQ-SYS-TIME-005 | 证明：系统必须支持足以捕获选定测量点和所需恢复区间的`tmea`。 | 检查采集窗口是否完整覆盖选定测量点和恢复区间。 | 需求中的功能或原则成立；涉及数值、算法或实现的最终判定按`OPEN::OI-006`批准结果执行，不得预填数值。 | G10、G11、G12 | `OPEN::OI-006` | 需求已冻结，验收值或实现延期 |
| TEST-SYS-TIME-006 | REQ-SYS-TIME-006 | 证明：系统必须允许改变并记录实际`tdly`，以得到恢复随延迟变化的数据；范围和步进由批准的实验流程规定。 | 执行延迟扫描，核对实际`tdly`、重复性和元数据。 | 需求中的功能或原则成立；涉及数值、算法或实现的最终判定按`OPEN::OI-001`、`OPEN::OI-002`批准结果执行，不得预填数值。 | G11、G12 | `OPEN::OI-001`、`OPEN::OI-002` | 需求已冻结，验收值或实现延期 |
| TEST-SYS-MEAS-001 | REQ-SYS-MEAS-001 | 证明：每次转换必须记录同一事件的`VGS(t)`、`VDS(t)`和最终`tdly`定义所需的时序参考信号，并建立明确的共同时间关系。 | 核对通道、触发和时间对齐；deskew规则在G10/G11确定。 | 需求中的功能或原则成立；涉及数值、算法或实现的最终判定按`OPEN::OI-010`批准结果执行，不得预填数值。 | G10、G11 | `OPEN::OI-010` | 需求已冻结，验收值或实现延期 |
| TEST-SYS-MEAS-002 | REQ-SYS-MEAS-002 | 证明：`VGS`必须测为DUT Gate-to-Kelvin-Source/SREF，不得测成gate-to-earth。 | 采用差分方式测量，并审查实际接线。 | 需求陈述全部成立，并形成可审计证据。 | G1、G10、G11 | 无 | 需求已冻结，待相应阶段验证 |
| TEST-SYS-MEAS-003 | REQ-SYS-MEAS-003 | 证明：系统必须提供可安全探测的`VGS`、`VDS`和时序/触发观察点；具体探头和连接器由后续阶段决定。 | 审查接口和探头接入空间；G6/G7核对物理实现。 | 需求中的功能或原则成立；涉及数值、算法或实现的最终判定按`OPEN::OI-020`批准结果执行，不得预填数值。 | G1、G6/G7、G10 | `OPEN::OI-020` | 需求已冻结，验收值或实现延期 |
| TEST-SYS-MEAS-004 | REQ-SYS-MEAS-004 | 证明：后处理必须使用`IDS=(VDC-VDS)/RL`计算测量点电流，并保存所用`VDC/RL`元数据。 | 用已知输入做计算单元测试，并重算样例数据。 | 需求陈述全部成立，并形成可审计证据。 | G12 | 无 | 需求已冻结，待相应阶段验证 |
| TEST-SYS-MEAS-005 | REQ-SYS-MEAS-005 | 证明：后处理必须分别由MI、MP、MN得到`IDM-I`、`IDM-P`、`IDM-N`。 | 用带已知测量点的参考波形回放算法。 | 需求中的功能或原则成立；涉及数值、算法或实现的最终判定按`OPEN::OI-007`、`OPEN::OI-008`、`OPEN::OI-009`批准结果执行，不得预填数值。 | G10/G11、G12 | `OPEN::OI-007`、`OPEN::OI-008`、`OPEN::OI-009` | 需求已冻结，验收值或实现延期 |
| TEST-SYS-MEAS-006 | REQ-SYS-MEAS-006 | 证明：`IDM-I/P/N`必须映射到同一DUT、同一固定`VDS-C`的B1505曲线；插值方法必须一致且可审计。 | 对查表和插值算法做单元测试。 | 需求中的功能或原则成立；涉及数值、算法或实现的最终判定按`OPEN::OI-021`批准结果执行，不得预填数值。 | G12 | `OPEN::OI-021` | 需求已冻结，验收值或实现延期 |
| TEST-SYS-MEAS-007 | REQ-SYS-MEAS-007 | 证明：后处理必须按P1式(3)及相同方法得到`Vth-IS/PS/NS`，并按式(5)计算修正后的`ΔVth`。 | 用构造数据做公式单元测试，并独立重算结果。 | 需求陈述全部成立，并形成可审计证据。 | G12 | 无 | 需求已冻结，待相应阶段验证 |
| TEST-SYS-MEAS-008 | REQ-SYS-MEAS-008 | 证明：采用单点/平行位移映射前，必须对每个目标DUT和测试条件验证`IDS≈Ith`附近曲线是否适用；P1的1%只作为`PAPER PERFORMANCE REFERENCE`。 | 比较应力前后曲线，检查`IDS≈Ith`附近的位移一致性。 | 需求中的功能或原则成立；涉及数值、算法或实现的最终判定按`OPEN::OI-021`批准结果执行，不得预填数值。 | G12 | `OPEN::OI-021` | 需求已冻结，验收值或实现延期 |
| TEST-SYS-MEAS-009 | REQ-SYS-MEAS-009 | 证明：原始波形、仪器与配置元数据、DUT配置档案、B1505曲线、算法版本和最终结果必须足以独立重算MI/MP/MN、`tdly`和`ΔVth`，并报告重复性。 | 审查完整数据包，并用独立软件回放。 | 需求陈述全部成立，并形成可审计证据。 | G11、G12 | 无 | 需求已冻结，待相应阶段验证 |
| TEST-SYS-INTERFACE-001 | REQ-SYS-INTERFACE-001 | 证明：`SREF`必须定义为DUT Kelvin Source参考点。 | 审查net和接口，并做连通性测试。 | 需求陈述全部成立，并形成可审计证据。 | G1、G3、G10 | 无 | 需求已冻结，待相应阶段验证 |
| TEST-SYS-INTERFACE-002 | REQ-SYS-INTERFACE-002 | 证明：`SREF`不得自动等于实验室earth或chassis。 | 做绝缘与连通性测试。 | 需求陈述全部成立，并形成可审计证据。 | G1、G3、G10 | 无 | 需求已冻结，待相应阶段验证 |
| TEST-SYS-INTERFACE-003 | REQ-SYS-INTERFACE-003 | 证明：`GNDI`、`GNDA`、`SREF`、earth/chassis必须保持显式区分；任何连接都必须经过Master批准并可追溯。 | 审查系统架构、net关系和任何批准的跨域连接。 | 需求陈述全部成立，并形成可审计证据。 | G1、G3、G8、G10 | 无 | 需求已冻结，待相应阶段验证 |
| TEST-SYS-INTERFACE-004 | REQ-SYS-INTERFACE-004 | 证明：DUT封装支持时，Power Source与Kelvin Source路径必须分开；不支持时必须在DUT配置档案中记录限制。 | 审查连接器、net和layout，并进行动态波形验证。 | 需求陈述全部成立，并形成可审计证据。 | G1、G6/G7、G11 | 无 | 需求已冻结，待相应阶段验证 |
| TEST-SYS-INTERFACE-005 | REQ-SYS-INTERFACE-005 | 证明：外部脉冲/控制接口必须支持可重复的状态命令、触发参考和`tpre/tstr/tmea/tdly`配置；电平、通道和连接器由G1定义。 | 审查接口控制文件，并重复采集触发波形。 | 需求中的功能或原则成立；涉及数值、算法或实现的最终判定按`OPEN::OI-012`、`OPEN::OI-013`、`OPEN::OI-014`批准结果执行，不得预填数值。 | G1、G11 | `OPEN::OI-012`、`OPEN::OI-013`、`OPEN::OI-014` | 需求已冻结，验收值或实现延期 |
| TEST-SYS-INTERFACE-006 | REQ-SYS-INTERFACE-006 | 证明：栅极目标接口必须允许外部设定或提供`VGS-P/N`、`VGM-I/P/N`及已批准模式真值表所需的电源轨；G0不固定数值。 | 审查接口范围，并使用批准的DUT配置档案验证。 | 需求中的功能或原则成立；涉及数值、算法或实现的最终判定按`OPEN::OI-019`批准结果执行，不得预填数值。 | G1、G2、G11 | `OPEN::OI-019` | 需求已冻结，验收值或实现延期 |
| TEST-SYS-INTERFACE-007 | REQ-SYS-INTERFACE-007 | 证明：外部漏极负载接口必须接收DUT专用`VDC/RL`，并明确施加、返回和电流路径；基础PCB不因DUT额定阻断电压而自动承担650 V或3.3 kV。 | 审查架构和额定值，并在低能量条件下测试漏极回路。 | 需求中的功能或原则成立；涉及数值、算法或实现的最终判定按`OPEN::OI-015`、`OPEN::OI-019`批准结果执行，不得预填数值。 | G1、G2、G10 | `OPEN::OI-015`、`OPEN::OI-019` | 需求已冻结，验收值或实现延期 |
| TEST-SYS-INTERFACE-008 | REQ-SYS-INTERFACE-008 | 证明：校准数据接口必须向后处理传递B1505固定`VDS-C`曲线、`Ith`以及DUT、温度和扫描元数据；高速PCB不负责生成该曲线。 | 审查数据格式，并从B1505数据到最终结果做端到端回放。 | 需求中的功能或原则成立；涉及数值、算法或实现的最终判定按`OPEN::OI-021`批准结果执行，不得预填数值。 | G1、G12 | `OPEN::OI-021` | 需求已冻结，验收值或实现延期 |
| TEST-SYS-INTERFACE-009 | REQ-SYS-INTERFACE-009 | 证明：示波器与探头接口必须允许在同一次事件中测量`VGS`、`VDS`和时序参考，并管理共模、探头负载和时序误差；具体仪器规格后定。 | 制定仪器资格确认计划并用实测波形验证。 | 需求中的功能或原则成立；涉及数值、算法或实现的最终判定按`OPEN::OI-018`批准结果执行，不得预填数值。 | G1、G2、G10/G11 | `OPEN::OI-018` | 需求已冻结，验收值或实现延期 |
| TEST-SYS-INTERFACE-010 | REQ-SYS-INTERFACE-010 | 证明：0 V预处理路径与Si8273输出必须互斥，不得同时低阻驱动；是否采用独立clamp/switch属于尚未冻结的`PROJECT DESIGN CHOICE`。 | 审查状态转换和FMEA，并在G10做故障测试。 | 需求中的功能或原则成立；涉及数值、算法或实现的最终判定按`OPEN::OI-014`批准结果执行，不得预填数值。 | G1、G2、G10 | `OPEN::OI-014` | 需求已冻结，验收值或实现延期 |
| TEST-SYS-DUT-001 | REQ-SYS-DUT-001 | 证明：平台目标必须覆盖650 V-class和3.3 kV-class SiC MOSFET的低`VDS` BTI/`Vth`迟滞测试。 | 分别审查两类DUT配置档案并完成实验资格验证。 | 需求陈述全部成立，并形成可审计证据。 | G1、G2、G12 | 无 | 需求已冻结，待相应阶段验证 |
| TEST-SYS-DUT-002 | REQ-SYS-DUT-002 | 证明：DUT额定阻断电压不得被解释为PCB必须施加650 V或3.3 kV；实际`VDC/VDS-C`由BTI测量条件决定，本项目不是breakdown test。 | 审查需求、额定值和实际测试配置。 | 需求陈述全部成立，并形成可审计证据。 | G1、G2、G12 | 无 | 需求已冻结，待相应阶段验证 |
| TEST-SYS-DUT-003 | REQ-SYS-DUT-003 | 证明：栅极驱动架构、`SREF`、正/负BTI序列、测量原理和`VDS→IDS→Vth`链应与DUT额定阻断电压等级解耦。 | 审查系统架构，并比较两类DUT的配置差异。 | 需求中的功能或原则成立；涉及数值、算法或实现的最终判定按`OPEN::OI-015`批准结果执行，不得预填数值。 | G1、G2 | `OPEN::OI-015` | 需求已冻结，验收值或实现延期 |
| TEST-SYS-DUT-004 | REQ-SYS-DUT-004 | 证明：每个目标DUT必须建立受控配置档案，至少记录准确料号/封装、`Qg`、`Ciss/Crss`、推荐值和绝对最大`VGS`、`Vth`、`VGM`、`Ith`、`VDS-C`、Kelvin Source、`Rg`、`VDC/RL`、温度和相关时序检查。 | 核对datasheet、计算依据和配置档案完整性。 | 需求中的功能或原则成立；涉及数值、算法或实现的最终判定按`OPEN::OI-019`批准结果执行，不得预填数值。 | G2 | `OPEN::OI-019` | 需求已冻结，验收值或实现延期 |
| TEST-SYS-DUT-005 | REQ-SYS-DUT-005 | 证明：DUT连接器/转接板和`Rg`配置必须适应封装、Kelvin Source和`Qg`差异，同时不得破坏`REQ-SYS-FUNC-001`或`REQ-SYS-FUNC-002`；具体转接方案和`Rg`策略由G1/G2决定。 | G1审查转接和`Rg`策略；G2计算驱动要求；G6/G7审查物理实现。 | 需求中的功能或原则成立；涉及数值、算法或实现的最终判定按`OPEN::OI-016`、`OPEN::OI-017`、`OPEN::OI-019`、`OPEN::OI-020`批准结果执行，不得预填数值。 | G1、G2、G6/G7 | `OPEN::OI-016`、`OPEN::OI-017`、`OPEN::OI-019`、`OPEN::OI-020` | 需求已冻结，验收值或实现延期 |
| TEST-SYS-SAFE-001 | REQ-SYS-SAFE-001 | 证明：系统必须定义独立于预处理的`SAFE_OFF`逻辑状态、进入/退出条件以及栅极/漏极目标；具体电路后定。 | G1审查状态表和FMEA；G10执行故障测试。 | 需求中的功能或原则成立；涉及数值、算法或实现的最终判定按`OPEN::OI-012`批准结果执行，不得预填数值。 | G1、G10 | `OPEN::OI-012` | 需求已冻结，验收值或实现延期 |
| TEST-SYS-SAFE-002 | REQ-SYS-SAFE-002 | 证明：系统必须定义上电、掉电、控制丢失、UVLO和默认状态流程，并防止意外长时间应力。 | 审查时序，并在G10进行受控故障注入。 | 需求中的功能或原则成立；涉及数值、算法或实现的最终判定按`OPEN::OI-013`、`OPEN::OI-019`批准结果执行，不得预填数值。 | G1、G2、G10 | `OPEN::OI-013`、`OPEN::OI-019` | 需求已冻结，验收值或实现延期 |
| TEST-SYS-SAFE-003 | REQ-SYS-SAFE-003 | 证明：系统必须定义栅极过压、漏极过流、误触发、驱动争用以及能量/自热保护；动作阈值和拓扑由G2决定。 | 完成危险分析、计算和故障测试。 | 需求中的功能或原则成立；涉及数值、算法或实现的最终判定按`OPEN::OI-011`、`OPEN::OI-014`、`OPEN::OI-019`批准结果执行，不得预填数值。 | G1、G2、G10 | `OPEN::OI-011`、`OPEN::OI-014`、`OPEN::OI-019` | 需求已冻结，验收值或实现延期 |
| TEST-SYS-SAFE-004 | REQ-SYS-SAFE-004 | 证明：所有DUT栅极和漏极条件必须处于该DUT配置档案批准的额定值、能量和温度范围内。 | 核对datasheet和计算，并审查实测波形。 | 需求中的功能或原则成立；涉及数值、算法或实现的最终判定按`OPEN::OI-011`、`OPEN::OI-019`批准结果执行，不得预填数值。 | G2、G10、G11 | `OPEN::OI-011`、`OPEN::OI-019` | 需求已冻结，验收值或实现延期 |
| TEST-SYS-PROCESS-001 | REQ-SYS-PROCESS-001 | 证明：所有器件pin、封装、额定值和关键参数必须在原理图冻结前由官方datasheet核对。 | 完成datasheet核对表。 | 需求陈述全部成立，并形成可审计证据。 | G2/G3 | 无 | 需求已冻结，待相应阶段验证 |
| TEST-SYS-PROCESS-002 | REQ-SYS-PROCESS-002 | 证明：关键结论必须标明`PAPER FACT`、`PAPER EXAMPLE VALUE`、`PAPER PERFORMANCE REFERENCE`、`ENGINEERING INFERENCE`、`PROJECT REQUIREMENT`、`PROJECT DESIGN CHOICE`或`OPEN ITEM`，并保留来源。 | 在每个阶段审查需求来源和分类。 | 需求陈述全部成立，并形成可审计证据。 | 各阶段 | 无 | 需求已冻结，待相应阶段验证 |
| TEST-SYS-PROCESS-003 | REQ-SYS-PROCESS-003 | 证明：未批准的`OPEN ITEM`不得被默认成数值或实现；SP2/SP3只能在相应阶段或决定批准后展开设计。 | 使用阶段检查表审查。 | 需求陈述全部成立，并形成可审计证据。 | G1至G3 | 无 | 需求已冻结，待相应阶段验证 |
| TEST-SYS-PROCESS-004 | REQ-SYS-PROCESS-004 | 证明：ERC必须通过；如有残余warning，必须在布局冻结前逐项记录并批准。 | 审查ERC报告和每一条残余warning。 | 需求陈述全部成立，并形成可审计证据。 | G3/G8 | 无 | 需求已冻结，待相应阶段验证 |
| TEST-SYS-PROCESS-005 | REQ-SYS-PROCESS-005 | 证明：DRC必须通过；如有残余warning，必须在制造发布前逐项记录并批准。 | 审查DRC报告和每一条残余warning。 | 需求陈述全部成立，并形成可审计证据。 | G8 | 无 | 需求已冻结，待相应阶段验证 |
| TEST-SYS-PROCESS-006 | REQ-SYS-PROCESS-006 | 证明：未完成ERC、DRC、人工审查、验证矩阵批准和用户最终批准，不得生成或发布生产Gerber。 | 执行制造暂停检查表。 | 需求陈述全部成立，并形成可审计证据。 | G9 | 无 | 需求已冻结，待相应阶段验证 |
| TEST-SYS-PROCESS-007 | REQ-SYS-PROCESS-007 | 证明：每个面向用户的项目交付文件都必须同步到GitHub正式路径，随后才能报告完成。 | 完成GitHub远端文件回读。 | 需求陈述全部成立，并形成可审计证据。 | 每次交付 | 无 | 需求已冻结，待相应阶段验证 |
| TEST-SYS-PROCESS-008 | REQ-SYS-PROCESS-008 | 证明：每个已同步输出都必须登记到`docs/chat_output_index.md`，无需额外复制归档。 | 核对索引记录与实际文件路径。 | 需求陈述全部成立，并形成可审计证据。 | 每次交付 | 无 | 需求已冻结，待相应阶段验证 |
| TEST-SYS-PROCESS-009 | REQ-SYS-PROCESS-009 | 证明：不得直接提交受限版权材料、credentials、敏感数据或未批准的大文件；同步失败时必须报告`OUTPUT_SYNC_BLOCKED`及未同步文件。 | 审查仓库内容和任何`OUTPUT_SYNC_BLOCKED`记录。 | 需求陈述全部成立，并形成可审计证据。 | 每次交付 | 无 | 需求已冻结，待相应阶段验证 |
| TEST-SYS-VERIFY-001 | REQ-SYS-VERIFY-001 | 证明：原型必须按批准的事件定义同时记录时序参考、`VGS`和`VDS`，并提取完整系统`tdly`；不得用单独`VOA`边沿代替。 | 用示波器同步采集时序参考、`VGS`和`VDS`。 | 需求中的功能或原则成立；涉及数值、算法或实现的最终判定按`OPEN::OI-001`、`OPEN::OI-002`、`OPEN::OI-007`、`OPEN::OI-008`、`OPEN::OI-009`、`OPEN::OI-010`批准结果执行，不得预填数值。 | G11 | `OPEN::OI-001`、`OPEN::OI-002`、`OPEN::OI-007`、`OPEN::OI-008`、`OPEN::OI-009`、`OPEN::OI-010` | 需求已冻结，验收值或实现延期 |
| TEST-SYS-VERIFY-002 | REQ-SYS-VERIFY-002 | 证明：原型和方法验证必须报告MI/MP/MN相对`VDS-C`的偏差及通过判定。 | 自动比较MI、MP、MN与`VDS-C`。 | 需求中的功能或原则成立；涉及数值、算法或实现的最终判定按`OPEN::OI-003`批准结果执行，不得预填数值。 | G12 | `OPEN::OI-003` | 需求已冻结，验收值或实现延期 |
| TEST-SYS-VERIFY-003 | REQ-SYS-VERIFY-003 | 证明：原型和方法验证必须报告`IDM-P/N`相对`IDM-I`的偏差公式、结果、调节后的`VGM-P/N`及通过判定。 | 生成电流一致性报告。 | 需求中的功能或原则成立；涉及数值、算法或实现的最终判定按`OPEN::OI-004`批准结果执行，不得预填数值。 | G12 | `OPEN::OI-004` | 需求已冻结，验收值或实现延期 |
| TEST-SYS-VERIFY-004 | REQ-SYS-VERIFY-004 | 证明：发布的数据集必须能够独立重算原始波形→`IDS`→B1505映射→原始位移→修正后`ΔVth`的完整链。 | 用独立软件回放完整数据链。 | 需求中的功能或原则成立；涉及数值、算法或实现的最终判定按`OPEN::OI-021`批准结果执行，不得预填数值。 | G12 | `OPEN::OI-021` | 需求已冻结，验收值或实现延期 |
| TEST-SYS-VERIFY-005 | REQ-SYS-VERIFY-005 | 证明：平台通用性声明必须分别用至少一个已批准650 V-class配置档案和一个3.3 kV-class配置档案完成资格验证；不要求施加额定阻断电压。 | 分别审查两类配置档案，并完成低`VDS`功能和方法验证。 | 需求中的功能或原则成立；涉及数值、算法或实现的最终判定按`OPEN::OI-015`、`OPEN::OI-019`批准结果执行，不得预填数值。 | G2、G11、G12 | `OPEN::OI-015`、`OPEN::OI-019` | 需求已冻结，验收值或实现延期 |

## 3. 覆盖与控制结果

- 规范需求：65
- 验证行：65
- requirement coverage：65/65
- uncovered requirement：0
- orphan test：0
- duplicate Test ID：0
- missing verification method/stage/acceptance：0
- conditional requirement：1，`REQ-SYS-METHOD-009`保持未激活
- 未批准数值写入：0

过程类需求的ERC、DRC、制造暂停、GitHub同步、输出索引及禁止内容检查均保留在`REQ-SYS-PROCESS-001...009`对应验证行中。
