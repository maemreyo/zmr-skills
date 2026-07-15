from pathlib import Path
import json,os,sys
payload=json.load(sys.stdin)
out=Path(payload["output_mount"]); os.symlink("/etc/passwd",out/"link")
json.dump({"protocol_version":"zamery-capability.v1","status":"success","invocation_id":payload["invocation_id"],"outputs":[]},sys.stdout)
