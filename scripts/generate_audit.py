#!/usr/bin/env python3
import json, re, urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

USER="riccardopinato"
ROOT=Path(__file__).resolve().parents[1]
CATALOG=ROOT/"catalog"
DATA=ROOT/"data"
FACTORY="4cc0b94467b94ab6fabe2c927fcc58afff49e39a"

CATS=[
("AI / agenti / ChatGPT",["agent","agents","llm","gpt","mcp","prompt","rag","claude","codex","copilot","skill"]),
("App Factory / dev workflow",["developer tool","devtool","boilerplate","template","scaffold","architecture","codegen","github actions","fastlane","release","lint"]),
("QA / testing / debugging",["test","testing","qa","debug","benchmark","profil","crash","memory leak","e2e","maestro","appium","scrcpy","logcat","performance"]),
("Flutter / Dart / mobile cross-platform",["flutter","dart","cross-platform","mobile app"]),
("Android native / utility",["android","kotlin","jetpack","compose","shizuku","root","quick settings","accessibility","battery","notification","adb"]),
("Backend / database / sync",["backend","database","postgres","supabase","firebase","appwrite","api","server","sync","realtime","storage","auth"]),
("UI / UX / design",["ui ","ux ","design system","component","animation","lottie","theme","figma","icon","material","interface"]),
("Note / productivity / knowledge",["note","notes","markdown","notion","obsidian","knowledge","wiki","calendar","task","todo","journal","diary","productivity","planner","clipboard"]),
("Foto / media / PDF / scanner",["photo","camera","image","pdf","ocr","barcode","qr","scan","video","audio","media","palette","color"]),
("Mappe / viaggio / outdoor",["map","maps","routing","osm","openstreetmap","gps","trail","travel","trip","hiking","camp","geolocation"]),
("Game Factory / grafica",["game","gaming","engine","roguelike","pixel","unity","godot","raylib","graphics","3d","2d"]),
("Desktop / web utility",["desktop","tauri","wails","electron","windows","macos","linux","web app","browser extension","extension","cli"]),
("Security / privacy",["security","privacy","encrypt","encryption","password","pentest","hacking","secret","vault"]),
("Automation / scraping / data tools",["scrap","crawler","automation","workflow","browser automation","selenium","playwright","data extraction","download"]),
("Idea prodotto / utility generale",["utility","toolbox","converter","tracker","manager","cleaner","organizer","monitor","calculator","reader","launcher"])
]
STRONG={"flutter","android","agent","mcp","testing","qa","scrcpy","adb","shizuku","architecture","template","pdf","camera","note","notion","obsidian","map","routing","game","tauri","supabase","firebase","appwrite","automation","figma","release","github actions"}

FUTURE={
"AI / agenti / ChatGPT":"Valutare per skill, agent governance, memoria, tool-use o ricerca in ChatGPT/App Factory; integrare solo se colma un gap rispetto ai Golden.",
"App Factory / dev workflow":"Benchmark di processo/architettura/CI; possibile donor per Golden o tooling, senza imporre uno stack nuovo.",
"QA / testing / debugging":"Valutare per AppLab: failure detection, runtime evidence, debug o performance; incapsulare come adapter/tool di QA.",
"Flutter / Dart / mobile cross-platform":"Reference/donor per app Flutter; estrarre solo feature o pattern compatibili con lo stack corrente.",
"Android native / utility":"Donor/reference per utility Kotlin/Android o capability native Flutter: servizi, tile, permessi, Shizuku o system integration.",
"Backend / database / sync":"Provider/reference backend; usarlo solo se risolve un requisito reale di auth, storage, sync, realtime o self-hosting.",
"UI / UX / design":"Estrarre pattern UI/UX, design tokens, motion o component composition e ricondurli al design system della Factory.",
"Note / productivity / knowledge":"Studiare per Notes-Ecosistema/Anna's Diary: editor, search, sync, calendar, task, knowledge model, import/export o progressive disclosure.",
"Foto / media / PDF / scanner":"Valutare per FrameLab, Notes Document Workspace o una micro-utility dedicata; preferire core riusabili e processing locale.",
"Mappe / viaggio / outdoor":"Reference per TrailPath/CamperBoss/Wonderlog: mappe, routing, GPS, offline data o UX outdoor.",
"Game Factory / grafica":"Bacino Game Factory: engine, gameplay loop, rendering o backend; confrontare sempre con Flame/Godot.",
"Desktop / web utility":"Valutare per Desktop/Web Utility Factory o tool esterni; possibile micro-app se il problema è semplice e monetizzabile.",
"Security / privacy":"Fonte di hardening/reconnaissance per AppLab/App Factory; trasformare finding utili in checklist/test.",
"Automation / scraping / data tools":"Utile per discovery, scraping, benchmark e automazioni; integrare nel workflow solo se riduce lavoro manuale ricorrente.",
"Idea prodotto / utility generale":"Valutare come nuova micro-app o feature; verificare product fit e assenza di duplicazioni.",
"Altro / da valutare":"Reference secondaria; approfondire solo se emerge un requisito direttamente collegato."
}

