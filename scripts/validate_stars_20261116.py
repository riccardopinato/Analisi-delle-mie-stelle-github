#!/usr/bin/env python3
"""Structural/data provenance gate for one-time stars census."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name):
    return json.loads((ROOT/name).read_text(encoding="utf-8"))
old=load("data/stars_public.json")
live=load("data/stars_current_2026-11-16.json")
delta=load("data/stars_delta_2026-11-16.json")
curated=load("data/stars_curated_2026-11-16.json")
xref=load("data/stars_crosswalk_oss95_2026-11-16.json")
def unique(a,key):
    names=[x[key].casefold() for x in a]
    assert len(names)==len(set(names)), ("DUPLICATE",key)
def same_set(a,b,key1,key2):
    assert {x[key1].casefold() for x in a}=={x[key2].casefold() for x in b}
unique(old,"name")
unique(live["repositories"],"name")
unique(delta["new_public"],"name")
unique(curated["records"],"repo")
unique(xref["records"],"repo")
assert len(old)==632
assert len(live["repositories"])==737
assert len(delta["new_public"])==110
assert len(curated["records"])==110
assert len(xref["records"])==110
same_set(delta["new_public"],curated["records"],"name","repo")
same_set(delta["new_public"],xref["records"],"name","repo")
assert sum(1 for x in live["repositories"] if x["snapshot_state"]=="STILL_PUBLIC_HISTORICAL")==627
assert len(delta["old_missing"])==5
assert sum(delta["summary"]["page_sizes"])==737
assert delta["summary"]["gap_from_user_report"]==13
assert delta["summary"]["readmes_checked"]==110
assert xref["counts"]=={
  "total":110,"oss95":89,"old_oss95_readme_same":70,
  "old_oss95_changed_or_gap":19,"prior_other":4,"previously_uncatalogued":17}
assert sum(curated["metadata"]["domain_counts"].values())==110
assert sum(curated["metadata"]["priority_counts"].values())==110
for r in curated["records"]:
    assert r["product_decision"]=="DA_VALUTARE" and r["code_integrated"] is False
    assert r["source_sha"] and len(r["source_sha"])==40
    assert r["readme_blob_sha"] and len(r["readme_blob_sha"])==40
for p in ["research/STARS_INCREMENTAL_2026-11-16.md",
          "research/CLASSIFICA_CURATA_110_2026-11-16.md",
          "research/INCROCIO_OSS95_2026-11-16.md",
          "research/STARS_ALL_2026-11-16.md"]:
    assert (ROOT/p).is_file(),p
print("STAR_750_AUDIT_VALIDATION_PASS public=737 new=110 curated=110 OSS95=89 prior=4 uncatalogued=17")
