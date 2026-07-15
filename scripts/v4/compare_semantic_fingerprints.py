from __future__ import annotations
import argparse,json
from pathlib import Path

def normalized(path: Path) -> dict[str,object]: return json.loads(path.read_text())
def main() -> int:
 p=argparse.ArgumentParser(); p.add_argument("left"); p.add_argument("right"); a=p.parse_args(); same=normalized(Path(a.left))==normalized(Path(a.right)); print("match" if same else "mismatch"); return 0 if same else 1
if __name__=="__main__": raise SystemExit(main())
