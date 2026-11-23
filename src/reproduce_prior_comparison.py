#!/usr/bin/env python3
"""Reproduce blind-prior concordance against transcript labels (not factual accuracy)."""
import hashlib, json, sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
record=json.loads((R/"audit/blind_priors.json").read_text(encoding="utf-8"))
p=record["priors"]
canonical=json.dumps(p,sort_keys=True).encode("utf-8")
digest=hashlib.sha256(canonical).hexdigest()
print("stored SHA-256:",record["sha256"])
print("recomputed SHA-256:",digest)
if digest != record["sha256"]:
    print("ERROR: prior payload does not match recorded hash",file=sys.stderr);sys.exit(2)
d=json.loads((R/"data/apps.json").read_text(encoding="utf-8"));by={x["app"]:x for x in d}
alias={"NotebookLM":"NotebookLM (Gemini Notebook)"}
access={"self_serve_free":"free","paid_plan":"paid","admin_approval":"admin","partner_gated":"partner"}
verdict={"build_now":"now","build_caveats":"caveats","outreach":"outreach"}
exclude={("Otter AI","mcp"),("Consensus","auth"),("Consensus","mcp"),("Grain","access"),("Ahrefs","mcp")} | {("Waterfall.io",f) for f in ("auth","access","api","mcp","verdict")}
hit=total=0;miss=[]
for app,prior in p.items():
    row=by.get(alias.get(app,app))
    if row is None: raise SystemExit(f"Prior app absent from normalized inventory: {app}")
    for field,value in prior.items():
        if (app,field) in exclude or value=="hint" or value=="unknown": continue
        total+=1
        if field=="auth":
            a=value.lower();need=set()
            if "oauth" in a: need.add("oauth2")
            if "api key" in a: need.add("api_key")
            if "basic" in a: need.add("basic")
            if "jwt" in a or "key-pair" in a: need.add("jwt_keypair")
            ok=bool(need) and need<=set(row["auth_methods"])
        elif field=="access": ok=access.get(value,value)==row["credential_access"]
        elif field=="api": ok=value==row["api_type"] or (value=="REST" and row["api_type"]=="REST+GraphQL")
        elif field=="mcp": ok=value==row["mcp_status"]
        else: ok=verdict.get(value,value)==row["buildability"]
        hit+=int(ok)
        if not ok: miss.append({"app":app,"field":field,"prior":value,"transcript_label":row.get({"auth":"auth_methods","access":"credential_access","api":"api_type","mcp":"mcp_status","verdict":"buildability"}[field])})
print(f"{hit}/{total} = {hit/total:.1%} agreement with transcript labels; NOT factual accuracy")
print("Disagreements:",len(miss))
print(json.dumps(miss,indent=2))
