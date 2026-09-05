import json
import sys

if len(sys.argv) != 3:
    raise SystemExit("usage: python3 scripts/summarize.py <data.json> <out.txt>")

data_path, out_path = sys.argv[1:]
rows = json.load(open(data_path))

def short_number(value):
    if value is None:
        return "-"
    if value < 1000:
        return str(value)
    if value < 1_000_000:
        return f"{value / 1000:.1f}k"
    return f"{value / 1_000_000:.1f}M"

def date(value):
    return value[:10] if value else "None"

def value(obj, key, default="None"):
    if not obj:
        return default
    item = obj.get(key)
    return default if item is None else str(item)

lines = []
for row in rows:
    gh = row.get("gh") or {}
    npm = row.get("npm") or {}
    lines.append(
        f"{row['cat']:>2}|{row['name']:<30}|{str(row.get('repo') or '-'): <34}| "
        f"{short_number(gh.get('stars')):>6}|{value(gh, 'license'):<11}|{date(gh.get('pushed'))}|"
        f"A={gh.get('archived', 'None')}|{str(row.get('pkg') or '-'): <30}|"
        f"v{value(npm, 'version'):<10}|wk={short_number(npm.get('weekly'))}|lic={value(npm, 'license')}|"
        f"react={value(npm, 'peer_react')}|tw={value(npm, 'peer_tailwind')}|"
        f"unp={short_number(npm.get('unpacked'))}|lt={date(npm.get('latest_time'))}|dep={bool(npm.get('deprecated'))}"
    )

with open(out_path, "w") as f:
    f.write("\n".join(lines) + "\n")
