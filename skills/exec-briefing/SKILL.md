---
name: exec-briefing
description: Generate structured executive briefing scripts for C-level stakeholder presentations. Based on Product Talk's "show your work" framework using the OOSE structure (Outcome-Opportunity-Solution-Evidence). Use when the user needs to prepare a CEO/CTO/VP update, executive review script, leadership briefing, stakeholder presentation, or quarterly business review narrative. Triggers on "写汇报稿", "executive update", "给老板汇报", "prepare a briefing", "C-level presentation", "管理层汇报".
---

# Executive Briefing Script Generator

Generate structured presentation scripts for C-level audiences using the OOSE framework (Outcome → Opportunity → Solution → Evidence).

## Core Principle

**展示过程，不推销结论。** 带来高管不掌握的新信息（用户洞察、验证数据、机会规律），而非邀请观点之争。

## Workflow

1. **Gather inputs** — Ask for: (a) 汇报对象和场景 (CEO周会? 季度评审? 电梯汇报?), (b) 产品/项目名称, (c) 当前目标和关键数据, (d) 用户洞察或客户反馈, (e) 时长限制
2. **Load framework** — Read [references/framework.md](references/framework.md) for the full OOSE structure and audience adaptation rules
3. **Select format** based on time budget:

| 时长 | 格式 | 章节数 |
|------|------|--------|
| 30秒 | 电梯汇报 | OOSE 各1句 |
| 5分钟 | 站会简报 | OOSE 各1段 + 下一步 |
| 15分钟 | 正式汇报 | 完整6章 |
| 30分钟+ | 深度评审 | 完整7步展开 |

4. **Draft script** — Follow the chapter structure below
5. **Review** — Check against anti-patterns, iterate with user
6. **Export to Markdown** — After the user confirms the script, save it as a `.md` file in the project's document directory (e.g., `PRD/` or a user-specified path). The exported file should be a clean, standalone document ready for sharing — include the metadata header (场景, 时长, 日期, 阶段) but strip any workflow-internal comments.

## Chapter Structure (15-minute standard format)

```
第一章：目标对齐 (Outcome)
  - 重申共享目标和关键指标
  - 确认目标未发生变化（若有变化，先说明）

第二章：机会发现 (Opportunity)
  - 用户洞察：我们发现了什么问题/需求
  - 数据支撑：影响面、频次、严重程度
  - 引用具体用户声音（访谈快照）

第三章：方案与验证 (Solution + Evidence)
  - 我们选择了什么方案，为什么
  - 假设验证：测试了什么，结果如何
  - 关键数据对比（before → after）

第四章：进展与里程碑
  - 本期完成了什么
  - 关键指标变化
  - 遇到的阻碍和应对

第五章：下一步计划
  - 下一个要验证的假设
  - 需要高管决策/支持的事项（明确ask）

第六章：开放讨论
  - 预留给高管的提问和建议空间
  - "我们是否遗漏了什么机会？"
```

## Writing Rules

- 每个章节标注建议时长（如 "[2分钟]"）
- 数据先行：先给数字，再解释含义
- 用 `**粗体**` 标记关键数据和结论
- 用 `> 引用格式` 呈现用户原话
- 每章结尾用一句话过渡到下一章
- 绝不推销结论——展示到达结论的路径
- 绝不否定高管可能的替代想法——将其纳入框架讨论

## Output Format

Default Markdown. Prefix each chapter with `## 第N章：标题 [Xmin]`.

## References

- **OOSE framework, audience adaptation, anti-patterns**: See [references/framework.md](references/framework.md)
