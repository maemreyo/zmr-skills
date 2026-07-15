from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml
from zamery_education_v4.application.cutover import PipelineConfig, switch_pipeline

def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("--mode",required=True); parser.add_argument("--verification"); parser.add_argument("--reason",required=True); parser.add_argument("--actor",default="operator"); parser.add_argument("--commit",default="working-tree"); parser.add_argument("--accept-canary",action="store_true"); parser.add_argument("--config",default="config/education-pipeline.yaml")
    args=parser.parse_args(); path=Path(args.config); current=PipelineConfig.model_validate(yaml.safe_load(path.read_text()))
    report_hash=None
    if args.verification:
        from zamery_education_v4.kernel.hashing import sha256_file
        report_hash=sha256_file(args.verification)
    updated=switch_pipeline(current,mode=args.mode,commit=args.commit,verification_report_hash=report_hash,actor=args.actor,reason=args.reason,canary_accepted=args.accept_canary)
    path.write_text(yaml.safe_dump(updated.model_dump(mode="json"),sort_keys=True)); print(updated.model_dump_json(indent=2)); return 0
if __name__ == "__main__": raise SystemExit(main())
