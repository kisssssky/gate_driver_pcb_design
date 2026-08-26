# G2电气计算 v1.0

- 日期：2026-08-26
- 状态：`G2 ACTIVE`；计算候选，未冻结，等待Master批准
- 计算脚本：`calculations/g2_calculations.py`
- 边界：不修改65条冻结需求或G1接口；不进入KiCad

## 1. 证据约定与计算输入

| 输入 | 数值 | 证据等级 | 来源/限制 |
|---|---:|---|---|
| Si8273 `ROH` | 2.7 Ω typ | DATASHEET FACT | Skyworks 206327E, Table 8, p.21 |
| Si8273 `ROL` | 1.0 Ω typ | DATASHEET FACT | 同上 |
| Si8273 peak source/sink | 1.8/4.0 A typ | DATASHEET FACT | 同上；15 V测试电路，脉宽<250 ns；不是保证的连续电流 |
| Si8273 propagation | 30 ns typ, 60 ns max | DATASHEET FACT | Table 8，`CL=200 pF`，low-jitter版本 |
| UCC27614 `ROH/ROL` | 2.5/0.34 Ω typ；4.5/0.55 Ω max | DATASHEET FACT | TI SLUSE26C, Table 6-5, p.5 |
| UCC27614 peak source/sink | 10/10 A typ | DATASHEET FACT | `VDD=12 V, CVDD=10 µF, CL=0.1 µF, 1 kHz`；非production test |
| UCC27614 propagation | 17.5 ns typ, 27 ns max | DATASHEET FACT | Table 6-6, `CL=1.8 nF, TJ=125°C` |
| 650 V DUT | `Qg=73 nC`, `Ciss=1370 pF`, `Rg,int=2 Ω` | DATASHEET FACT | ST DS12885 Rev 3, Table 4, p.3 |
| 3.3 kV代理 | `Qg=340 nC`, `Ciss=7302 pF`, `Rg,int=1.2 Ω` | DATASHEET FACT + ENGINEERING ASSUMPTION | G2R50MT33K Rev 23/Jul, p.2；转换为三端口代理不是datasheet事实 |
| Gate loop电阻 | 0.2 Ω nominal，0.1–0.5 Ω扫描 | ENGINEERING ASSUMPTION | 待G7布局与G11实测 |
| Gate loop电感 | 10 nH nominal，2–30 nH扫描 | ENGINEERING ASSUMPTION | 含PCB/adapter，不含三引脚封装公共Source电感 |
| 公共Source电感 | 5 nH nominal，1–20 nH扫描 | ENGINEERING ASSUMPTION | 两个DUT均无datasheet封装寄生数值 |

所有典型值只用于候选尺寸和仿真中心点；批准额定值必须使用max/min或实测包络。`Qg`和电容测试条件与本项目低`VDS`不同，不能互换为保证值。

## 2. Gate rail候选

| profile | 模式 | `VDDA-SREF` | `GNDA-SREF` | span | 状态 |
|---|---|---:|---:|---:|---|
| 650 V | Positive | +18 V | +4 V | 14 V | PROPOSED |
| 650 V | Negative | +4 V | −5 V | 9 V | PROPOSED |
| 3.3 kV代理 | Positive | +20 V | +3 V | 17 V | PROPOSED |
| 3.3 kV代理 | Negative | +3 V | −5 V | 8 V | PROPOSED |

- FROZEN G1 INTERFACE：Positive为`VIA HIGH→LOW`，Negative为`VIA LOW→HIGH`，上述电压保持这一极性。
- DATASHEET FACT：`Si8273AB-IS1`输出侧工作范围4.2–30 V；5 V UVLO正向阈值max 6.3 V。最小8 V span相对该阈值有1.7 V静态裕量。
- DATASHEET FACT：UCC27614工作4.5–26 V、UVLO正向max 4.4 V；四种span均兼容。
- ENGINEERING ASSUMPTION：`VGM-I/P/N`只是计算中心点。最终值由B1505曲线、目标`Ith`及DUT实测决定。
- 限制：650 V DUT推荐`VGS=-5…+18 V`；3.3 kV商业代理推荐−5/+20 V。rail容差、纹波与过冲均不得把DUT推过绝对最大值。

