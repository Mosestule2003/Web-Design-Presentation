import base64,html,io,glob,re
from PIL import Image
G=[('public','Public and sign-in','The first impression and the way in. One reeded-glass panel per page.',[('P01','Landing','Home page with the event hero and sign-in entry.',0,'HERO-01, ART-01'),('P02','Login','Split layout: form left, art right. Mandatory.',1,'AUTH-03'),('P03','Sign up','Account creation, same split layout.',0,'AUTH-04'),('P04','Password reset','Request a reset link. Mandatory.',1,'AUTH-02')]),
('customer','Customers','Find an event, pick seats, pay, and keep the ticket.',[('P05','Discover events','Calendar and date cards with category filters.',0,'LIST-01, LIST-02'),('P06','Event details','Halftone stage art with the booking card.',0,'AUTH-01, HERO-01'),('P07','Seat selection','Seat map with text-labelled states, summary and hold timer.',0,'SEAT-01'),('P08','Checkout','Ticket preview next to the order summary.',0,'SEAT-01'),('P09','Order confirmation','Confirmation card and the issued ticket.',0,'CARD-02'),('P10','My tickets','Wallet-style stack of upcoming tickets.',0,'CARD-01'),('P11','Profile','Account details on a dot-matrix sphere. Mandatory.',1,'AUTH-02')]),
('organiser','Organisers','Create events, define ticket types, watch sales and get paid.',[('P12','Create event','Step form: basics, date, tickets, publish.',0,'LIST-01'),('P13','Custom ticket types','Tier cards with state tags.',0,'CARD-01'),('P14','Event dashboard','Stat tiles and a dot-matrix sales chart.',0,'DASH-01'),('P15','Payout details','Balance, payout history and bank details.',0,'DASH-01')]),
('admin','Admin','The admin dashboard has eight tabs: every segment below sits inside its tab, with a sidebar in two directions and top tabs in the third.',[('P16','Admin overview','Activity heat grid and platform totals. Mandatory.',1,'DASH-01'),('P17','Admin users','User list with roles and moderation status. Mandatory.',1,'DASH-01')])]
def b64(p):
    im=Image.open(p).convert('RGB');im.thumbnail((1100,1100));bio=io.BytesIO();im.save(bio,'JPEG',quality=80,optimize=True);return base64.b64encode(bio.getvalue()).decode()
def files(code):
    return {v:glob.glob(f'/tmp/claude-0/ill/out/final/{code}_*/*_{v}.png')[0] for v in 'ABC'}
VN={'A':'Variant A · Peach','B':'Variant B · Ember','C':'Variant C · Magenta'}
def tile(code,name,v,span,rows,fp):
    t=html.escape(f'{code} {name} — {VN[v]}')
    return f'<a class="tile" style="--c:{span};--r:{rows}" href="#" data-t="{t}"><img loading="lazy" alt="{t}" src="data:image/jpeg;base64,{b64(fp)}"></a>'
nav=''.join(f'<a href="#{g[0]}">{g[1]}</a>' for g in G);cards='';body=''
for gid,gn,gd,pages in G:
    body+=f'<section id="{gid}"><header class="gh"><p class="eyebrow">{len(pages)} pages</p><h2>{gn}</h2><p class="sub">{gd}</p></header>'
    for code,name,note,req,ref in pages:
        f=files(code);n=code[1:]
        cards+=f'<a class="card" href="#{code}"><b>{n}</b><span>{html.escape(name)}</span><i>{gn}</i></a>'
        tag='<em>Required</em>' if req else ''
        body+=f'<div class="cat" id="{code}"><div class="ch"><h3>{code} · {html.escape(name)}</h3>{tag}<em>Ref {ref}</em></div><p class="note">{note}</p><div class="mosaic">{tile(code,name,"A",4,2,f["A"])}{tile(code,name,"B",2,1,f["B"])}{tile(code,name,"C",2,1,f["C"])}</div></div>'
    body+='</section>'
hero=''.join(f'<img alt="" src="data:image/jpeg;base64,{b64(files(c)[v])}">' for c,v in [('P07','B'),('P01','A'),('P14','C'),('P10','A'),('P13','B')])
head=open('head.html').read().replace('</style>',open('extra.css').read()+'</style>').replace('Ticketing UI References','Untitled Illustrations')
page=head+f'''<div class="wrap">
<div class="top"><p class="eyebrow">Untitled · Events and Ticketing Engine</p><h1>Every screen, <br>one quiet stage.</h1><p class="lead">51 original illustrations for the 17 pages, drawn in the language of the reference folder: ribbed glass, dot-matrix, halftone and grain. Click any image to enlarge.</p>
<div class="stats"><div><b>17</b><span>pages</span></div><div><b>3</b><span>variants each</span></div><div><b>4</b><span>user groups</span></div></div></div>
<div class="hero">{hero}</div>
<nav aria-label="User groups">{nav}</nav>
<section class="index"><header class="gh"><h2>All 17 pages</h2><p class="sub">Jump straight to the illustrations for any page.</p></header><div class="cards">{cards}</div></section>
{body}
<footer>Illustrations generated for Untitled (COMP 3540). File names follow UNT-ILL-Pxx_page_variant. Style references are the UNT-REF set in the Illustrative designs folder. Seat and ticket states are always shown with text as well as colour. Account numbers and names shown are placeholders.</footer>
</div>
<div id="lb" class="lb" hidden><button class="x" id="lbx" aria-label="Close">&times;</button><figure><img id="lbi" alt=""><figcaption><span id="lbt"></span></figcaption></figure></div>
<script>
(function(){{var lb=document.getElementById('lb'),im=document.getElementById('lbi'),t=document.getElementById('lbt');
function close(){{lb.hidden=true;document.body.style.overflow=''}}
document.querySelectorAll('.tile').forEach(function(a){{a.addEventListener('click',function(e){{e.preventDefault();im.src=a.querySelector('img').src;t.textContent=a.dataset.t;lb.hidden=false;document.body.style.overflow='hidden'}})}});
lb.addEventListener('click',function(e){{if(e.target===lb||e.target.id==='lbx')close()}});
document.addEventListener('keydown',function(e){{if(e.key==='Escape')close()}});}})();
</script>'''
out='/tmp/claude-0/-home-claude/b6500908-ee3b-5855-9837-591c56227862/scratchpad/ticketing-ui-references.html'
open(out,'w').write(page);print(len(page)//1024,'KB')
