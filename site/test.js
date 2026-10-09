// Headless smoke tests for CodeDium, using Node's built-in APIs only.
"use strict";
const fs=require("node:fs"),vm=require("node:vm"),assert=require("node:assert/strict");
const html=fs.readFileSync("site/index.html","utf8");
const script=html.match(/<script>([\s\S]*?)<\/script>/);
assert(script,"Expected one inline application script");
const initial={
 "app-id":"my-first-app","app-name":"My First App","app-version":"1.0.0",
 "app-summary":"A tiny FalconOS application",
 "source":"# CodeDium example\nclear\necho Hello from CodeDium\nuname\ndate\n"
};
const nodes=new Map(), clicks=[];
function element(id){
 if(!nodes.has(id)) nodes.set(id,{
   value: initial[id]??"", textContent:"", files:[],
   classList:{toggle(){}}, replaceChildren(){}, append(){},
   click(){clicks.push({download:this.download,href:this.href})}, remove(){},
   setAttribute(){}, getAttribute(){return null}
 });
 return nodes.get(id);
}
const context=vm.createContext({
 document:{getElementById:element,createElement:()=>element(Symbol("anchor")),body:{append(){}}},
 URL:{createObjectURL:()=> "blob:mock",revokeObjectURL(){}},
 Blob,TextEncoder,Date,BigInt,
 setTimeout:fn=>fn(), alert:msg=>{throw Error(msg)},
 window:{open(){}},
 fetch:async()=>({ok:true,json:async()=>[]})
});
vm.runInContext(script[1],context);
let valid=vm.runInContext("validate()",context);
assert.match(valid.pkg,/^FAPP\/1\nid=my-first-app\n/);
assert.equal(valid.manifest.id,"my-first-app");

function rejects(id,value,pattern){
 const old=element(id).value;element(id).value=value;
 assert.throws(()=>vm.runInContext("validate()",context),pattern);
 element(id).value=old;
}
rejects("app-id","../evil",/ID:/);
rejects("app-version","1.0.0-alpha.01",/prerelease/);
rejects("source","echo hello | sh\n",/prohibited/);
rejects("source","# "+"x".repeat(181)+"\n",/too long|180 characters/);
rejects("source","echo bad\tcommand\n",/printable ASCII/);

// The browser export must produce both files required by the GitHub source registry.
element("export-source").onclick();
assert.deepEqual(clicks.map(x=>x.download),[
 "my-first-app-v1.0.0-manifest.json","my-first-app-v1.0.0-main.fsh"
]);
const parsed=vm.runInContext("parsePackage(validate().pkg)",context);
assert.equal(parsed.fields.id,"my-first-app");
assert.equal(parsed.source,initial.source);
assert.throws(()=>vm.runInContext('parsePackage("invalid")',context),/FAPP\/1/);
console.log("CodeDium validation, package import and two-file export tests passed");