## 3. Gate drive计算

### 3.1 `Qg/t`必要条件

公式：

\[
I_{G,avg}=\frac{Q_g}{t_{target}}
\]

其中`Qg`为指定datasheet测试条件的总Gate电荷，`t_target=100 ns`。

| profile | `Qg` | `Qg/100 ns` | 结论 |
|---|---:|---:|---|
| 650 V | 73 nC | 0.73 A | 小于Si8273典型source/sink，但仍需RC、Miller和时序预算 |
| 3.3 kV代理 | 340 nC | 3.40 A | 大于Si8273 1.8 A典型source，接近4 A sink；仅直接驱动不能证明双向100 ns |

`Qg/t`只给出平均电流必要条件。高`VDS` datasheet `Qg`对低`VDS` BTI回路偏保守的程度未知；不得用此公式单独判定PASS。

### 3.2 峰值电流与外部`Rg`

一阶公式：

\[
I_{pk}=\min\left(\frac{|V_H-V_L|}{R_{out}+R_{g,ext}+R_{g,int}+R_{loop}},I_{driver,pk}\right)
\]

候选采用Si8273后接同一浮动rail域的`UCC27614DR`非反相buffer。`VOA`仍是冻结的快速状态选择信号；buffer只提高电流，未改变P/N真值表。

| profile/转换 | 方向 | `Rg,ext` | `Rtotal` typ | `Ipk` typ | `2.2RtotalCiss` |
|---|---|---:|---:|---:|---:|
| 650 V Positive stress→measurement | sink | 1.0 Ω | 3.54 Ω | 3.96 A | 10.7 ns |
| 650 V Negative stress→measurement | source | 1.0 Ω | 5.70 Ω | 1.58 A | 17.2 ns |
| 3.3 kV代理 Positive stress→measurement | sink | 0.5 Ω | 2.24 Ω | 7.59 A | 36.0 ns |
| 3.3 kV代理 Negative stress→measurement | source | 0.5 Ω | 4.40 Ω | 1.82 A | 70.7 ns |

数值来源：脚本输出；`Rloop=0.2 Ω`。裕量与限制：

- UCC27614 10 A为典型、特定测试条件且非production test；不能把表中峰值当保证值。
- UCC27614 `ROH` max为4.5 Ω；3.3 kV代理Negative在max `ROH`下RC会显著变慢。
- `Rg`提议绑定adapter/profile：650 V nominal 1.0 Ω，扫描0.5/1/2.2/4.7/10 Ω；3.3 kV代理nominal 0.5 Ω，扫描0.22/0.5/1/2.2/4.7 Ω。PROPOSED，Master批准前不发布BOM。
- 同一profile内P/N不更换`Rg`；切换profile允许更换已批准adapter和其`Rg`，符合PROJECT REQUIREMENT。

### 3.3 寄生电感与过冲

公式：

\[
V_L=L\frac{\Delta I}{\Delta t}
\]

以`Lgate=10 nH`、电流10 ns建立估算，四个候选分别约3.95、1.58、7.59、1.82 V。该结果显示3.3 kV sink路径即使低`VDS`也可能因Gate loop产生明显ringing；不是允许过冲。控制措施：短loop、adapter局部`Rg`、Gate-to-rail低电感Schottky clamp候选、分离source/sink阻值预留、示波器验证。

公共Source电感产生：

\[
V_{S,bounce}=L_{CS}\frac{dI_D}{dt}
\]

它同时改变真实`VGS`和测得`VGS`。三引脚封装无法在PCB上消除该项；参数扫描1–20 nH并在G11同步测`VGS/VDS`。

### 3.4 driver功耗与温升

每周期近似Gate能量：

\[
E_g\approx Q_g\Delta V,\quad P_g\approx Q_g\Delta V f_{rep}
\]

1 kHz示例：650 V、14 V为1.02 mW；3.3 kV代理、17 V为5.78 mW。加静态电流后，Si8273输出侧无负载active电流max 11 mA；UCC27614静态max约1 mA。最坏温升：

\[
\Delta T_J\le P_{IC}\theta_{JA}
\]

