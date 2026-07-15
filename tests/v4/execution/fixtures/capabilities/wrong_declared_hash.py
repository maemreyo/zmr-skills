import json,sys
payload=json.load(sys.stdin)
json.dump({"protocol_version":"zamery-capability.v1","status":"success","invocation_id":payload["invocation_id"],"outputs":[{"output_type":"record","path":"record.json","declared_hash":"sha256:"+"0"*64,"record_type":"teaching_brief"}]},sys.stdout)
