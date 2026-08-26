# G2器件选型与电路计算报告 v1.0

- 项目：SiC MOSFET BTI Fast Gate Driver PCB / Fig. 3 Reproduction
- 日期：2026-08-26
- 状态：`G2 ACTIVE`；`G3 BLOCKED`
- 需求基线：65条`REQ-SYS-*`，`FROZEN`
- G1接口基线：25条接口，`FROZEN`
- 本文件：G2候选，不表示Master批准或冻结

## 1. 基线完整性检查

| 检查 | 结果 | 证据等级 |
|---|---|---|
| canonical `REQ-SYS-*` | 65个唯一ID；verification 65/65 | PROJECT REQUIREMENT |
| G1接口基线 | `FROZEN` | FROZEN G1 INTERFACE |
| DUT物理边界 | Gate/Drain/Source三个物理引脚 | FROZEN G1 INTERFACE |
| Source关系 | `SREF`与`DRET`只在`DUT_SOURCE/SOURCE_STAR`汇合 | FROZEN G1 INTERFACE |
| Calibration接口 | `IF-GATE-01 / CAL_GATE_TARGET`已冻结 | FROZEN G1 INTERFACE |
| G3 | `BLOCKED` | PROJECT REQUIREMENT |

未发现需要改变冻结接口的技术矛盾。旧文件头部的历史状态按版本时点保留；当前权威状态以`G1_master_review_v1.0.md`、`DEC-019`和项目状态文件为准。结论：无需`BASELINE_CHANGE_REQUIRED`。

## 2. G2输入完整性清单

### 2.1 已有输入

| 类别 | 输入 | 处理 |
|---|---|---|
| 650 V DUT | `SCTW35N65G2VAG`，用户确认手头已有 | 建立实际器件profile |
| 3.3 kV DUT | 非商业/无公开datasheet，性能接近GeneSiC第二代 | 建立三引脚工程代理profile，不伪装为实物datasheet |
| Si8273 | 已购买但无法获得完整后缀照片 | 用户授权选择典型完整料号；提议`Si8273AB-IS1` |
| 示波器 | 2.5 GSa/s量级常规实验室设备 | 只反推最低要求；型号资格留G10/G11 |
| Pulse Generator/探头/电源 | 用户明确不要求G2管理具体型号 | 不假设型号；输出接口和安全资格清单 |
| B1505A | 主机、N1265A、10 kV UHCU背景已知；配置不完整 | 只定义其需完成的曲线/参数，不猜模块 |
| LTspice | 尚未安装；用户将安装 | 交付可运行文本工程；不得报告仿真通过 |

### 2.2 USER INPUT REQUIRED（集中保留）

以下已经压缩为仅能由用户完成的任务，不阻止工程文档和仿真工程准备：

1. 在本地Windows安装LTspice并按README运行全部case，回传`.log`、关键波形截图及版本号。
2. 以B1505实际曲线确认每个DUT的`VGM-I/P/N`、`Ith`、MI/MP/MN目标、温度点与`VDS-C`。
3. 在G10/G11按本报告最低要求确认示波器、VGS/VDS探头、电源浮地和接地拓扑。
4. 实际非商业3.3 kV DUT可用时记录完整内部编号、三引脚pin定义和实测Gate charge/公共Source寄生包络。

## 3. 官方证据目录

不提交datasheet PDF或受限模型，只记录链接和定位。