Si8273 NB-SOIC16 `θJA=104 °C/W`；UCC27614 SOIC8 `θJA=126.4 °C/W`。重复率未知，故只提供参数化公式；G10以壳温/环境温度确认。不得把1 kHz示例当实验设定。

## 4. 去耦计算

每次转换本地电容至少供给`Q`：

\[
C_{ideal}\ge\frac{Q}{\Delta V};\qquad C_{design}=M\frac{Q}{\Delta V}
\]

取允许droop 0.5 V、裕量`M=2`：650 V需0.292 µF；3.3 kV代理需1.36 µF。PROPOSED每个浮动rail span在Si8273和buffer处各放：

- 100 nF C0G/X7R高频；
- 2.2 µF有效容量不低于1.5 µF的X7R中频；
- 10 µF低ESR本地bulk；
- 电压额定≥35 V，工作温度≥105 °C；MLCC按实际DC bias曲线保证有效容量。

Skyworks Figure 24给出输出侧0.1 µF+10 µF、输入侧0.1 µF+1 µF示例；TI要求UCC27614一般≥1 µF+0.1 µF。`2.2 µF+10 µF`满足电荷估算且保留DC-bias余量。ESR droop与ESL尖峰：

\[
\Delta V\approx\frac{Q}{C}+I_{pk}ESR+ESL\frac{dI}{dt}
\]

因此bulk容量不能补偿远距离/高ESL；100 nF和2.2 µF必须直接闭合`VDD-buffer-GND`回路。每rail平均Gate电流为`Iavg=Nedge Qg frep`；1 kHz两边沿分别0.146 mA和0.680 mA，仅用于电源平均电流下限。

## 5. `VDC/RL`与能量

FROZEN G1 INTERFACE：漏极回路为`VDC→RL→Drain→DUT_SOURCE/SOURCE_STAR→DRET→return`，且平台只施加低`VDS`。

\[
I_{DS}=\frac{V_{DC}-V_{DS}}{R_L}
\]

\[
P_{R,pulse}=I_{DS}^2R_L,\quad E_R=P_{R,pulse}t_p,\quad P_{R,avg}=E_R f_{rep}
\]

\[
E_{fault,max}\le V_{DC}I_{limit}t_{clear}+\frac12C_{bus}V_{DC}^2
\]

`VDC=10 V, VDS=2 V, RL=100 Ω`仅作复算示例：`IDS=80 mA`；1 µs时电源能量上界0.8 µJ。正式选择流程：

1. 由B1505固定`VDS-C`曲线选`Ith`和MI/MP/MN目标区间；
2. 选择`VDC`，使测量窗口内`VDS≈VDS-C`且不接近额定阻断电压；
3. 对`Vth min/max`、温度与`RDS(on)`扫描求`RL`；
4. 以电源限流、串联RL、NO drain relay和bleeder共同限制fault能量；
5. 校验电阻脉冲额定、寄生电感与自热。

电阻寄生条件：若希望RL电流在10 ns内建立，`L_R/R_L << 10 ns`；即`L_R << 10 ns·RL`。例如100 Ω时上限量级1 µH，仍需以器件脉冲模型和实测替代经验判断。

650 V与3.3 kV差异：本平台VDC都低，但3.3 kV代理Gate电容更大、封装公共Source寄生未知，导致同一`RL/VDC`的`VDS`到达时间和自热不同。不得用额定电压比例放大VDC。

## 6. 完整时序预算

从Pulse Generator命令到可解释`VDS`点：

\[
t_{sys}=t_{PG}+t_{Si8273}+t_{buffer}+t_{gate}+t_{DUT}+t_{VDS}+t_{probe}+t_{scope}+t_{extract}
\]

| 项 | nominal | worst-case/不确定性 | 证据等级 |
|---|---:|---:|---|
| Pulse Generator延迟/jitter | 未计入绝对延迟；jitter待资格 | OPEN / NOT VERIFIED | USER CONFIRMATION REQUIRED |
| Si8273 propagation | 30 ns | 60 ns | DATASHEET FACT |
| UCC27614 propagation | 17.5 ns | 27 ns | DATASHEET FACT |
| Si8273 rise/fall | 不作为Gate功率边沿 | 其VOA必须跨过buffer阈值 | DATASHEET FACT + CALCULATION |
| DUT Gate 10–90% | 10.7–70.7 ns typ中心 | R/C/Qg/温度/寄生扫描 | CALCULATION |
| DUT导电与VDS响应 | 未验证 | 取决于`Vth`, `RL`, `Coss`, source bounce | OPEN / NOT VERIFIED |
| 探头传播延迟/通道skew | deskew后目标≤2 ns | 型号未知 | USER CONFIRMATION REQUIRED |
| trigger/jitter | 预算1 ns示例 | 实测替代 | ENGINEERING ASSUMPTION |
| 数据提取 | 预留5–10 ns稳定窗 | 算法待G11/G12 | ENGINEERING ASSUMPTION |