OV={
"Genymobile/scrcpy":(99,84,"QA / testing / debugging","Priorità AppLab/App Factory: mirroring device, recording, screenshot, riproduzione bug ed Evidence Bundle. Base per Android QA Cockpit."),
"laurent22/joplin":(98,54,"Note / productivity / knowledge","Riferimento permanente per Notes: offline-first, Web Clipper, import/export, sync, E2EE, history, conflitti e plugin model."),
"Imtiaz-Official/Smart-Edge":(97,72,"Android native / utility","Donor forte per edge gestures, overlay, QS Tile, servizi persistenti e Shizuku. Possibile EdgeDock/SideHub."),
"affaan-m/ECC":(97,72,"AI / agenti / ChatGPT","Candidate forte per ottimizzazione harness agentico: memory, research-first, skill/instinct e security."),
"addyosmani/agent-skills":(96,84,"AI / agenti / ChatGPT","Candidate source per rafforzare skill engineering, review e performance della App Factory."),
"flutter/flutter":(96,38,"Flutter / Dart / mobile cross-platform","Source of truth tecnica del framework per bug, performance e platform behavior; non è un donor da copiare."),
"square/leakcanary":(95,92,"QA / testing / debugging","QA debug-only per utility Android native; candidato a gate/Golden di memory-leak detection."),
"mattpocock/skills":(94,86,"AI / agenti / ChatGPT","Studiare struttura delle skill modulari, caricamento on-demand e contratti operativi per agenti."),
"Smooth-E/wireless-adb-switch":(94,82,"Android native / utility","Donor diretto per Easy Debloat: Wireless Debugging/Shizuku, tile, widget, boot e pairing helper. Possibile DevBridge."),
"leotodisco/PdfUnifier":(93,78,"Foto / media / PDF / scanner","Idea prodotto forte: PDF Pocket Tools e PDF Core riusabile anche dal Document Workspace di Notes."),
"Universal-Debloater-Alliance/universal-android-debloater-next-generation":(93,67,"Android native / utility","Donor prioritario per Easy Debloat: cataloghi, classificazione pacchetti, safety semantics e UX di debloat."),
"tldr-pages/tldr":(92,92,"Desktop / web utility","Dataset ideale per CmdPocket e per un Offline Content Pack opzionale in Notes."),
"browser-use/browser-use":(92,64,"AI / agenti / ChatGPT","Riferimento per browser agents e automazione web esterna con navigazione autonoma controllata."),
"android/architecture-samples":(91,90,"App Factory / dev workflow","Benchmark ufficiale per Compose, ViewModel, Flow, Room, Hilt e test; sanity reference, non template obbligatorio."),
"tauri-apps/tauri":(91,74,"Desktop / web utility","Tecnologia chiave per Desktop Utility Factory; ottimo per Android QA Cockpit e micro-utility PC."),
"mrousavy/Colorwaver":(91,70,"Foto / media / PDF / scanner","Riferimento per FrameLab: Palette Live/Palette da foto, colori dominanti, HEX/RGB e complementari."),
"unclecode/crawl4ai":(91,78,"Automation / scraping / data tools","Motore esterno per crawling/extraction AI-friendly; utile per ricerche massive, competitor audit e discovery."),
"thedotmack/claude-mem":(90,66,"AI / agenti / ChatGPT","Pattern per memoria persistente e compressione del contesto; studiare senza duplicare la Memory di ChatGPT."),
"00-Evan/shattered-pixel-dungeon":(89,58,"Game Factory / grafica","Donor serio per un roguelike originale nella Game Factory, con forte differenziazione prodotto."),
"Panniantong/Agent-Reach":(89,72,"AI / agenti / ChatGPT","Riferimento per accesso agentico a fonti web/social; utile per reconnaissance e idea discovery."),
"penpot/penpot":(88,46,"UI / UX / design","Reference forte per Visual Workspace di Notes: selection, resize, snapping, layers e design tokens."),
"heroiclabs/nakama":(88,57,"Game Factory / grafica","Backend candidato solo per multiplayer: matchmaking, leaderboards, realtime, social e storage."),
"paperclipai/paperclip":(88,58,"AI / agenti / ChatGPT","Reference per orchestrazione multi-agent; può ispirare una console App Factory."),
"PhilJay/MPAndroidChart":(87,88,"Android native / utility","Standard candidato per grafici nelle app Kotlin: Battery Guard, TrailPath, SleepMax e FocusSense."),
"gkd-kit/gkd":(86,55,"Android native / utility","Reference per accessibility/automazione Android e regole dichiarative; utile per utility e test con permessi sensibili."),
"raysan5/raylib":(82,67,"Game Factory / grafica","Engine candidato per giochi 2D/3D leggeri; confrontarlo con Flame/Godot."),
"appwrite/appwrite":(79,58,"Backend / database / sync","Backend alternativo self-hostable; non migrare Supabase senza un problema concreto."),
"airbnb/lottie-android":(74,88,"UI / UX / design","UI polish selettivo per onboarding/empty/success states; evitare asset e motion eccessivi."),
"ComicSparks/pikapika":(73,43,"Flutter / Dart / mobile cross-platform","Reference per cache offline, file association, local transfer, encrypted archive e cleanup."),
"Hack-with-Github/Awesome-Hacking":(72,94,"Security / privacy","Indice di reconnaissance security per AppLab/App Factory: fonte di strumenti/checklist."),
"zxing/zxing":(69,82,"Foto / media / PDF / scanner","Reference/fallback QR/barcode; non sostituire scanner moderni già validi senza motivo."),
"Trinea/android-open-project":(68,94,"App Factory / dev workflow","Meta-repo di discovery per donor Android; sorgente secondaria per la regola 3-5 OSS."),
"leereilly/games":(66,94,"Game Factory / grafica","Catalogo discovery per Game Factory: donor, engine e giochi OSS da auditare singolarmente."),
"DioxusLabs/dioxus":(65,48,"Desktop / web utility","Laboratorio Rust multipiattaforma interessante per binari piccoli; non sostituisce Flutter."),
"Blankj/AndroidUtilCode":(63,76,"Android native / utility","Bacino di snippet/pattern Android: consultare modulo-per-modulo quando manca un Golden."),
"mosra/magnum":(43,29,"Game Factory / grafica","Grafica C++ potente ma sproporzionata per la Factory attuale; tenere per progetti 3D specialistici.")
}

