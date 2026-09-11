'use strict';
(()=>{
  const cfg=window.COURSE_GATE_CONFIG||{},frame=document.getElementById('module');
  if(!frame||!cfg.module||!cfg.src)return;
  const DASH='tvaSpecialisteTvaDashboardV1',GKEY='tva_course_gate_'+cfg.module+'_v2';
  const required=cfg.sections||['theory','legis','cases','errors','quiz','memo','vocab','cheat'];
  let gate={visited:{theory:true},quizPassed:false,quizScore:0,done:false};
  try{gate=Object.assign(gate,JSON.parse(localStorage.getItem(GKEY)||'{}'));gate.visited=Object.assign({theory:true},gate.visited||{})}catch(e){}
  const save=()=>{try{localStorage.setItem(GKEY,JSON.stringify(gate))}catch(e){}};
  const mark=s=>{if(required.includes(s)){gate.visited[s]=true;save()}};
  const setText=(el,text)=>{if(el&&el.textContent.trim()!==text.trim())el.textContent=text};
  function inferObject(o){
    if(!o||typeof o!=='object')return;
    required.forEach(s=>{if(o[s]===1||o[s]===true)gate.visited[s]=true;if(o.done&&(o.done[s]===1||o.done[s]===true))gate.visited[s]=true;if(o.visited&&(o.visited[s]===1||o.visited[s]===true))gate.visited[s]=true});
    if(required.includes(o.section))gate.visited[o.section]=true;
    const pass=o.quiz_passed===1||o.quiz_passed===true||o.quizPassed===1||o.quizPassed===true;
    const scores=[o.quiz_score,o.quizScore,o.quiz_best,o.quizBest,o.bestScore,o.lastScore,o.quiz&&o.quiz.score,o.quiz&&o.quiz.best];
    const score=Math.max(0,...scores.map(Number).filter(Number.isFinite));
    if(pass||score>=75){gate.quizPassed=true;gate.quizScore=Math.max(gate.quizScore||0,score||75)}
  }
  function inferStorage(){for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i)||'';if(!cfg.storagePrefixes?.some(p=>k.startsWith(p)))continue;try{inferObject(JSON.parse(localStorage.getItem(k)||'{}'))}catch(e){}}save()}
  function scoreFromDom(d){
    let best=gate.quizScore||0;const view=d.defaultView||window;
    ['#r-pct','#score','#result-score','#quiz-score','.results-score','.score'].forEach(sel=>d.querySelectorAll(sel).forEach(el=>{const style=view.getComputedStyle(el);if(style.display==='none'||style.visibility==='hidden')return;const m=(el.textContent||'').match(/(\d{1,3})(?:\s*%|$)/);if(m)best=Math.max(best,Number(m[1]))}));
    if(best>=75){gate.quizPassed=true;gate.quizScore=best;save()}
  }
  function activeSection(d){const view=d.defaultView||window;required.forEach(s=>{const el=d.getElementById('sec-'+s);if(!el)return;const cs=view.getComputedStyle(el);if(el.classList.contains('active')||(cs.display!=='none'&&cs.visibility!=='hidden'))mark(s)})}
  function sectionFromTarget(t){const h=t.closest('[data-sec],[data-s],[data-section]');if(h)return h.dataset.sec||h.dataset.s||h.dataset.section||'';const oc=t.getAttribute?.('onclick')||'',m=oc.match(/(?:NAV\.)?(?:go|goto)\(\s*['"]([^'"]+)['"]/);return m?m[1]:''}
  function completionTarget(t){const oc=t.getAttribute?.('onclick')||'',txt=(t.textContent||'').trim();return /(?:finishModule|PROG\.finish|PROG\.goNext|goNextModule)\s*\(/.test(oc)||/(?:Terminer|Marquer)/i.test(txt)&&txt.includes(cfg.module)}
  function wantsNext(t){const oc=t.getAttribute?.('onclick')||'',txt=(t.textContent||'').trim();return /(?:goNextModule|PROG\.goNext)\s*\(/.test(oc)||/^Continuer\b/i.test(txt)||/Module suivant/i.test(txt)}
  function gateStatus(){inferStorage();const d=frame.contentDocument;if(d){activeSection(d);scoreFromDom(d)}const missing=required.filter(s=>!gate.visited[s]);return{ok:missing.length===0&&gate.quizPassed,missing}}
  function toast(d,msg,ok){let x=d.getElementById('course-gate-toast');if(!x){x=d.createElement('div');x.id='course-gate-toast';x.style.cssText='position:fixed;right:16px;bottom:16px;z-index:99999;max-width:520px;padding:13px 16px;border-radius:9px;font:13px/1.5 system-ui,sans-serif;box-shadow:0 8px 28px #0003';d.body.appendChild(x)}x.style.background=ok?'#E7F5EC':'#FEF3D8';x.style.color=ok?'#1f5d3b':'#684600';x.style.border='1px solid '+(ok?'#8DC7A2':'#dfbf70');x.textContent=msg;clearTimeout(x._t);x._t=setTimeout(()=>x.remove(),7000)}
  function finalize(d,next){gate.done=true;save();try{const x=JSON.parse(localStorage.getItem(DASH)||'{}');x[cfg.module]='done';localStorage.setItem(DASH,JSON.stringify(x))}catch(e){}toast(d,cfg.module+' validÃ© : toutes les sections ont Ã©tÃ© parcourues et le QCM a atteint au moins 75 %.',true);if(next&&cfg.next)setTimeout(()=>{window.top.location.href=cfg.next},250)}
  function replaceText(d,repls){const w=d.createTreeWalker(d.body,NodeFilter.SHOW_TEXT);let n;while((n=w.nextNode())){let v=n.nodeValue||'',nv=v;for(const [a,b] of repls)if(nv.includes(a))nv=nv.split(a).join(b);if(nv!==v)n.nodeValue=nv}}
  function patchPortalLinks(d){d.querySelectorAll('a[href*="eportal.admin.ch"]').forEach(a=>{a.href='https://www.estv.admin.ch/fr/services-en-ligne-afc';if(/ePortal/i.test(a.textContent||''))a.textContent='Portail AFC â†—'})}
  function legalPatch(d){
    if(cfg.module==='M01'){
      d.querySelectorAll('.vocab-card').forEach(c=>{const k=c.querySelector('.vfr')?.textContent.trim(),def=c.querySelector('.vdef');if(!def)return;if(k==='TVA / Taxe sur la valeur ajoutÃ©e')def.textContent='ImpÃ´t fÃ©dÃ©ral gÃ©nÃ©ral sur la consommation. Le systÃ¨me vise la neutralitÃ© pour lâ€™entreprise dans la mesure oÃ¹ elle dispose effectivement du droit Ã  la dÃ©duction de lâ€™impÃ´t prÃ©alable.';if(k==='ImpÃ´t prÃ©alable (DIP)')def.textContent='TVA grevant certaines acquisitions, dÃ©ductible dans la mesure oÃ¹ les conditions des art. 28 ss LTVA sont remplies et selon lâ€™affectation.';if(k==='OpÃ©ration exclue')def.textContent='Prestation exclue de lâ€™impÃ´t selon lâ€™art. 21 LTVA. Ã€ distinguer dâ€™une prestation localisÃ©e hors de Suisse. Sans option ou droit spÃ©cial, pas de TVA de sortie et pas de DIP sur les coÃ»ts directement affectÃ©s.';if(k==='DÃ©compte TVA')def.textContent='DÃ©claration TVA selon la pÃ©riode de dÃ©compte applicable : en principe trimestrielle (effective/TaF) ou semestrielle (TDFN), avec dÃ©compte annuel possible sur demande sous les conditions de lâ€™art. 35a LTVA. La remise se fait dans DÃ©compte TVA pro sur le Portail AFC.';if(k==='MÃ©thode effective')def.textContent='TVA due rÃ©elle moins DIP dÃ©ductible rÃ©el. PÃ©riode de dÃ©compte en principe trimestrielle; dÃ©compte annuel possible sur demande si les conditions lÃ©gales sont rÃ©unies.';if(k==='TDFN / Taux de la dette fiscale nette')def.textContent='MÃ©thode simplifiÃ©e : TDFN appliquÃ© au chiffre dâ€™affaires dÃ©terminant TVA comprise, sous les limites actuelles. DÃ©compte en principe semestriel; dÃ©compte annuel possible sur demande sous conditions.'});
      replaceText(d,[['Les opÃ©rations exclues sont hors champ.','Les prestations exclues selon lâ€™art. 21 ne sont pas comprises dans le chiffre dâ€™affaires dÃ©terminant de lâ€™art. 10; elles ne doivent pas Ãªtre confondues avec des prestations localisÃ©es hors de Suisse.'],['Hors champ/exclu =','Prestation exclue art. 21 ='],['Taux normal 2024','Taux normal actuel (depuis 01.01.2024)'],['Taux rÃ©duit 2024','Taux rÃ©duit actuel (depuis 01.01.2024)'],['Taux hÃ©bergement 2024','Taux hÃ©bergement actuel (depuis 01.01.2024)'],['via ePortal AFC','via le Portail AFC'],['Via ePortal AFC','Via le Portail AFC'],['Via ePortal','Via le Portail AFC'],['formulaires, ePortal et jurisprudence','formulaires, Portail AFC / DÃ©compte TVA pro et jurisprudence']]);patchPortalLinks(d);
    }
    if(cfg.module==='M02')replaceText(d,[["Une cotisation statutaire d'association sans but lucratif est :","Une cotisation dâ€™un organisme sans but lucratif, fixÃ©e conformÃ©ment aux statuts et rÃ©ellement versÃ©e en qualitÃ© de membre, est en principe :"],["Les cotisations de membres d'organismes sans but lucratif sont exclues art. 21 al. 2 ch. 13. Condition : la cotisation doit donner accÃ¨s aux prestations communes (statut homogÃ¨ne). Si paiement de prestation spÃ©cifique â†’ imposable.","Lâ€™art. 21 al. 2 ch. 13 peut exclure les prestations fournies aux membres contre une cotisation fixÃ©e conformÃ©ment aux statuts. La pratique AFC adaptÃ©e le 26.05.2026 impose dâ€™examiner concrÃ¨tement la catÃ©gorie de membre, les droits attachÃ©s Ã  cette qualitÃ©, la rÃ¨gle de fixation de la cotisation et les prestations liÃ©es; une prestation individualisÃ©e, publicitÃ© ou sponsoring se qualifie sÃ©parÃ©ment."],["Cotisations statutaires des membres (CHF 45'000) â€” quel rÃ©gime ?","Cotisations des membres (CHF 45!,ƒÒ! ãH]œ˜Z\ÛÛˆİZ\ÜÙNÈğêXİ\š\Ù\ˆH˜Z]8 &Y^Ü][Ûˆ]™XÈ\È[ŞY[œÈH™]]™H\ÜÛšX›\É×KÉĞÛÛ™\Ú[Ûˆ]™XÈÚˆÎÈÈT™Y\ğêHÚH0êXÚ\Ú[ÛˆÑ‘ˆXœÙ[IË	ĞÛÛ™\Ú[Ûˆ]™XÈÚˆÎÎÈš\Ü]YHH™Y\ÈHTÚH8 &Z[\0í0è8 &Z[\Ü][Û‹8 &Z[\Ü]]\ˆ]\ÈÛÛ™][ÛœÈH8 &X\ˆ™HÛÛ\ÈİY™š\Ø[[Y[›İ]°ê\É×KÉÜX›pê\Èİ\ˆTÜ[QÉË	ÜX›pê\È\ˆ8 &PQÉ×KÉÜX›pêHİ\ˆTÜ[QÉË	ÜX›pêH\ˆ8 &PQÉ×KÉÙ›Ü›][Z\™H[ˆYÛ™Hİ\ˆTÜ[QÉË	Ú[œØÜš\[Ûˆ[ˆYÛ™HšXHHÜZ[QÉ×WJNÂˆÛÛœİÌOY™Ù][[Y[RY
	ÛM˜ÌL\ÌIÊK›ØÚÏ\ÌOË˜ÛÜÙ\İ
	Ë˜Ø\ÙKX›ØÚÉÊNÚYŠ›ØÚÊ^ØÛÛœİØÏX›ØÚËœ]Y\TÙ[XİÜ”ØÙ[XİÜ[
	Ë˜Ø\ÙK\ØÙ[˜\š[ÉÊNÚYŠØÉ‰ˆ\ØË™]\Ù]›YØ[]ÚY
^ÜØËš[›™\’SIÏİ›Û™ÏÛÛ^HÜİ›Û™Ïˆİ\\XÚĞH
]\Ø[›™JH0ê[X\œ™HÛÛˆXİ]š]0êH[ˆŒ‹ˆ]H[˜Ù[Y[ÛÛˆ\Ú[™\ÜÈ[‹\ÈÛÛ˜]È0êZ°èÚYÛ°ê\È]ÛÛˆ\[[™H™[™[Øš™Xİ]™[Y[°ê]š\ÚX›H[ˆÚY™œ™H8 &XY™˜Z\™\È0ê]\›Z[˜[8 &Y[š\›Ûˆİ›Û™ÏÒˆN	Ìİ\ˆ\Èİ^™H[Ú\ÈİZ]˜[ÏÜİ›Û™ÏˆˆÒˆW	ÌH™\İ][ÛœÈ0è\ÈÛY[ÈİZ\ÜÙ\ËÒˆ	ÌHÙ\šXÙ\ÈŒˆ0è\ÈÛY[ÈQKÕTÈ]ÒˆÍW	ÌHÙ\šXÙ\ÈŒˆ0è\ÈÛY[È\ÚX]\]Y\ËˆÙ\È™\İ][ÛœÈ™HÛÛ\È^ÛY\È]HÙ[œÈH8 &X\ˆŒKˆH\™Xİ[Ûˆ[œÙH°êX[›[Ú[œÈ]YHÙ][HĞHİZ\ÜÙHÛÛ\Hİ\ˆHÙ]Z[‰ÎÜØË™]\Ù]›YØ[]ÚYIÌIßXÛÛœİÜÏ\ÌKœ]Y\TÙ[XİÜ[
	Ëœİ\[Ü	ÊNÚYŠÜÖÌWJ\Ù]^
ÜÖÌWKŠHİZH0êÈH0êX]H8 &XXİ]š]0êHˆ\ÈÚ\˜ÛÛœİ[˜Ù\È™[™[°ê]š\ÚX›H[ˆĞH[Û™X[0ê]\›Z[˜[ˆÒˆL	Ìİ\ˆ\ÈLˆ[Ú\ÈİZ]˜[ÈŠNØÛÛœİ^Y™Ù][[Y[RY
	ÛM˜ÌL\ÌKY^	ÊNÚYŠ^	‰ˆY^™]\Ù]›YØ[]ÚY
^Ù^š[›™\’SIÏİ›Û™Ï‘]^0ê]\\È\İ[˜İ\ËÜİ›Û™ÏˆHÙ]Z[HÒˆL	ÌÙHY\İ\™Hİ\ˆHÚY™œ™H8 &XY™˜Z\™\È[Û™X[›İ™[˜[\Èİ›Û™Ïœ™\İ][ÛœÈ]ZH™HÛÛ\È^ÛY\ÏÜİ›Û™ÏˆHÚ[\H8 &Z[\0íÈ\ÈÙ\šXÙ\ÈØØ[\ğê\È0è8 &pê]˜[™Ù\ˆÙ[Ûˆ8 &X\ˆ]]™[Û˜ÈÛÛ\\‹ˆİ\ˆ[™H[™\š\ÙHİZ\ÜÙH]ZHİ›Û™Ï™0êX]OÜİ›Û™ÏˆÛÛˆXİ]š]0êK8 &X\ÜİZ™]\ÜÙ[Y[ÛÛ[Y[˜ÙH0êÈH0êX]ÜœÜ]YH\ÈÚ\˜ÛÛœİ[˜Ù\È\›Y][H°ê]›Ú\ˆ]YHÙHÙ]Z[Ù\˜H]Z[[œÈ\Èİ^™H[Ú\ÈİZ]˜[ËˆXÚK\È˜Z]ÈZ›İ]0ê\È]HØ\È™[™[Ù]H°ê]š\Ú[ÛˆİY™š\Ø[[Y[ÛÛ˜Ü°êKˆ0à8 &Z[™\œÙK[™H[™\š\ÙHİZ\ÜÙH0êZ°è^\İ[H]\Ü]x &X[ÜœÈX°ê\°êYH™H]šY[\È]]ÛX]\]Y[Y[\ÜİZ™]YH]H›İ\ˆğîH[Hœ˜[˜Ú]L	Ìœ˜[˜ÜÈˆÚHHÙ]Z[¸ &pê]Z]\È0êZ°è°ê]š\ÚX›HÙ[Ûˆ\È°êÛ\È\XØX›\Ë8 &X\ÜİZ™]\ÜÙ[Y[Ø›YØ]Ú\™H[\šY[[ˆš[˜Ú\H0è8 &Y^\˜][ÛˆH8 &Y^\˜ÚXÙH]HÛİ\œÈ\]Y[HÙ]Z[H0ê]0êH]Z[]ˆÛ\ÜÏH˜\\™Yˆ¼'äâÈ\ˆL]MH0­È˜]\]YHQÈ\ÜİZ™]\ÜÙ[Y[Ù]‰ÎÙ^™]\Ù]›YØ[]ÚYIÌIß_BˆÛÛœİÌÏY™Ù][[Y[RY
	ÛM˜ÌL\ÌÉÊNÚYŠÌÊ^ØÛÛœİÜÏ\ÌËœ]Y\TÙ[XİÜ[
	Ëœİ\[Ü	ÊNÚYŠÜÖÌWJ\Ù]^
ÜÖÌWK	ĞŠHø &X[››Û˜Ù\ˆ[œÈ\ÈÌ›İ\œÈ0êÈH0êX]H8 &X\ÜİZ™]\ÜÙ[Y[È0ê]\›Z[™\ˆ8 &XX›Ü™Ù]H]HÙ[Ûˆ8 &X\ˆM]\È˜Z]ÉÊNØÛÛœİ^Y™Ù][[Y[RY
	ÛM˜ÌL\ÌËY^	ÊNÚYŠ^	‰ˆY^™]\Ù]›YØ[]ÚY
^Ù^š[›™\’SIÏİ›Û™Ï“H0ê[ZHHÌ›İ\œÈÛİ\0êÈH0êX]H8 &X\ÜİZ™]\ÜÙ[Y[Üİ›Û™ÏÈ[™Hø &XYÚ]\È8 &][™H°êÛHğê[°ê\˜[H0ªÌÌ›İ\œÈ\°êÈHœ˜[˜Ú\ÜÙ[Y[HÙ]Z[0®Ëˆ[œÈH°ê\Ù[Ø\ËZ\Ü]YHHÙ]Z[0ê]Z]Øš™Xİ]™[Y[°ê]š\ÚX›H]H0ê[X\œ˜YÙK8 &X\ÜİZ™]\ÜÙ[Y[ÛÛ[Y[˜ÙH]H0êX]H8 &XXİ]š]0êH]8 &X[››Û˜ÙHÚ]İZ]œ™H[œÈ\ÈÌ›İ\œËˆİ\ˆ[™H[™\š\ÙH^\İ[H]\\˜]˜[X°ê\°êYKH]HH0êX]]]0ê™HY™°ê\™[H]Ú]0ê™H0ê]\›Z[°êYH]˜[HØ[İ[\ˆH0ê[ZKˆ[ˆ™]\™]][˜pë›™\ˆ˜\[][0ê\°êÈ]Ù[Ûˆ\È˜Z]Ë[ˆš\Ü]YH0ê[˜[ˆ[™H0ê[›Û˜ÚX][ÛˆÜÛ[°êYH™Hİ\š[YH\È]]ÛX]\]Y[Y[8 &X[Y[™Hˆ8 &YY™™]0ê[˜[˜]›Ü˜X›H0ê\[™H™\ÜXİHİ]\È\ÈÛÛ™][ÛœÈH8 &X\ˆL‹[™\È]YH8 &Z[\0í]\È[0ê\°êÈ™\İ[[ˆš[˜Ú\H\Ë]ˆÛ\ÜÏH˜\\™Yˆ¼'äâÈ\ˆM0­Èˆ0­ÈÈ0­ÈMˆ0­ÈLˆOÙ]‰ÎÙ^™]\Ù]›YØ[]ÚYIÌIß_Bˆ]ÚÜ[[šÜÊ
NÂˆBˆYŠÙ™Ë›[Ù[OOOIÓL	ÊYœ]Y\TÙ[XİÜ[
	Ë›ØØX‹XØ\™	ÊK™›Ü‘XXÚ
ÏOØÛÛœİÏXËœ]Y\TÙ[XİÜ”ØÙ[XİÜ[
	Ë™œ‰ÊOË^ÛÛ[š[J
KYXËœ]Y\TÙ[XİÜ”ØÙ[XİÜ[
	Ë™Y‰ÊK\XËœ]Y\TÙ[XİÜŠ	Ë˜\	ÊNÚYŠYYŠ\™]\›ÚYŠÏOOH“Ü[Ûˆ	Ú[\ÜÚ][Ûˆ[[[Øš[pê™HŸÏOOIÓÜ[Ûˆ8 &Z[\ÜÚ][Ûˆ[[[Øš[pê™IÊ^ÙY‹^ÛÛ[IÑ›Ú]HÛİ[Y]™H›ÛÛZ\™[Y[[™HÜ0ê\˜][Ûˆ[[[Øš[pê™H^ÛYH0èHHÜœÜ]YH8 &X\ˆŒˆH\›Y]ˆ°ê\šYšY\ˆ8 &]\ØYÙHHšY[‹\È^Û\Ú[ÛœÈ0è8 &[Ü[Ûˆ]H[Ù[]0êKİ[Z[™È8 &Y^\˜ÚXÙNÈ[¸ &Y^\İH\È[™H\œ°ê]›ØØXš[]0êHğê[°ê\˜[Hİ\ˆİ]HH\°êYHHÛÛ˜]‰ÎÚYŠ\
X\^ÛÛ[IØ\ˆŒˆH0­È\ˆÎHÕH0­È˜]\]YHQÈ[[[Øš[Y\‰ßZYŠÏOOIÒ[[Y]X›HZ^IÊ^ÙY‹^ÛÛ[IÒ[[Y]X›HY™™Xİ0êH0è\È\ØYÙ\ÈÛ›˜[]™HÛ›˜[\È›Ú]]HTˆ›ØğêY\ˆ8 &XX›Ü™0è8 &XY™™Xİ][Ûˆ\™XİH\ÈÛğîİËZ\È\\]Y\ˆ[™HÛ0êHØš™Xİ]™H[š\]Y[Y[]^œ˜Z\ÈÛğîİÈÛÛ[][œË‰ÎÚYŠ\
X\^ÛÛ[IØ\ˆÌH0­È˜]\]YHQÉßZYŠÏOOIĞÛ0êHH°ê\\][ÛˆT	Ê^ÙY‹^ÛÛ[IÓpê]ÙHØš™Xİ]™Hİ\ˆ\ÈÛğîİÈ°êY[[Y[ÛÛ[][œÈ\°êÈY™™Xİ][Ûˆ\™XİKˆHÛ0êHÚ]™Y›0ê]\ˆ8 &]][\Ø][ÛˆY™™Xİ]™NÈİ\™˜XÙK™XÙ]\ÈİH]]™HÜš]0ê™H™HÛÛ\È\ÈÛ0ê\È0êYØ[\È[š]™\œÙ[\Ë‰ÎÚYŠ\
X\^ÛÛ[IØ\ˆÌH0­Èpê]ÙHØš™Xİ]™HØİ[Y[0êYIßZYŠÏOOHÚ[™Ù[Y[	ØY™™Xİ][ÛˆŠ^ÙY‹^ÛÛ[IÔ\ÜØYÙH8 &][ˆ\ØYÙHÛ›˜[›Ú]]HT0è[ˆ\ØYÙH¸ &^HÛ›˜[\È›Ú]İH[™\œÙ[Y[ˆ[˜[\Ù\ˆÛÜœ™Xİ[Û‹Ù0êYÜ°ê™[Y[İ\ˆH˜[]\ˆ°ê\ÚYY[NÈİ\ˆ8 &Z[[[Øš[Y\‹H0ê\°êXÚX][Ûˆ›Ü™˜Z]Z\™H\İHH	H\ˆ[›°êYH
ÙÚ\]YHKÌŒ
HÙ[Ûˆ\ÈÛÛ™][ÛœÈ0êYØ[\Ë‰ÎÚYŠ\
X\^ÛÛ[IØ\ˆÌx $ÌÌˆH0­È\ˆÌ8 $ÍÌÈÕIßZYŠÏOOH’[\ÜÚ][Ûˆ0è	ØXÜ]Z\Ú][Ûˆ
˜]˜]^
HŠ^ÙY‹^ÛÛ[IÔİ\ˆ[ˆ[™\™[™]\ˆ0ê]˜[™Ù\ˆ[\™[˜[İ\ˆ[ˆ[[Y]X›HİZ\ÜÙK]X[YšY\ˆ8 &XX›Ü™H›^]HY]KZ\È°ê\šYšY\ˆÛÛˆ0ê]™[Y[HØ›YØ][Ûˆ8 &Z[œØÜš\[Ûˆ[ˆİZ\ÜÙK8 &Z[\Ü]]\ˆ]HH0è8 &Z[\Ü][Û‹ˆ8 &Z[\0íİ\ˆ\ÈXÜ]Z\Ú][ÛœÈ¸ &Z[\šY[]YHÚH\ÈÛÛ™][ÛœÈH8 &X\ˆHÛÛ™[\Y\Ë‰ÎÚYŠ\
X\^ÛÛ[IØ\ˆ0­ÈL0­ÈH0­ÈLÜÈIß_JNÂˆBˆ[˜İ[Ûˆ]XÚ

^ØÛÛœİYœ˜[YK˜ÛÛ[Øİ[Y[ÚYŠY
\™]\›Ú[™™\”İÜ˜YÙJ
NØXİ]™TÙXİ[ÛŠ
NÛYØ[]Ú

NÙœ]Y\TÙ[XİÜ[
	ØVÚ™Y—IÊK™›Ü‘XXÚ
OOØÛÛœİXK™Ù]]šX]J	Ú™Y‰Ê_	ÉÎÚYŠ	‰ˆZœİ\ÕÚ]
	ÈÉÊI‰ˆK×šÏÎ‹ÚK\İ

I‰ˆZœİ\ÕÚ]
	Ú˜]˜\ØÜš\‰ÊI‰ˆZœİ\ÕÚ]
	ÛXZ[Î‰ÊI‰ˆZœİ\ÕÚ]
	İ[‰ÊJXK\™Ù]I×İÜ	ßJNÙ˜Y]™[\İ[™\Š	ØÛXÚÉËOOØÛÛœİYK\™Ù]˜ÛÜÙ\İ
	Ø]Û‹IÊNÚYŠ]
\™]\›ØÛÛœİÏ\ÙXİ[Û‘œ›ÛU\™Ù]

NÚYŠÊ[X\šÊÊNÚYŠÛÛ\][Û•\™Ù]

J^ÙKœ™]™[Y˜][

NÙKœİÜ[[YYX]T›ÜYØ][ÛŠ
NÜÙ][Y[İ]


OOÛYØ[]Ú

NÜØÛÜ™Qœ›ÛQÛJ
NØÛÛœİİYØ]Tİ]\Ê
NÚYŠ\İ›ÚÊ^İØ\İ
	Õ˜[Y][Ûˆ™Y\ğêYHˆ	ÊÊİ›Z\ÜÚ[™Ë›[™İÉÜÙXİ[ÛœÈ0è\˜Ûİ\š\ˆˆ	ÊÜİ›Z\ÜÚ[™Ëš›Ú[Š	Ë	ÊJÉËˆ	Î‰ÉÊJÊYØ]Kœ]Z^”\ÜÙYÉÔPÓH8¢iHÍH	H™\]Z\Ë‰Î‰ÉÊK˜[ÙJNÜ™]\›ŸYš[˜[^™JØ[Ó™^

J_K
_Y[ÙHÙ][Y[İ]


OOØXİ]™TÙXİ[ÛŠ
NÜØÛÜ™Qœ›ÛQÛJ
NÛYØ[]Ú

_K
_KYJNÙ˜Y]™[\İ[™\Š	ØÚ[™ÙIËOOØÛÛœİYK\™Ù]Ë˜[YNÚYŠ™\]Z\™Yš[˜ÛY\ÊŠJ[X\šÊŠNÜÙ][Y[İ]


OO˜Xİ]™TÙXİ[ÛŠ
K
_KYJNØÛÛœİ[Ï[™]È]]][Û“ØœÙ\™\Š

OOØÛX\•[Y[İ]
[Ë—İ
NÛ[Ë—İ\Ù][Y[İ]


OOØXİ]™TÙXİ[ÛŠ
NÜØÛÜ™Qœ›ÛQÛJ
NÛYØ[]Ú

_K
_JNÛ[Ë›ØœÙ\™J˜›ÙKÜİX™YNYKÚ[\İYKÚ\˜Xİ\‘]NYK]šX]\ÎYK]šX]Qš[\–ÉØÛ\ÜÉË	Üİ[I×_J_Bˆœ˜[YK˜Y]™[\İ[™\Š	ÛØY	Ë]XÚ
NÙœ˜[YKœÜ˜ÏXÙ™ËœÜ˜ÎÂŸJJ
NÂ