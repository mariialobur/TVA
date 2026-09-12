from pathlib import Path

MODULES = [
    Path('m09-secteurs-sensibles-tva.html'),
    Path('m10-digital-plateformes-ecommerce.html'),
    Path('m11-controle-afc-tva.html'),
    Path('m12-jurisprudence-lab-tva.html'),
    Path('m13-communication-fiscale-cabinet.html'),
]

for path in MODULES:
    text = path.read_text(encoding='utf-8')
    if 'course-capstone-dossiers.js' not in text:
        if '</body>' not in text:
            raise SystemExit(f'{path}: closing body not found')
        text = text.replace('</body>', '<script src="course-capstone-dossiers.js"></script></body>', 1)
        path.write_text(text, encoding='utf-8')
        print(f'{path}: written capstone layer injected')
    else:
        print(f'{path}: already wired')

practice = Path('course-practice-gates.js')
text = practice.read_text(encoding='utf-8')
if 'practiceGateCapstoneListener' not in text:
    needle = "    return true;\n  }\n\n  function init(){"
    repl = "    if(!doc.body.dataset.practiceGateCapstoneListener){\n      doc.body.dataset.practiceGateCapstoneListener='1';\n      doc.addEventListener('tva:capstone-complete',()=>decorate(doc));\n    }\n    return true;\n  }\n\n  function init(){"
    if needle not in text:
        raise SystemExit('course-practice-gates.js: attach return marker not found')
    text = text.replace(needle, repl, 1)
    practice.write_text(text, encoding='utf-8')
    print('course-practice-gates.js: capstone completion refresh enabled')

static = Path('tools/course-qa.mjs')
text = static.read_text(encoding='utf-8')
if "'course-capstone-dossiers.js'" not in text:
    text = text.replace("'course-practice-gates.js',", "'course-practice-gates.js','course-capstone-dossiers.js',", 1)

if "const capstone=read('course-capstone-dossiers.js')" not in text:
    needle = "try{new Function(practice);ok('practical mastery gate JavaScript parses')}catch(e){die('course-practice-gates.js syntax: '+e.message)}"
    repl = needle + "const capstone=read('course-capstone-dossiers.js');try{new Function(capstone);ok('written capstone JavaScript parses')}catch(e){die('course-capstone-dossiers.js syntax: '+e.message)}"
    if needle not in text:
        raise SystemExit('course-qa.mjs: practice parse marker not found')
    text = text.replace(needle, repl, 1)

text = text.replace("||!s.includes('course-practice-gates.js'))die(m+' completion/practice gate contract incomplete')", "||!s.includes('course-practice-gates.js')||!s.includes('course-capstone-dossiers.js'))die(m+' completion/practice/capstone contract incomplete')")
if "essential written capstone configuration missing" not in text:
    needle = "for(const m of ['M09','M10','M11','M12','M13'])if(!practice.includes(m+':{required:['))die(m+' essential-case configuration missing');if(!process.exitCode)ok('M09–M13 completion and practical mastery gate contracts present');"
    repl = "for(const m of ['M09','M10','M11','M12','M13'])if(!practice.includes(m+':{required:['))die(m+' essential-case configuration missing');for(const m of ['M09','M10','M11','M12','M13'])if(!capstone.includes(m+':{caseIndex:'))die(m+' essential written capstone configuration missing');if(!process.exitCode)ok('M09–M13 completion, practical mastery and written capstone contracts present');"
    if needle not in text:
        raise SystemExit('course-qa.mjs: M09-M13 contract marker not found')
    text = text.replace(needle, repl, 1)
static.write_text(text, encoding='utf-8')
print('course-qa.mjs: capstone asset, syntax and wiring checks enabled')
