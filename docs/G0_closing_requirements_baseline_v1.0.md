# SiC MOSFET BTI Fast Gate Driver PCB / Fig. 3 Reproduction

## G0 Closing — Canonical Requirement Baseline Proposal

- 版本：G0-CRB-v1.0
- 日期：2026-08-24
- 状态：**PROPOSED — READY FOR MASTER REVIEW；未标记 FROZEN，未宣告 G0 PASS**
- 目的：将 Master 已批准的 `SP1-v0.2 + SP1-FGR-v1.0` 与现有项目级 requirements、decisions、interfaces、verification、risk 和 Stage-Gate 合并为单一、无编号冲突、可追溯的候选需求基线。
- 边界：本文件不重新审核 P1，不修改 SP1 结论，不选择具体器件数值、`Rg`、0 V clamp/switch、connector pinout、保护拓扑、原理图或 PCB layout。

## 1. Inputs reviewed

以下输入均已从 GitHub `kisssssky/gate_driver_pcb_design` 默认分支读取，无 `MISSING_INPUT`：

1. `docs/SP1_paper_method_system_requirements_v0.2.md`
2. `docs/SP1_final_gate_review_v1.0.md`
3. `docs/SP1_master_review_v1.0.md`
4. `docs/requirements.md`
5. `docs/decisions.md`
6. `docs/interfaces.md`
7. `docs/verification_matrix.md`
8. `docs/risk_register.md`
9. `docs/project_status.md`
10. `docs/stage_gate.md`

治理约束同时核对了 `AGENTS.md`、`docs/output_sync_policy.md` 和 `docs/chat_output_index.md`。

### 1.1 Evidence precedence

本文件严格使用以下证据分类：

- **PAPER FACT**：只来自 Master 已批准 SP1 baseline 中的论文事实。
- **PAPER EXAMPLE VALUE**：P1 的 1.2 kV DUT/实验示例数值，不自动成为本项目数值。
- **PAPER PERFORMANCE REFERENCE**：P1 报告的约 100 ns、±20%、1% 等性能或实验结果；不自动成为本项目 PASS。
- **ENGINEERING INFERENCE**：由方法链为可实现/可测量而推导，论文没有直接规定。
- **PROJECT REQUIREMENT**：本项目的规范性要求；只有这一层可以约束项目实现。
- **PROJECT DESIGN CHOICE**：实现某条 requirement 的具体方案，不伪装为论文要求。
- **OPEN ITEM**：仍需在指定 Gate 决定的数值、算法、接口或实现。

本文件的 canonical `REQ-*` 均处于 **PROJECT REQUIREMENT** 层。其 `Source` 列再独立标明所依据的 PAPER FACT、PAPER PERFORMANCE REFERENCE、ENGINEERING INFERENCE 或 Master decision，避免把事实、参考性能与规范混为一层。

## 2. Requirement reconciliation summary

### 2.1 Numbering strategy

- SP1 的 36 个旧 ID 是已批准证据基线的一部分，保留在 SP1 文件中，不改写、不回收。
- 现有 `REQ-001...016`、`REQ-100...108` 作为 legacy project IDs 保留追溯意义，但不继续作为 canonical 编号。
- 本提案采用语义前缀：`REQ-FUNC`、`REQ-METHOD`、`REQ-TIME`、`REQ-MEAS`、`REQ-INTERFACE`、`REQ-DUT`、`REQ-SAFE`、`REQ-PROCESS`、`REQ-VERIFY`。
- canonical ID 只在本层唯一；旧 ID 通过 crosswalk 映射，不再产生 `REQ-010` 与 `REQ-TIME-002` 这类层级歧义。

### 2.2 Duplicates, conflicts, and obsolete wording resolved

| Issue | Finding | Canonical disposition |
|---|---|---|
| 旧 `REQ-008/009` 与 SP1 `REQ-FUNC-002/004` | 三序列、0 V precondition、MI/MP/MN 被重复描述 | 合并为 `REQ-FUNC-003`、`REQ-METHOD-001`、`REQ-FUNC-006`，保留全部来源。 |
| 旧 `REQ-010` 与 SP1 `REQ-TIME-002`、`REQ-VERIFY-001` | 都指向约 100 ns，但一个像目标、一个明确为 reported performance reference | 合并为 `REQ-TIME-002` 与 `REQ-VERIFY-001`：现在冻结其**系统级目标性质**，精确 PASS 算法延期。 |
| 旧 `REQ-012` 与 SP1 `REQ-FUNC-001` | 都要求 Fig. 3 电阻负载链 | 合并为 `REQ-FUNC-004`。 |
| 旧 `REQ-014` 与 SP1 `REQ-MEAS-001` | 都要求 `VGS/VDS` 可测；旧条目还含 trigger | 分为 `REQ-MEAS-001/003` 与 `REQ-INTERFACE-005/009`，避免把测量内容和接口实现混写。 |
| 旧 `REQ-005/006/007` | Si8273 VOA 及 rail/truth-table 是 Master 批准的实现选择，不是 P1 requirement | 保留为 `REQ-FUNC-007/008`，统一标为 PROJECT REQUIREMENT，来源为 `DEC-005...007`。 |
| `interfaces.md` precondition wording | 写成“A separate mechanism shall…”，但独立 clamp/switch 仅是 `PROP-001` | canonical 只要求 Gate-to-SREF 0 V、互斥/无争用；“独立 clamp/switch”仍为 PROJECT DESIGN CHOICE，未冻结。 |
| SP1 `REQ-CTRL-003` | multiple-pulse/Fig. 10 是 optional scope，不是最小 Fig. 3 baseline | 映射为 `REQ-METHOD-009`，状态 `CONDITIONAL-INACTIVE`；只有 Master 激活后才约束项目。 |
| `verification_matrix.md` | 仍指向 superseded SP1-v0.1，且未覆盖 SP1-v0.2 的 36-ID 集 | 标为需要在 Master 批准本提案后重建；本文件先给每条 canonical REQ verification concept/stage。 |
| 论文示例值 | `10 V`、`10 mA`、`+20/-5 V`、`0.2–200 µs`、`±20%` 可能被误当通用值 | 只保留为 PAPER EXAMPLE VALUE / PAPER PERFORMANCE REFERENCE；不写入通用数值 PASS。 |
| 650 V / 3.3 kV | blocking rating 容易被错误转换成 PCB drain-voltage requirement | `REQ-DUT-001/002` 明确限定为 low-`VDS` BTI；实际 `VDC/VDS-C` 由 DUT profile 决定。 |

### 2.3 Legacy crosswalk

| Legacy source ID(s) | Canonical ID(s) |
|---|---|
| SP1 `REQ-FUNC-001...005` | `REQ-FUNC-004`、`REQ-FUNC-003`、`REQ-FUNC-005`、`REQ-FUNC-006`、`REQ-METHOD-006` |
| SP1 `REQ-VOLT-001...006` | `REQ-METHOD-001...005`、`REQ-METHOD-002` |
| SP1 `REQ-TIME-001...006` | `REQ-TIME-001...006` |
| SP1 `REQ-MEAS-001...010` | `REQ-MEAS-001`、`REQ-MEAS-004...008`、`REQ-METHOD-003/007/008` |
| SP1 `REQ-CTRL-001...003` | `REQ-FUNC-003`、`REQ-INTERFACE-005`、`REQ-METHOD-006/009` |
| SP1 `REQ-SAFE-001...002` | `REQ-SAFE-001...003` |
| SP1 `REQ-VERIFY-001...004` | `REQ-VERIFY-001...004` |
| Project `REQ-001...016` | `REQ-FUNC-001/002/003/004/007/008`、`REQ-TIME-002`、`REQ-MEAS-002/003`、`REQ-INTERFACE-001...004/009`、`REQ-DUT-001...005` |
| Project `REQ-100...104` | `REQ-PROCESS-001...006` |
| Project `REQ-105...108` | `REQ-PROCESS-007...009` |
| `OPEN-REQ-001...008` | `OI-019`、`OI-018/019`、`OI-003/004/019`、`OI-012`、`OI-018`、`OI-015...017`、`OI-001/007...010`、`OI-000` |

