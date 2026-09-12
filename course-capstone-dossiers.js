'use strict';
(()=>{
  const CONFIG={
    M09:{caseIndex:9,minChars:400,minWords:60},
    M10:{caseIndex:11,minChars:400,minWords:60},
    M11:{caseIndex:11,minChars:400,minWords:60},
    M12:{caseIndex:11,minChars:400,minWords:60},
    M13:{caseIndex:11,minChars:400,minWords:60}
  };
  const m=(location.pathname.match(/\/m(09|10|11|12|13)-/i)||[])[1],MODULE=m?'M'+m:null;
  if(!MODULE||!CONFIG[MODULE])return;
  const cfg=CONFIG[MODULE],STORE='tvaCapstoneDossierV1_'+MODULE,PRACTICE='tvaPracticeGateV1_'+MODULE;

  const readJson=(k)=>{try{return JSON.parse(localStorage.getItem(k)||'{}')}catch(e){return {}}};
  const writeJson=(k,v)=>{try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}};
  const words=s=>(String(s||'').trim().match(/\S+/g)||[]).length;
  const ready=s=>String(s||'').trim().length>=cfg.minChars&&words(s)>=cfg.minWords;
  const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const cleanOption=s=>String(s||'').replace(/^\s*[A-D]\)\s*/,'').trim();

  function addStyles(doc){
    if(doc.getElementById('capstone-dossier-style'))return;
    const st=doc.createElement('style');st.id='capstone-dossier-style';st.textContent=`
      .capstone-dossier{outline:2px solid rgba(201,168,76,.68);outline-offset:3px}
      .capstone-dossier .capstone-workspace{margin:16px 0 2px;padding:18px;border:1px solid #D9CFB5;border-radius:12px;background:#FFFCF5}
      .capstone-dossier .capstone-kicker{font-size:11px;font-weight:900;letter-spacing:.08em;text-transform:uppercase;color:#7A5200;margin-bottom:7px}
      .capstone-dossier .capstone-workspace h4{margin:0 0 8px;color:#0B2545;font-size:17px}
      .capstone-prompts{margin:9px 0 15px;padding-left:21px}.capstone-prompts li{margin:6px 0}
      .capstone-dossier textarea{width:100%;min-height:220px;resize:vertical;border:1px solid #C9C1AF;border-radius:9px;background:#fff;padding:13px;font:13.5px/1.55 Arial,Helvetica,sans-serif;color:#1A1A2E}
      .capstone-dossier textarea:focus{outline:2px solid rgba(31,77,140,.22);border-color:#1F4D8C}
      .capstone-meta{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;margin:7px 0 12px;font-size:11.5px;color:#667085}
      .capstone-actions{display:flex;gap:10px;align-items:center;flex-wrap:wrap}.capstone-compare{border:0;border-radius:8px;padding:9px 13px;background:#0B2545;color:#fff;font-weight:800;cursor:pointer}.capstone-compare:disabled{opacity:.45;cursor:not-allowed}
      .capstone-model{display:none;margin-top:16px;padding:16px;border-left:4px solid #2A6B48;background:#E7F5EC;border-radius:9px}.capstone-model.show{display:block}.capstone-model h4{margin:0 0 10px}.capstone-model-item{margin:11px 0}.capstone-model-item strong{color:#0B2545}.capstone-model-item p{margin:4px 0}
      .capstone-saved{font-size:11.5px;color:#2A6B48;font-weight:700}.capstone-legacy-note{margin:10px 0 0;padding:9px 11px;border-radius:7px;background:#EFF4FB;color:#1F4D8C;font-size:11.5px}
      @media(max-width:700px){.capstone-dossier textarea{min-height:260px}.capstone-meta{display:block}}
    `;doc.head.appendChild(st);
  }

  function extract(card){
    const title=(card.querySelector('.casehead,.caseh,h3')?.textContent||'Dossier de synthèse').trim();
    const scenario=(card.querySelector('.scenario')?.textContent||'').trim();
    const stepEls=[...card.querySelectorAll('.qstep,.qs')];
    const steps=stepEls.map((el,i)=>{
      const q=(el.querySelector('.q')?.textContent||el.querySelector(':scope > b')?.textContent||('Question '+(i+1))).trim();
      const opts=[...el.querySelectorAll('.opt')];
      const correct=opts.find(b=>b.dataset.ok==='1'||/(?:caseAnswer|ans)\s*\(\s*this\s*,\s*true\s*\)/.test(b.getAttribute('onclick')||''));
      const expl=(el.querySelector('.expl')?.textContent||'').trim();
      return {q,answer:cleanOption(correct?.textContent||''),expl};
    });
    return {title,scenario,stepEls,steps};
  }

  function modelHtml(data){
    return data.steps.map((s,i)=>`<div class="capstone-model-item"><strong>${i+1}. ${esc(s.q)}</strong>${s.answer?`<p><b>Position :</b> ${esc(s.answer)}</p>`:''}${s.expl?`<p>${esc(s.expl)}</p>`:''}</div>`).join('');
  }

  function markPractice(doc){
    const pg=readJson(PRACTICE);if(!pg.complete)pg.complete={};pg.complete[String(cfg.caseIndex)]=true;pg.updatedAt=Date.now();writeJson(PRACTICE,pg);
    try{doc.dispatchEvent(new doc.defaultView.CustomEvent('tva:capstone-complete',{detail:{module:MODULE,caseIndex:cfg.caseIndex}}))}catch(e){}
  }

  function transform(doc){
    if(!doc?.body)return false;addStyles(doc);
    const cards=[...doc.querySelectorAll('#sec-cases .case')],card=cards[cfg.caseIndex];
    if(!card)return false;if(card.dataset.capstoneDossier==='1')return true;
    const data=extract(card);if(!data.stepEls.length)return false;
    card.dataset.capstoneDossier='1';card.classList.add('capstone-dossier');
    const saved=readJson(STORE),practice=readJson(PRACTICE),legacyDone=practice.complete?.[String(cfg.caseIndex)]===true&&!saved.modelShown;
    const workspace=doc.createElement('div');workspace.className='capstone-workspace';
    workspace.innerHTML=`<div class="capstone-kicker">Dossier professionnel · réponse libre</div><h4>Votre mission</h4><p>Rédigez une courte note professionnelle avant de consulter le modèle. Structurez votre réponse comme si elle devait être relue par un senior : qualification, base juridique, traitement TVA, preuves/risques et action recommandée.</p><ol class="capstone-prompts">${data.steps.map(s=>`<li>${esc(s.q)}</li>`).join('')}</ol><label><strong>Votre position</strong></label><textarea class="capstone-draft" spellcheck="true" placeholder="Rédigez votre analyse ici…">${esc(saved.draft||'')}</textarea><div class="capstone-meta"><span class="capstone-count"></span><span>Minimum : ${cfg.minWords} mots et ${cfg.minChars} caractères avant comparaison.</span></div><div class="capstone-actions"><button type="button" class="capstone-compare">Comparer avec le modèle</button><span class="capstone-saved"></span></div>${legacyDone?'<div class="capstone-legacy-note">Ce cas était déjà validé dans votre progression précédente. Vous conservez cet acquis ; ce nouveau format vous permet de refaire le dossier avec une réponse rédigée.</div>':''}<div class="capstone-model"><h4>Modèle de réponse</h4><p class="note">Modèle pédagogique fondé sur les corrections juridiques du cas. Comparez le raisonnement, pas seulement la conclusion.</p>${modelHtml(data)}</div>`;
    data.stepEls.forEach(el=>el.remove());
    const scenario=card.querySelector('.scenario');if(scenario)scenario.insertAdjacentElement('afterend',workspace);else card.appendChild(workspace);
    const ta=workspace.querySelector('.capstone-draft'),count=workspace.querySelector('.capstone-count'),btn=workspace.querySelector('.capstone-compare'),model=workspace.querySelector('.capstone-model'),savedMsg=workspace.querySelector('.capstone-saved');
    const refresh=()=>{const v=ta.value,ok=ready(v);count.textContent=words(v)+' mots · '+v.trim().length+' caractères';btn.disabled=!ok&&!saved.modelShown;btn.textContent=saved.modelShown?'✓ Modèle affiché':'Comparer avec le modèle';model.classList.toggle('show',!!saved.modelShown);savedMsg.textContent=saved.modelShown?'Dossier comparé et enregistré.':(v.trim()?'Brouillon enregistré.':'')};
    ta.addEventListener('input',()=>{saved.draft=ta.value;saved.updatedAt=Date.now();writeJson(STORE,saved);refresh()});
    btn.addEventListener('click',()=>{if(!ready(ta.value)&&!saved.modelShown)return;saved.draft=ta.value;saved.modelShown=true;saved.completedAt=Date.now();writeJson(STORE,saved);markPractice(doc);refresh();model.scrollIntoView({behavior:'smooth',block:'nearest'})});
    if(saved.modelShown)markPractice(doc);refresh();
    return true;
  }

  function init(){
    const frame=document.getElementById('module');
    if(!frame){let n=0;const t=setInterval(()=>{n++;if(transform(document)||n>100)clearInterval(t)},50);return}
    const apply=()=>{try{return transform(frame.contentDocument)}catch(e){return false}};
    frame.addEventListener('load',()=>{setTimeout(apply,0);setTimeout(apply,200)});
    let n=0;const t=setInterval(()=>{n++;if(apply()||n>120)clearInterval(t)},50);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();
