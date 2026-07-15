from __future__ import annotations
import argparse,json,tempfile
from pathlib import Path
from zamery_education_v4.testing import GoldenRunner

def main() -> int:
 p=argparse.ArgumentParser(); p.add_argument("--fixture",default="unit1-lesson1"); p.add_argument("--output"); args=p.parse_args()
 with tempfile.TemporaryDirectory() as left, tempfile.TemporaryDirectory() as right:
  first=GoldenRunner().run_production(args.fixture); second=GoldenRunner().run_production(args.fixture)
  report={"fixture":args.fixture,"left_workspace":Path(left).name,"right_workspace":Path(right).name,"graph_hash_match":first.graph_hash==second.graph_hash,"gate_subject_match":first.gate_decisions==second.gate_decisions,"semantic_fingerprint_match":first.deliverables==second.deliverables}
 report["passed"]=all(v for k,v in report.items() if k.endswith("match")); text=json.dumps(report,indent=2,sort_keys=True); print(text)
 if args.output:
  output = Path(args.output); output.parent.mkdir(parents=True, exist_ok=True); output.write_text(text+"\n")
 return 0 if report["passed"] else 1
if __name__=="__main__": raise SystemExit(main())