## 3. Canonical requirement hierarchy proposed

状态含义：`CONFIRMED` 表示其内容已有 Master decision 或已批准 SP1 方法依据；`PROPOSED` 表示新形成的项目级规范化措辞仍需 Master 批准；`ACCEPTANCE DEFERRED` 表示功能要求已确认，但数值/算法按 Section 5 延期；`CONDITIONAL-INACTIVE` 表示当前不进入最小 Fig. 3 scope。任何状态都不等于 `FROZEN`。

### 3.1 Functional requirements

| ID | Requirement statement | Category | Source classification | Source | Reason | Verification concept | Verification stage | Status |
|---|---|---|---|---|---|---|---|---|
| REQ-FUNC-001 | 同一块已装配的 base PCB 必须支持 positive BTI 与 negative BTI。 | Functional | PROJECT REQUIREMENT | `DEC-001`; legacy `REQ-001` | 避免为极性建立两套板级平台。 | 设计审查；同一板执行 P/N 模式测试。 | G1, G11, G12 | CONFIRMED |
| REQ-FUNC-002 | P/N 模式切换不得要求重新焊接或更换 base-PCB 元件；只允许改变外部 `VDDA/GNDA`、控制波形及批准的 DUT-specific configuration。 | Functional | PROJECT REQUIREMENT | `DEC-002`; legacy `REQ-002` | 冻结极性切换边界，同时为 DUT adapter/profile 留接口。 | 配置审计；模式切换前后比较 PCB assembly。 | G1, G11 | CONFIRMED；“DUT-specific configuration”边界见 OI-015...017 |
| REQ-FUNC-003 | 系统必须支持三条完整序列：Calibration=`PRECONDITION→MEASUREMENT_I`；Positive=`PRECONDITION→POSITIVE_STRESS→MEASUREMENT_P`；Negative=`PRECONDITION→NEGATIVE_STRESS→MEASUREMENT_N`。 | Functional | PROJECT REQUIREMENT | Approved SP1 `REQ-FUNC-002`（PAPER FACT）；`DEC-008` | 这是 MI/MP/MN 提取的完整方法链。 | 同步捕获三条状态波形并核对顺序。 | G11, G12 | CONFIRMED |
| REQ-FUNC-004 | 系统必须支持 `VDC→RL→DUT Drain→DUT Power Source→return` 的低能量串联电阻负载测量回路。 | Functional | PROJECT REQUIREMENT | Approved SP1 `REQ-FUNC-001`（PAPER FACT）；legacy `REQ-012` | 允许由 `VDS` 间接计算 `IDS`。 | 连通性、低能量功能测试与公式一致性。 | G1, G10, G12 | CONFIRMED |
| REQ-FUNC-005 | `MEASUREMENT_I/P/N` 必须使 DUT 处于不完全导通、产生有限且可计算的 `IDS`，不能仅为关断状态。 | Functional | PROJECT REQUIREMENT | Approved SP1 `REQ-FUNC-003`（PAPER FACT） | MI/MP/MN 必须能映射到 calibration curve。 | 证明 `0<VDS<VDC`、`IDS>0`；margin 后定。 | G11, G12 | CONFIRMED；ACCEPTANCE DEFERRED G12 |
| REQ-FUNC-006 | 系统必须捕获可解释、可重复的 MI、MP、MN；P/N measurement 还必须保留 measured point 后的 recovery 波形。 | Functional | PROJECT REQUIREMENT | Approved SP1 `REQ-FUNC-004`（PAPER FACT）；`DEC-009` | Recovery 会造成快速 `Vth` shift 被低估。 | 多次波形捕获、点识别与重复性报告。 | G11, G12 | CONFIRMED；算法 ACCEPTANCE DEFERRED G10/G11 |
| REQ-FUNC-007 | Si8273 channel A / `VOA` 必须承担关键 stress→measurement gate-voltage 快速转换。 | Functional | PROJECT REQUIREMENT | `DEC-005`; legacy `REQ-005`（PROJECT DESIGN CHOICE 已由 Master 批准） | 保持既定平台实现边界。 | 原理图追溯 + `VIA/VOA/VGS` 波形。 | G3, G10, G11 | CONFIRMED |
| REQ-FUNC-008 | Positive 模式必须实现 `VDDA=VGS-P`、`GNDA=VGM-P`、`VIA HIGH→LOW`；Negative 模式必须实现 `VDDA=VGM-N`、`GNDA=VGS-N`、`VIA LOW→HIGH`。 | Functional | PROJECT REQUIREMENT | `DEC-006/007`; legacy `REQ-006/007`（PROJECT DESIGN CHOICE 已由 Master 批准） | 形成已批准的两级快速切换 truth table。 | 模式表审查 + dummy-load `VGS` 波形。 | G1, G10, G11 | CONFIRMED |

### 3.2 Method requirements

| ID | Requirement statement | Category | Source classification | Source | Reason | Verification concept | Verification stage | Status |
|---|---|---|---|---|---|---|---|---|
| REQ-METHOD-001 | 每条序列必须支持 Gate-to-SREF `VGS=0 V` 的 PRECONDITION；具体 0 V 拓扑不在 G0 指定。 | Method | PROJECT REQUIREMENT | Approved SP1 `REQ-VOLT-001`（PAPER FACT）；`DEC-008` | 重置前次 hysteresis；避免把实现方案误写成方法。 | 相对 SREF 测量 precondition `VGS`；容差后定。 | G10, G12 | CONFIRMED；tolerance/topology DEFERRED |
| REQ-METHOD-002 | 系统必须支持 `VGM-I`、`VGM-P`、`VGM-N`；`VGM-I=initial Vth`，`VGM-P/N` 必须可分别调节，三者不要求相等。 | Method | PROJECT REQUIREMENT | Approved SP1 `REQ-VOLT-003`（PAPER FACT） | 补偿 stress 后 `RDUT` 改变并对齐测量点。 | 三个 target 的独立设置与波形验证。 | G2, G11, G12 | CONFIRMED；范围/分辨率 DEFERRED G2 |
| REQ-METHOD-003 | B1505 必须在 DUT-specific fixed `VDS-C` 下取得 initial `IDS-VGS` curve，并以 DUT-specific `Ith` crossing 定义 initial `Vth`。 | Method | PROJECT REQUIREMENT | Approved SP1 `REQ-VOLT-004`, `REQ-MEAS-008`（PAPER FACT） | 建立快速点测的统一参考曲线。 | B1505 test record 与独立 crossing 重算。 | G2, G12 | CONFIRMED；数值 DEFERRED G2 |
| REQ-METHOD-004 | MI/MP/MN 的 measured-point `VDS` 必须与对应 `VDS-C` 对齐到已批准容差内。 | Method | PROJECT REQUIREMENT | Approved SP1 `REQ-VOLT-005`（PAPER FACT 原则） | 保持高速点与 calibration drain-bias 可比。 | 自动比较 `VDS(point)-VDS-C`。 | G12 | CONFIRMED principle；tolerance DEFERRED G12 |
| REQ-METHOD-005 | 每个 measurement operating point 必须满足 `VDS-C>VGS-Vth`；所需 margin 由 DUT profile 定义。 | Method | PROJECT REQUIREMENT | Approved SP1 `REQ-VOLT-006`（PAPER FACT） | 保持论文映射所需工作区。 | 由记录量计算不等式和 margin。 | G2, G12 | CONFIRMED；margin DEFERRED G2 |
| REQ-METHOD-006 | Calibration 接受后，P/N tests 必须保持 `VDC`、`RL` 不变，只调节 `VGM-P/N` 完成 operating-point alignment。 | Method | PROJECT REQUIREMENT | Approved SP1 `REQ-FUNC-005`, `REQ-CTRL-002`（PAPER FACT） | 防止比较条件随 stress 极性改变。 | 配置 audit + 三组实验 metadata。 | G12 | CONFIRMED |
| REQ-METHOD-007 | `IDM-P`、`IDM-N` 必须与 `IDM-I` 匹配到批准容差内；P1 的 ±20% 仅保留为 PAPER PERFORMANCE REFERENCE。 | Method | PROJECT REQUIREMENT | Approved SP1 `REQ-MEAS-007`; P1 reported range | 限制 current mismatch 引入的 `ΔVth` 误差。 | 报告明确百分比公式和 P/N deviation。 | G12 | CONFIRMED principle；tolerance DEFERRED G12 |
| REQ-METHOD-008 | Positive-stress `IDS` 与能量必须受到 DUT-specific limit 约束，使 self-heating 不致使 `Vth` 结果不可解释。 | Method | PROJECT REQUIREMENT | Approved SP1 `REQ-MEAS-010`（PAPER FACT 原则）+ ENGINEERING INFERENCE | 分离 thermal shift 与 BTI hysteresis。 | G2 计算 envelope；G10/G11 实测电流/能量/必要热代理。 | G2, G10, G11 | PROPOSED；limit DEFERRED G2 |
| REQ-METHOD-009 | 只有 Master 激活 full-paper/Fig. 10 scope 后，系统才需要满足批准的 multiple-pulse stress protocol。 | Method | OPEN ITEM | Approved SP1 `REQ-CTRL-003`; P1 values are PAPER EXAMPLE VALUE | 不把扩展实验误设为最小 Fig. 3 强制功能。 | 激活后记录 pulse train、总 stress time 与结果。 | G12 | CONDITIONAL-INACTIVE |

