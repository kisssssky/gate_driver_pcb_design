# G2 Final Gate Review v1.0

- 日期：2026-08-26
- 审核状态：`G2 ACTIVE — NOT READY FOR MASTER REVIEW`
- G0：`PASS`；Requirement baseline：`FROZEN`
- G1：`PASS`；G1 interface baseline：`FROZEN`
- G3：`BLOCKED`

## 1. A–V审查

| 项 | 结果 | 证据/FAIL原因 | 责任人与下一步 |
|---|---|---|---|
| A Si8273完整料号/封装 | PASS | `Si8273AB-IS1`, SOIC-16 NB；Skyworks 206327E p.41 | Master批准候选 |
| B 650 V完整型号/profile | PASS | `SCTW35N65G2VAG`, `DUT-650-...-v1.0` | 用户实物已确认 |
| C 3.3 kV完整型号/profile | PASS（代理范围） | `DUT-PROXY-3K3-G2R50MT33K-3P-v0.1`；不是实际非商业DUT资格 | 用户取得实物后替换/收紧profile |
| D 关键datasheet参数追溯 | PASS | Si8273/ST/GeneSiC/TI参数含页码、表、条件；商业4pin到3pin转换单列假设 | Master review |
| E P/N rail与兼容性 | PASS | 四个rail span 8–17 V；Si8273/UCC UVLO及DUT VGS已核 | Master批准具体rail |
| F Gate current/`Rg` | PASS | `Qg/t`、峰值、R/C、source/sink分开；profile Rg扫描 | LTspice/G11收敛最终值 |
| G 去耦/rail droop | PASS | `C≥Q/ΔV`、2×裕量、ESR/ESL、DC bias和布局要求 | G3按批准值实现 |
| H 0 V PRECONDITION选择并验证 | FAIL | NC monostable relay拓扑已选择；无LTspice真实运行/台架验证 | 用户运行states case；Master批准 |
| I CAL/VGM-I选择并验证 | FAIL | 浮动VGM-I+relay拓扑已选择；B1505目标和仿真证据缺失 | 用户给B1505曲线并运行case |
| J SAFE_OFF/sequence/fault分析 | PASS（分析） | 硬件NC Gate clamp、NO drain、fault latch与顺序已定义；实证仍在H/P | G10故障注入 |
| K VDC/RL/功率/能量/自热 | FAIL | 公式和扫描已完成，但正式MI/MP/MN、`VDS-C`、VDC/RL依赖B1505数据 | 用户提供曲线；脚本复算 |
| L 完整约100 ns预算 | PASS | nominal/worst/uncertainty预算已建；结论是两个profile worst-case尚无满足证据 | LTspice+G11验证 |
| M scope/probe最低要求 | PASS（要求范围） | 由10/20 ns边沿反推带宽、采样、memory、deskew、earth路径 | 用户G10按实物型号资格确认 |
| N Positive BTI LTspice | FAIL | 输入deck已建立；无`.raw/.log/截图` | 用户本地运行 |
| O Negative BTI LTspice | FAIL | 同上 | 用户本地运行 |
| P PRE/CAL/SAFE_OFF LTspice | FAIL | 同上 | 用户本地运行 |
| Q 两profile最坏/扫描 | FAIL | 扫描配置已建立；未实际运行 | 用户本地运行 |
| R 计算可复算 | PASS | Python标准库脚本self-check通过 | 复核脚本输出 |
| S 假设/未知/用户输入明确 | PASS | 报告各节与本表 | 按HANDOFF逐项关闭 |
| T 未修改冻结需求/G1接口 | PASS | 仅新增G2文件和状态/风险记录 | remote diff复核 |
| U 未进入KiCad/G3 | PASS | 无`.kicad_*`、footprint、placement、routing或BOM发布 | 保持G3 BLOCKED |
| V GitHub同步/远端回读 | PASS | 13个变更文件在分支`g2/component-selection-calculations-v1`逐文件远端回读与本地内容MATCH；draft PR #5 | 合并由用户/Master决定 |

关键FAIL：H、I、K、N、O、P、Q；因此不得宣布G2完成、PASS或READY FOR MASTER REVIEW。

## 2. OPEN项

