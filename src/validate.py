#!/usr/bin/env python3
import json,re,sys
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parents[1]
p=R/"data/apps.json"
if not p.exists():
 print("Normalized findings file missing; publication gate not met.",file=sys.stderr);sys.exit(2)
rows=json.loads(p.read_text());err=[]
if len(rows)!=100:err.append(f"expected 100 records, got {len(rows)}")
if sorted(x.get("id") for x in rows)!=list(range(1,101)):err.append("IDs not unique 1..100")
if len({x.get("app") for x in rows})!=100:err.append("app names not unique")
cats=Counter(x.get("category") for x in rows)
if len(cats)!=10 or set(cats.values())!={10}:err.append(f"category balance: {dict(cats)}")
fields=["description","auth_methods","credential_access","api_type","api_breadth","mcp_status","buildability","blocker","evidence_urls","confidence"]
for x in rows:
 for f in fields:
  if not x.get(f):err.append(f"{x.get('app')}: missing {f}")
 for u in x.get("evidence_urls",[]):
  if not re.match(r"^https://[^\\s]+$",u):err.append(f"{x.get('app')}: invalid URL {u}")
print(f"rows={len(rows)} unique={len(set(x['app'] for x in rows))} categories={len(cats)} evidence_urls={sum(len(x['evidence_urls']) for x in rows)}")
print("structural errors:",len(err));print("\\n".join(err[:50]))
sys.exit(bool(err))
