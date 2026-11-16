# Confronto vero: censimento stelle 750 / API 737 / OSS95 — 16-11-2026

**Fonte:** GitHub API pubblica, 8 pagine = 737; confronto archivio storico 632 = 110 nuove e 5 precedenti assenti; nel conteggio UI comunicato dall’utente 750 rimangono 13 stelle non enumerabili. Non è accesso API autenticato a /user/starred.

**Dedup storico cruciale:** delle 110 nuove rispetto allo snapshot pubblico, 89 già presenti nella ricerca curata OSS95 dell’8/11/2026; 4 già studiate separatamente (GBrain, Deskland, OpenTaskbar, LumaBar); 17 senza dossier precedente individuato. Non interpretare 110 come 110 CAP nuove.

## Dati di delta

| Metrica | N |
|---|---:|
| total | 110 |
| oss95 | 89 |
| old_oss95_readme_same | 70 |
| old_oss95_changed_or_gap | 19 |
| prior_other | 4 |
| previously_uncatalogued | 17 |

## Le 17 fonti senza dossier individuato prima di oggi

| Fonte | Score | Ambito | App interessata | Licenza metadata |
|---|---:|---|---|---|
| [MobSF/Mobile-Security-Framework-MobSF](https://github.com/MobSF/Mobile-Security-Framework-MobSF) | 98 | QA e sicurezza | AppLab | GPL-3.0 |
| [aquasecurity/trivy](https://github.com/aquasecurity/trivy) | 97 | QA e sicurezza | AppLab | Apache-2.0 |
| [github/codeql](https://github.com/github/codeql) | 96 | QA e sicurezza | AppLab | MIT |
| [semgrep/semgrep](https://github.com/semgrep/semgrep) | 95 | QA e sicurezza | AppLab | LGPL-2.1 |
| [OpenHands/OpenHands](https://github.com/OpenHands/OpenHands) | 94 | Agenti e App Factory | App-Factory-Agent-Core | MIT |
| [alztrk/OpenWidget](https://github.com/alztrk/OpenWidget) | 89 | Desktop e widget | App Factory Control Center | MIT |
| [zaproxy/zaproxy](https://github.com/zaproxy/zaproxy) | 84 | QA e sicurezza | AppLab | Apache-2.0 |
| [ai-boost/awesome-image-video-prompts](https://github.com/ai-boost/awesome-image-video-prompts) | 81 | Design e workflow visuale | Notes-Ecosistema | GPL-3.0 |
| [tonhowtf/omniget](https://github.com/tonhowtf/omniget) | 81 | Agenti e App Factory | App-Factory-Agent-Core | GPL-3.0 |
| [greenbone/openvas-scanner](https://github.com/greenbone/openvas-scanner) | 75 | QA e sicurezza | AppLab | GPL-2.0 |
| [onmyway133/Promptberry](https://github.com/onmyway133/Promptberry) | 75 | Agenti e App Factory | App-Factory-Agent-Core | MIT |
| [SonarSource/sonarqube](https://github.com/SonarSource/sonarqube) | 74 | QA e sicurezza | AppLab | LGPL-3.0 |
| [exo-explore/exo](https://github.com/exo-explore/exo) | 71 | Agenti e App Factory | App-Factory-Agent-Core | Apache-2.0 |
| [PaoloJN/recap](https://github.com/PaoloJN/recap) | 65 | Produttivita e privacy | FocuSense | MIT |
| [SunshineStream/Sunshine](https://github.com/SunshineStream/Sunshine) | 55 | Desktop e widget | Send-to-PC | GPL-3.0 |
| [20220402jp-coder/attendance-management-system](https://github.com/20220402jp-coder/attendance-management-system) | 40 | Non pertinente | Nessuna | NOASSERTION |
| [Cracked5pider/Ekko](https://github.com/Cracked5pider/Ekko) | 10 | Non pertinente | Nessuna | NOASSERTION |

## 19 fonti OSS95 con README cambiato o precedente non registrato

Il cambio SHA README NON prova differenze funzionali né modifica di codice. Le fonti che avevano hash storico assente richiedono semplicemente una prima baseline comparabile.

- [codexu/note-gen](https://github.com/codexu/note-gen) — blob README attuale 397ca483970face5c33ec6f798a88d47388930f2
- [siyuan-note/siyuan](https://github.com/siyuan-note/siyuan) — blob README attuale ad72a90695ddd4212ee3a7d21285c6948373a0a6
- [baserow/baserow](https://github.com/baserow/baserow) — blob README attuale 3c434cf485fe316d2bc4a25e065fe51361a3871e
- [saber-notes/saber](https://github.com/saber-notes/saber) — blob README attuale 856cf7654f552157f8aa79f03c4683abce8c431c
- [LifetimeLabsHQ/PrivacyNotes.app](https://github.com/LifetimeLabsHQ/PrivacyNotes.app) — blob README attuale f06898951cd5291b406955cffdd0ed5110189230
- [Zackriya-Solutions/meetily](https://github.com/Zackriya-Solutions/meetily) — blob README attuale c4712d787a32b8e0b67b4fc8a0c80850ff909a55
- [OrangeCatzhang/orange-schedule](https://github.com/OrangeCatzhang/orange-schedule) — blob README attuale 2f086e2c486a31e98bc5413b7c1152ae7c7e3fab
- [foambubble/foam](https://github.com/foambubble/foam) — blob README attuale a504233dcefb32f2623d5d0dd1aff85f5cfc0020
- [vnotex/vnote](https://github.com/vnotex/vnote) — blob README attuale 73027764924015786211d222292132397d2d4dcb
- [makeplane/plane](https://github.com/makeplane/plane) — blob README attuale cbfc816629b866da6a8a2f46f10e9bea28bbcd1b
- [nocodb/nocodb](https://github.com/nocodb/nocodb) — blob README attuale 5ea4f2339115f2ca070d9b960628aa528ec88460
- [cryptpad/cryptpad](https://github.com/cryptpad/cryptpad) — blob README attuale 3eede8d6284cfa90b5ceeaf3f86d58d42e716848
- [xyflow/xyflow](https://github.com/xyflow/xyflow) — blob README attuale 074ae40c29e2893f6cdd4ded544e6bdabfa45707
- [jazzband/Watson](https://github.com/jazzband/Watson) — blob README attuale 3b51437ec610ba410ba481fcf3a98249d8779be5
- [bzg/org-mode](https://github.com/bzg/org-mode) — blob README attuale e72403b6889bed1ec42cc93a54455d30ce596793
- [gristlabs/grist-core](https://github.com/gristlabs/grist-core) — blob README attuale fae5fa1365bf85fb807c2795609719465d10e456
- [yjs/yjs](https://github.com/yjs/yjs) — blob README attuale 4b265183f5b254192a8bd74bf843cfbb3098df79
- [BookStackApp/BookStack](https://github.com/BookStackApp/BookStack) — blob README attuale 297d26559871362356f6a5d210424e1a45f159dc
- [seatable/seatable](https://github.com/seatable/seatable) — blob README attuale a92f8772111039049cbc617058b1786b9063ad03

## Cinque repository precedenti non presenti nell'insieme pubblico attuale

Nessuno viene dichiarato unstar senza evidenza autenticata.

- ai-boost/awesome-gpts
- lizardbyte/sunshine
- oneshot-repo/oneshot
- paolojn/youtube-ai-extension
- zoicware/removewindowsai

## Regole di ammissione

La classifica [curata 110](CLASSIFICA_CURATA_110_2026-11-16.md) è E0: punteggi di opportunità, non probabilità. Le 17 nuove hanno README e metadati verificati, non audit codice/CI o licenze per file. Non creare doppioni di CAP già catalogate in Idee-app-Archivi-riferimenti (per esempio CAP-0031, CAP-0098, CAP-0112, CAP-0144, CAP-0161, CAP-0167, CAP-0182) senza diff del requisito e ammissione prodotto.
