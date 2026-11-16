#!/usr/bin/env python3
"""Public Github Stars incremental census; old 632-row snapshot is immutable."""
import base64
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import runpy
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT=Path(__file__).resolve().parents[1]
USER="riccardopinato"
DATE="2026-11-16"
BASELINE="c5adc147046beb7024629466d10eeb799c3c2619"
CLASSIFIER=runpy.run_path(str(ROOT/"scripts"/"generate_audit.py"))["classify"]
TOKEN=os.environ.get("GH_TOKEN","")
APP_TERMS=[
 (["launcher","dock","taskbar","wallpaper"],["Adaptive-Landscape-Android","Design-App"]),
 (["markdown","editor","notes","notebook","kanban","whiteboard","knowledge"],["Notes-Ecosistema","Agenda-per-Anna"]),
 (["calendar","diary","journal","reminder"],["Agenda-per-Anna","World-Days"]),
 (["scanner","pdf","camera","gallery","video","ocr"],["FrameLab","Android-Omni-Cleaner"]),
 (["battery","charging","energy","power usage"],["Battery_Guard","FocuSense"]),
 (["cleaner","cleanup","duplicate files","file manager"],["Android-Omni-Cleaner"]),
 (["map","route","travel","gps","hiking","outdoor"],["TrailPath","CamperBoss","Wonderlog"]),
 (["finance","trading","stocks","portfolio"],["CashMate-AI","Finance-Intelligence-Agent"]),
 (["agent","llm","mcp","codex","automation"],["App-Factory-Agent-Core","App Factory Core"]),
 (["test","benchmark","ci","github actions","debug"],["AppLab","App Factory Core"]),
 (["widget","dashboard","usage limits","system monitor"],["App Factory Control Center","FocuSense"]),
 (["animation","design system","user interface","flutter","dart"],["Design-App","App Factory Core"]),
 (["game","shader","rendering engine"],["Game Factory","Adaptive-Landscape-Android"])
]

def api(path):
    headers={"User-Agent":"AppFactory-Stars-Audit","Accept":"application/vnd.github+json",
             "X-GitHub-Api-Version":"2022-11-28"}
    if TOKEN:
        headers["Authorization"]="Bearer "+TOKEN
    with urlopen(Request("https://api.github.com"+path,headers=headers),timeout=30) as response:
        return json.load(response)

def audit_repo(repo):
    name=repo["full_name"]
    key="/repos/"+"/".join(quote(x,safe="") for x in name.split("/"))
    errs=[]
    text=""
    readme_path=None
    readme_blob=None
    head=None
    try:
        obj=api(key+"/readme")
        readme_path=obj.get("path")
        readme_blob=obj.get("sha")
        if obj.get("encoding")=="base64":
            text=base64.b64decode(obj["content"]).decode("utf-8","replace")
        else:
            errs.append("README_ENCODING_UNAVAILABLE")
    except Exception as e:
        errs.append("README_"+type(e).__name__)
    try:
        obj=api(key+"/commits/"+quote(repo.get("default_branch") or "main",safe=""))
        head=obj.get("sha")
    except Exception as e:
        errs.append("HEAD_"+type(e).__name__)
    bullets=[]
    for line in text[:100000].splitlines():
        line=line.strip()
        if re.match(r"^#{1,4}\s+",line) or re.match(r"^[-*]\s+\S",line):
            line=re.sub(r"<[^>]*>","",line)
            line=re.sub(r"!\[[^\]]*\]\([^)]+\)","",line)
            line=re.sub(r"\[([^\]]+)\]\([^)]+\)",r"\1",line)
            line=re.sub(r"\s+"," ",line).replace("|","/")
            if len(line)>8:
                bullets.append(line[:170])
            if len(bullets)>=14:
                break
    keyword_text=(" ".join([name,repo.get("description") or "",
                    " ".join(repo.get("topics") or [])," ".join(bullets)])).lower()
    candidates=[]
    for words,apps in APP_TERMS:
        if any(w in keyword_text for w in words):
            for app in apps:
                if app not in candidates:
                    candidates.append(app)
    license_meta=(repo.get("license") or {}).get("spdx_id") or "NOASSERTION"
    basic=CLASSIFIER(repo)
    priority="P1" if basic["utility"]>=86 else "P2" if basic["utility"]>=70 else "P3"
    if not text and not repo.get("description"):
        priority="EVIDENCE_GAP"
    return {**basic,
        "priority":priority,"source_ref":head,"readme_path":readme_path,
        "readme_blob_sha":readme_blob,"readme_evidence":bullets,
        "readme_sha256":hashlib.sha256(text.encode()).hexdigest() if text else None,
        "readme_status":"VERIFIED_EXCERPTS" if text else "EVIDENCE_GAP",
        "audit_errors":errs,"license_spdx_metadata":license_meta,
        "copy_code_status":"NEEDS_FILE_LEVEL_LICENSE_REVIEW" if license_meta!="NOASSERTION" else "REFERENCE_ONLY",
        "candidate_apps_heuristic":candidates[:8],
        "implementation":"NOT_VERIFIED","product_decision":"DA_VALUTARE"}

