# 决策记录

## 已批准基线决策

- DEC-001：使用同一块PCB支持Positive BTI和Negative BTI。
- DEC-002：BTI极性只通过外部`VDDA/GNDA`电压与`VIA`波形极性切换，不更换PCB元件。
- DEC-003：定义`SREF`为DUT Kelvin Source reference；其对当前三引脚DUT的受控解释见DEC-018。
- DEC-004：不得假定`SREF`等于实验室earth。
- DEC-005：使用Si8273 channel A / `VOA`执行stress-to-measurement快速转换。
- DEC-006：Positive BTI采用`VDDA=VGS-P`、`GNDA=VGM-P`，stress结束时`VIA HIGH→LOW`。
- DEC-007：Negative BTI采用`VDDA=VGM-N`、`GNDA=VGS-N`，stress结束时`VIA LOW→HIGH`。
- DEC-008：完整复现除stress和measurement外还必须包含0 V precondition状态。
- DEC-009：系统成功标准是在stress移除后约100 ns获得可解释的`VDS`测量点，而不是只看`VOA`边沿速度。
- DEC-010：ERC、DRC、人工审核和验证矩阵批准前不得发布制造输出。
- DEC-011：每个项目聊天产生的输出文件必须保存到本GitHub仓库，之后任务才可视为完成。
- DEC-012：输出文件保存到规范工程路径并登记在`docs/chat_output_index.md`，不要求重复归档副本。
- DEC-013：不得直接提交不可再分发的PDF、credentials、敏感信息或未批准的大文件；必须记录替代处理方式。
- DEC-014：Master批准`SP1-v0.2 + SP1-FGR-v1.0`为完成的论文方法/系统需求证据基线。除非发现来源错误，SP1保持关闭。
- DEC-015：SP1完成不自动关闭G0；在项目级验收定义和canonical requirement baseline冻结前，G0保持`ACTIVE`。
- DEC-016：平台目标包括650 V-class与3.3 kV-class SiC MOSFET的低`VDS` BTI/`Vth`迟滞测试。DUT额定阻断电压不要求BTI PCB施加650 V或3.3 kV。
- DEC-017：Master批准`G0-CRB-v1.2`、65条`REQ-SYS-*`规范需求、69行SP1/legacy crosswalk及`OPEN::OI-001...022`延期控制；`OPEN::OI-000`批准并关闭。自本决定生效起，`docs/requirements.md`是唯一项目级规范需求基线，状态`FROZEN`；G0=`PASS`，G1=`ACTIVE`，G3=`BLOCKED`。改变冻结需求ID、技术含义、分类、scope、证据层级或crosswalk必须经过Master change approval。该决定不批准任何具体电路拓扑、器件数值、DUT参数、`Rg`/电容值、0 V实现、保护实现、connector pinout、原理图、PCB或BOM。
- DEC-018：Master确认当前使用及计划支持的650 V-class和3.3 kV-class SiC MOSFET均为Gate/Drain/Source三引脚器件。当前G1不得把DUT建模为Gate/Kelvin Source/Power Source/Drain四端器件，也不得声称直接支持独立第四个Kelvin Source引脚。`DUT_SOURCE`是唯一Source物理引脚；`SREF`是从该引脚或焊盘处`SOURCE_STAR`引出的Gate回流和`VGS`测量Kelvin式参考路径；`DRET`是从同一`SOURCE_STAR`引出的漏极功率返回路径。两者在`SOURCE_STAR`有意连接，不是相互绝缘的电气域，且不得在更上游再次连接。三引脚封装内部公共Source阻抗必须进入DUT profile、风险登记和G11验证。`REQ-SYS-INTERFACE-001`按三引脚Source端Kelvin式取点解释，`REQ-SYS-INTERFACE-004`按封装不支持独立Kelvin Source时记录限制执行；不修改65条冻结需求。未来四引脚Kelvin Source器件必须重新进行接口和adapter审核，不属于当前G1基线。

- DEC-019：Master于2026-08-26批准`G1-SYS-ARCH-v1.1`、`G1-ICD-v1.1`及`OI-012...017`的G1架构解决方案。G1阶段门状态为`PASS`；`docs/interfaces.md`成为G1逻辑接口唯一冻结基线，状态`FROZEN`；`OI-012...017`标记为`MASTER APPROVED / RESOLVED AT G1`。本批准不选择或冻结具体器件、数值、connector pinout、0 V/保护/Calibration Gate物理拓扑、原理图、PCB、BOM或制造文件。G2正式转为`ACTIVE`；G3继续`BLOCKED`直到G2通过。批准记录为`docs/G1_master_review_v1.0.md`。

## 尚未冻结的提案

- PROP-001：为Gate-to-`SREF`的0 V precondition提供独立功能路径，同时由Si8273负责P/N两级stress-to-measurement快速转换。具体clamp/switch实现未批准。
- PROP-002：PCB connector使用通用标签`VDDA`、`GNDA`、`SREF`，不使用固定电压标签。具体connector和pinout未批准。

## 决策状态规则

- `DEC-*`表示已批准基线。
- `PROP-*`表示提案，Codex不得将其视为冻结。
- 修改任何`DEC-*`必须经过Master批准，并同步进行接口与风险审核。
- DEC-011至DEC-013于2026-08-24由Master明确批准。
- DEC-014至DEC-016于2026-08-24的SP1 Master Review中批准。
- DEC-017于2026-08-25的G0 Master Review和规范基线安装中生效。
- DEC-018于2026-08-25的G1 Master返修指令中生效；它是项目范围说明，不是冻结需求变更。
- DEC-019于2026-08-26的G1 Master最终审核中生效；G1=`PASS`，G1接口基线=`FROZEN`，G2=`ACTIVE`，G3=`BLOCKED`。

