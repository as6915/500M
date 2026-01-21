hereconst models = [
  { id:"blackbox", name:"Blackbox", icon:"B" },
  { id:"copilot", name:"Copilot", icon:"C" },
  { id:"deepai", name:"DeepAI", icon:"D" },
  { id:"gemini", name:"Gemini", icon:"G" },
  { id:"venice", name:"Venice", icon:"V" }
];

let active = models[0];

const log = document.getElementById("log");
const input = document.getElementById("txt");
const sendBtn = document.getElementById("send");
const modelBtn = document.getElementById("modelBtn");
const activeLabel = document.getElementById("activeModel");
const modelsLayer = document.getElementById("models");

activeLabel.textContent = active.name;

function add(role,text){
  const d=document.createElement("div");
  d.className="msg "+role;
  d.textContent=text;
  log.appendChild(d);
  log.scrollTop=log.scrollHeight;
  return d;
}

async function send(){
  const v=input.value.trim();
  if(!v) return;
  input.value="";
  add("user",v);
  const loader=add("ai","Thinking...");

  try{
    const r=await fetch("/api/chat",{
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify({model:active.id,message:v})
    });
    loader.textContent=await r.text();
  }catch{
    loader.textContent="Error";
  }
}

sendBtn.onclick=send;
input.onkeydown=e=>{if(e.key==="Enter")send()};

const box=document.createElement("div");
box.className="box";
models.forEach(m=>{
  const d=document.createElement("div");
  d.className="model-item";
  d.innerHTML=`<div class="icon">${m.icon}</div><div>${m.name}</div>`;
  d.onclick=()=>{
    active=m;
    activeLabel.textContent=m.name;
    modelsLayer.style.display="none";
  };
  box.appendChild(d);
});
modelsLayer.appendChild(box);

modelBtn.onclick=()=>modelsLayer.style.display="flex";
modelsLayer.onclick=e=>{if(e.target===modelsLayer)modelsLayer.style.display="none"};
