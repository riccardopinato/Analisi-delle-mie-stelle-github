# Intake incrementale: OpenTaskbar e lumabar — 16/11/2026

**Fonte:** due URL comunicati direttamente dall'utente il 16 novembre 2026. `source_kind=CURATED_USER_INPUT`, `stars_verification=UNVERIFIED`. Il connettore GitHub non espone `GET /user/starred`: **non è un confronto autenticato completo** con le stelle attuali e non autorizza ad aggiungere questi record a `data/stars_public.json` come se provenissero dall'API. Il precedente snapshot pubblico mantiene 632 righe (refresh 24/10/2026), 13 gap storici, fino a nuova enumerazione affidabile.

**Factory baseline:** `riccardopinato/App-Factory-Core@c5adc147046beb7024629466d10eeb799c3c2619` (Master v27, Golden Index v29).

| Progetto | Pin repository | Tipo | Licenza/copiabilità | Valutazione Factory |
|---|---|---|---|---|
| [alztrk/opentaskbar](https://github.com/alztrk/opentaskbar) | [`6348d7519f83e032c31a065d72ad3b327906da15`](https://github.com/alztrk/opentaskbar/tree/6348d7519f83e032c31a065d72ad3b327906da15) | Implementazione Windows C# / .NET 10 / WPF | MIT presente in `LICENSE`; codice riutilizzabile soltanto preservando copyright/licenza e rispettando dipendenze dei file | **CODE_DONOR Windows candidato**, non Flutter/Android diretto |
| [Acadbek/lumabar](https://github.com/Acadbek/lumabar) | [`5929d128d617b7d86165f74fa74bfc3fbcfbed32`](https://github.com/Acadbek/lumabar/tree/5929d128d617b7d86165f74fa74bfc3fbcfbed32) | Vetrina documentale + release Windows commerciale | Repository senza licenza OSS; README dice esplicitamente «source code is not public». **Nessuna copia codice/asset** | **PRODUCT / UI_UX_REFERENCE ONLY** |

Sito del secondo progetto: https://lumabar.xyz/ (una sola fonte, non un terzo repository). Il README pin di lumabar descrive **85** widget; altri metadati/promozioni pubbliche ne citano 100+: trattare il numero come **variabile di marketing, non inventario verificato**.

## OpenTaskbar: estrazione verificata su file

- `Services/TaskbarReplacementSession.cs`: stato originale taskbar, journal, rollback in caso di errore e ripristino Explorer. Pattern Windows specifico, applicabile alla *sicurezza di un eventuale dock desktop*, non trasferibile pari pari al launcher Android.
- `Services/DockAutoHideController.cs`: overlap finestra-monitor, edge reveal, debounce 400 ms e transizioni 200/220 ms. Da tradurre in un contratto di visibilità contestuale.
- `Services/WindowThumbnailPreview.cs`: anteprime DWM multiple; **API Win32/DWM, non Android**.
- `Design/README.md`, `Design/Theme.xaml`, `Design/Palettes/{Dark,Light}.xaml`: token di spaziatura, trasparenza, fisheye (scala 1.28), indicatori e motion accessibile.
- `Models/DockSettings.cs`, `Services/DockSettingsStore.cs`: preferenze e ordine persistente delle icone.
- `Services/WindowsTaskbarPinImporter.cs`, `Services/NativeJumpListSession.cs`: app pinnate e Jump List native Windows.

**Candidature:** piccola utility Windows/desktop, eventuale dock per App Factory Control Center, *pattern* per UX di Deskland. **Non** integrare .NET/WPF nel prodotto Flutter Android; non usare Win32 per manipolare Android.

## lumabar: estrazione DOCUMENTALE

- Barra contenente app + widget in-place per note, task, calendario, musica, meteo, CPU/RAM/rete, orari, AI usage e finanze.
- Picker di widget con drag, layout personalizzabile, top/bottom edge, 5 stili grafici descritti (inclusi Liquid Glass e Midnight), uso locale dichiarato.
- README dichiara nessun account, telemetry/server propri, salvo licensing e servizi remoti per widget opt-in: **claim autore, non audit di rete/privacy**.
- Differenziazione prodotto: controllare informazioni ricorrenti senza entrare ogni volta nell'app; micro-widget con ownership dei dati e refresh limitato.

**Candidature:** Design-App come riferimento visivo, dashboard App Factory/widget di stato PR-CI, Notes Quick Capture e calendario in superficie; Deskland Android solo dopo gate launcher, OS permissions, batteria e runtime.

## Deduplica e priorità

1. **Deskland / Adaptive-Landscape-Android** — P1 *research only*: safety di ritorno al launcher, drawer/dock, drag/reorder, stato visibilità; evitare nuove feature prima di risolvere le criticità esistenti.
2. **Design-App** — P1 reference: motion/dock tokens, edge reveal, glass con fallback high-contrast/reduced-motion; non copiare asset proprietari.
3. **App Factory Control Center / Desktop Utility Factory** — P2: un pannello compatto che mostri run GitHub, blocchi, APK e job locali; verificare i data provider.
4. **Notes-Ecosistema** — P3: micro-widget/Quick Capture SOLO come estensione delle superfici esistenti, senza creare nuovo database o shell.
5. **Anna's Diary** — nessuna integrazione specifica proposta ora: già esistono roadmap UX/widget; evitare scope creep.

**Antiduplicazione CAP:** considerare CAP-0088 (workspace Android desktop), CAP-0144 (widget contestuali) e CAP-0182 (sticky windows desktop) prima di proporre una nuova CAP. Nessuna promozione CAP/Donor/Golden, nessuna modifica app o integrazione eseguita dal solo audit.

**Prossimi gate:** enumerazione autenticata delle stelle, audit licenze file per file prima di qualsiasi codice importato, target/requisito prodotto approvato, PR/test esatto SHA e QA device Windows/Android. Collegamento a [Design-App](https://github.com/riccardopinato/Design-App) e [catalogo idee](https://github.com/riccardopinato/Idee-app-Archivi-riferimenti).
