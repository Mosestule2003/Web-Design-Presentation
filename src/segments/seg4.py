from seg3 import *
def statt(v,a,b,c,k=False):
    if v==1: return f'<div style="border-top:1px solid #0d0d0d;padding:16px 24px 8px 0"><div class="m">{a}</div><div style="font-size:60px;font-weight:300;letter-spacing:-.03em;margin:28px 0 6px">{b}</div><div class="m" style="color:var(--acc)">{c}</div></div>'
    if v==2: return f'<div class="card" style="padding:28px"><div class="row" style="justify-content:space-between"><span class="m">{a}</span>{tag(c)}</div><div style="font-size:56px;font-weight:300;letter-spacing:-.03em;margin-top:40px">{b}</div></div>'
    return f'<div style="border:1.5px solid #0d0d0d;border-radius:20px;padding:24px;{"background:#0d0d0d;color:#fff" if k else ""}"><span class="m">{a}</span><div class="l" style="font-size:72px;margin:28px 0 8px">{b}</div><span class="pill {"a" if k else ""}">{c}</span></div>'
def barchart(v,h=260,n=14):
    vals=[.4,.55,.5,.7,.62,.45,.5,.8,.95,.7,.6,.55,.75,.85]
    if v==3: return '<div class="row" style="gap:6px;align-items:end;height:%dpx">'%h+''.join(f'<div style="flex:1;display:flex;flex-direction:column;gap:4px;justify-content:end">'+''.join(f'<span style="height:10px;border-radius:50%;background:{"var(--acc)" if i==8 else "#0d0d0d"}"></span>' for _ in range(int(x*14)))+'</div>' for i,x in enumerate(vals))+'</div>'
    return '<div class="row" style="gap:12px;align-items:end;height:%dpx">'%h+''.join(f'<div style="flex:1;height:{int(x*h)}px;border-radius:{"8px 8px 2px 2px" if v==2 else "0"};background:{"var(--acc)" if i==8 else ("#e4e4e8" if v==2 else "#0d0d0d")}"></div>' for i,x in enumerate(vals))+'</div>'
def stats(v):
    S=[('Tickets sold','4,812','+12.4%'),('Gross revenue','$218k','+8.1%'),('Check-ins','3,206','67%'),('Refunds','1.2%','-0.3%')]
    top=head(v,'Summer Stage','Event dashboard',tag('Last 14 days','k')+tag('Export'))
    tiles=f'<div class="g" style="grid-template-columns:repeat(4,1fr);gap:{"20px" if v!=1 else "28px"}">'+''.join(statt(v,*s,k=(i==1)) for i,s in enumerate(S))+'</div>'
    ch=f'<div class="m" style="margin:48px 0 20px">Sales · last 14 days</div>'+(box(2,barchart(2),32) if v==2 else barchart(v))
    return top+tiles+ch
def salesorders(v):
    R=[['UNT-48213','Alex Morgan','3 × Reserved','$252.00',tag('Paid','a')],['UNT-48212','Priya Nair','2 × General','$90.00',tag('Paid','a')],['UNT-48211','Jon Weber','1 × VIP','$220.00',tag('Pending')],['UNT-48210','Mia Tremblay','4 × General','$180.00',tag('Refunded')],['UNT-48209','Kofi Mensah','2 × Reserved','$168.00',tag('Paid','a')]]
    t=tbl(v,['Order','Customer','Tickets','Amount','Status'],R,'1fr 1.2fr 1.2fr 1fr 1fr')
    side=f'<div class="m">Sales by ticket type</div>'+''.join(f'<div style="margin-top:22px"><div class="row" style="justify-content:space-between;font-size:15px"><span>{a}</span><span class="m">{b}</span></div><div style="height:{"8px" if v!=3 else "4px"};border-radius:4px;background:#ececec;margin-top:8px"><div style="width:{w}%;height:100%;border-radius:4px;background:{"var(--acc)" if v!=1 else "#0d0d0d"}"></div></div></div>' for a,b,w in [('General','1,420 / 2,000',71),('Reserved','2,880 / 3,200',90),('VIP','112 / 200',56)])
    if v==2: return head(2,'Recent orders','Sales')+f'<div class="g" style="grid-template-columns:1.8fr 1fr;gap:24px"><div class="card" style="padding:32px">{t}</div><div class="card" style="padding:32px">{side}</div></div>'
    return head(v,'Recent orders','Sales')+f'<div class="g" style="grid-template-columns:1.8fr 1fr;gap:72px"><div>{t}</div><div>{side}</div></div>'