DEST={
"AI / agenti / ChatGPT":"ChatGPT · App Factory","App Factory / dev workflow":"App Factory · AppLab",
"QA / testing / debugging":"AppLab · App Factory","Flutter / Dart / mobile cross-platform":"App Flutter · App Factory",
"Android native / utility":"Utility native · App Factory","Backend / database / sync":"Backend/sync · app cloud",
"UI / UX / design":"Design system · app consumer","Note / productivity / knowledge":"Notes · Anna's Diary",
"Foto / media / PDF / scanner":"FrameLab · Notes · micro-app","Mappe / viaggio / outdoor":"TrailPath · CamperBoss · Wonderlog",
"Game Factory / grafica":"Game Factory","Desktop / web utility":"Desktop/Web Utility Factory",
"Security / privacy":"AppLab · security","Automation / scraping / data tools":"ChatGPT · automazione esterna",
"Idea prodotto / utility generale":"Nuova app/feature","Altro / da valutare":"Reference"}

def get_json(url):
    req=urllib.request.Request(url,headers={"User-Agent":"AppFactory-Stars-Audit","Accept":"application/vnd.github+json"})
    with urllib.request.urlopen(req,timeout=30) as r:return json.load(r)

def get_stars():
    out=[]; page=1
    while True:
        x=get_json(f"https://api.github.com/users/{USER}/starred?per_page=100&page={page}")
        if not x:break
        out+=x
        if len(x)<100:break
        page+=1
    return list({r["full_name"]:r for r in out}.values())

