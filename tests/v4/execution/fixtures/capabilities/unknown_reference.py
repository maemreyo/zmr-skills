import json,sys
payload=json.load(sys.stdin)
json.dump({"protocol_version":"zamery-capability.v1","status":"failure","invocation_id":payload["invocation_id"],"failure_code":"UNKNOWN_REFERENCE","message":"reference missing","retryable":False,"affected_ids":["unknown:1"]},sys.stdout)
