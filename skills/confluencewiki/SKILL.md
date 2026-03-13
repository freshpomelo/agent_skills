---
name: confluencewiki
description: 用于操作 Confluence Wiki 的技能
version: 1.0.0
---
# Confluence Wiki Management

Manage the project's Confluence wiki. Supports get, update, create, and token management.

## Credential Loading

Credentials are stored in `~/.claude/confluence-config.json` (personal, NOT in repo).

Before any API call, read the config file:

```bash
cat ~/.claude/confluence-config.json
```

Extract `email`, `api_token`, `base_url`, and `account_id` from it.

**CRITICAL: Never display or log the API token in output.**

Due to the token containing special characters, always use Python `subprocess` for API calls instead of direct shell curl. Example pattern:

```python
python3 << 'PYEOF'
import json, subprocess

with open('/Users/admin/.claude/confluence-config.json') as f:
    cfg = json.load(f)

result = subprocess.run([
    'curl', '-s',
    '-u', f"{cfg['email']}:{cfg['api_token']}",
    f"{cfg['base_url']}/rest/api/content/{page_id}?expand=body.storage,version",
    '-H', 'Accept: application/json'
], capture_output=True, text=True)

data = json.loads(result.stdout)
PYEOF
```

## Security Rules

**CRITICAL: Write protection**

- `get` (read): No restrictions, can query any page.
- `update` / `create` / `delete`: MUST verify the page's creator `accountId` matches `account_id` from config. If not, REFUSE the operation and display: "Access denied: you can only modify pages created by your account."

Verification: when fetching a page for update, check `version.by.accountId` or use the history API:

```
GET /rest/api/content/{pageId}/history
```

Compare `history.createdBy.accountId` with `account_id` from config.

## Actions

Based on the user's command arguments, perform one of the following:

### `get` - Read a wiki page

Extract page ID from the URL or argument, then fetch via Python subprocess:

```python
# Fetch page
result = subprocess.run([
    'curl', '-s',
    '-u', f"{cfg['email']}:{cfg['api_token']}",
    f"{cfg['base_url']}/rest/api/content/{page_id}?expand=body.storage,version",
    '-H', 'Accept: application/json'
], capture_output=True, text=True)
```

Display the page title, version, and a human-readable summary of the content.

### `update` - Update an existing wiki page

1. Fetch the current page (get `version.number` and verify ownership)
2. **Verify ownership** (see Security Rules above). STOP if not owned by user.
3. Convert content to Confluence storage format (XHTML)
4. Build JSON payload in Python, write to `/tmp/confluence_update.json`
5. PUT with `version.number + 1` via Python subprocess
6. Clean up temp file after success

```python
payload = {
    "id": page_id,
    "type": "page",
    "title": title,
    "body": {
        "storage": {
            "value": new_body,
            "representation": "storage"
        }
    },
    "version": {
        "number": current_version + 1
    }
}
```

### `create` - Create a new wiki page

1. Determine the parent page and space key (default: `DlabDev`)
2. Convert content to Confluence storage format
3. POST to create via Python subprocess

```python
payload = {
    "type": "page",
    "title": title,
    "space": {"key": space_key},
    "ancestors": [{"id": parent_id}],
    "body": {
        "storage": {
            "value": body_html,
            "representation": "storage"
        }
    }
}
```

### `token` - Update API token

Update the API token in `~/.claude/confluence-config.json`:

1. Read the current config
2. Replace the `api_token` field with the new value provided by user
3. Write back to `~/.claude/confluence-config.json`

Usage: `/wiki token <new-api-token>`

## Confluence Storage Format Reference

Code block:
```xml
<ac:structured-macro ac:name="code" ac:schema-version="1">
  <ac:parameter ac:name="language">json</ac:parameter>
  <ac:parameter ac:name="breakoutMode">wide</ac:parameter>
  <ac:parameter ac:name="breakoutWidth">760</ac:parameter>
  <ac:plain-text-body><![CDATA[code here]]></ac:plain-text-body>
</ac:structured-macro>
```

Info panel:
```xml
<ac:structured-macro ac:name="info" ac:schema-version="1">
  <ac:rich-text-body><p>text here</p></ac:rich-text-body>
</ac:structured-macro>
```

Warning panel:
```xml
<ac:structured-macro ac:name="warning" ac:schema-version="1">
  <ac:rich-text-body><p>text here</p></ac:rich-text-body>
</ac:structured-macro>
```

Table:
```xml
<table data-table-width="760" data-layout="default">
  <tbody>
    <tr><th><p>Header</p></th><th><p>Header</p></th></tr>
    <tr><td><p>Cell</p></td><td><p>Cell</p></td></tr>
  </tbody>
</table>
```

## Important Notes

- Always fetch the latest version before updating (avoid conflicts)
- Use Confluence storage format (XHTML), NOT markdown
- Page ID can be extracted from URL pattern: `pages/{pageId}/PageTitle`
- For large body replacements, use Python with `re.sub` for section-level updates
- Write large payloads to temp file, use `-d @/tmp/file.json`
- Clean up temp files after use
- NEVER display or log the API token in output
- Always use Python subprocess for curl calls to avoid shell escaping issues with the API token
