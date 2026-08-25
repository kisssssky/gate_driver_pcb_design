# Risk Register

Status: **ACTIVE — G1 architecture responsibilities added; no risk closed**

| ID | Risk | Consequence | G1 architecture control / responsibility | REQ trace | Verification Gate | Status |
|---|---|---|---|---|---|---|
| RISK-001 | `SREF` accidentally tied to laboratory earth | unintended short/current path; invalid `VGS` reference | 显式domain、禁止implicit connection；User与instrument qualification负责最终接线 | `REQ-SYS-INTERFACE-001...003`; `REQ-SYS-MEAS-002` | G2/G3/G10 | Open |
| RISK-002 | External supplies are not truly isolated/floating | supply shorting or incorrect rail voltages | Floating-rail valid/interlock；非浮地时禁止arm | `REQ-SYS-INTERFACE-002/003/006`; `REQ-SYS-SAFE-002/004` | G2/G10 | Open |
| RISK-003 | Negative-BTI default/UVLO state drives gate to negative stress rail | unintended prolonged negative gate stress | control loss/UVLO强制`SAFE_OFF`；fault不自动恢复 | `REQ-SYS-SAFE-001/002`; `REQ-SYS-FUNC-008` | G2/G10 | Open |
| RISK-004 | 0 V precondition path fights Si8273 output | destructive shoot-through between rails | Base PCB状态互锁与break-before-make功能；具体拓扑后定 | `REQ-SYS-INTERFACE-010`; `REQ-SYS-SAFE-003` | G2/G10 | Open |
| RISK-005 | Gate-loop parasitic inductance causes overshoot/ringing | `VGS` overstress and inaccurate timing | `Rg`纳入DUT profile；scope资格与G11波形验证 | `REQ-SYS-DUT-004/005`; `REQ-SYS-SAFE-003/004`; `REQ-SYS-VERIFY-001` | G2/G6/G7/G11 | Open |
| RISK-006 | `VDS` measurement chain too slow | apparent `tdly` meets target while device response is unresolved | 同次事件`VGS/VDS/timing`；instrument qualification | `REQ-SYS-MEAS-001/003`; `REQ-SYS-INTERFACE-009`; `REQ-SYS-VERIFY-001` | G2/G10/G11 | Open |
| RISK-007 | Power Source and Kelvin Source share excessive impedance | source bounce corrupts `VGS/VDS` interpretation | 逻辑接口分离；无KS时profile记录限制 | `REQ-SYS-INTERFACE-001/004`; `REQ-SYS-DUT-004/005` | G4/G6/G7/G11 | Open |
| RISK-008 | `RL/VDC` combination produces excess self-heating | `Vth` shifts due to temperature instead of intended hysteresis | VDC/RL模块限制能量；software记录/计算；User批准profile | `REQ-SYS-METHOD-008`; `REQ-SYS-SAFE-003/004` | G2/G10/G11 | Open |
| RISK-009 | Codex or automation invents pinout/rating/topology details | latent schematic or PCB error | G1仅逻辑接口；所有具体事实推迟到datasheet/对应Gate | `REQ-SYS-PROCESS-001...003` | G2/G3/G4 | Mitigated, monitor |
| RISK-010 | Manufacturing files produced before design review | fabricated board contains unresolved errors | G3继续`BLOCKED`；制造hold不变 | `REQ-SYS-PROCESS-004...006` | G8/G9 | Mitigated, monitor |
| RISK-011 | Output synchronization commits restricted/secret/large material | legal/privacy/security exposure or unusable history | 继续执行sync policy exclusions与远端回读 | `REQ-SYS-PROCESS-007...009` | 每次交付 | Mitigated, monitor |
| RISK-012 | False trigger or illegal state transition | unintended stress or invalid MI/MP/MN | 合法前序状态、command-valid、interlock和fault log | `REQ-SYS-INTERFACE-005`; `REQ-SYS-SAFE-002/003` | G2/G10/G11 | Open |
| RISK-013 | Control loss or UVLO leaves output in stress state | persistent stress, DUT damage, invalid data | 异步`SAFE_OFF`请求、drain disable、无自动restart | `REQ-SYS-SAFE-001/002`; `REQ-SYS-INTERFACE-005` | G2/G10 | Open |
| RISK-014 | DUT adapter/pin orientation is wrong | short, wrong `SREF`, DUT damage | Adapter属于profile；G4 pin/footprint核对；invalid禁止arm | `REQ-SYS-DUT-004/005`; `REQ-SYS-SAFE-004` | G4/G10 | Open |
| RISK-015 | 650 V-class and 3.3 kV-class profiles are mixed | gate overvoltage, wrong `Rg/VDC/RL`, self-heating | 唯一profile绑定DUT/adapter/`Rg`/参数；User批准 | `REQ-SYS-FUNC-002`; `REQ-SYS-DUT-001...005`; `REQ-SYS-SAFE-004` | G2/G10/G12 | Open |
| RISK-016 | Scope/probe/chassis creates hidden earth path | `SREF/GNDA/DRET` clamped, short or bad measurement | earth连接受控；差分探头/共模/机壳在G2/G10资格确认 | `REQ-SYS-INTERFACE-002/003/009`; `REQ-SYS-MEAS-002/003` | G2/G10 | Open |

## G1 risk disposition

- 关闭/退休风险：0。
- 新增定量发生率或风险等级：0。
- `RISK-001...008`仅补充G1责任与REQ追溯，仍保持Open。
- `RISK-009...011`继续`Mitigated, monitor`，不等于Closed。
- 新增`RISK-012...016`覆盖false trigger、control loss/UVLO、adapter错接、DUT profile混用和probe earth路径。
- 详细14项简化FMEA见`docs/G1_system_architecture_v1.0.md`第10章。

