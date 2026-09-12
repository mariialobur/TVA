from pathlib import Path

DIRECT = [
    Path('m09-secteurs-sensibles-tva.html'),
    Path('m12-jurisprudence-lab-tva.html'),
    Path('m13-communication-fiscale-cabinet.html'),
]

for path in DIRECT:
    text = path.read_text(encoding='utf-8')
    if 'course-practice-gates.js' not in text:
        marker = '</body></html>'
        if marker in text:
            text = text.replace(marker, '<script src="course-practice-gates.js"></script></body></html>', 1)
        elif '</body>' in text:
            text = text.replace('</body>', '<script src="course-practice-gates.js"></script></body>', 1)
        else:
            raise SystemExit(f'{path}: closing body not found')
        path.write_text(text, encoding='utf-8')
        print(f'{path}: practice gate script injected')
    else:
        print(f'{path}: already wired')

qa = Path('tools/course-browser-qa.mjs')
text = qa.read_text(encoding='utf-8')
old = "await p.evaluate(([k,ss])=>{const v={visited:{},quizScore:75};ss.forEach(s=>v.visited[s]=1);localStorage.setItem(k,JSON.stringify(v))},[key,secs]);"
new = "await p.evaluate(([k,ss,m])=>{const v={visited:{},quizScore:75};ss.forEach(s=>v.visited[s]=1);localStorage.setItem(k,JSON.stringify(v));const req={M09:[2,5,7,9],M10:[4,6,9,11],M11:[2,4,9,11],M12:[0,6,7,11],M13:[1,4,6,11]}[m]||[],pg={complete:{}};req.forEach(i=>pg.complete[String(i)]=true);localStorage.setItem('tvaPracticeGateV1_'+m,JSON.stringify(pg))},[key,secs,mod]);"
if old in text:
    text = text.replace(old, new, 1)
    qa.write_text(text, encoding='utf-8')
    print('course-browser-qa: valid late-module state now includes practical gate')
elif 'tvaPracticeGateV1_' in text:
    print('course-browser-qa: already practice-aware')
else:
    raise SystemExit('course-browser-qa: expected valid-gate fixture not found')

static = Path('tools/course-qa.mjs')
text = static.read_text(encoding='utf-8')
if "'course-practice-gates.js'" not in text:
    text = text.replace("'course-current-law-2026.js',", "'course-current-law-2026.js','course-practice-gates.js',", 1)

old_parse = "const gate=read('course-legacy-gate.js'),law=read('course-current-law-2026.js');try{new Function(gate);ok('legacy gate JavaScript parses')}catch(e){die('course-legacy-gate.js syntax: '+e.message)}try{new Function(law);ok('current-law JavaScript parses')}catch(e){die('course-current-law-2026.js syntax: '+e.message)}"
new_parse = "const gate=read('course-legacy-gate.js'),law=read('course-current-law-2026.js'),practice=read('course-practice-gates.js');try{new Function(gate);ok('legacy gate JavaScript parses')}catch(e){die('course-legacy-gate.js syntax: '+e.message)}try{new Function(law);ok('current-law JavaScript parses')}catch(e){die('course-current-law-2026.js syntax: '+e.message)}try{new Function(practice);ok('practical mastery gate JavaScript parses')}catch(e){die('course-practice-gates.js syntax: '+e.message)}"
if old_parse in text:
    text = text.replace(old_parse, new_parse, 1)

old_contract = "for(const [m,f] of [['M09','m09-secteurs-sensibles-tva.html'],['M10','m10-digital-plateformes-ecommerce.html'],['M11','m11-controle-afc-tva.html'],['M12','m12-jurisprudence-lab-tva.html'],['M13','m13-communication-fiscale-cabinet.html']]){const s=read(f);if(!s.includes('finishModule')||!s.includes('quizScore')||!s.includes('>=75')||!s.includes(`${m}='done'`))die(m+' completion gate contract incomplete')}if(!process.exitCode)ok('M09–M13 completion gate contracts present');"
new_contract = "for(const [m,f] of [['M09','m09-secteurs-sensibles-tva.html'],['M10','m10-digital-plateformes-ecommerce.html'],['M11','m11-controle-afc-tva.html'],['M12','m12-jurisprudence-lab-tva.html'],['M13','m13-communication-fiscale-cabinet.html']]){const s=read(f);if(!s.includes('finishModule')||!s.includes('quizScore')||!s.includes('>=75')||!s.includes(`${m}='done'`)||!s.includes('course-practice-gates.js'))die(m+' completion/practice gate contract incomplete')}for(const m of ['M09','M10','M11','M12','M13'])if(!practice.includes(m+':{required:['))die(m+' essential-case configuration missing');if(!process.exitCode)ok('M09–M13 completion and practical mastery gate contracts present');"
if old_contract in text:
    text = text.replace(old_contract, new_contract, 1)
elif 'practical mastery gate contracts present' not in text:
    raise SystemExit('course-qa: expected M09-M13 completion contract not found')
static.write_text(text, encoding='utf-8')
print('course-qa: practice asset, syntax and wiring checks enabled')
