import { NextRequest, NextResponse } from "next/server";
const base=process.env.API_INTERNAL_URL || "http://api:8000";
async function handler(request:NextRequest, context:{params:Promise<{path:string[]}>}){
  const {path}=await context.params;
  const allowed=new Set(["health","me","sales","stocks/low","stocks/movements","ask","forecast","observability"]);
  const endpoint=path.join("/");
  if(!allowed.has(endpoint))return NextResponse.json({detail:"Route interdite"},{status:404});
  const url=new URL(request.url);
  const target=base+"/"+endpoint+url.search;
  const auth=request.headers.get("authorization") || "";
  try{
    const response=await fetch(target,{method:request.method,headers:{"Content-Type":"application/json",...(auth?{"Authorization":auth}:{})},body:request.method==="POST"?await request.text():undefined,cache:"no-store",signal:AbortSignal.timeout(90000)});
    return new NextResponse(await response.text(),{status:response.status,headers:{"Content-Type":"application/json","Cache-Control":"no-store"}});
  }catch{return NextResponse.json({detail:"API indisponible. Vérifiez Docker Compose."},{status:502});}
}
export {handler as GET,handler as POST};