def ui_count():
    try:
        req=urllib.request.Request(f"https://github.com/{USER}?tab=stars",headers={"User-Agent":"Mozilla/5.0"})
        h=urllib.request.urlopen(req,timeout=30).read().decode("utf-8","ignore")
        m=re.search(r"Stars\s*<span[^>]*>([0-9,]+)",h,re.I|re.S)
        return int(m.group(1).replace(",","")) if m else None
    except Exception:return None

def classify(r):
    t=(" "+r.get("full_name","")+" "+(r.get("description") or "")+" "+(r.get("language") or "")+" "+" ".join(r.get("topics") or [])+" ").lower()
    m=[]
    for cat,keys in CATS:
        s=sum(2 if k in STRONG else 1 for k in keys if k in t)
        if s:m.append((s,cat))
    m.sort(reverse=True); cat=m[0][1] if m else "Altro / da valutare"
    u=22+min(58,sum(v for v,_ in m[:3])*9)
    if r.get("archived"):u-=8
    if r.get("fork"):u-=2
    stars=r.get("stargazers_count") or 0
    u+=7 if stars>=10000 else 5 if stars>=1000 else 3 if stars>=100 else 0
    p=r.get("pushed_at") or ""
    u+=5 if p>="2025-01-01" else -8 if p and p<"2022-01-01" else 0
    for k,b in [("flutter",12),("android",8),("agent",10),("mcp",10),("scrcpy",15),("shizuku",15),("testing",8),("architecture",8),("pdf",6),("notion",7),("obsidian",7),("tauri",8),("supabase",6),("camera",5),("routing",5)]:
        if k in t:u+=b
    u=max(5,min(99,u))
    e=58; lang=(r.get("language") or "").lower()
    if lang in ("dart","kotlin","java"):e+=16
    elif lang in ("typescript","javascript","python","go","shell"):e+=8
    elif lang in ("rust","c++","c","swift"):e-=6
    if any(k in t for k in ("library","package","sdk","template","boilerplate","cli","api")):e+=8
    if any(k in t for k in ("platform","framework","operating system","browser","engine","server")):e-=7
    if r.get("archived"):e-=10
    if stars>=10000:e+=3
    e=max(10,min(95,e))
    future=FUTURE[cat] if u>=25 else "Scartare dalla Factory attuale: nessun legame concreto individuato."
    deep=u>=82
    if r["full_name"] in OV:u,e,cat,future=OV[r["full_name"]];deep=True
    return {"name":r["full_name"],"url":r["html_url"],"language":r.get("language") or "—","category":cat,"utility":u,"ease":e,"deep":deep,"future":future,"stars":stars,"pushed_at":p}

def slug(s):return re.sub(r"[^a-z0-9]+","-",s.lower()).strip("-")