### 3.3 Timing requirements

| ID | Requirement statement | Category | Source classification | Source | Reason | Verification concept | Verification stage | Status |
|---|---|---|---|---|---|---|---|---|
| REQ-TIME-001 | 系统必须支持 positive/negative stress→对应 measurement 的快速、可重复转换。 | Timing | PROJECT REQUIREMENT | Approved SP1 `REQ-TIME-001`（PAPER FACT） | 减少 stress removal 后 recovery 引起的低估。 | 同次捕获 timing reference、`VGS`、`VDS`。 | G11 | CONFIRMED |
| REQ-TIME-002 | 项目必须以 P1 报告的约 100 ns system-level `tdly` 为设计/验证目标；该目标不是单独 `VOA` edge 指标，也暂不等同无歧义的 `<100 ns` 或 `≤100 ns` PASS。 | Timing | PROJECT REQUIREMENT | `DEC-009`; PAPER PERFORMANCE REFERENCE; legacy `REQ-010` | 保留论文性能方向但不伪造工程算法。 | 按后续冻结事件算法提取完整 system `tdly`。 | G11 | CONFIRMED target nature；numeric PASS DEFERRED G10/G11 |
| REQ-TIME-003 | 系统必须支持可配置 `tpre`，并允许用 MI/`Vth-IS` 稳定性建立 reset-complete 判据。 | Timing | PROJECT REQUIREMENT | Approved SP1 `REQ-TIME-003`（PAPER FACT: long-term；数值未公开） | 控制 history dependence。 | `tpre` sweep 与 repeatability study。 | G12 | CONFIRMED capability；value/criterion DEFERRED G12 |
| REQ-TIME-004 | 系统必须支持可配置 `tstr`；P1 的 0.2–200 µs、10 µs、2 µs 只作为 PAPER EXAMPLE VALUE。 | Timing | PROJECT REQUIREMENT | Approved SP1 `REQ-TIME-004`（PAPER FACT capability） | 支持不同 stress duration 条件。 | programmed vs measured duration sweep。 | G11, G12 | CONFIRMED capability；project range DEFERRED G2/G12 |
| REQ-TIME-005 | 系统必须支持足以捕获 selected measured point 和所需 recovery interval 的 `tmea`。 | Timing | PROJECT REQUIREMENT | Approved SP1 `REQ-TIME-005`（PAPER FACT capability） | 防止采集窗口截断极值/恢复。 | acquisition-window coverage review。 | G10, G11, G12 | CONFIRMED capability；duration DEFERRED G10/G11 |
| REQ-TIME-006 | 系统必须允许改变和记录实际 `tdly`，以生成 recovery-vs-delay 数据；范围与步进按批准 protocol 定义。 | Timing | PROJECT REQUIREMENT | Approved SP1 `REQ-TIME-006`（PAPER FACT capability） | 支持 delay dependence 方法验证。 | delay sweep 的 repeatability 与 metadata audit。 | G11, G12 | CONFIRMED capability；range/step DEFERRED G12 |

### 3.4 Measurement and data requirements

| ID | Requirement statement | Category | Source classification | Source | Reason | Verification concept | Verification stage | Status |
|---|---|---|---|---|---|---|---|---|
| REQ-MEAS-001 | 每次转换必须记录同一事件的 `VGS(t)`、`VDS(t)` 及满足最终 `tdly` 定义所需的 timing-reference signal(s)，并建立已定义的共同时间关系。 | Measurement | PROJECT REQUIREMENT | Approved SP1 `REQ-MEAS-001`（PAPER FACT + ENGINEERING INFERENCE） | 支持完整 system timing，而非孤立 edge。 | channel association、trigger、time-alignment audit。 | G10, G11 | CONFIRMED；deskew policy DEFERRED G10/G11 |
| REQ-MEAS-002 | `VGS` 必须测为 DUT Gate-to-Kelvin-Source/SREF，不得测成 gate-to-earth。 | Measurement | PROJECT REQUIREMENT | `DEC-003/004`; legacy `REQ-011` | 避免 reference error 与危险 ground path。 | differential measurement 与接线审查。 | G1, G10, G11 | CONFIRMED |
| REQ-MEAS-003 | 系统必须提供可安全探测的 `VGS`、`VDS` 与 timing/trigger observation points；具体 probe/connector 由后续 Gate 决定。 | Measurement | PROJECT REQUIREMENT | legacy `REQ-014`; ENGINEERING INFERENCE | 使关键功能可验证。 | interface inspection + probe-access review。 | G1, G6/G7, G10 | CONFIRMED function；physical design DEFERRED G6/G7 |
| REQ-MEAS-004 | 后处理必须使用 `IDS=(VDC-VDS)/RL` 计算 measured-point current，并保留采用的 `VDC/RL` metadata。 | Measurement | PROJECT REQUIREMENT | Approved SP1 `REQ-MEAS-002`（PAPER FACT） | 建立 `VDS→IDS` 链。 | known-vector unit test 与数据重算。 | G12 | CONFIRMED |
| REQ-MEAS-005 | 后处理必须从 MI、MP、MN 分别取得 `IDM-I`、`IDM-P`、`IDM-N`。 | Measurement | PROJECT REQUIREMENT | Approved SP1 `REQ-MEAS-003`（PAPER FACT） | 提供三条阈值提取输入。 | reference-waveform replay。 | G10/G11, G12 | CONFIRMED；extremum algorithm DEFERRED G10/G11 |
| REQ-MEAS-006 | `IDM-I/P/N` 必须映射到同一 DUT、同一 fixed-`VDS-C` 的 B1505 curve；插值方法必须一致且可审计。 | Measurement | PROJECT REQUIREMENT | Approved SP1 `REQ-MEAS-004`（PAPER FACT） | 建立 `IDS→equivalent VGS` 链。 | lookup/interpolation unit test。 | G12 | CONFIRMED；interpolation acceptance DEFERRED G12 |
| REQ-MEAS-007 | 后处理必须按 P1 式 (3) 与“same method”取得 `Vth-IS/PS/NS`，并按式 (5) 计算 corrected `ΔVth`。 | Measurement | PROJECT REQUIREMENT | Approved SP1 `REQ-MEAS-005/006`（PAPER FACT；P/N 展开为 ENGINEERING RESTATEMENT） | 完成可核对的阈值位移链。 | 公式 unit test + independent recomputation。 | G12 | CONFIRMED |
| REQ-MEAS-008 | 在依赖单点/平行位移映射前，必须对每个目标 DUT/条件验证 `IDS≈Ith` 附近 curve 的适用性；P1 的 1% 仅为 PAPER PERFORMANCE REFERENCE。 | Measurement | PROJECT REQUIREMENT | Approved SP1 `REQ-MEAS-009`; P1 reported result | 防止把论文器件的平行移位假设直接外推。 | pre/post-stress curve comparison。 | G12 | PROPOSED；acceptance DEFERRED G12 |
| REQ-MEAS-009 | 原始波形、instrument/config metadata、DUT profile、B1505 curve、算法版本与最终结果必须足以独立重算 MI/MP/MN、`tdly` 和 `ΔVth`，并报告重复性。 | Measurement | PROJECT REQUIREMENT | Approved SP1 `REQ-VERIFY-004`; `DEC-009`; ENGINEERING INFERENCE | 实现可解释、可重复、可追溯结果。 | dataset audit + independent replay。 | G11, G12 | PROPOSED |