def payoutbal(v):
    R=[['Summer Stage','02 Nov',tag('Paid','a'),'$6,210.00'],['Cup Final','26 Oct',tag('Paid','a'),'$7,480.00'],['Open Mic Gala','19 Oct',tag('Pending'),'$2,130.00'],['Tech Summit','12 Oct',tag('Paid','a'),'$2,600.00']]
    t=tbl(v,['Event','Date','Status','Amount'],R,'1.6fr 1fr 1fr 1fr')
    bal=f'<div class="m">Available balance</div><div class="l" style="font-size:{"140px" if v==3 else "88px"};margin:16px 0 12px">$18,420.00</div><div class="row" style="gap:12px;align-items:center"><span class="m">Next payout Fri 07 Nov · account ending 4821</span>{tag("Verified","a")}</div>'
    if v==2: return f'<div class="card" style="padding:44px;margin-bottom:24px;display:flex;justify-content:space-between;align-items:end"><div>{bal}</div><span class="btn a" style="white-space:nowrap">Request payout</span></div><div class="card" style="padding:32px">{t}</div>'
    return head(v,'Payouts','Organiser','<span class="btn a">Request payout</span>')+bal+'<div style="margin-top:48px"></div>'+t
def bank(v):
    F=lambda l,x:f'<div><div class="m lab" style="margin-top:0">{l}</div><div class="in">{x}</div></div>'
    body=f'<div class="g" style="grid-template-columns:1fr 1fr;gap:20px">{F("Account holder","Summer Stage Society")}{F("Bank","Example Credit Union")}{F("Institution / transit","•••• / •••••")}{F("Account number","•••••• 4821")}<div style="grid-column:span 2">{F("Payout schedule","Weekly · every Friday")}</div></div><div class="row" style="gap:12px;margin-top:32px"><span class="btn o">Cancel</span><span class="btn a">Save payout details</span></div>'
    side='<div class="m">Verification</div>'+''.join(f'<div class="row" style="gap:12px;align-items:center;margin-top:20px"><span class="dot"></span><span>{x}</span></div>' for x in ['Identity confirmed','Bank account linked','Tax details submitted'])
    if v==2: return f'<div class="g" style="grid-template-columns:1.6fr 1fr;gap:24px"><div class="card" style="padding:44px"><h2 class="t" style="font-size:36px;margin-bottom:28px">Payout details</h2>{body}</div><div class="card" style="padding:44px">{side}</div></div>'
    return head(v,'Payout details','Organiser')+f'<div class="g" style="grid-template-columns:1.6fr 1fr;gap:72px"><div style="{"border:1.5px solid #0d0d0d;border-radius:24px;padding:40px" if v==3 else ""}">{body}</div><div>{side}</div></div>'
def adminkpi(v):
    heat='<div class="g" style="grid-template-columns:repeat(24,1fr);gap:4px">'+''.join(f'<span style="aspect-ratio:1;border-radius:{"50%" if v==3 else "3px" if v==1 else "6px"};background:{["#eee","#f8c9b8","#f3977a","var(--acc)"][min(3,int((0.5+0.45*math.sin(j*.4+i*.3)+((i*31+j*17)%10-5)/20)*4))]}"></span>' for i in range(7) for j in range(24))+'</div>'
    S=[('Orders','12,481','+9%'),('New users','1,204','+14%'),('Open flags','7','-2')]
    tiles=f'<div class="g" style="grid-template-columns:repeat(3,1fr);gap:24px">'+''.join(statt(v,*s,k=(i==2)) for i,s in enumerate(S))+'</div>'
    return head(v,'Platform overview','Admin',tag('12 weeks','k')+tag('Export'))+tiles+'<div class="m" style="margin:44px 0 18px">Activity</div>'+(box(2,heat,28) if v==2 else heat)
def approvals(v):
    R=[['Lakeside Fest','Festival','Organiser: Okafor Events',tag('Review'),'<span class="btn s a">Approve</span>'],['Night Derby','Sport','Organiser: Prairie Sports',tag('Review'),'<span class="btn s a">Approve</span>'],['Tech Summit','Conference','Organiser: Interior Tech',tag('Flagged','k'),'<span class="btn s o">Inspect</span>'],['Open Mic Gala','Theatre','Organiser: Stage Left',tag('Review'),'<span class="btn s a">Approve</span>']]
    t=tbl(v,['Event','Type','Organiser','Status',''],R,'1.3fr 1fr 1.6fr 1fr 120px')
    return head(v,'Pending approvals','Moderation',tag('4 waiting','a'))+(box(2,t,32) if v==2 else t)
