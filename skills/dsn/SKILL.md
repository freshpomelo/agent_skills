---
name: dsn
description: 将用户的灵感、思想火花、想读的书或文章快速记录到 Notion。当用户说"帮我记一下"、"记录一下"、"记个笔记"、"存到notion"或表达想保存某个想法/灵感/链接时触发。支持三种输入：纯文本想法、图片（解析内容保存文字）、URL（提取标题和摘要）。
---

# Daily Spark Notes

将用户的灵感快速保存到 Notion 页面，按日期分节组织。

## 前置条件

环境变量 `NOTION_API_KEY` 必须已设置。若未设置，提醒用户配置。

## 处理流程

### 1. 判断输入类型

| 输入 | 处理方式 |
|------|----------|
| **纯文本** | 去口语化（去掉语气词、重复、口头禅），保留原始含义，不做拓展 |
| **图片** | 用 Read 工具读取图片，识别内容（书名、电影名、截图文字等），提取纯文字信息 |
| **URL** | 先用 WebFetch 获取页面；若失败或内容为空，改用 Jina Reader 爬虫脚本获取 |

### 2. 去口语化规则

- 删除语气词：嗯、啊、就是、然后、那个、反正、emmm 等
- 删除重复表述，合并冗余
- 保持原始含义和关键信息，绝不拓展或添加内容
- 输出简洁的书面语

### URL 回退：Jina Reader 爬虫

当 WebFetch 无法正常获取页面内容时（返回错误、内容为空、JS 渲染页面如微信公众号等），使用 Jina Reader 脚本：

```bash
python ~/.claude/skills/dsn/scripts/jina_fetch.py "https://example.com"
```

- 需要环境变量 `JINA_API_KEY`
- 始终启用 `X-Engine: cf-browser-rendering`，确保 JS 重度页面也能正常抓取
- 输出 JSON，包含 `url`、`title`、`summary`、`raw_content` 字段
- 从输出中提取 `title` 和 `summary` 用于保存到 Notion

### 3. 保存到 Notion

使用此 skill 自带的脚本保存。脚本位于 skill 目录下：`~/.claude/skills/dsn/scripts/save_to_notion.py`

```bash
# 文本笔记
python ~/.claude/skills/dsn/scripts/save_to_notion.py --type text --content "整理后的内容"

# URL 笔记
python ~/.claude/skills/dsn/scripts/save_to_notion.py --type url --content "https://..." --title "页面标题" --summary "摘要"
```

> **注意**：这是全局 skill，脚本路径不依赖当前工作目录，始终使用上述绝对路径。

脚本自动按日期（H2 标题）分节，同一天的笔记追加到当天节下。

### 4. 确认

保存成功后，简短回复用户已记录的内容摘要。
