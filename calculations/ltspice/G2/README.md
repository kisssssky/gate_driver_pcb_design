# G2 LTspice运行包

状态：`INPUT DECK READY / NOT RUN`。本目录没有真实`.raw`、截图或LTspice log，不能标记`LTSPICE RESULT`或“仿真通过”。

## 模型边界

- `G2_fast_bti_parametric.cir`：Si8273、可选buffer、DUT和寄生均为人工行为/简化等效模型。
- `G2_gate_states_faults.cir`：relay、interlock、UVLO/control loss为人工状态模型。
- `G2_vdc_rl_faults.cir`：DUT channel为电压控制开关，fault为人工短路。
- 未包含Skyworks官方Si8273模型；未把G2R50MT33K官方模型复制进仓库；无模型时的结论只限架构和敏感性。

## 本地运行

1. 从Analog Devices官方下载并安装LTspice；记录版本。
2. 分别打开三个`.cir`，点击Run。
3. 第一次只保留文件内已启用的`.step`；确认收敛后逐项取消带`*`的扫描指令，每次只增加一组扫描。
4. 保存`.log`；截图必须显示trace名、时间轴、step参数和游标。
5. 大型`.raw`不提交；筛选后的关键数据可导出CSV并压缩。

## 14项覆盖矩阵

| 要求case | 输入文件/设置 | 必看波形/状态 |
|---|---|---|
| Positive stress→measurement | fast，`POL=1` | `V(VIA)`, `V(VOA)`, `V(VO_RAW,SREF)`, `V(GATE,SRCINT)`, `V(DRAIN,SRCINT)`, `I(VIG)`, `I(BHI)`, `I(BLO)`, `I(VVDC)` |
| Negative stress→measurement | fast，`POL=0` | 同上 |
| 0 V PRECONDITION | states，`SCEN=5` | `V(GATE,SREF)`, `V(DREN)` |
| Calibration PRE→VGM-I | states，`SCEN=6`后`SCEN=0` | `V(CCAL)`, `V(GATE,SREF)` |
| SAFE_OFF | states，`SCEN=7` | `V(CSAFE)`, `V(GATE,SREF)`, `V(DREN)` |
| 正常上电/掉电 | states，`SCEN=0` | 全部enable/path状态 |
| control loss | states，`SCEN=1` | `V(VALID)`, `V(GATE,SREF)`, `V(DREN)` |
| UVLO | states，`SCEN=2` | 同上；将事件阈值改为实测值复跑 |
| rail失效 | states，`SCEN=3` | 同上与`V(VOA,SREF)` |
| Gate路径争用 | states，`SCEN=4` | `V(CCAL)`, `V(CFAST)`, path currents；此case应被interlock判fault，不是可接受状态 |
| VDC/RL正常 | drain，`FAULT=0` | `V(DRAIN)`, `I(VSENSE)`, `I(RRL)` |
| VDC/RL fault | drain，`FAULT=1` | 峰值电流、`E_RL`、clear time |
| 650 V profile | fast，`PROFILE=0` | 所有fast traces |
| 3.3 kV profile | fast，`PROFILE=1` | 所有fast traces；特别看source方向与`Lcs` |

## 必做扫描

逐个启用fast文件中的：`Rg`、`Cscale`（等效Gate电容/电荷范围）、`Lgate`、`Lcs`、`RailTol`、`Rsrc/Rsink`、`Cdec`、`ESR/ESL`；drain文件中的`RLVAL`；states文件中的`DEAD`。每个扫描记录nominal、worst waveform和失败边界。

## 接受条件

- `VGS`不超过对应DUT绝对最大范围，且recommended范围外的过冲必须有批准的瞬态依据。
- stress end到可解释`VDS`点：目标约100 ns；报告nominal/worst/uncertainty，不只测VOA。
- Gate路径任何时刻最多一个获权；争用case必须触发invalid/SAFE_OFF。
- control loss、UVLO、rail fail后drain disable且Gate回0 V安全目标，不自动重启。
- `VDC/RL`fault能量低于电阻、电源、relay和DUT的批准脉冲能力。

## 用户需回传的最小证据

- LTspice版本和Windows版本；
- 三个`.log`；
- Positive、Negative、PRECONDITION/CAL/SAFE_OFF、fault、650 V/3.3 kV worst共至少8张截图；
- 若修改输入文件，提交diff；
- 关键游标值：stress-end、VGS跨阈值、VDS进入容差窗、overshoot/undershoot、峰值Gate/drain current、rail droop。