def users(v):
    N=[('Amara Okafor','Organiser','Active'),('Liam Chen','Customer','Active'),('Sofia Rossi','Customer','Flagged'),('Noah Patel','Organiser','Active'),('Mia Tremblay','Admin','Active'),('Kofi Mensah','Customer','Suspended')]
    def av(i): return f'<span style="display:flex;align-items:center;gap:12px"><span class="art" style="width:36px;height:36px;border-radius:50%;background-image:url({A}a{i%6}.jpg)"></span>{N[i][0]}</span>'
    R=[[av(i),n[1],tag(n[2],'k' if n[2]!='Active' else ''),'<span class="m">Manage</span>'] for i,n in enumerate(N)]
    t=tbl(v,['User','Role','Status',''],R,'2fr 1fr 1fr 100px')
    sr=f'<div class="in" style="width:320px;height:44px">Search users</div>'
    return head(v,'Users','Admin',sr)+(box(2,t,32) if v==2 else t)
def userdetail(v):
    rows=[('Role','Customer'),('Joined','Jan 2026'),('Orders','7'),('Reports','2 open'),('Last active','Today')]
    li=''.join(f'<div class="row" style="justify-content:space-between;padding:14px 0;border-top:1px solid {"#0d0d0d" if v==3 else "var(--ln)"}"><span class="m">{a}</span><span>{b}</span></div>' for a,b in rows)
    head_=f'<div class="row" style="gap:24px;align-items:center"><div class="art" style="width:96px;height:96px;border-radius:50%;background-image:url({A}sph_{"peach" if v==1 else "mag" if v==2 else "ember"}.jpg)"></div><div><div class="l" style="font-size:48px">Sofia Rossi</div><div style="margin-top:8px">{tag("Flagged","a")}</div></div></div>'
    act=f'<div class="m">Moderation</div><div class="in" style="height:110px;align-items:flex-start;padding-top:14px;margin-top:12px">Add a note…</div><div class="row" style="gap:10px;margin-top:16px"><span class="btn o">Dismiss flag</span><span class="btn o">Suspend</span><span class="btn a">Remove content</span></div>'
    if v==2: return f'<div class="g" style="grid-template-columns:1fr 1fr;gap:24px"><div class="card" style="padding:40px">{head_}<div style="margin-top:28px">{li}</div></div><div class="card" style="padding:40px">{act}</div></div>'
    return f'<div class="g" style="grid-template-columns:1fr 1fr;gap:72px"><div>{head_}<div style="margin-top:28px">{li}</div></div><div>{act}</div></div>'
SEGS=[('P01','Landing',[('hero','Hero',hero),('events','Featured events',events),('categories','Categories',cats),('how-it-works','How it works',how),('organiser-cta','Organiser call to action',orgcta),('footer','Footer',footer)]),
('P02','Login',[('form','Sign in',auth('login'))]),('P03','Sign up',[('form','Create account',auth('signup'))]),('P04','Password reset',[('form','Reset link',auth('reset'))]),
('P05','Discover events',[('search','Search and filters',filters),('results','Results',results),('calendar','Calendar',calendar)]),
('P06','Event details',[('hero','Event hero',evhero),('about','About and info',evabout),('lineup','Lineup and upcoming',evlineup),('tickets','Tickets and booking bar',evtiers)]),
('P07','Seat selection',[('map','Seat map',seatmap),('summary','Selection summary',seatsummary)]),
('P08','Checkout',[('payment','Contact and payment',payform),('summary','Order summary',ordersum)]),
('P09','Order confirmation',[('confirmation','Confirmation',confirm)]),
('P10','My tickets',[('list','Ticket list',mytickets),('detail','Ticket detail',ticketdetail)]),
('P11','Profile',[('account','Account',profile)]),
('P12','Create event',[('basics','Basics',createform),('publish','Review and publish',publish)]),
('P13','Ticket types',[('editor','Ticket type editor',tiereditor)]),
('P14','Event dashboard',[('stats','Stats and chart',stats),('orders','Orders and sales',salesorders)]),
('P15','Payout details',[('balance','Balance and history',payoutbal),('bank','Bank details',bank)]),
('P16','Admin overview',[('overview','Platform overview',adminkpi),('approvals','Approvals',approvals)]),
('P17','Admin users',[('list','User list',users),('detail','User detail',userdetail)])]