### 3.5 Interface requirements

| ID | Requirement statement | Category | Source classification | Source | Reason | Verification concept | Verification stage | Status |
|---|---|---|---|---|---|---|---|---|
| REQ-INTERFACE-001 | `SREF` 必须定义为 DUT Kelvin Source reference。 | Interface | PROJECT REQUIREMENT | `DEC-003`; legacy `REQ-003` | 冻结驱动和测量参考。 | net/interface review 与 continuity test。 | G1, G3, G10 | CONFIRMED |
| REQ-INTERFACE-002 | `SREF` 不得自动等于 laboratory earth/chassis。 | Interface | PROJECT REQUIREMENT | `DEC-004`; legacy `REQ-004` | 避免短路、共模错误与无效 `VGS`。 | isolation/continuity test。 | G1, G3, G10 | CONFIRMED |
| REQ-INTERFACE-003 | `GNDI`、`GNDA`、`SREF`、earth/chassis 必须保持显式不同的 reference domains；任何连接均需 Master 批准和追溯。 | Interface | PROJECT REQUIREMENT | `AGENTS.md`; `interfaces.md` forbidden connections | 防止隐式 ground merge。 | architecture/net review。 | G1, G3, G8, G10 | CONFIRMED |
| REQ-INTERFACE-004 | DUT Power Source 与 Kelvin Source 路径在 package 支持时必须分离；不支持时须由 DUT profile 明确记录限制。 | Interface | PROJECT REQUIREMENT | legacy `REQ-013`; ENGINEERING INFERENCE | 降低 source bounce 对驱动/测量的污染。 | connector/net/layout review 与动态测量。 | G1, G6/G7, G11 | CONFIRMED |
| REQ-INTERFACE-005 | 外部 pulse/control interface 必须支持可重复 state command、trigger reference 及 `tpre/tstr/tmea/tdly` 配置；电平、通道和 connector 在 G1 定义。 | Interface | PROJECT REQUIREMENT | Approved SP1 `REQ-CTRL-001`（sequence=PAPER FACT；接口=ENGINEERING INFERENCE） | 让时序和采集可同步。 | ICD review + repeated trigger capture。 | G1, G11 | PROPOSED |
| REQ-INTERFACE-006 | Gate-target interface 必须允许外部设定/提供 `VGS-P/N`、`VGM-I/P/N` 与 approved mode truth table 所需 rails，不在 G0 固定数值。 | Interface | PROJECT REQUIREMENT | `DEC-006/007`; Approved SP1 `REQ-VOLT-002/003` | 把通用架构与 DUT-specific levels 解耦。 | interface range review + profile test。 | G1, G2, G11 | PROPOSED |
| REQ-INTERFACE-007 | External drain-load interface 必须接收 DUT-specific `VDC/RL` 并明确 force/return/current path；base PCB 不因 DUT blocking rating 自动承担 650 V/3.3 kV。 | Interface | PROJECT REQUIREMENT | Approved SP1 boundary（ENGINEERING INTERFACE ALLOCATION）；`DEC-016` | 防止把额定耐压混为测试偏压。 | architecture/rating review 与低能量回路测试。 | G1, G2, G10 | PROPOSED |
| REQ-INTERFACE-008 | Calibration-data interface 必须传递 B1505 fixed-`VDS-C` curve、`Ith`、DUT/temperature/sweep metadata 给后处理；PCB 不负责生成该 curve。 | Interface | PROJECT REQUIREMENT | Approved SP1 Section 7（PAPER FACT + ENGINEERING INTERFACE ALLOCATION） | 划清 B1505 与高速 PCB 职责。 | data-schema review + end-to-end replay。 | G1, G12 | PROPOSED |
| REQ-INTERFACE-009 | Oscilloscope/probe interface 必须允许同次测量 `VGS/VDS/timing reference`，并管理 common-mode、loading 和 timing error；具体仪器规格后定。 | Interface | PROJECT REQUIREMENT | Approved SP1 boundary（ENGINEERING INFERENCE） | 确保 measured point 与 `tdly` 可解释。 | instrument-qualification plan 与波形验证。 | G1, G2, G10/G11 | PROPOSED |
| REQ-INTERFACE-010 | 0 V precondition path 与 Si8273 output 必须互斥、不得出现 simultaneous low-impedance contention；是否采用独立 clamp/switch 是未冻结的 PROJECT DESIGN CHOICE。 | Interface | PROJECT REQUIREMENT | `RISK-004`; `PROP-001` 未批准 | 冻结安全功能而不提前选择拓扑。 | state-transition/FMEA review + fault test。 | G1, G2, G10 | PROPOSED |

### 3.6 DUT compatibility requirements

| ID | Requirement statement | Category | Source classification | Source | Reason | Verification concept | Verification stage | Status |
|---|---|---|---|---|---|---|---|---|
| REQ-DUT-001 | 平台目标必须覆盖 650 V-class 与 3.3 kV-class SiC MOSFET 的 low-`VDS` BTI / `Vth`-hysteresis test。 | DUT compatibility | PROJECT REQUIREMENT | `DEC-016`; legacy `REQ-015` | 冻结双电压等级目标范围。 | 两类批准 DUT profile 的配置/实验资格验证。 | G1, G2, G12 | CONFIRMED |
| REQ-DUT-002 | DUT blocking-voltage rating 不得被解释为本 PCB 必须施加 650 V/3.3 kV；实际 `VDC/VDS-C` 由 BTI measurement condition 决定，禁止将本项目转为 breakdown test。 | DUT compatibility | PROJECT REQUIREMENT | `DEC-016`; Master SP1 Review §5 | 防止形成错误的高压绝缘需求或危险测试。 | requirement/rating review；test profile audit。 | G1, G2, G12 | CONFIRMED |
| REQ-DUT-003 | Gate-driver architecture、SREF、P/N sequence、measurement principle 与 `VDS→IDS→Vth` chain 应与 blocking-voltage class 解耦。 | DUT compatibility | PROJECT REQUIREMENT | ENGINEERING INFERENCE from `DEC-016` and approved SP1 | 最大化平台复用并隔离 DUT 差异。 | architecture review；两类 DUT configuration comparison。 | G1, G2 | PROPOSED |
| REQ-DUT-004 | 每个 target DUT 必须建立受控 profile，至少包含：exact part/package、`Qg`、`Ciss/Crss`、recommended/absolute `VGS`、`Vth`、`VGM`、`Ith`、`VDS-C`、Kelvin Source、`Rg`、`VDC/RL`、temperature 和 relevant timing checks。 | DUT compatibility | PROJECT REQUIREMENT | legacy `REQ-016`; Master Review §5 | 将所有不可通用参数留在 DUT profile。 | datasheet/calculation audit 与 profile completeness check。 | G2 | CONFIRMED principle；values DEFERRED G2 |
| REQ-DUT-005 | DUT connector/adapter 与 `Rg` configuration 必须容纳 package/Kelvin/Qg 差异，同时不得破坏 `REQ-FUNC-001/002`；具体 adapter 和 fixed/replaceable/selectable `Rg` policy 由 G1/G2 决定。 | DUT compatibility | PROJECT REQUIREMENT | `OPEN-REQ-006`; ENGINEERING INFERENCE | 在“不换 base PCB”与“DUT-specific hardware”之间建立明确边界。 | G1 ICD/adapter policy review；G2 drive calculation；G6/G7 physical review。 | G1, G2, G6/G7 | PROPOSED；implementation DEFERRED |

