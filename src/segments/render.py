import sys,os,json
from seg5 import *
from playwright.sync_api import sync_playwright
only=sys.argv[1:]
meta=[]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1440,'height':900},device_scale_factor=1.25)
    for code,name,segs in SEGS:
        if only and code not in only: continue
        for sid,sname,fn in segs:
            for v in (1,2,3):
                html=f'<!doctype html><meta charset=utf-8><style>{CSS}</style><body>{page(fn(v),v)}'
                open('/tmp/claude-0/seg/tmp.html','w').write(html); pg.goto('file:///tmp/claude-0/seg/tmp.html'); pg.wait_for_timeout(150)
                d=f'out/{code}_{name.lower().replace(" ","-")}'; os.makedirs(d,exist_ok=True)
                fp=f'{d}/UNT-SEG-{code}_{sid}_V{v}.png'; pg.locator('#seg').screenshot(path=fp)
    b.close()
print('ok')
