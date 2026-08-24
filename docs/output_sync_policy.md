# 聊天输出文件 GitHub 同步准则

状态：**APPROVED PROJECT RULE**

生效日期：2026-08-24

## 1. 核心规则

本项目每个 ChatGPT、Codex 或子项目聊天产生的用户可交付输出文件，都必须同步保存到本 GitHub 仓库。没有完成 GitHub 同步和索引登记时，不得把该输出文件标记为项目已归档或正式完成。

本规则约束的是“输出文件”，不是要求把每一句聊天内容原样提交到仓库。没有生成文件的普通讨论不需要人为创建空文件。

## 2. 适用文件

包括但不限于：

- Markdown、Word、PDF、PowerPoint、Excel、CSV；
- Python/MATLAB/脚本、计算文件、分析结果；
- KiCad 原理图、PCB、BOM、规则和检查报告；
- LTspice 模型、仿真配置和结果摘要；
- 图片、图表、接口图、状态图和验证记录；
- Master/SP1–SP7 产生的 HANDOFF、需求、决策、风险和进度文件。

## 3. 保存位置

1. 输出优先保存到其正式工程位置，不为“聊天输出”额外复制一份：
   - 系统、需求、决策、风险、报告：`docs/`
   - 电路与 PCB：`hardware/`
   - 计算：`calculations/`
   - 数据处理代码：`analysis/`
   - 实验数据：`measurements/`
   - 可合法再分发的参考资料或元数据：`references/`
2. 每个新输出同时登记到 `docs/chat_output_index.md`。
3. 文件名应包含明确主题；需要版本管理的交付物应包含版本号，例如 `v0.1`。
4. 同一正式文件的后续修订应更新原路径并利用 Git 历史保留版本；只有需要并行保留多个正式版本时才创建新文件。

## 4. 每次交付的完成条件

每个产生输出文件的聊天在结束前必须完成：

1. 输出文件内容检查；
2. 保存到正确仓库路径；
3. 更新 `docs/chat_output_index.md`；
4. 提交到 GitHub，并确认远端文件可读取；
5. 在最终回复中给出 GitHub 文件或 PR/commit 链接；
6. 同时检查 `docs/project_status.md` 和 `docs/stage_gate.md` 是否需要更新。

若同步失败，必须明确报告 `OUTPUT_SYNC_BLOCKED`、失败原因和仍未同步的本地文件，不得声称已经完成。

## 5. 禁止直接提交的内容

以下内容不得因为本规则而被盲目提交：

- 无再分发权限的论文或书籍原 PDF；
- API key、token、密码、证书、私钥和连接凭据；
- 个人敏感信息或不应进入项目仓库的数据；
- 未批准进入普通 Git 的超大原始数据或二进制文件。

此类文件应在 `docs/chat_output_index.md` 中记录“未提交原因”和可用来源；确需版本管理时，先由 Master 决定 Git LFS、外部存储或脱敏方案。

## 6. 与工程文档的关系

- `docs/chat_output_index.md` 是输出文件登记表，不替代需求、决策、风险或状态文档。
- 每个输出文件仍必须遵守 `AGENTS.md`、`docs/requirements.md`、`docs/decisions.md` 和 Stage-Gate。
- 论文事实、工程推断、项目选择和未知项必须保持分离；保存到 GitHub 不代表开放项已经冻结。

## 7. 当前首次正式登记

本规则生效后的首个正式登记文件是：

- `docs/SP1_paper_method_system_requirements_v0.1.md`
- 来源：SP1 — 论文方法与系统需求
- 版本：SP1-v0.1
- 状态：已同步；其中 OPEN / PAPER_NOT_SPECIFIED 项仍等待 Master 决策。