### 3.7 Safety requirements

| ID | Requirement statement | Category | Source classification | Source | Reason | Verification concept | Verification stage | Status |
|---|---|---|---|---|---|---|---|---|
| REQ-SAFE-001 | 系统必须定义独立于 PRECONDITION 的 `SAFE_OFF` logical state、进入/退出条件和 gate/drain intent；具体电路后定。 | Safety | PROJECT REQUIREMENT | Approved SP1 `REQ-SAFE-001`（non-P1）；`RISK-003` | 覆盖上电、故障、待机与连接操作。 | G1 state/FMEA review；G10 fault test。 | G1, G10 | CONFIRMED need；definition DEFERRED G1 |
| REQ-SAFE-002 | 必须定义 power-up、power-down、loss-of-control、UVLO/default-state sequence，并禁止造成意外 prolonged stress。 | Safety | PROJECT REQUIREMENT | Approved SP1 `REQ-SAFE-002`; `RISK-002/003` | 防止默认状态损伤 DUT 或短接 supplies。 | sequence review + controlled fault injection。 | G1, G2, G10 | PROPOSED；logic G1/setpoints G2 |
| REQ-SAFE-003 | 必须定义 gate overvoltage、drain overcurrent、false-trigger、contention 与 energy/self-heating protection；setpoint 与 topology 由 G2 决定。 | Safety | PROJECT REQUIREMENT | Approved SP1 `REQ-SAFE-002`; `RISK-004/005/008` | P1 未提供原型安全边界。 | hazard/FMEA review、calculation、fault test。 | G1, G2, G10 | PROPOSED |
| REQ-SAFE-004 | 所有 DUT gate/drain conditions 必须处于该 DUT profile 的批准 ratings、energy 和 temperature envelope 内。 | Safety | PROJECT REQUIREMENT | ENGINEERING INFERENCE; legacy `REQ-100` | 防止把通用平台目标变成无界测试。 | datasheet + calculation + measured waveform audit。 | G2, G10, G11 | PROPOSED |

### 3.8 Process requirements

| ID | Requirement statement | Category | Source classification | Source | Reason | Verification concept | Verification stage | Status |
|---|---|---|---|---|---|---|---|---|
| REQ-PROCESS-001 | 所有器件 pin、package、ratings 和关键参数必须在 schematic freeze 前由 authoritative datasheet 验证。 | Process | PROJECT REQUIREMENT | legacy `REQ-100`; `AGENTS.md` | 禁止猜测硬件事实。 | datasheet audit。 | G2/G3 | CONFIRMED |
| REQ-PROCESS-002 | 关键结论必须标为 PAPER FACT、PAPER EXAMPLE VALUE、PAPER PERFORMANCE REFERENCE、ENGINEERING INFERENCE、PROJECT REQUIREMENT、PROJECT DESIGN CHOICE 或 OPEN ITEM，并保留 source。 | Process | PROJECT REQUIREMENT | legacy `REQ-101`; Master SP1 approval | 保持证据与规范分层。 | document traceability audit。 | Every gate | CONFIRMED |
| REQ-PROCESS-003 | 未批准 OPEN ITEM 不得被默认为数值或实现；SP2/SP3 设计只能在对应 Gate/decision 后展开。 | Process | PROJECT REQUIREMENT | `AGENTS.md`; Master Review boundary | 防止需求空白被设计猜测填补。 | review checklist。 | G1-G3 | CONFIRMED |
| REQ-PROCESS-004 | ERC 必须通过，或每个残余 warning 在 layout freeze 前有明确审核记录。 | Process | PROJECT REQUIREMENT | legacy `REQ-102` | 保证原理图机器检查闭环。 | ERC report audit。 | G3/G8 | CONFIRMED |
| REQ-PROCESS-005 | DRC 必须通过，或每个残余 warning 在 manufacturing release 前有明确审核记录。 | Process | PROJECT REQUIREMENT | legacy `REQ-103` | 保证 PCB rule check 闭环。 | DRC report audit。 | G8 | CONFIRMED |
| REQ-PROCESS-006 | 未经 ERC、DRC、manual review、verification-matrix approval 与用户最终批准，不得生成/发布 production Gerber。 | Process | PROJECT REQUIREMENT | `DEC-010`; legacy `REQ-104` | 防止未审核设计进入制造。 | manufacturing hold checklist。 | G9 | CONFIRMED |
| REQ-PROCESS-007 | 每个用户可交付项目文件必须同步至其 canonical GitHub path，随后才可报告完成。 | Process | PROJECT REQUIREMENT | `DEC-011`; legacy `REQ-105` | 保持工程记录持久化。 | remote-file readback。 | Every deliverable | CONFIRMED |
| REQ-PROCESS-008 | 每个已同步输出必须登记 `docs/chat_output_index.md`，不要求重复归档副本。 | Process | PROJECT REQUIREMENT | `DEC-012`; legacy `REQ-106` | 建立单一索引与路径。 | index/path audit。 | Every deliverable | CONFIRMED |
| REQ-PROCESS-009 | 禁止直接提交受限版权材料、credentials、敏感数据或未批准大文件；同步失败必须报告 `OUTPUT_SYNC_BLOCKED` 和具体未同步文件。 | Process | PROJECT REQUIREMENT | `DEC-013`; legacy `REQ-107/108` | 防止 persistence rule 导致安全/版权问题。 | repository-content/blocked-state audit。 | Every deliverable | CONFIRMED |

### 3.9 Verification-level requirements

| ID | Requirement statement | Category | Source classification | Source | Reason | Verification concept | Verification stage | Status |
|---|---|---|---|---|---|---|---|---|
| REQ-VERIFY-001 | Prototype 必须按已批准事件定义同时记录所需 timing reference、`VGS`、`VDS` 并提取完整 system `tdly`；不得以孤立 `VOA` edge 代替。 | Verification | PROJECT REQUIREMENT | Approved SP1 `REQ-VERIFY-001`; `DEC-009` | 直接验证核心系统目标。 | synchronous oscilloscope capture。 | G11 | CONFIRMED；algorithm DEFERRED G10/G11 |
| REQ-VERIFY-002 | Prototype/method validation 必须报告 MI/MP/MN 相对 `VDS-C` 的偏差和 PASS。 | Verification | PROJECT REQUIREMENT | Approved SP1 `REQ-VERIFY-002` | 证明 calibration compatibility。 | automated point comparison。 | G12 | CONFIRMED；tolerance DEFERRED G12 |
| REQ-VERIFY-003 | Prototype/method validation 必须报告 `IDM-P/N` 相对 `IDM-I` 的明确偏差公式、结果、调节后的 `VGM-P/N` 和 PASS。 | Verification | PROJECT REQUIREMENT | Approved SP1 `REQ-VERIFY-003` | 控制 current mismatch error。 | current-consistency report。 | G12 | CONFIRMED；tolerance DEFERRED G12 |
| REQ-VERIFY-004 | Released dataset 必须通过 raw waveform→`IDS`→B1505 mapping→raw shift→corrected `ΔVth` 的独立重算。 | Verification | PROJECT REQUIREMENT | Approved SP1 `REQ-VERIFY-004` | 证明最终结果可追溯。 | independent software replay。 | G12 | CONFIRMED；numeric software tolerance DEFERRED G12 |
| REQ-VERIFY-005 | 平台通用性声明必须分别用至少一个经批准的 650 V-class profile 和一个 3.3 kV-class profile 完成 requirement/configuration qualification；不要求施加 blocking rating。 | Verification | PROJECT REQUIREMENT | `DEC-016`; ENGINEERING INFERENCE | 防止仅凭架构推测宣称“双等级兼容”。 | profile audit + low-`VDS` functional/method test。 | G2, G11, G12 | PROPOSED |

