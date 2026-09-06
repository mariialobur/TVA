from pathlib import Path
p=Path('m05-deduction-impot-prealable-dip.html')
t=p.read_text(encoding='utf-8')
for old,new in [
    ('quittance e-dec OFDF','preuve / décision électronique OFDF'),
    ('Quittance e-dec OFDF','Preuve / décision électronique OFDF'),
    ('quittance e-dec','preuve électronique OFDF'),
    ('Quittance e-dec','Preuve électronique OFDF'),
    ('décision de taxation e-dec','décision de taxation / preuve électronique OFDF'),
    ('e-dec ou décision de taxation OFDF','preuve / décision électronique OFDF'),
]:
    if old in t:
        print('replace',old,t.count(old)); t=t.replace(old,new)
p.write_text(t,encoding='utf-8')