| 器件 | 官方资料 | 版本/日期 | 关键页 |
|---|---|---|---|
| Si827x | https://www.skyworksinc.com/-/media/SkyWorks/SL/documents/public/data-sheets/Si827x.pdf | 206327E, 2026-01-23 | pp.3, 11–13, 18, 20–29, 41 |
| SCTW35N65G2VAG | https://www.st.com/resource/en/datasheet/sctw35n65g2vag.pdf | DS12885 Rev 3, 2020-09 | pp.1–3, 5–6, 8–10 |
| SCTW产品页 | https://www.st.com/en/power-transistors/sctw35n65g2vag.html | 在线状态 | obsolete/out of production，需供应风险管理 |
| G2R50MT33K | datasheet内官方最新链接：`https://www.genesicsemi.com/sic-mosfet/G2R50MT33K/G2R50MT33K.pdf` | Rev 23/Jul | pp.1–3, 6–7, 9–14；官方站本次自动访问失败，使用制造商原版镜像核读 |
| G2R50MT33K model | `https://www.genesicsemi.com/sic-mosfet/G2R50MT33K/G2R50MT33K_SPICE.zip` | datasheet p.14列出 | MANUFACTURER MODEL FACT：链接存在；未下载、未验证许可/兼容性 |
| UCC27614 | https://www.ti.com/lit/ds/symlink/ucc27614.pdf | SLUSE26C, 2022-01 | pp.1, 3–6, 25–26 |
| IM03GR relay | https://www.te.com/en/product-1-1462037-4.html | active product page | exact TE PN `1-1462037-4`；datasheet `108-98001 Rev 4` pp.1–4 |
| LTspice | https://www.analog.com/en/resources/design-tools-and-calculators/ltspice-simulator.html | 官方下载页 | 本地版本待用户记录 |

## 4. 器件选型表

| 功能 | 完整料号/标识 | 状态 | 依据与用途 |
|---|---|---|---|
| 隔离快速命令 | `Si8273AB-IS1` | PROPOSED | 5 V UVLO、low-jitter、无deglitch、SOIC-16 NB、2.5 kVrms；Channel A/VOA |
| 同域Gate buffer | `UCC27614DR`，SOIC-8 | PROPOSED | 4.5–26 V、10 A typ source/sink、27 ns max propagation；由VOA非反相驱动 |
| 650 V DUT | `SCTW35N65G2VAG` | USER-PROVIDED / PROFILED | 三引脚HiP247，实际已有；生命周期obsolete |
| 3.3 kV代理 | `DUT-PROXY-3K3-G2R50MT33K-3P-v0.1` | ENGINEERING PROXY | 只借用G2R50MT33K die级电气参数；外部强制三端口，共Source寄生单独扫描 |
| Gate路径relay | `IM03GR`, TE `1-1462037-4` | PROPOSED | 5 V monostable 2 Form C；失电返回NC；接点<50 mΩ初始，1 ms typ/3 ms max |
| Gate-to-rail clamp | 双向至`VDDA/GNDA`的低电感Schottky位置 | PROPOSED / exact diode OPEN | 需要在选定寄生扫描后按峰值电流和电容定料，不能先猜TVS钳位 |
| drain隔离 | NO relay + bench supply remote inhibit + bleed | PROPOSED / rating由`Ilimit`决定 | 失电断开VDC并释放能量；不属于100 ns路径 |

`UCC27614DR` pin依据TI p.3 SOIC top view：1/8=`VDD`，2=`IN`，3=`EN`，4/5=`GND`，6/7=`OUT`。Si8273 pin见第5节。Relay pin编号在G3必须逐pin使用TE product drawing `1462037-2 Rev A10`，本报告不转录图形以避免方向错误。

## 5. Si8273完整datasheet审查

### 5.1 料号、封装和pin

- DATASHEET FACT：`Si8273AB-IS1`，Si8273 HS/LS overlap-protected配置；`A`=5 V UVLO，`B`=2.5 kVrms，`-I`=industrial，`S1`=NB SOIC-16；无`D`表示无integrated deglitch、low-jitter。Ordering Guide p.41。
- DATASHEET FACT：NB SOIC-16 pin：1 VIA，2 VIB，3/8 VDDI，4 GNDI，5 EN，6/7/12/13 NC，9 GNDB，10 VOB，11 VDDB，14 GNDA，15 VOA，16 VDDA。Table 2 p.3。
- PROPOSED：Channel A作冻结快速路径；Channel B不使用，VIB经10 kΩ固定LOW；`VDDB=VDDA`、`GNDB=GNDA`并在B引脚旁独立0.1 µF+2.2 µF去耦，VOB不连接。这样B输出处于已供电的确定LOW，而非悬空/欠压状态。NC保持NC。

### 5.2 供电、逻辑和真值表