## 4. 650 V / 3.3 kV compatibility boundary

| 应保持通用的系统概念 | 必须 DUT-specific 的参数/接口 |
|---|---|
| `VGS` control concept | `Qg`, `Ciss`, `Crss` |
| `SREF=DUT Kelvin Source` concept | recommended/absolute `VGS` |
| Positive/negative BTI sequence | `Vth`, `VGM-I/P/N`, `Ith` |
| 0 V precondition function | `VDS-C`, `VDC`, `RL` |
| `VOA` stress→measurement role | exact package and pinout |
| `VDS→IDS→Vth→ΔVth` chain | Kelvin Source availability/adapter |
| B1505/high-speed-PCB responsibility boundary | `Rg`, required driver current, decoupling envelope |
| system-level `tdly` concept and traceability | instrument/common-mode/bandwidth needs for the actual waveform |

结论：blocking-voltage class 是 DUT qualification attribute，不是本 low-`VDS` BTI PCB 的 drain operating voltage。通用性通过“base architecture + DUT profile + adapter/configuration”实现；G0 不选择任何具体数值。

## 5. OPEN-item disposition

分类含义：`MUST_FREEZE_G0`=Master 在关闭 G0 时批准；其余分类表示不会阻止 G1 架构工作，但必须在 owner Gate 的 deadline 前作出决定并按列示方法验证。

| OI | Open item | Disposition / Owner Gate | Decision deadline | Why now / why deferrable | Verification method |
|---|---|---|---|---|---|
| OI-000 | 本 canonical hierarchy、legacy crosswalk 与新增 PROJECT REQUIREMENT 是否批准 | **MUST_FREEZE_G0 / Master** | G0 final approval | 它决定唯一 normative source；这是唯一仍需 G0 Master 动作的治理项。 | Master diff/review；批准后更新 `requirements.md`。 |
| OI-001 | `tdly` 精确 start event、crossing 与 end definition | **DEFER_TO_G10_G11 / SP6 measurement owner** | G11 test-plan freeze 前 | G1 只需保留 control/`VGS`/`VDS` observability；精确算法需真实波形。 | 同步 reference/`VGS`/`VDS` capture + algorithm replay。 |
| OI-002 | 约 100 ns 最终采用 `<100 ns`、`≤100 ns`、band 或统计指标 | **DEFER_TO_G10_G11 / Master + SP6** | G11 acceptance freeze 前 | 其“system-level target”已确定；最终数值 PASS 需 repeatability/noise evidence。 | 多次 `tdly` distribution 与 uncertainty report。 |
| OI-003 | `VDS≈VDS-C` tolerance | **DEFER_TO_G12 / SP7 method owner** | 首次 G12 dataset acceptance 前 | 不影响 G1 topology；需结合 curve sensitivity 与 DUT profile。 | sensitivity study + measured-point comparison。 |
| OI-004 | `IDM-P/N≈IDM-I` 百分比公式与 tolerance | **DEFER_TO_G12 / SP7** | 首次 G12 method qualification 前 | P1 ±20% 不能直接外推；不影响 G1接口。 | 明确 denominator/sign convention；error/sensitivity study。 |
| OI-005 | `tpre` 最低值/reset-complete criterion | **DEFER_TO_G12 / SP7** | 正式 BTI protocol release 前 | “long-term”无论文数值；需用目标 DUT 的 MI/`Vth-IS` history 验证。 | `tpre` sweep + repeatability/stability test。 |
| OI-006 | `tmea` length、exit condition、recovery window | **DEFER_TO_G10_G11 / SP6** | G11 acquisition-plan freeze 前 | G1 只需可配置/可采集；实际长度取决于 waveform 与 scope memory。 | window-coverage study；确认不截断 measured point/recovery。 |
| OI-007 | MI/MP/MN extremum extraction algorithm/search window | **DEFER_TO_G10_G11 / SP6+SP7** | G11 algorithm freeze 前 | 真实 ringing/noise 尚未知；接口只需保留原始信号。 | labeled waveform set + replay/unit tests。 |
| OI-008 | Filtering/averaging/interpolation in waveform processing | **DEFER_TO_G10_G11 / SP6+SP7** | G11 algorithm freeze 前 | 现在定数值会猜测 instrument noise。 | raw-vs-processed comparison、phase/amplitude bias check。 |
| OI-009 | Ringing treatment 与多个 local extrema 的选择 | **DEFER_TO_G10_G11 / SP6+SP7** | G11 algorithm freeze 前 | 必须基于 prototype waveform；G1/G2 仍以降低 ringing 为设计目标。 | synthetic + captured ringing cases；manual cross-check。 |
| OI-010 | Deskew / cable-delay / de-embedding policy | **DEFER_TO_G10_G11 / SP6** | G11 instrument qualification 前 | G1 只需提供 common timing interface；校正值依赖最终 probe/cable。 | calibration fixture/known-edge deskew verification。 |
| OI-011 | self-heating/positive-stress current-energy limit | **DEFER_TO_G2 / SP3+DUT owner** | G2 electrical envelope freeze 前 | 需要 DUT thermal/electrical data；但 G0 已要求必须有限制。 | `IDS`, pulse energy, duty/temperature calculation；G10/G11 validation。 |
| OI-012 | `SAFE_OFF` gate/drain intent 与 entry/exit logic | **DEFER_TO_G1 / G1 architecture owner** | G1 state/interface freeze 前 | 架构必须知道故障态；不需要先选 clamp/relay/MOSFET。 | state table + FMEA review；G10 fault test plan。 |
| OI-013 | power-up/down、loss-of-control、UVLO/default sequence | **DEFER_TO_G1 / G1 architecture owner** | G1 control/power interface freeze 前 | 需要先分配模块职责；thresholds/components 可在 G2。 | sequence diagram/FMEA；G10 staged bring-up。 |
| OI-014 | protection functions、interlock 与 energy limiting allocation | **DEFER_TO_G1 / G1 architecture owner** | G1 safety interface freeze 前 | G1 必须分配谁检测/切断；setpoints/topology 不必在 G0。 | hazard analysis + interface review；G2 calculations/G10 fault tests。 |
| OI-015 | 650 V/3.3 kV compatibility architecture/configuration boundary | **DEFER_TO_G1 / G1 architecture owner** | G1 block/ICD freeze 前 | “low-`VDS`、base architecture decoupled”已确定；模块边界仍需画清。 | 两类 DUT configuration walk-through。 |
| OI-016 | DUT connector/adapter strategy | **DEFER_TO_G1 / G1 interface owner** | G1 DUT-interface freeze 前 | 不影响方法需求，但影响后续 package/return-path实现。 | ICD/adapter matrix；G6/G7 physical review。 |
| OI-017 | 是否及如何允许 DUT-specific `Rg` 更换/选择 | **DEFER_TO_G1 / G1 interface owner** | G1 configuration-policy freeze；数值 G2 | G1 必须说明它是否算“DUT configuration”而非“P/N mode rework”；具体阻值需 Qg。 | policy review + G2 drive calculation + G11 waveform。 |
| OI-018 | exact instrument model、minimum bandwidth/sample rate/common-mode/loading | **DEFER_TO_G2 / measurement owner** | G2 instrument requirement freeze 前 | 需由 100 ns target 和预估 edge/ringing 反推；不阻止 G1定义信号接口。 | bandwidth/error budget；G10/G11 instrument qualification。 |
| OI-019 | exact DUT、package、`Qg/Ciss/Crss`、`VGS/VGM`、`Ith`、`VDS-C`、`VDC/RL`、temperature | **DEFER_TO_G2 / DUT+SP2+SP3 owners** | 对应 DUT profile 的 G2 freeze 前 | 都是 DUT-specific；G0 冻结参数类别而非猜数值。 | datasheet audit、calculation、LTspice/bench where required。 |
| OI-020 | probe pads、connector mechanics、Kelvin routing 与 physical separation | **DEFER_TO_G6_G7 / PCB owner** | placement/routing freeze 前 | G1 先定义 logical nets；物理实现需要 package/stackup。 | placement/routing review + continuity/parasitic inspection。 |
| OI-021 | B1505 curve interpolation、software numeric tolerance、file schema | **DEFER_TO_G12 / SP7** | G12 software release 前 | 公式链已冻结；实现细节不影响 G1 hardware architecture。 | unit tests、golden vectors、independent replay。 |
| OI-022 | 是否激活 multiple-pulse/Fig. 10 reproduction | **DEFER_TO_G12 / Master** | G12 scope freeze 前 | 最小 Fig. 3 reproduction 不需要该扩展，硬件仅在已批准接口能力内评估。 | scope decision；激活后 protocol verification。 |

