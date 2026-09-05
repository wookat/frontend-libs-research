# frontend-libs-research

前端优秀开源库全景研究。所有数字为一手实查（GitHub `gh api repos/<o>/<r>` + npm registry / downloads API），不转述博客。

- `docs/frontend-libs-2026.md` — 15 类 / 219 候选对比表、四象限结论、链接索引（实查日期 2026-09-05）
- `data/candidates-2026-09-05.json` — 原始采集数据（stars / SPDX / pushed / archived / npm 版本 / 周下载 / license / peer / unpackedSize）
- `scripts/collect.py`、`scripts/downloads.py` — 采集脚本（需 `gh` 登录；下载 API 有 429 限流已做退避）

复现：`python3 scripts/collect.py && python3 scripts/downloads.py`
