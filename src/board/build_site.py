import base64,html,io,glob,os,re,sys
from PIL import Image
exec(open('build4.py').read().split('def b64')[0])
sys.path.insert(0,'/tmp/claude-0/seg')
from seg5 import SEGS
SO={c:ss for c,n,ss in SEGS}
G=[list(g) for g in G]
G[0][2]='Entry points and authentication.'; G[1][2]='Browse, choose, pay, keep.'; G[2][2]='Create, price, sell, get paid.'; G[3][2]='Eight tabs: Overview, Events, Orders, Users, Payouts, Reports, Settings, Audit log.'
NOTE={'P01':'Hero, events, categories, process, organiser entry, footer.','P02':'Split layout, form left.','P03':'Account creation.','P04':'Request a reset link.','P05':'Search, results, calendar.','P06':'Hero, details, lineup, tickets.','P07':'Seat map and selection summary.','P08':'Contact, payment, order summary.','P09':'Confirmation and issued ticket.','P10':'Ticket list and ticket detail.','P11':'Account details.','P12':'Event basics, then review.','P13':'Ticket tier editor.','P14':'Stats, chart, orders.','P15':'Balance, history, bank details.','P16':'Overview, events, orders, approvals.','P17':'Users, payouts, reports, settings, audit.'}
def b64(p,w=1000,q=74):
    im=Image.open(p).convert('RGB'); im.thumbnail((w,w*3)); bio=io.BytesIO(); im.save(bio,'JPEG',quality=q,optimize=True); return base64.b64encode(bio.getvalue()).decode()
def ov(code): return {v:glob.glob(f'/tmp/claude-0/ill/out/final/{code}_*/*_{v}.png')[0] for v in 'ABC'}
VN=['Grid','Cards','Type']
os.makedirs('/tmp/claude-0/site/images',exist_ok=True)
def tile(fp,t,w):
    base=os.path.basename(fp).replace('.png','').replace('UNT-ILL-','').replace('UNT-SEG-','seg-')
    im=Image.open(fp).convert('RGB'); im.thumbnail((w,w*3)); im.save(f'/tmp/claude-0/site/images/{base}.jpg',quality=82,optimize=True)
    with Image.open(f'/tmp/claude-0/site/images/{base}.jpg') as z: W,H=z.size
    return f'<a class="t" href="images/{base}.jpg" data-t="{html.escape(t)}"><img loading="lazy" width="{W}" height="{H}" alt="{html.escape(t)}" src="images/{base}.jpg"></a>'
NS=sum(len(s) for s in SO.values()); NI=NS*3+51
idx='';body=''
for gid,gn,gd,pages in G:
    idx+=f'<div class="ig"><button type="button" class="ih"><span>{gn}</span><span class="ar"></span></button>'+''.join(f'<a href="#{c}" data-open="{c}">{c} {html.escape(n)}</a>' for c,n,_,_,_ in pages)+'</div>'
    body+=f'<section id="{gid}"><div class="gh"><h2>{gn}</h2><p>{gd}</p><span class="cnt">{len(pages)} pages</span></div>'
    for code,name,note,req,ref in pages:
        d=glob.glob(f'/tmp/claude-0/seg/out/{code}_*')[0]; o=ov(code)
        ns=len(SO[code])
        body+=f'<details class="pg" id="{code}"><summary><span class="n">{code}</span><span class="nm">{html.escape(name)}{"<i>Required</i>" if req else ""}</span><span class="ds">{NOTE[code]}</span><span class="ct">{ns} segment{"" if ns==1 else "s"}</span><span class="pm"></span></summary><div class="pb">'
        body+=f'<details class="sg"><summary><span class="nm">Full page</span><span class="ds">Art direction, 3 variants</span><span class="ct">Ref {ref}</span><span class="pm"></span></summary><div class="tri">'+''.join(tile(o[v],f'{code} {name} / art {v}',700) for v in 'ABC')+'</div></details>'
        for sid,sname,_f in SO[code]:
            body+=f'<details class="sg"><summary><span class="nm">{html.escape(sname)}</span><span class="ds"></span><span class="ct">3 directions</span><span class="pm"></span></summary><div class="tri">'+''.join(tile(f'{d}/UNT-SEG-{code}_{sid}_V{v}.png',f'{code} {sname} / {VN[v-1]}',900) for v in (1,2,3))+'</div></details>'
        body+='</div></details>'
    body+='</section>'
