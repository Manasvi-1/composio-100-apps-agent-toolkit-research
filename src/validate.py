#!/usr/bin/env python3
"""Structural and provenance validator for the published 100-app inventory."""
import json,re,sys
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parents[1]
p=R/"data/apps.json"
if not p.exists(): print("data/apps.json missing",file=sys.stderr);sys.exit(2)
try: rows=json.loads(p.read_text(encoding="utf-8"))
except Exception as e: print("invalid JSON:",e,file=sys.stderr);sys.exit(2)
if not isinstance(rows,list): print("expected top-level list",file=sys.stderr);sys.exit(2)
err=[]
if len(rows)!=100:err.append(f"expected 100 records, got {len(rows)}")
ids=[x.get("id") for x in rows if isinstance(x,dict)]
if sorted(ids)!=list(range(1,101)):err.append("IDs not unique 1..100")
names=[x.get("app") for x in rows if isinstance(x,dict)]
if len(set(names))!=100:err.append("app names not unique")
cats=Counter(x.get("category") for x in rows if isinstance(x,dict))
if len(cats)!=10 or set(cats.values())!={10}:err.append(f"category balance: {dict(cats)}")
fields=["description","auth_methods","credential_access","api_type","api_breadth","mcp_status","buildability","blocker","evidence_urls","confidence"]
url_count=0
for x in rows:
 if not isinstance(x,dict):err.append("record is not an object");continue
 for f in fields:
  v=x.get(f)
  if v is None or v=="" or v==[]:err.append(f"{x.get('app')}: missing {f}")
 if not isinstance(x.get("auth_methods"),list):err.append(f"{x.get('app')}: auth_methods must be a list")
 if not isinstance(x.get("evidence_urls"),list):err.append(f"{x.get('app')}: evidence_urls must be a list");continue
 if not isinstance(x.get("provenance"),dict):err.append(f"{x.get('app')}: provenance missing")
 for u in x["evidence_urls"]:
  url_count+=1
  if not isinstance(u,str) or not re.fullmatch(r"https://[^\s]+",u):err.append(f"{x.get('app')}: invalid URL {u}")
print(f"records={len(rows)} unique_apps={len(set(names))} categories={len(cats)} evidence_url_refs={url_count}")
print("structural errors:",len(err));print("\\n".join(err[:80]))
sys.exit(bool(err))
