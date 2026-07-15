import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

let input=""; for await (const chunk of process.stdin) input += chunk;
const inv=JSON.parse(input);
function normalize(value){
  if(typeof value === "string") return value.normalize("NFC");
  if(Array.isArray(value)) return value.map(normalize);
  if(value && typeof value === "object") return Object.fromEntries(Object.keys(value).sort().map(k=>[k.normalize("NFC"),normalize(value[k])]));
  return value;
}
const record={record_type:"source",schema_version:"4.0.0",record_id:"source:echo",title:"Echo",authority:"reference",source_kind:"reference"};
const payload=JSON.stringify(normalize(record));
const digest="sha256:"+crypto.createHash("sha256").update(Buffer.from(payload)).digest("hex");
fs.writeFileSync(path.join(inv.output_mount,"echo.json"), payload);
process.stdout.write(JSON.stringify({protocol_version:"zamery-capability.v1",status:"success",invocation_id:inv.invocation_id,outputs:[{output_type:"echo_record",path:"echo.json",declared_hash:digest,record_type:"source"}],metrics:{}}));