CSS='''
:root{color-scheme:light;--ln:#cfcfd2;--mu:#76767b;--ink:#111}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:#fff;color:var(--ink);font:14px/1.45 "Helvetica Neue",Helvetica,Inter,Arial,sans-serif;-webkit-font-smoothing:antialiased;padding:0 max(20px,env(safe-area-inset-right,0px)) 120px max(20px,env(safe-area-inset-left,0px))}
a{color:inherit;text-decoration:none}
.bar{max-width:1280px;margin:0 auto;height:64px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--ln);position:sticky;top:0;background:#fff;z-index:5}
.bar b{font-weight:700;letter-spacing:.02em}.bar span{color:var(--mu)}
.bar button{font:inherit;background:none;border:0;color:var(--ink);cursor:pointer;padding:0;margin-left:20px}.bar button:hover{text-decoration:underline}
.wrap{max-width:1280px;margin:0 auto;display:grid;grid-template-columns:220px 1fr;gap:0 40px}
aside{position:sticky;top:64px;align-self:start;max-height:calc(100vh - 64px);overflow:auto;padding:36px 0;font-size:13px}
.ig{margin-bottom:22px}.ig a{display:block;color:var(--mu);padding:1px 0}
.ih{all:unset;box-sizing:border-box;display:flex!important;width:100%;justify-content:space-between;align-items:center;cursor:pointer;color:var(--ink);font-weight:600;margin-bottom:4px;padding:1px 0}
.ar{width:8px;height:8px;border-right:1px solid var(--ink);border-bottom:1px solid var(--ink);transform:rotate(45deg) translate(-2px,-2px);transition:transform .2s}
.ig.shut .ar{transform:rotate(-45deg)}.ig.shut a{display:none}
.wrap{transition:grid-template-columns .25s}body.nox .wrap{grid-template-columns:0 1fr}body.nox aside{visibility:hidden;opacity:0;overflow:hidden}aside{transition:opacity .2s}
body.nox .top,body.nox main{grid-column:2}.ig a:hover{color:var(--ink)}
.top{grid-column:2;padding:88px 0 8px}
.top h1{font-size:clamp(40px,6vw,72px);line-height:1;font-weight:500;letter-spacing:-.04em;margin:0 0 24px}
.top p{margin:0;color:var(--mu);max-width:520px}
main{grid-column:2}
section{padding-top:72px}
.gh{display:grid;grid-template-columns:1fr 1fr 120px;gap:20px;border-top:1px solid var(--ink);padding-top:16px;align-items:start}
.gh h2{margin:0;font-size:28px;font-weight:500;letter-spacing:-.025em;line-height:1.1}.gh p{margin:4px 0 0;color:var(--mu)}.cnt{text-align:right;color:var(--mu)}
details>summary{list-style:none;cursor:pointer}details>summary::-webkit-details-marker{display:none}
.pg>summary{display:grid;grid-template-columns:56px 1.1fr 1.4fr 110px 24px;gap:20px;align-items:baseline;padding:20px 0;border-bottom:1px solid var(--ln)}
.pg:first-of-type>summary{margin-top:0}
.pg .n{color:var(--mu);font-size:12px}.pg .nm{font-size:22px;letter-spacing:-.02em;font-weight:400}.pg .nm i{font-style:normal;font-size:11px;color:var(--mu);border:1px solid var(--ln);border-radius:999px;padding:1px 8px;margin-left:10px;vertical-align:middle}
.ds{color:var(--mu)}.ct{color:var(--mu);text-align:right;font-size:13px}
.pm{position:relative;width:14px;height:14px;justify-self:end;align-self:center}.pm:before,.pm:after{content:"";position:absolute;left:0;right:0;top:6.5px;height:1px;background:var(--ink)}.pm:after{transform:rotate(90deg);transition:transform .2s}
details[open]>summary>.pm:after{transform:rotate(0)}
.pg>summary:hover .nm{text-decoration:underline;text-underline-offset:4px}
.pb{padding:0 0 24px 76px}
.sg>summary{display:grid;grid-template-columns:1.1fr 1.4fr 110px 24px;gap:20px;align-items:baseline;padding:14px 0;border-bottom:1px solid var(--ln)}
.sg .nm{font-size:15px}.sg>summary:hover .nm{text-decoration:underline;text-underline-offset:3px}
.tri{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;align-items:start;padding:20px 0 28px}
.t{display:block;cursor:zoom-in}.t img{display:block;width:100%;height:auto;background:#fff;border:1px solid var(--ln)}
footer{margin-top:96px;border-top:1px solid var(--ink);padding-top:14px;color:var(--mu);font-size:12px}
.lb{position:fixed;inset:0;background:rgba(255,255,255,.97);z-index:20;display:flex;align-items:center;justify-content:center;padding:56px 72px 40px}
.lb[hidden]{display:none!important}.lb figure{margin:0;max-width:100%;max-height:100%;display:flex;flex-direction:column;gap:12px;align-items:center}.lb img{max-width:100%;max-height:calc(100vh - 140px);border:1px solid var(--ln)}
.lb figcaption{color:var(--mu);font-size:13px}.lb button{position:absolute;background:none;border:0;font:inherit;font-size:13px;cursor:pointer;color:var(--ink)}
#lbx{top:20px;right:28px}#lbp{left:24px;top:50%}#lbn{right:24px;top:50%}
@media(max-width:900px){.wrap{display:block}aside{display:none}#tx{display:none}.top{padding:56px 0 32px}.gh{grid-template-columns:1fr}.cnt{text-align:left}.pg>summary{grid-template-columns:44px 1fr 24px}.pg .ds,.pg .ct{display:none}.pb{padding-left:0}.sg>summary{grid-template-columns:1fr 24px}.sg .ds,.sg .ct{display:none}.tri{grid-template-columns:1fr}.lb{padding:56px 16px 24px}}
'''
CSS+='''
.bar{max-width:none;margin:0;display:block;height:64px;padding:0 40px;border:0;border-bottom:1px solid var(--ln)}
.bc{display:flex;align-items:center;justify-content:space-between;height:63px}
.c{max-width:1080px;margin:0 auto}
#pg{margin-left:248px;transition:margin-left .28s ease;padding:0 40px 0 0;min-height:100vh}
#pg .bar{padding:0 0 0 0}#pg .bar .c{padding:0 0 0 40px}
#pg .c{padding:0 0 0 40px}
#sb{position:fixed;left:0;top:0;bottom:0;width:248px;background:#fff;border-right:1px solid var(--ln);z-index:8;overflow:hidden;transition:width .28s ease,transform .28s ease}
.sbh{height:64px;display:flex;align-items:center;justify-content:space-between;padding:0 14px 0 24px;border-bottom:1px solid var(--ln)}
#tx{all:unset;cursor:pointer;width:34px;height:34px;display:flex;align-items:center;justify-content:center;border-radius:8px;color:var(--ink);flex:none}#tx:hover{background:#f1f1f3}
.sbl{height:calc(100% - 64px);overflow:auto;padding:28px 24px;font-size:13px;width:248px;transition:opacity .2s}
body.nox #sb{width:64px}body.nox .sbl{opacity:0;pointer-events:none}body.nox .sbh{padding:0;justify-content:center}body.nox .sbh b{display:none}
body.nox #pg{margin-left:64px}
#tm{display:none;margin:0}
.top{padding:88px 0 8px}
@media(max-width:900px){#pg{margin-left:0!important;padding:0}#pg .bar{padding:0 16px}#pg .c{padding:0 16px}#sb{transform:translateX(-100%);width:248px!important}body.mopen #sb{transform:none;box-shadow:0 0 0 100vmax rgba(0,0,0,.18)}body.nox .sbl{opacity:1;pointer-events:auto}body.nox .sbh{justify-content:space-between;padding:0 14px 0 24px}body.nox .sbh b{display:inline}#tm{display:inline;margin:0}.bc span{display:none}.top{padding:48px 0 8px}}
'''
page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Untitled Reference Board</title><meta name="description" content="Untitled: Events and Ticketing Engine design reference board"><style>{CSS}</style></head><body>
<nav id="sb" aria-label="Pages"><div class="sbh"><b>UNTITLED</b><button id="tx" type="button" aria-label="Toggle sidebar" title="Toggle sidebar"><svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.4"><rect x="2.5" y="3.5" width="15" height="13" rx="2"/><path d="M7.5 3.5v13"/></svg></button></div><div class="sbl">{idx}</div></nav>
<div id="pg"><div class="bar"><div class="c bc"><button id="tm" type="button">Index</button><span>Reference board</span><div><button id="ea">Expand all</button><button id="ca">Collapse all</button></div></div></div>
<div class="c"><div class="top"><h1>Events and<br>Ticketing Engine</h1><p>17 pages, {NS} segments, {NI} images.</p></div>
<main>{body}
<footer>Names, emails and card numbers are placeholders.</footer></main></div></div>
<div id="lb" class="lb" hidden><button id="lbx">Close</button><button id="lbp">Prev</button><button id="lbn">Next</button><figure><img id="lbi" alt=""><figcaption id="lbt"></figcaption></figure></div>
<script>
(function(){{var $=function(s){{return document.querySelectorAll(s)}};
var tx=document.getElementById('tx');function idxState(h){{document.body.classList.toggle('nox',h);try{{localStorage.setItem('nox',h?'1':'0')}}catch(e){{}}}}
tx.onclick=function(){{if(innerWidth<=900){{document.body.classList.remove('mopen')}}else idxState(!document.body.classList.contains('nox'))}};
document.getElementById('tm').onclick=function(e){{e.stopPropagation();document.body.classList.toggle('mopen')}};
document.addEventListener('click',function(e){{if(document.body.classList.contains('mopen')&&!e.target.closest('#sb'))document.body.classList.remove('mopen')}});
try{{if(localStorage.getItem('nox')==='1')idxState(true)}}catch(e){{}}
$('.ih').forEach(function(b){{b.addEventListener('click',function(){{b.parentNode.classList.toggle('shut')}})}});
function setAll(v){{$('details').forEach(function(d){{d.open=v}})}}
document.getElementById('ea').onclick=function(){{setAll(true)}};document.getElementById('ca').onclick=function(){{setAll(false)}};
function openId(id){{var e=document.getElementById(id);if(e&&e.tagName==='DETAILS'){{e.open=true;setTimeout(function(){{e.scrollIntoView()}},30)}}}}
$('[data-open]').forEach(function(a){{a.addEventListener('click',function(e){{e.preventDefault();document.body.classList.remove('mopen');openId(a.dataset.open);history.replaceState(null,'','#'+a.dataset.open)}})}});
if(location.hash)openId(location.hash.slice(1));
var lb=document.getElementById('lb'),im=document.getElementById('lbi'),cap=document.getElementById('lbt'),cur=[],ix=0;
function show(){{var a=cur[ix];im.src=a.querySelector('img').src;cap.textContent=a.dataset.t+'  ('+(ix+1)+'/'+cur.length+')'}}
function close(){{lb.hidden=true;document.body.style.overflow=''}}
$('.t').forEach(function(a){{a.addEventListener('click',function(e){{e.preventDefault();cur=[].slice.call(a.parentNode.querySelectorAll('.t'));ix=cur.indexOf(a);show();lb.hidden=false;document.body.style.overflow='hidden'}})}});
function step(d){{ix=(ix+d+cur.length)%cur.length;show()}}
document.getElementById('lbp').onclick=function(e){{e.stopPropagation();step(-1)}};document.getElementById('lbn').onclick=function(e){{e.stopPropagation();step(1)}};document.getElementById('lbx').onclick=close;
lb.addEventListener('click',function(e){{if(e.target===lb)close()}});
document.addEventListener('keydown',function(e){{if(lb.hidden)return;if(e.key==='Escape')close();if(e.key==='ArrowLeft')step(-1);if(e.key==='ArrowRight')step(1)}});}})();
</script></body></html>'''
out='/tmp/claude-0/site/index.html'
open(out,'w').write(page);print(len(page)//1024,'KB')