结论：除 `OI-000` 的 Master baseline approval 外，没有仍需在 G0 猜测的技术数值。所有 OPEN 均有 owner Gate、deadline 和 verification method。

## 6. G0 final questions

### A. PCB 必须实现哪些功能？

- 同一 base PCB 完成 P/N BTI，极性切换不靠 base-PCB 元件重焊；
- 以 `SREF=DUT Kelvin Source` 为驱动/测量参考，保持 reference domains 显式；
- 支持 Gate-to-SREF 0 V precondition，以及 calibration/positive/negative 三条序列；
- 使用 Si8273 `VOA` 完成已批准的 stress→measurement 两级高速切换 truth table；
- 连接/支持低-`VDS` `VDC-RL-DUT` 回路、DUT Gate/Kelvin/Power Source 和必要测量节点；
- 使 `VGM-I/P/N`、`VGS-P/N`、时序与 DUT profile 可由外部接口配置；
- 支持获得可解释、可重复的 MI/MP/MN 与完整 system `tdly` 证据；
- 支持 650 V-class 与 3.3 kV-class DUT 的 low-`VDS` configuration/adapter，而不是承担其额定 blocking voltage。

### B. PCB 明确不负责哪些功能？

- 不执行 B1505 slow fixed-`VDS-C` `IDS-VGS` calibration sweep；
- 不替代 pulse generator、external gate-rail supplies、`VDC` supply、oscilloscope/probes 或后处理软件；
- 不直接完成 curve mapping、MI/MP/MN algorithm、`Vth/ΔVth` 计算或数据归档逻辑；
- 不进行 breakdown test，也不因 DUT 为 650 V/3.3 kV 就施加该额定电压；
- 不在 G0 决定 exact DUT values、instrument model、connector pinout、`Rg`、protection/clamp topology 或 PCB layout；
- 不以 `VOA` edge 单独证明系统达成约 100 ns 目标。

### C. 哪些量属于外部可调参数？

`VDDA/GNDA`、`VGS-P/N`、`VGM-I/P/N`、`VIA` waveform/polarity、`tpre/tstr/tmea/tdly` control profile、`VDC`、`RL`、B1505 `VDS-C/Ith/sweep profile`、temperature、scope acquisition/trigger settings，以及批准的 DUT adapter/`Rg` configuration。它们必须记录在 DUT/experiment metadata 中；“可调”不表示范围现在已冻结。

### D. 哪些接口必须在 G1 定义？

Reference-domain/return-path、pulse/control/trigger、external gate rails、0 V precondition functional interface、Si8273 enable/default/safety behavior、DUT Gate/Kelvin/Power Source、`VDC/RL` drain loop、scope sense/timing、B1505 calibration-data、DUT adapter/configuration、SAFE_OFF/power/protection responsibility allocation。G1 只需定义 logical/electrical intent，不需猜 connector pin 或器件值。

### E. 哪些参数必须等 DUT datasheet 进入 G2 后确定？

Exact part/package/pinout、Kelvin availability、`Qg/Ciss/Crss`、recommended/absolute `VGS`、`Vth`、`VGM` range/resolution、`Ith`、`VDS-C`、`VDC/RL`、`Rg`、driver current、decoupling/rail envelope、thermal/current/energy limits、temperature profile、器件额定裕量，以及由目标波形反推的 instrument minimum specification。

### F. 哪些验收指标现在已经冻结？

严格说，本文件不能自行将 requirement 标为 `FROZEN`；但以下约束已有 Master decision/approved SP1 支持，作为 G0 review 的不变输入：同一 base PCB P/N；P/N 不靠元件重焊；`SREF` 定义及不自动接 earth；`VOA` 的关键快速转换职责；0 V precondition；三条方法序列；Fig. 3 resistive-load/`VDS→IDS→Vth` 原理；可解释、可重复 MI/MP/MN；约 100 ns 是完整系统目标而非单一 edge；low-`VDS` 双 DUT class 范围；禁止未审核 production Gerber。

### G. 哪些验收指标允许延期？

`tdly` 精确事件与数值 PASS、`VDS`/`IDM` tolerance、`tpre/tmea/tstr/tdly` 数值范围、extremum/filter/ringing/deskew/de-embedding、parallel-shift acceptance、software tolerance、self-heating limit、instrument bandwidth、SAFE_OFF/sequencing/protection 细节、DUT connector/adapter/`Rg` policy 和全部 DUT-specific electrical values。延期不取消 requirement，必须按 Section 5 的 Gate/deadline 关闭。

### H. G1 能否在不猜系统需求的情况下开始？

**能。** G1 已获得状态、序列、参考点、模块职责、通用/特定边界、安全功能和必须定义的接口清单。它可以把未定数值保留为 named parameters/constraints；不得自行填入数值或拓扑。`OI-000` 经 Master 批准后，本提案才成为 canonical normative baseline。

## 7. Proposed update to `docs/requirements.md`

本次不直接改写 `docs/requirements.md`。建议由 Master 批准后执行一次受控更新：

1. 状态改为 `canonical baseline approved by Master`（仅 Master 可执行），并引用本文件/批准记录；
2. 用 Section 3 的 semantic-ID hierarchy 替代 `REQ-001...016` 与 `REQ-100...108` 作为 normative list；
3. 保留 legacy crosswalk appendix，不删除 SP1 的 36 个历史 ID；
4. 将 `OPEN-REQ-008` 在 Master 批准后标为 resolved-by-merge；其余 `OPEN-REQ-*` 替换为 Section 5 的 OI owner/deadline records；
5. 明确 `REQ-FUNC-007/008` 是 Master-approved PROJECT DESIGN CHOICE 转化的 PROJECT REQUIREMENT，不是 PAPER REQUIREMENT；
6. 明确 0 V requirement 是功能/互斥约束，独立 clamp/switch 仍是未冻结 implementation；
7. 不把任何 PAPER EXAMPLE VALUE 或 PAPER PERFORMANCE REFERENCE 变成通用数值；
8. 随后重建 `docs/verification_matrix.md`，移除对 superseded SP1-v0.1 的主引用，并覆盖每个 canonical ID；
9. 在 G1 完成后再同步 `docs/interfaces.md`，修正 precondition “separate mechanism shall”的过强措辞并加入 DUT adapter/safety interface。

