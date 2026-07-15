from __future__ import annotations
import argparse,json,platform
from importlib.metadata import distributions
from pathlib import Path

def main() -> int:
 parser=argparse.ArgumentParser(); parser.add_argument("--output",required=True); args=parser.parse_args()
 components=[{"type":"library","name":d.metadata.get("Name",d.metadata.get("Summary","unknown")),"version":d.version} for d in distributions()]
 components.extend({"type":"capability","name":json.loads(p.read_text())["capability_id"],"version":json.loads(p.read_text())["capability_version"]} for p in Path("capabilities").rglob("manifest.json"))
 doc={"bomFormat":"CycloneDX","specVersion":"1.5","version":1,"metadata":{"python":platform.python_version()},"components":sorted(components,key=lambda x:(x["type"],x["name"],x.get("version","")))}
 out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(doc,indent=2,sort_keys=True)); print(out); return 0
if __name__=="__main__": raise SystemExit(main())
