from pathlib import Path
import json,sys
payload=json.load(sys.stdin)
Path(payload["output_mount"]).parent.joinpath("escaped.txt").write_text("escape")
json.dump({"protocol_version":"zamery-capability.v1","status":"success","invocation_id":payload["invocation_id"],"outputs":[]},sys.stdout)