| 项 | datasheet事实 | 设计采用 |
|---|---|---|
| VDDI | 2.5–5.5 V | 3.3或5 V逻辑，G3选定 |
| VDDA/GNDA span | 4.2–30 V | 8–17 V候选span |
| logic | `VIH≥2.0 V`, `VIL≤0.8 V`, hysteresis≥350 mV | Pulse Generator必须满足 |
| EN | LOW时VOA/VOB LOW | 用作一级异步inhibit；不是唯一SAFE_OFF |
| Si8273 A truth | VIA L/VIB L→A/B L；H/L→A H/B L；H/H→both L invalid | VIB固定LOW，VIA控制A |
| input-side失电 | 输出LOW；恢复输入状态最长7 µs说明 | fail-safe链仍需relay NC clamp |
| output-side UVLO | 输出LOW | rail失效时不会维持stress high，但LOW可能等于负stress rail，故不能单独当SAFE_OFF |

### 5.3 驱动、时序、UVLO

| 参数 | 保证/典型 | 条件/页码 | 采用方式 |
|---|---|---|---|
| `ROH/ROL` | 2.7/1.0 Ω typ | Table 8 p.21 | 典型计算和范围扫描 |
| peak source/sink | 1.8/4.0 A typ | 15 V test circuit；<250 ns | 不作为保证值；3.3 kV需要buffer候选 |
| propagation | 20 min/30 typ/60 max ns | low-jitter, CL=200 pF | nominal/worst timing |
| rise/fall | 4/10.5/16 ns；5.5/13.3/18 ns | CL=200 pF | VOA节点，不等于DUT边沿 |
| PWD | 3.6 typ/8 max ns | Si8271/3/5 | uncertainty预算 |
| jitter | 200 ps p-p typ | low-jitter | uncertainty预算，不是系统jitter |
| min pulse | 30 ns typ | Table 8 | 控制脉冲下限 |
| startup | 16 typ/30 max µs | p.23 | rail valid后等待≥30 µs再arm |
| shutdown/restart via EN | max 60/60 ns | p.23 | 与relay去能量链共同使用 |
| 5 V UVLO+ | 4.9/5.5/6.3 V | p.21 | span必须高于6.3 V并有裕量 |
| 5 V UVLO− | 4.6/5.2/5.9 V | p.21 | rail falling检测 |

### 5.4 CMTI、绝缘、温度和保护边界

- DATASHEET FACT：low-jitter CMTI min 150 kV/µs、typ 300、max列400，`VCM=1500 V`；首页营销摘要200 kV/µs不能替代表格min。
- DATASHEET FACT：UL1577 2500 Vrms/1 min；IEC60747-17 `VIOWM=445 Vrms`, `VIORM=630 Vpeak`, `VIOTM=3535 Vpeak`；只是basic insulation。
- DATASHEET FACT：NB-SOIC16 nominal clearance/creepage 3.9/3.9 mm；VDE说明>4.7 mm。器件额定不自动成为PCB clearance规则。
- DATASHEET FACT：工业OPN `TA=-40…125°C`，`TJ max=150°C`，NB-SOIC16 `θJA=104°C/W`。
- OPEN / NOT VERIFIED：datasheet未给输出短路/主动过流保护保证；不得依赖内部限流。外部`Rg`、rail限流和fault shutdown必需。

### 5.5 去耦、悬空与模型

- DATASHEET FACT：每个VDD/GND供电单独去耦并尽量贴近；Figure 24示例输入1 µF+0.1 µF、输出10 µF+0.1 µF。
- DATASHEET FACT：VDDI不存在而VDDx存在时输出默认LOW；输入可能通过内部二极管反向供电，control loss要把VIA/VIB钳为LOW而非悬空。
- PROPOSED：VIB=10 kΩ到GNDI；EN=10 kΩ到GNDI且由许可逻辑主动拉高；NC不连接。
- OPEN / NOT VERIFIED：Skyworks官方页面未找到Si8273可下载SPICE macromodel。LTspice采用人工行为模型，只做架构/敏感性分析。

## 6. DUT profile

### 6.1 `DUT-650-SCTW35N65G2VAG-v1.0`

