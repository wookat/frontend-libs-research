import json, urllib.request, urllib.parse, time
d=json.load(open("/home/ubuntu/fe-research/data.json"))
pkgs=sorted({r["pkg"] for r in d if r["pkg"]})
unscoped=[p for p in pkgs if not p.startswith("@")]
scoped=[p for p in pkgs if p.startswith("@")]
res={}
def get(url):
    for i in range(6):
        try:
            with urllib.request.urlopen(url,timeout=30) as f: return json.load(f)
        except urllib.error.HTTPError as e:
            if e.code==429: time.sleep(5*(i+1)); continue
            return {"error":e.code}
        except Exception as e:
            time.sleep(3)
    return {"error":"giveup"}
for i in range(0,len(unscoped),100):
    chunk=unscoped[i:i+100]
    j=get("https://api.npmjs.org/downloads/point/last-week/"+",".join(chunk))
    if len(chunk)==1: j={chunk[0]:j}
    for k,v in (j or {}).items():
        if v: res[k]=v.get("downloads")
    time.sleep(1)
for p in scoped:
    j=get("https://api.npmjs.org/downloads/point/last-week/"+urllib.parse.quote(p,safe='@'))
    res[p]=j.get("downloads") if j else None
    time.sleep(0.8)
for r in d:
    if r["pkg"] and r["npm"] is not None:
        r["npm"]["weekly"]=res.get(r["pkg"]); r["npm"].pop("weekly_error",None)
json.dump(d,open("/home/ubuntu/fe-research/data.json","w"),ensure_ascii=False,indent=1)
print("missing:",[p for p in pkgs if res.get(p) is None])
