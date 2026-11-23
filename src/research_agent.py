#!/usr/bin/env python3
"""Evidence-first Exa + OpenAI-compatible research runner; preserves source inventory."""
import argparse, json, os, time, urllib.request, urllib.error
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT_FIELDS=["description","auth_methods","credential_access","api_type","api_breadth","mcp_status","buildability","blocker","evidence"]
def request_json(url,headers,payload,retries=4):
    body=json.dumps(payload).encode()
    for attempt in range(retries):
        req=urllib.request.Request(url,data=body,headers={**headers,"Content-Type":"application/json"},method="POST")
        try:
            with urllib.request.urlopen(req,timeout=90) as res:return json.loads(res.read())
        except urllib.error.HTTPError as e:
            if e.code not in (429,500,502,503,504) or attempt==retries-1: raise
            time.sleep(min(2**attempt,20))
        except (urllib.error.URLError,TimeoutError):
            if attempt==retries-1: raise
            time.sleep(min(2**attempt,20))
def research_one(app,exa_key,llm_key,model,base):
    query=f"{app['app']} official developer API authentication API credentials pricing trial MCP server documentation"
    search=request_json("https://api.exa.ai/search",{"x-api-key":exa_key},{"query":query,"type":"auto","numResults":8,"contents":{"text":{"maxCharacters":3500}}})
    hits=search.get("results",[])
    context=[{"title":h.get("title",""),"url":h.get("url",""),"text":h.get("text","")} for h in hits]
    prompt=("Research the named integration using ONLY the retrieved source snippets. Prefer official vendor docs; mark unknown rather than infer. "
      "Credential access must distinguish free/trial from paid/admin/partner gates. API and MCP statements require explicit source support. "
      "Return a JSON object with description, auth_methods (array), credential_access, api_type, api_breadth, mcp_status, buildability, blocker, "
      "and evidence (array of {url, supports}). Cite only URLs present in supplied results; if evidence is absent, state unknown. "
      "Keep source snippets and uncertainty; do not claim the API endpoint itself was tested.\nAPP: "+json.dumps(app,ensure_ascii=False)+"\nSOURCES: "+json.dumps(context,ensure_ascii=False))
    answer=request_json(base.rstrip("/")+"/chat/completions",{"Authorization":"Bearer "+llm_key},{"model":model,"temperature":0,"response_format":{"type":"json_object"},"messages":[{"role":"system","content":"You are a careful API integration researcher. No unsupported claims."},{"role":"user","content":prompt}]})
    text=answer["choices"][0]["message"]["content"]
    try: result=json.loads(text)
    except json.JSONDecodeError as e: raise ValueError(f"model did not return valid JSON for {app['app']}: {e}")
    allowed={x["url"] for x in context}
    invalid=[x.get("url") for x in result.get("evidence",[]) if x.get("url") not in allowed]
    if invalid: raise ValueError(f"model cited URLs not returned by search for {app['app']}: {invalid}")
    return {"app_id":app["id"],"app":app["app"],"category":app["category"],"retrieved_at_utc":datetime.now(timezone.utc).isoformat(),"query":query,"search_results":context,"agent_findings":result,"human_review_required":True,"live_api_tested":False}
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--limit",type=int,default=100);ap.add_argument("--start",type=int,default=1);ap.add_argument("--dry-run",action="store_true")
    ap.add_argument("--output",default=None);args=ap.parse_args()
    rows=json.loads((ROOT/"data/apps.json").read_text(encoding="utf-8"))
    chosen=[r for r in rows if r["id"]>=args.start][:args.limit]
    if args.dry_run:
        print(f"dry-run: {len(chosen)} app jobs; first={chosen[0]['app'] if chosen else 'none'}; no network/API calls")
        return
    exa=os.getenv("EXA_API_KEY");key=os.getenv("OPENAI_API_KEY")
    if not exa or not key: raise SystemExit("Set EXA_API_KEY and OPENAI_API_KEY; research runner does not silently fabricate results.")
    model=os.getenv("OPENAI_MODEL","gpt-4.1-mini");base=os.getenv("OPENAI_BASE_URL","https://api.openai.com/v1")
    out=Path(args.output) if args.output else ROOT/"research_runs"/(datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")+"_findings.jsonl")
    out.parent.mkdir(parents=True,exist_ok=True)
    with out.open("a",encoding="utf-8") as f:
        for i,app in enumerate(chosen,1):
            record=research_one(app,exa,key,model,base);f.write(json.dumps(record,ensure_ascii=False)+"\n");f.flush()
            print(f"[{i}/{len(chosen)}] {app['app']} evidence={len(record['agent_findings'].get('evidence',[]))} review=required")
    print("Wrote candidate agent findings:",out)
if __name__=="__main__":main()