| 项 | 值 | 证据 |
|---|---|---|
| 制造商/完整型号 | STMicroelectronics `SCTW35N65G2VAG` | USER CONFIRMATION + DATASHEET FACT |
| 封装/pin | HiP247；1 Gate，2 Drain/TAB，3 Source | DATASHEET FACT, p.1 |
| `VDS` | 650 V | DATASHEET FACT |
| `VGS` | abs −10…+22 V；recommended −5…+18 V | DATASHEET FACT, Table 1 p.2 |
| `VGS(th)` | 1.8 min/3.2 typ/5 max V | `VDS=VGS, ID=1 mA`, Table 3 p.3 |
| `Qg/Qgs/Qgd` | 73/14/27 nC typ | `VDD=400 V, ID=20 A, VGS 0→20 V` |
| `Ciss/Coss/Crss` | 1370/125/30 pF typ | `VGS=0, VDS=400 V, 1 MHz` |
| internal `Rg` | 2 Ω typ | `1 MHz, ID=0` |
| `RDS(on)` | 55 mΩ typ at18 V；45 typ/67 max mΩ at20 V | `ID=20 A, 25°C` |
| current | 45 A cont at25°C；90 A pulse，受SOA限制 | DATASHEET FACT |
| thermal/TJ | `RθJC=0.72°C/W`, `RθJA=40°C/W`, `TJ max=200°C` | Tables 1–2 |
| common Source | 三引脚，共用Source引线；数值未给 | DATASHEET FACT + OPEN / NOT VERIFIED |
| 生命周期 | obsolete/out of production | MANUFACTURER PAGE FACT |

缺失项验证：Gate/Source及Drain/Source阻抗用fixture open/short和TDR/VNA或脉冲ringing拟合；实际`Qg`用恒流Gate充电；公共Source影响用同步`VGS/VDS`及重复性验证。

### 6.2 `DUT-PROXY-3K3-G2R50MT33K-3P-v0.1`

| 项 | 商业参考事实 | 三引脚代理处理 |
|---|---|---|
| 制造商/参考型号 | GeneSiC/Navitas `G2R50MT33K` | 只作为电气参数来源，不是计划装板完整型号 |
| 商业封装 | TO-247-4：D/G/S/KS，单独driver source | 外部只暴露G/D/S；KS与S在代理内部合并 |
| `VDS` | 3300 V | 平台仍只用低VDS |
| `VGS` | dynamic abs −10/+25 V；recommended −5/+20 V | rail候选按−5/+20限制 |
| `VGS(th)` | 2.0 min/3.5 max V | `VDS=VGS, ID=10 mA` |
| `Qg/Qgs/Qgd` | 340/120/100 nC | `VDS=1000 V, ID=40 A, −5/+20 V` |
| `Ciss/Coss/Crss` | 7302/131/12.3 pF | `VDS=1000 V, VGS=0, 1 MHz, 25 mV` |
| internal `Rg` | 1.2 Ω | `1 MHz, 25 mV` |
| `RDS(on)` | 50 mΩ typ at20 V/40 A/25°C；91 mΩ at150°C | 代理中心值 |
| current/thermal | 72 A at25°C，46 A at100°C；235 A pulse≤3 µs/D≤1%；`RθJC=0.24°C/W`；datasheet abs `TJ max=150°C` | 不外推至实际非商业DUT |
| common Source | 商业件通过KS减轻；三引脚代理故意移除KS | `RCS/LCS`单独扫描1–20 nH，风险上调 |

证据边界：上述数值为DATASHEET FACT；“合并KS/S并形成三引脚代理”为ENGINEERING ASSUMPTION；实际项目3.3 kV器件所有参数为OPEN / NOT VERIFIED。仿真只能说明架构对大Gate负载和公共Source寄生的敏感性。

## 7. 650 V与3.3 kV兼容性对比