| ID | 项目 | 证据等级 | 责任人/关闭条件 |
|---|---|---|---|
| OI-G2-001 | 本地LTspice版本与14 case真实结果 | USER CONFIRMATION REQUIRED | 用户安装并回传log/截图 |
| OI-G2-002 | B1505的`Ith/VDS-C/VGM-I/P/N/MI/MP/MN` | USER CONFIRMATION REQUIRED | 用户完成/提供曲线 |
| OI-G2-003 | 非商业3.3 kV DUT真实profile | USER CONFIRMATION REQUIRED | 用户提供内部型号、pin和实测参数 |
| OI-G2-004 | rail、buffer、relay、`Rg`和power sequence | MASTER DECISION REQUIRED | Master逐项批准PROP-G2-001…012 |
| OI-G2-005 | Gate-to-rail clamp二极管确切料号 | OPEN / NOT VERIFIED | 由LTspice/台架峰值、电容和脉冲电流选定 |
| OI-G2-006 | 实际仪器/浮地接线资格 | USER CONFIRMATION REQUIRED | G10/G11按最低要求审核 |

## 3. 变更报告

- 创建：G2器件/计算报告、Final Gate Review、计算说明、Python脚本、三个LTspice输入deck及README。
- 更新：风险、项目状态、stage gate、聊天索引（随同一分支提交）。
- 电气行为候选：Si8273 A/VOA后加同域buffer；两级monostable relay实现0 V/CAL/FAST互斥；失电Gate回SREF、drain NO断开。
- 计算：Gate电流、R/C/Qg、寄生过冲、去耦、rail功耗、VDC/RL/energy、完整时序和测量链。
- datasheet：Skyworks/ST/GeneSiC/TI/TE官方资料；不提交PDF。
- 仿真假设：全部为简化/人工模型；无LTSPICE RESULT。
- ERC/DRC：`NOT RUN / NOT APPLICABLE AT G2`，因为未创建KiCad设计。
- 新增风险：3.3 kV代理误差、三引脚公共Source寄生、100 ns worst-case、ST obsolete、relay bounce、保护clamp未定。
- 退休风险：无。
- Master待批准：PROP-G2-001…012和具体rail/`Rg`/buffer/relay。

## 4. HANDOFF_PACKET

```yaml
HANDOFF_PACKET:
  project: SiC MOSFET BTI Fast Gate Driver PCB / Fig. 3 Reproduction
  authoritative_status:
    G0: PASS
    requirement_baseline: FROZEN
    G1: PASS
    G1_interface_baseline: FROZEN
    G2: ACTIVE
    G3: BLOCKED
  frozen_boundary:
    dut_physical_pins: [Gate, Drain, Source]
    source_rule: SREF and DRET meet only at DUT_SOURCE/SOURCE_STAR
    fast_interface: Si8273 channel A / VOA
    calibration_interface: IF-GATE-01 / CAL_GATE_TARGET
  proposed_parts:
    isolator: Si8273AB-IS1
    buffer: UCC27614DR
    dut_650v: SCTW35N65G2VAG
    dut_3k3_proxy: DUT-PROXY-3K3-G2R50MT33K-3P-v0.1
    path_relay: IM03GR / TE 1-1462037-4
  user_only_actions:
    - Install LTspice on local Windows and record version
    - Run all README cases and return logs/screenshots/cursor values
    - Provide B1505 curves/targets for Ith, VDS-C, VGM-I/P/N, MI/MP/MN
    - Qualify actual scope/probes/floating supplies and earth paths at G10/G11
    - Replace proxy data when the unpublished 3.3 kV DUT becomes available
  master_actions:
    - Approve or reject PROP-G2-001 through PROP-G2-012
    - Approve rail centers, Rg by profile, buffer and relay topology
  prohibited_next_steps:
    - Do not mark G2 PASS
    - Do not freeze any G2 parameter/topology
    - Do not start KiCad/G3
```

## 5. GitHub同步记录

- 分支：`g2/component-selection-calculations-v1`
- Draft PR：https://github.com/kisssssky/gate_driver_pcb_design/pull/5
- 初次完整远端回读：13/13文件MATCH
- `SYNCED`只表示该分支可回读，不表示PR已合并或G2已PASS。