固定传播项nominal为47.5 ns，worst-case为87 ns；尚未包含Gate、DUT、VDS和测量链。因此：

- 650 V nominal有希望在约100 ns形成有效点，但无worst-case证据。
- 3.3 kV代理Negative的Ciss一阶70.7 ns，加固定nominal即118.2 ns；低`VDS`有效Gate电荷可能较小，但未经LTspice实跑和实测，不得宣告满足。
- 结论：约100 ns为设计目标，G2尚不能证明两个profile的worst-case满足；必须保留G10/G11验收。

示例独立时间误差按RSS：

\[
u_t=\sqrt{u_{PG}^2+u_{iso}^2+u_{probe}^2+u_{skew}^2+u_{extract}^2}
\]

用1、0.2、1、2、3 ns得3.88 ns。真实值必须从仪器手册、校准和重复采集替换。

## 7. 测量链反推

示波器与探头组合上升时间：

\[
t_{r,meas}\approx\sqrt{t_{r,signal}^2+t_{r,scope}^2+t_{r,probe}^2},\quad BW\approx\frac{0.35}{t_r}
\]

为使测量链上升时间不超过被测边沿的1/5，保守取`BWmin=5×0.35/tr_signal`；每边沿20点取`Fsmin=20/tr_signal`。

| 假定最短边沿 | 组合带宽下限 | 采样率下限 |
|---:|---:|---:|
| 10 ns | 175 MHz | 2.0 GSa/s |
| 20 ns | 87.5 MHz | 1.0 GSa/s |

2.5 GSa/s只满足10 ns边沿的采样点数下限，不能证明示波器模拟带宽、探头带宽或共模性能。候选采购/资格要求：

- scope模拟带宽≥200 MHz，采样≥2.5 GSa/s同时采集至少VIA/VGS/VDS；
- memory：`N≥Fs·Trecord`。若记录10 ms且2.5 GSa/s，需要25 Mpoints/active channel；
- 有效垂直分辨率：在所选range、带宽限制和averaging设置下，Gate误差目标≤50 mV或`VGS`跨度的1%，取更严者；
- VGS差分探头：≥200 MHz，小于约2 pF differential input capacitance为资格目标；范围覆盖−10…+25 V并留过冲裕量；
- VDS探头：尽管VDS低，输入共模和差分范围必须覆盖实际浮地；≥200 MHz；
- 通道deskew residual目标≤2 ns；每次换探头/电缆重做deskew与零点；
- 所有探头负端不得建立`SREF-earth`路径。USB/LAN、机壳和电源PE在G10接线审核中逐项检查。

这些是CALCULATION派生的最低性能，不是对任何未提供仪器型号的MANUFACTURER FACT。

## 8. 计算结论与边界

- CALCULATION：Si8273直接驱动3.3 kV代理的source方向电流裕量不足；PROPOSED增加`UCC27614DR`同域buffer。
- CALCULATION：本地有效去耦至少1.36 µF（3.3 kV代理、0.5 V droop、2×裕量），拟用0.1+2.2+10 µF分层。
- CALCULATION：650 V nominal接近约100 ns目标；3.3 kV代理worst-case没有证据。
- OPEN / NOT VERIFIED：实际非商业3.3 kV DUT的Gate charge、封装公共Source阻抗与温度特性。
- USER CONFIRMATION REQUIRED：B1505曲线确定`VGM-I/P/N`、MI/MP/MN、VDC/RL；本地LTspice运行；实物仪器资格。
- MASTER DECISION REQUIRED：rail中心值、buffer、relay路径、各profile `Rg`与保护策略。