| 项 | 通用架构 | 650 V | 3.3 kV代理 |
|---|---|---|---|
| DUT物理接口 | G/D/S三引脚；`SREF/DRET`只在Source star汇合 | HiP247 adapter | 非商业三引脚adapter；不照搬TO-247-4 |
| fast path | Si8273 A/VOA→同域buffer→profile `Rg` | `Rg` nominal 1 Ω PROPOSED | `Rg` nominal 0.5 Ω PROPOSED；更高ringing风险 |
| rail | 外部浮地，按profile接VDDA/GNDA | +18/+4或+4/−5 | +20/+3或+3/−5 |
| Gate负载 | 同一Base PCB | 73 nC/1.37 nF | 340 nC/7.302 nF代理 |
| `VDC/RL` | 同一低VDS受限能量架构 | B1505曲线选值 | 独立B1505曲线选值；不得按额定电压缩放 |
| probe | 同一最低带宽/deskew流程 | 范围覆盖−10…+22 V | 覆盖−10…+25 V；更强source bounce |
| adapter差异 | profile ID与interlock | HiP247 3-pin pinout | 项目器件真实机械/pin待用户 |
| 缺失证据 | G10/G11寄生实测 | package source L/R | 实际DUT全部动态/热/Source寄生 |

## 8. G2候选拓扑决定

所有编号均为`PROP-*`，不是批准的`DEC-*`。

| ID/事项 | 候选比较 | 推荐与故障处理 | 状态 |
|---|---|---|---|
| PROP-G2-001 0 V PRECONDITION | MOSFET开关快但失电状态和双向压差复杂；PhotoMOS泄漏/导通阻抗；monostable relay慢但浮动、低泄漏、可NC | `IM03GR` K_SAFE NC把Gate经`RSAFE`接SREF；PRECONDITION用同一物理目标但独立逻辑状态 | PROPOSED |
| PROP-G2-002 `CAL_GATE_TARGET` | 高压analog mux快但寄生/供电复杂；relay慢但Calibration不在100 ns关键路径 | 第二个relay K_SEL在K_SAFE隔离Gate时选择VGM-I或FAST；VGM-I由外部浮动精密源相对SREF提供 | PROPOSED |
| PROP-G2-003 SAFE_OFF | 仅EN LOW会把VOA拉到GNDA，Negative模式可能等于负stress；不足 | 去能时K_SAFE物理返回NC Gate→SREF，drain relay掉电；fault latch阻止自动重启 | PROPOSED |
| PROP-G2-004 break-before-make | 软件deadtime单点失效；analog mux BBM依型号；relay changeover机械互斥但有bounce | 两级relay：先K_SAFE回NC隔离，等待≥5 ms，再切K_SEL，等待≥5 ms，再释放K_SAFE；contact feedback/电压valid双确认 | PROPOSED |
| PROP-G2-005 rail enable | 只关bench supply可能慢；板载开关需额定/反灌设计 | 外部供电remote enable + 低电流series limit + bleeder；rail-valid窗口比较；不合格即K_SAFE | PROPOSED |
| PROP-G2-006 control loss/UVLO | 只依Si8273输出LOW不安全 | EN/VIA/VIB硬件下拉；watchdog丢失→K_SAFE掉电；UVLO任一侧→数据invalid、drain off、fault latch | PROPOSED |
| PROP-G2-007 drain能量 | 仅software enable无法隔离；固态开关快但漏电 | supply remote inhibit + NO drain relay + series RL + bleed；断开顺序先drain后Gate safe保持 | PROPOSED |
| PROP-G2-008 Gate保护 | 单一G-S TVS难同时容纳+20/−5；rail clamp更符合不对称rails | 预留Gate→VDDA与GNDA的低L Schottky位置、series Rg、rail current limit；确切二极管在LTspice/台架峰值后定 | PROPOSED / exact diode OPEN |
| PROP-G2-009 `Rg`绑定 | Base固定无法适配负载；可调电阻寄生/误设 | `Rg`装在DUT adapter并由profile ID检查；同profile P/N不变 | PROPOSED |
| PROP-G2-010 浮地 | 非隔离bench supply可能经PE/USB闭合 | 每个Gate rail输出必须浮地；GNDI/GNDA/SREF/earth无隐式连接；上电前绝缘检查 | PROPOSED |
| PROP-G2-011 unused B | 浮空输入或未定义输出供电危险；完整供电增加少量去耦 | VIB/EN各10 kΩ下拉；`VDDB=VDDA`、`GNDB=GNDA`；B侧独立0.1+2.2 µF；VOB不连接 | PROPOSED |
| PROP-G2-012 power sequence | 同时上电有争用；顺序化可验证 | 见下表；任一步valid失败即回SAFE_OFF且不得自动重启 | PROPOSED |