## 8. Risks

| Risk | Disposition |
|---|---|
| `tdly` 由不同 crossing/filter/extremum 定义得到不同结果 | `REQ-TIME-002/REQ-VERIFY-001` + OI-001/002/007...010；G11 前冻结算法。 |
| Ringing/probe loading 伪造 MP/MN | 保留 raw waveform；G6/G7 probe access；G10/G11 instrument qualification。 |
| `VDS/IDM` 对齐不足破坏 B1505 mapping | `REQ-METHOD-004/007` + G12 sensitivity/tolerance。 |
| Precondition history 和 self-heating 混入 hysteresis | `REQ-TIME-003`、`REQ-METHOD-008`；G2 thermal envelope + G12 stability。 |
| 将 650 V/3.3 kV rating 当作实际 drain bias | `REQ-DUT-002` 明确禁止；DUT profile 控制实际 `VDC/VDS-C`。 |
| Adapter/`Rg` 灵活性破坏“一块 PCB”约束 | `REQ-DUT-005`；G1 明确 base PCB vs DUT configuration boundary。 |
| 0 V precondition path 与 `VOA` 争用 | `REQ-INTERFACE-010`；不提前选 topology，G1/G2/G10 闭环。 |
| SAFE_OFF/default state 未定义导致意外 stress | `REQ-SAFE-001/002`；G1 state/FMEA，G10 fault test。 |
| 旧 ID/旧 matrix 继续被当作 canonical | 本 crosswalk + Master 后更新 `requirements.md`/`verification_matrix.md`。 |

## 9. G0 Final Gate Review

| Gate | Result | Evidence |
|---|---|---|
| A. SP1 已正式合并进入项目 requirements | PASS | Section 3 将 SP1 36-ID 全部映射至 canonical hierarchy；Section 2.3 保留 crosswalk。 |
| B. Requirement ID 不存在冲突 | PASS | 新 ID 使用语义 namespace；legacy IDs 只作 source，不作 canonical。 |
| C. 所有关键功能都有 canonical REQ | PASS | Functional/Method/Timing/Measurement/Interface/DUT/Safety/Process/Verification 九类齐全。 |
| D. 所有关键 REQ 都有 traceability | PASS | 每条均有 Source classification 与 Source。 |
| E. 所有关键 REQ 都有 verification concept | PASS | 每条均有 method 与 stage。 |
| F. Positive/Negative BTI 范围明确 | PASS | `REQ-FUNC-001/002/003/008`。 |
| G. 650 V/3.3 kV low-`VDS` BTI 范围明确 | PASS | `REQ-DUT-001...005`；明确非 breakdown。 |
| H. SREF 定义冻结 | PASS | `REQ-INTERFACE-001...003` 直接追溯 `DEC-003/004`。 |
| I. 约 100 ns 系统目标性质明确 | PASS | `REQ-TIME-002/REQ-VERIFY-001`；数值算法正式延期。 |
| J. 所有 OPEN 都有 owner Gate | PASS | Section 5 每项均有 Gate、deadline、verification。 |
| K. 不存在必须在 G0 决定但仍无人负责的 OPEN | PASS | 唯一 `MUST_FREEZE_G0` 为 OI-000，owner=Master，本文件即审核包。 |
| L. 没有进入具体 SP2/SP3 电路设计 | PASS | 无器件值、拓扑、原理图、BOM、layout 或 Gerber。 |
| M. 没有把论文 example value 变成通用数值 | PASS | 所有示例值均明确为 PAPER EXAMPLE VALUE / PERFORMANCE REFERENCE。 |
| N. G1 可以无需猜测系统需求而工作 | PASS | Section 5 分配所有未定项；Section 6D 定义 G1 必须输出的 interfaces。 |

# G0 STATUS: READY FOR MASTER REVIEW

该结论表示交付物具备 Master 审核条件，不表示本文件已 `FROZEN`，也不表示 G0 已由 Master 判定 `PASS`。

---

HANDOFF_PACKET

Subproject:
G0 Closing

Version:
G0-CRB-v1.0

Inputs reviewed:
SP1-v0.2、SP1-FGR-v1.0、SP1 Master Review、`requirements.md`、`decisions.md`、`interfaces.md`、`verification_matrix.md`、`risk_register.md`、`project_status.md`、`stage_gate.md`；无 MISSING_INPUT。

Canonical requirements proposed:
九类 semantic-ID hierarchy：8 FUNC、9 METHOD、6 TIME、9 MEAS、10 INTERFACE、5 DUT、4 SAFE、9 PROCESS、5 VERIFY；合计 65 条。

Duplicate/conflicting requirements resolved:
合并三序列、约 100 ns、resistive-load、measurement points 等重复项；将 Si8273 rail/truth table 正确归为 Master-approved project choice；纠正 precondition “独立机制 shall”与 `PROP-001` 的冲突；隔离 conditional multiple-pulse scope；消除旧 ID 层级歧义。

New project requirements:
Gate architecture 与 blocking class 解耦；DUT profile；adapter/`Rg` configuration boundary；self-heating envelope；cross-DUT qualification；raw-data/algorithm traceability；common timing relationship。

Deferred requirements:
OI-001...022 均分配 owner Gate、deadline 与 verification；没有 ownerless OPEN。

Items frozen now:
本文件不自行标记 FROZEN。已存在的 Master decisions/approved inputs包括：一块 base PCB P/N、极性切换不重焊、SREF定义/非earth、VOA高速职责、0 V precondition、完整三序列、系统级约100 ns目标性质、可解释/可重复 MI/MP/MN、low-`VDS` 650 V/3.3 kV scope、制造 hold。

Items deferred to G1:
SAFE_OFF logical state；power/default sequence；protection responsibility；reference/control/gate/drain/scope/data interfaces；650 V/3.3 kV configuration boundary；DUT adapter；`Rg` policy。

Items deferred to G2:
Exact DUT/Si8273/instrument facts；`Qg/Ciss/Crss`；VGS/VGM/Ith/VDS-C/VDC/RL/Rg；driver/decoupling/rating/thermal envelope；minimum instrument specification。

Items deferred to prototype validation:
完整 `tdly` 算法与数值 PASS；tmea/acquisition；extremum/filter/ringing/deskew/de-embedding；VDS/IDM tolerance；tpre reset criterion；parallel-shift/software acceptance；repeatability。

650V / 3.3kV compatibility requirements:
同一 low-`VDS` base architecture，通用 sequence/SREF/measurement chain；blocking rating 不等于 test voltage；通过 DUT-specific profile、adapter、Kelvin/connector、Rg、VDC/RL 配置适配并分别 qualification。

Risks:
Timing-definition bias、ringing/probe loading、mapping mismatch、history/self-heating、rating误读、adapter/Rg边界、precondition contention、unsafe default、legacy-ID误用。

Open questions:
仅 OI-000 必须由 G0 Master 批准；其余问题按 OI-001...022 延期并有 owner/deadline。

G0 gate result:
READY

Items requiring Master approval:
批准/退回 canonical hierarchy 与 crosswalk；批准新增 PROJECT REQUIREMENT；确认 deferred-item owner/deadline；批准后授权更新 `requirements.md` 和重建 `verification_matrix.md`。不要求 Master 现在选择任何 DUT-specific 数值或电路拓扑。

Recommended next action:
Master 审核 G0-CRB-v1.0。若批准，则将本 hierarchy 写入 canonical `docs/requirements.md`、关闭 legacy `OPEN-REQ-008`、重建 `docs/verification_matrix.md`，并让 G1 按 Section 6D 完成 system block/interface definition；在批准前保持 G0 ACTIVE，不标记 PASS/FROZEN。

END_HANDOFF_PACKET
