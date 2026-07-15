from __future__ import annotations
import argparse,json,tempfile
from dataclasses import asdict
from pathlib import Path
from zamery_education_v4.kernel.storage import StoreLayout, RecordStore, rebuild_index
from zamery_education_v4.kernel.records.context import TeachingBrief

def main() -> int:
 p=argparse.ArgumentParser(); p.add_argument("--fixture",default="unit1-lesson1"); p.add_argument("--output"); args=p.parse_args()
 with tempfile.TemporaryDirectory() as root:
  layout=StoreLayout(Path(root)); store=RecordStore(layout.root); store.commit(TeachingBrief(record_id="brief:rebuild",duration_minutes=90,learner_level="A2",source_ids=("source:unit1",)))
  first=rebuild_index(layout.index_path,store,()); layout.index_path.unlink(); second=rebuild_index(layout.index_path,store,())
 report={"fixture":args.fixture,"first":asdict(first),"second":asdict(second),"passed":first==second}; text=json.dumps(report,indent=2,sort_keys=True); print(text)
 if args.output:
  output = Path(args.output); output.parent.mkdir(parents=True, exist_ok=True); output.write_text(text+"\n")
 return 0 if report["passed"] else 1
if __name__=="__main__": raise SystemExit(main())
