import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
import research_agent
class PipelineTests(unittest.TestCase):
 def test_search_results_are_the_only_citable_urls(self):
  calls=[]
  def fake(url,headers,payload):
   calls.append(url)
   if url=="https://api.exa.ai/search":
    return {"results":[{"title":"Official docs","url":"https://vendor.example/docs","text":"OAuth and REST docs"}]}
   return {"choices":[{"message":{"content":'{"description":"API","auth_methods":["oauth2"],"credential_access":"unknown","api_type":"REST","api_breadth":"medium","mcp_status":"unknown","buildability":"caveats","blocker":"Access not established","evidence":[{"url":"https://vendor.example/docs","supports":"OAuth and REST"}]}'}}]}
  research_agent.request_json=fake
  row={"id":1,"app":"Example","category":"Test","description":"Example integration"}
  out=research_agent.research_one(row,"exa-test","llm-test","mock-model","https://llm.example/v1")
  self.assertEqual(out["app_id"],1)
  self.assertFalse(out["live_api_tested"])
  self.assertTrue(out["human_review_required"])
  self.assertEqual(len(out["agent_findings"]["evidence"]),1)
  self.assertEqual(len(calls),2)
 def test_rejects_citations_not_in_search(self):
  def fake(url,headers,payload):
   if url=="https://api.exa.ai/search":return {"results":[{"url":"https://vendor.example/docs","text":"snippet"}]}
   return {"choices":[{"message":{"content":'{"evidence":[{"url":"https://made-up.example","supports":"fabricated"}]}'}}]}
  research_agent.request_json=fake
  with self.assertRaisesRegex(ValueError,"cited URLs not returned"):
   research_agent.research_one({"id":1,"app":"Example","category":"Test"},"x","y","m","https://llm.example/v1")
if __name__=="__main__":unittest.main()
