from __future__ import annotations
import argparse, subprocess
from pathlib import Path

def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("--tag",required=True); parser.add_argument("--output",required=True); args=parser.parse_args()
    try: files=subprocess.check_output(["git","ls-tree","-r","--name-only",args.tag],text=True).splitlines()
    except Exception: files=[]
    out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(f"# Education V3 final inventory\n\nTag: `{args.tag}`\n\n"+"\n".join(f"- `{item}`" for item in files)+"\n"); return 0
if __name__ == "__main__": raise SystemExit(main())
