#!/usr/bin/env python3
"""Audit arithmetic and referential integrity for the recorded 13-app review."""
import json, re, sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
review=json.loads((R/"audit/sample_review.json").read_text(encoding="utf-8"))
apps=json.loads((R/"data/apps.json").read_text(encoding="utf-8"))
by_id={x["id"]:x for x in apps}
errors=[]
records=review.get("records",[])
if len(records)!=13: errors.append(f"expected 13 reviewed apps, found {len(records)}")
counts={"confirmed":0,"corrected":0,"not_established":0,"other":0}
seen=set()
for rec in records:
    aid=rec.get("app_id")
    if aid not in by_id: errors.append(f"{rec.get('app')}: app_id {aid} not in inventory"); continue
    if by_id[aid]["app"]!=rec.get("app"): errors.append(f"app/id mismatch: {aid} {rec.get('app')}")
    if aid in seen: errors.append(f"duplicate review app_id {aid}")
    seen.add(aid)
    for check in rec.get("field_checks",[]):
        status=check.get("source_review_status","other")
        counts[status if status in counts else "other"]+=1
        for url in check.get("evidence_urls",[]):
            if not isinstance(url,str) or not url.startswith("https://") or " " in url: errors.append(f"invalid review evidence URL: {url}")
summary=review.get("summary",{})
reported={"confirmed":summary.get("first_pass_supported"),"corrected":summary.get("first_pass_corrected"),"not_established":summary.get("not_established_or_unscored")}
for k,v in reported.items():
    if counts[k]!=v: errors.append(f"{k}: actual {counts[k]}, summary {v}")
resolved=counts["confirmed"]+counts["corrected"]
if resolved!=summary.get("source_resolvable_claims"): errors.append(f"source-resolvable claims: actual {resolved}, summary {summary.get('source_resolvable_claims')}")
if sum(counts.values())!=summary.get("field_claims"): errors.append("field claim totals don't reconcile")
if "not external human" not in review.get("source","").lower(): errors.append("review provenance must state it was not external human sign-off")
print(f"reviewed_apps={len(records)} field_claims={sum(counts.values())} confirmed={counts['confirmed']} corrected={counts['corrected']} not_established={counts['not_established']} source_resolvable={resolved}")
print("audit arithmetic: PASS" if not errors else "audit arithmetic: FAIL")
for e in errors: print("ERROR:",e)
if "--write" in sys.argv:
    out={"source_file":"audit/sample_review.json","reviewed_apps":len(records),"field_claims":sum(counts.values()),"first_pass_supported":counts["confirmed"],"first_pass_corrected":counts["corrected"],"not_established":counts["not_established"],"source_resolvable_claims":resolved,"first_pass_agreement":counts["confirmed"]/resolved if resolved else None,"post_correction_source_alignment":1.0 if resolved else None,"interpretation":"Selected 13-app assistant-assisted source review; not independent human/statistical accuracy.","validation":"passed" if not errors else "failed"}
    (R/"audit/verification_summary.json").write_text(json.dumps(out,indent=2)+chr(10),encoding="utf-8")
sys.exit(bool(errors))
