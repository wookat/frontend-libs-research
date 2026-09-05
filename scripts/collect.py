import concurrent.futures as cf
import importlib.util
import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request


def load_items(path):
    spec = importlib.util.spec_from_file_location("items_module", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load items module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.ITEMS


if len(sys.argv) != 3:
    raise SystemExit("usage: python3 scripts/collect.py <items_module> <out.json>")

ITEMS = load_items(sys.argv[1])
OUT = sys.argv[2]


def gh(repo):
    if not repo:
        return None
    try:
        out = subprocess.run(["gh", "api", f"repos/{repo}", "--jq",
            '{stars:.stargazers_count,license:(.license.spdx_id // "NONE"),pushed:.pushed_at,archived:.archived,desc:.description,created:.created_at,forks:.forks_count,issues:.open_issues_count,default_branch:.default_branch}'],
            capture_output=True, text=True, timeout=40)
        if out.returncode != 0:
            return {"error": out.stderr.strip()[:200]}
        return json.loads(out.stdout)
    except Exception as e:
        return {"error": str(e)}


def npm(pkg):
    if not pkg:
        return None
    r = {}
    try:
        with urllib.request.urlopen(f"https://registry.npmjs.org/{urllib.parse.quote(pkg, safe='@')}", timeout=30) as f:
            d = json.load(f)
        latest = d["dist-tags"].get("latest")
        r["version"] = latest
        r["tags"] = {k: v for k, v in d["dist-tags"].items() if k in ("latest", "next", "beta", "canary", "alpha", "rc")}
        r["modified"] = d.get("time", {}).get("modified")
        r["latest_time"] = d.get("time", {}).get(latest)
        r["created"] = d.get("time", {}).get("created")
        v = d["versions"].get(latest, {})
        repository = v.get("repository")
        r["repository"] = repository.get("url") if isinstance(repository, dict) else repository
        r["license"] = v.get("license") if isinstance(v.get("license"), str) else (v.get("license", {}) or {}).get("type")
        pd = v.get("peerDependencies", {}) or {}
        r["peer_react"] = pd.get("react")
        r["peer_tailwind"] = pd.get("tailwindcss")
        r["unpacked"] = (v.get("dist", {}) or {}).get("unpackedSize")
        r["deps_count"] = len(v.get("dependencies", {}) or {})
        r["types"] = bool(v.get("types") or v.get("typings"))
        r["deprecated"] = v.get("deprecated")
    except Exception as e:
        r["error"] = str(e)[:200]
    try:
        with urllib.request.urlopen(f"https://api.npmjs.org/downloads/point/last-week/{urllib.parse.quote(pkg, safe='@')}", timeout=30) as f:
            r["weekly"] = json.load(f).get("downloads")
    except Exception as e:
        r["weekly_error"] = str(e)[:100]
    return r


def work(item):
    cat, name, repo, pkg = item
    return {"cat": cat, "name": name, "repo": repo, "pkg": pkg, "gh": gh(repo), "npm": npm(pkg)}


with cf.ThreadPoolExecutor(8) as ex:
    res = list(ex.map(work, ITEMS))
os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
json.dump(res, open(OUT, "w"), ensure_ascii=False, indent=1)
print(len(res), "done; errors:", sum(1 for r in res if (r["gh"] and "error" in r["gh"]) or (r["npm"] and "error" in r["npm"])))
