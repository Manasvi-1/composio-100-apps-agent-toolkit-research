#!/usr/bin/env python3
"""Reproduces prior-vs-transcript label concordance. Not ground-truth accuracy."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
p=json.loads((R/"audit/blind_priors.json").read_text())
d=json.loads((R/"data/apps.json").read_text());by={x["app"]:x for x in d}
alias={"NotebookLM":"NotebookLM (Gemini Notebook)"}
access={"self_serve_free":"free","paid_plan":"paid","admin_approval":"admin","partner_gated":"partner"}
verdict={"build_now":"now","build_caveats":"caveats","outreach":"outreach"}
exclude={("Otter AI","mcp"),("Consensus","auth"),("Consensus","mcp"),("Grain","access"),("Ahrefs","mcp")} | {("Waterfall.io",f) for f in ("auth","access","api","mcp","verdict")}
hit=total=0;miss=[]
for app,prior in p["priors"].items():
 row=by[alias.get(app,app)]
 for f,v in prior.items():
  if (app,f) in exclude or v=="hint":continue
  total+=1
  if f=="auth":
   a=v.lower();need=set()
   if "oauth" in a:need.add("oauth2")
   if "api key" in a or ("token" in a and "jwt" not in a):need.add("api_key")
   if "basic" in a:need.add("basic")
   if "jwt" in a or "key-pair" in a:need.add("jwt_keypair")
   ok=bool(need) and need<=set(row["auth_methods"])
  elif f=="access":ok=access.get(v,v)==row["credential_access"]
  elif f=="api":ok=v==row["api_type"] or (v=="REST" and row["api_type"]=="REST+GraphQL")
  elif f=="mcp":ok=v==row["mcp_status"]
  else:ok=verdict.get(v,v)==row["buildability"]
  hit+=ok
  if not ok:miss.append({"app":app,"field":f,"prior":v,"transcript":row.get(f)})
print(f"{hit}/{total} = {hit/total:.1%} agreement with transcript labels; NOT factual accuracy")
print("Disagreements:",len(miss));print(json.dumps(miss,indent=2))