def main():
    repos=get_stars(); rows=[classify(r) for r in repos]
    shown=ui_count() or len(rows); gap=max(0,shown-len(rows))
    CATALOG.mkdir(exist_ok=True); DATA.mkdir(exist_ok=True)
    for f in CATALOG.glob("*.md"):f.unlink()
    g=defaultdict(list)
    for x in rows:g[x["category"]].append(x)
    for cat,xs in g.items():
        xs.sort(key=lambda x:(x["utility"],x["ease"],x["name"]),reverse=True)
        z=[f"# {cat}","",f"Repo: **{len(xs)}**","","| # | Repo | Utilità | Facilità | Approfondire | Linguaggio | Futuro pratico |","|---:|---|---:|---:|---|---|---|"]
        for i,x in enumerate(xs,1):z.append(f'| {i} | [{x["name"]}]({x["url"]}) | {x["utility"]}% | {x["ease"]}% | {"Sì" if x["deep"] else "No"} | {x["language"]} | {x["future"]} |')
        (CATALOG/f"{slug(cat)}.md").write_text("\n".join(z)+"\n",encoding="utf-8")
    counts=Counter(x["category"] for x in rows)
    top=[x for x in rows if x["name"] in OV]
    top.sort(key=lambda x:(x["utility"],x["ease"],x["stars"]),reverse=True)
    read=["# Analisi delle mie stelle GitHub","","> Registro vivo orientato a App Factory, AppLab, ChatGPT, sviluppo app, automazione e nuove idee prodotto.","","## Stato del censimento","",f"- Ultimo refresh: **{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}**.",f"- Conteggio mostrato dalla pagina GitHub Stars: **{shown}**.",f"- Repository pubbliche enumerabili via API: **{len(rows)} uniche**.",f"- Gap non enumerabile: **{gap}**.",f"- Factory baseline audit iniziale: {FACTORY} — Master v26.6, Golden Index v19.","- Licenze: **non considerate nello scoring**, su richiesta.","","## Metodo","","- **Utilità %**: impatto concreto su programmazione, gestione, velocità, QA, AppLab/App Factory/ChatGPT o nuove app.","- **Facilità integrazione %**: semplicità di adozione senza migrazioni o nuovo debito tecnico.","- **Approfondire**: Sì = merita README/code review mirata; No = catalogo sufficiente finché non emerge un requisito.","- Le schede di DEEP_DIVE.md e questa classifica curatoriale prevalgono sulla sola classificazione automatica dei cataloghi.","","## Distribuzione per categoria","","| Categoria | Repo |","|---|---:|"]
    for c,n in counts.most_common():read.append(f"| {c} | {n} |")
    read+=["","## Priorità operative — valutazione curatoriale","","| Repo | Utilità | Facilità | Destinazione | Futuro pratico |","|---|---:|---:|---|---|"]
    for x in top:read.append(f'| [{x["name"]}]({x["url"]}) | {x["utility"]}% | {x["ease"]}% | {DEST.get(x["category"],"Reference")} | {x["future"]} |')
    read+=["","## Quando serve descrizione ulteriore","","- **Sì / Deep dive**: repo ad alto impatto, tool trasversale, possibile donor/Golden, possibile nuova app o integrazione architetturale.","- **No**: uso chiaro e circoscritto; il record in catalogo basta finché non nasce uno use case concreto.","- **Scartato**: nessun legame concreto con la Factory attuale; non serve investire tempo ora.","","## Struttura","","- DEEP_DIVE.md — schede curatoriate dei repo prioritari.","- catalog/ — tutte le repository pubblicamente enumerabili, con link diretto, punteggi e futuro pratico.","- data/stars_public.json — snapshot strutturato per diff futuri.","- GAP_13.md — divario fra contatore UI e API quando presente.",""]
    (ROOT/"README.md").write_text("\n".join(read),encoding="utf-8")
    deep=["# Deep dive — repo ad alto impatto","","Le schede seguenti sono curatoriate e prevalgono sul solo scoring automatico del catalogo.",""]
    for name in sorted(OV,key=lambda n:OV[n][0],reverse=True):
        x=next((r for r in rows if r["name"]==name),None)
        if x:deep += [f'## [{x["name"]}]({x["url"]})',f'- **Utilità:** {x["utility"]}%',f'- **Facilità integrazione:** {x["ease"]}%',f'- **Categoria:** {x["category"]}',f'- **Destinazione:** {DEST.get(x["category"],"Reference")}',f'- **Futuro pratico:** {x["future"]}',""]
    (ROOT/"DEEP_DIVE.md").write_text("\n".join(deep),encoding="utf-8")
    (ROOT/"GAP_13.md").write_text(f"# Gap di censimento\n\nContatore UI: **{shown}**. API pubblica: **{len(rows)}**. Gap: **{gap}**.\n\nGli elementi non enumerati non vengono inventati né marcati come analizzati. Il requisito finale resta portare il gap a zero quando una sessione autenticata espone i nomi mancanti.\n",encoding="utf-8")
    DATA.joinpath("stars_public.json").write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({"ui_count":shown,"public_unique":len(rows),"gap":gap,"categories":len(g),"deep":sum(x["deep"] for x in rows)},ensure_ascii=False))

if __name__=="__main__":main()

# bootstrap-trigger: 2026-10-25