def put(name,obj):
    path=ROOT/name
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

def safe(text):
    return str(text or "—").replace("|","/").replace("\n"," ")[:150]

def main():
    old=json.loads((ROOT/"data/stars_public.json").read_text(encoding="utf-8"))
    oldset={r["name"].lower() for r in old}
    if len(old)!=632 or len(oldset)!=632:
        raise RuntimeError("Historical 632 repository baseline was altered")
    public=[]
    page_sizes=[]
    for page in range(1,31):
        chunk=api("/users/"+USER+"/starred?per_page=100&page="+str(page))
        if not isinstance(chunk,list):
            raise RuntimeError("GitHub stars endpoint did not return a list")
        page_sizes.append(len(chunk))
        public.extend(chunk)
        if len(chunk)<100:
            break
    else:
        raise RuntimeError("Pagination stopped without final page")
    keys=[r["full_name"].lower() for r in public]
    if len(public)<500 or len(keys)!=len(set(keys)):
        raise RuntimeError("Unexpected public stars coverage or duplicate pages")
    new=[r for r in public if r["full_name"].lower() not in oldset]
    absent=sorted(oldset-set(keys))
    details=[]
    with ThreadPoolExecutor(max_workers=6) as workers:
        futures={workers.submit(audit_repo,r):r for r in new}
        for future in as_completed(futures):
            repo=futures[future]
            try:
                details.append(future.result())
            except Exception as e:
                x=CLASSIFIER(repo)
                details.append({**x,"priority":"EVIDENCE_GAP","readme_status":"EVIDENCE_GAP",
                  "audit_errors":[type(e).__name__],"readme_evidence":[],
                  "candidate_apps_heuristic":[],"source_ref":None,
                  "license_spdx_metadata":(repo.get("license") or {}).get("spdx_id") or "NOASSERTION",
                  "copy_code_status":"REFERENCE_ONLY","product_decision":"DA_VALUTARE",
                  "implementation":"NOT_VERIFIED"})
    details.sort(key=lambda x:(-x["utility"],-x["ease"],x["name"].lower()))
    detail_by_name={r["name"].lower():r for r in details}
    full=[]
    for repo in public:
        name=repo["full_name"].lower()
        item=detail_by_name.get(name) or CLASSIFIER(repo)
        full.append({**item,"snapshot_state":"NEW_PUBLIC" if name in detail_by_name else "STILL_PUBLIC_HISTORICAL"})
    full.sort(key=lambda x:(-x["utility"],-x["ease"],x["name"].lower()))
    report={
      "source_kind":"PUBLIC_USER_STARRED_API","source_endpoint":"GET /users/riccardopinato/starred",
      "authenticated_to_user":"NO; public endpoint accessed with Github Actions token",
      "user_reported_ui_stars":750,"current_public":len(public),
      "gap_from_user_report":750-len(public),"old_public":len(old),
      "still_public_historical":len(public)-len(details),"new_public":len(details),
      "historical_absent_from_public":len(absent),
      "readmes_checked":sum(x.get("readme_status")=="VERIFIED_EXCERPTS" for x in details),
      "page_sizes":page_sizes,"retrieved_at_utc":datetime.now(timezone.utc).isoformat(),
      "source_baseline_factory":BASELINE,
      "warning":"Set comparison is not event history; missing private stars cannot be identified."
    }
    put("data/stars_current_"+DATE+".json",{"summary":report,"repositories":full})
    put("data/stars_delta_"+DATE+".json",{"summary":report,"new_public":details,"old_missing":absent})
    header=[
      "# Nuove stelle GitHub - audit incrementale "+DATE,"",
      "Censimento PUBBLICO verificato via GitHub REST: "+str(len(public))+
      " repository, pagine "+str(page_sizes)+". Il valore UI 750 e riferito dall'utente e non autenticato da questa API.",
      "Precedenti 632, nuove nel confronto "+str(len(details))+
      ", precedenti ancora accessibili "+str(len(public)-len(details))+
      ", precedenti assenti dal set pubblico "+str(len(absent))+
      ". Le assenze NON sono cancellazioni di stella certificate.",
      "README verificate "+str(report["readmes_checked"])+"/"+str(len(details))+
      ". Tutte le idee sono E0/da valutare, mai implementate o donor certificate sulla base di questo report.",
      "", "## Conteggi per categoria","",
      "| Categoria | Repo |","|---|---:|"]
    for cat,n in Counter(x["category"] for x in details).most_common():
        header.append("| "+cat+" | "+str(n)+" |")
    header+=["","## Classifica integrale delle nuove stelle pubbliche","",
      "| # | Repository | Utilita | Facilita | Priorita | Categoria | Licenza metadata | App candidate | Evidenza README |",
      "|---:|---|---:|---:|---|---|---|---|---|"]
    for i,x in enumerate(details,1):
        header.append("| "+str(i)+" | ["+x["name"]+"]("+x["url"]+") | "+str(x["utility"])+
          " | "+str(x["ease"])+" | "+x["priority"]+" | "+x["category"]+" | "+
          safe(x.get("license_spdx_metadata"))+" | "+
          safe(", ".join(x.get("candidate_apps_heuristic",[])[:3]))+" | "+x["readme_status"]+" |")
    header+=["","## Schede tecniche per ogni nuova fonte", ""]
    for x in details:
        header += ["### ["+x["name"]+"]("+x["url"]+")",
          "- Source HEAD: "+str(x.get("source_ref"))+"; README path: "+str(x.get("readme_path"))+
          "; blob: "+str(x.get("readme_blob_sha"))+"; license metadata: "+str(x.get("license_spdx_metadata"))+".",
          "- Evidenza estratta: "+safe("; ".join(x.get("readme_evidence",[])[:6])),
          "- Candidate app da confermare su codice/Product Bible: "+safe(", ".join(x.get("candidate_apps_heuristic",[]))),
          "- Nessun codice copiato, nessuna CAP o integrazione automaticamente ammessa.",""]
    header+=["## Precedenti assenti dalla nuova enumerazione pubblica (non unstar verificati)",""]
    header+=["- "+x for x in absent] or ["- Nessuna"]
    header+=["","## Note metodologiche",
      "README source excerpts non sono test o audit completi del codice. Score euristici derivati da scripts/generate_audit.py. License SPDX metadata non sostituisce la LICENSE del singolo file. La classifica non autorizza roadmap, CAP o Golden.",""]
    (ROOT/"research").mkdir(exist_ok=True)
    (ROOT/"research"/("STARS_INCREMENTAL_"+DATE+".md")).write_text("\n".join(header),encoding="utf-8")
    alltext=["# Classifica complessiva delle stelle pubbliche - "+DATE,"",
        "Non include le stelle inaccessibili. Score euristici, non risultati di test.","",
        "| # | Repository | Utilita | Facilita | Categoria | Stato |",
        "|---:|---|---:|---:|---|---|"]
    for i,x in enumerate(full,1):
        alltext.append("| "+str(i)+" | ["+x["name"]+"]("+x["url"]+") | "+str(x["utility"])+
                       " | "+str(x["ease"])+" | "+x["category"]+" | "+x["snapshot_state"]+" |")
    (ROOT/"research"/("STARS_ALL_"+DATE+".md")).write_text("\n".join(alltext)+"\n",encoding="utf-8")
    print("AUDIT_SUMMARY",json.dumps(report,ensure_ascii=False))
    print("TOP_NEW",json.dumps([{"name":x["name"],"score":x["utility"],"apps":x.get("candidate_apps_heuristic",[])} for x in details[:25]],ensure_ascii=False))

if __name__=="__main__":
    main()