速度/寄生/器件数权衡：relay只在试验状态间切换，不参加stress→measurement纳秒边沿；FAST状态内K_SAFE/K_SEL保持静态，Si8273+buffer完成边沿。新增buffer和两个relay增加器件数，但将大Gate负载、失电安全与路径互斥从软件假设变为可测试硬件。

### 8.1 具体上电/掉电顺序

上电：

1. K_SAFE失电NC、drain NO断开、rail disabled。
2. 上VDDI；确认VIA/VIB/EN LOW。
3. 建立当前profile浮动rails；等待Si8273 `tSTART max=30 µs`外加1 ms验证窗。
4. 选择K_SEL目标，K_SAFE仍NC；等待relay max操作/回跳共10 ms裕量。
5. PRECONDITION保持Gate=0 V并验证。
6. enable drain，验证`VDS=VDC`后才起算`tpre`。
7. 到达stress前先disable drain（若实验序列要求），按状态表释放K_SAFE进入FAST；P/N在FAST内只由VIA切换。

正常掉电/故障：

1. 立即撤销data-valid并禁止新stress。
2. 断开drain remote enable和NO relay；等待`VDS`低于安全阈值。
3. EN LOW；K_SAFE掉电返回Gate→SREF。
4. 关闭浮动rails并由bleeder放电；最后关闭VDDI。
5. fault latch保持，必须显式reset/re-arm。

## 9. 电气计算摘要

完整公式、来源、worst case和限制见`calculations/G2_electrical_calculations_v1.0.md`。核心结果：

- CALCULATION：`Qg/100 ns`为0.73 A（650 V）和3.40 A（3.3 kV代理）。
- CALCULATION：提出`UCC27614DR`buffer，否则Si8273 source 1.8 A typ不能覆盖大Gate代理双向速度。
- CALCULATION：0.5 V droop、2×裕量时本地有效C至少0.292/1.36 µF；每rail拟用0.1+2.2+10 µF。
- CALCULATION：固定传播nominal 47.5 ns、worst 87 ns，未含Gate/DUT/VDS/探头；约100 ns worst-case尚未证明。
- CALCULATION：10 ns边沿最低组合带宽175 MHz、采样2.0 GSa/s；2.5 GSa/s本身不能证明模拟带宽。
- OPEN / NOT VERIFIED：正式VDC/RL必须由B1505 `IDS-VGS`、`Ith`和目标MI/MP/MN确定。

## 10. 模型与LTspice边界

- MANUFACTURER MODEL FACT：GeneSiC datasheet列出G2R50MT33K SPICE zip URL；文件未取得/未确认再分发许可。
- OPEN / NOT VERIFIED：未找到Si8273官方SPICE model；未把搜索结果或相似型号冒充官方模型。
- 人工模型：Si8273延迟/输出R、buffer延迟/输出R、Gate C/Q范围、Coss/Crss、Gate/source寄生、relay状态和VDC/RL均为可扫描行为模型。
- LTSPICE RESULT：无。用户尚未本地运行，没有`.raw`、截图或log，因此N–Q相关评审不得PASS。

## 11. 风险变化

新增/上调：

- 3.3 kV实际DUT与商业代理不一致，尤其KS合并后的公共Source寄生。
- ST 650 V DUT已obsolete，备件/批次一致性风险。
- 约100 ns指标在3.3 kV代理worst-case无证据。
- relay触点bounce/寿命和切换等待时间需状态机强制。
- Gate-to-rail保护二极管确切料号需以模拟/台架峰值和电容选定。

缓解：参数扫描、adapter profile绑定、硬件NC SAFE_OFF、NO drain切断、同域高电流buffer、分层去耦和G10/G11同步验证。无风险退休。

## 12. G2边界结论

工程侧已把器件、公式、候选拓扑和可运行仿真输入落盘；但没有本地LTspice真实结果、实际3.3 kV器件证据或Master批准。故：

`G2 ACTIVE — NOT READY FOR MASTER REVIEW`

`G3 BLOCKED`
