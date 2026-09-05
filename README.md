# frontend-libs-research

前端优秀开源库全景研究。所有数字为一手实查（GitHub `gh api repos/<o>/<r>` + npm registry / downloads API），不转述博客。

- `docs/frontend-libs-2026.md` — 34 类 / 609 候选对比表（第一批 §1–§15 219 个，第二批 §16–§23 121 个新增 + 4 个对照，第三批 §24–§34 269 个新增 + 10 个交叉引用）、四象限结论、风险清单、链接索引（实查日期 2026-09-05）
- `data/candidates-2026-09-05.json` / `.txt` — 第一批原始采集数据与逐行摘要
- `data/candidates-round2-2026-09-05.json` / `.txt` — 第二批原始数据（新增 `npm.repository`、`npm.created` 字段）与逐行摘要
- `data/candidates-round3-2026-09-05.json` / `.txt` — 第三批原始数据（§24–§34，279 条）与逐行摘要
- `scripts/items_round1.py`、`scripts/items_round2.py`、`scripts/items_round3.py` — 候选清单（`ITEMS = [(cat, name, github_repo, npm_pkg), ...]`）
- `scripts/collect.py`、`scripts/downloads.py`、`scripts/summarize.py` — 采集 / 补周下载 / 摘要脚本（需 `gh` 登录；下载 API 有 429 限流已做退避）

复现：

```bash
python3 scripts/collect.py scripts/items_round2.py data/candidates-round2-2026-09-05.json
python3 scripts/downloads.py data/candidates-round2-2026-09-05.json
python3 scripts/summarize.py data/candidates-round2-2026-09-05.json data/candidates-round2-2026-09-05.txt
```
