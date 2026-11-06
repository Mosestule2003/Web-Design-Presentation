from seg4 import *
import seg4
TABS=['Overview','Events','Orders','Users','Payouts','Reports','Settings','Audit log']
def shell(v,active,inner):
    top=lambda: f'<div class="row" style="justify-content:space-between;align-items:center"><div class="row" style="gap:14px;align-items:center"><span class="logo">UNTITLED</span>{tag("Admin","k")}</div><div class="row" style="gap:12px;align-items:center"><div class="in" style="width:300px;height:42px;font-size:14px">Search orders, users, events</div><div class="art" style="width:40px;height:40px;border-radius:50%;background-image:url({A}sph_mag.jpg)"></div></div></div>'
    if v==1:
        side='<div style="border-top:1px solid #0d0d0d">'+''.join(f'<div class="row" style="justify-content:space-between;padding:14px 0;border-bottom:1px solid var(--ln);font-size:16px;{"font-weight:600" if t==active else "color:#666"}"><span>{t}</span>{"<span class=dot></span>" if t==active else "<span class=m>"+str(i+1).zfill(2)+"</span>"}</div>' for i,t in enumerate(TABS))+'</div>'
        return f'{top()}<div class="hr" style="margin:20px 0 36px"></div><div class="g" style="grid-template-columns:220px 1fr;gap:56px"><div>{side}</div><div>{inner}</div></div>'
    if v==2:
        side='<div class="card" style="padding:14px;border-radius:24px">'+''.join(f'<div style="padding:12px 16px;border-radius:999px;font-size:15px;margin-bottom:2px;{"background:#0d0d0d;color:#fff" if t==active else "color:#555"}">{t}</div>' for t in TABS)+'</div>'
        return f'<div class="card" style="padding:16px 24px;border-radius:999px;margin-bottom:28px">{top()}</div><div class="g" style="grid-template-columns:230px 1fr;gap:28px"><div>{side}</div><div>{inner}</div></div>'
    tabs='<div class="row" style="gap:28px;border-bottom:1.5px solid #0d0d0d;margin:24px 0 36px">'+''.join(f'<span style="padding:12px 0;font-size:16px;{"font-weight:600;border-bottom:4px solid var(--acc);margin-bottom:-2px" if t==active else "color:#777"}">{t}</span>' for t in TABS)+'</div>'
    return f'{top()}{tabs}{inner}'
def W(active,fn): return lambda v: shell(v,active,fn(v))
def adminevents(v):
    R=[['Summer Stage','Okafor Events','14 Jun','4,812',tag('Live','a')],['Cup Final','Prairie Sports','21 Jun','2,140',tag('Live','a')],['Open Mic Gala','Stage Left','02 Jul','310',tag('Review')],['Tech Summit','Interior Tech','18 Jul','880',tag('Flagged','k')],['Lakeside Fest','Okafor Events','26 Jul','0',tag('Draft')]]
    t=tbl(v,['Event','Organiser','Date','Sold','Status'],R,'1.4fr 1.3fr 1fr 1fr 1fr')
    return head(v,'Events','Manage',tag('All','k')+tag('Live')+tag('Review')+tag('Flagged'))+(box(2,t,28) if v==2 else t)
def adminorders(v):
    R=[['UNT-48213','Alex Morgan','Summer Stage','$274.05',tag('Paid','a'),'<span class=m>Refund</span>'],['UNT-48212','Priya Nair','Cup Final','$99.00',tag('Paid','a'),'<span class=m>Refund</span>'],['UNT-48211','Jon Weber','Tech Summit','$220.00',tag('Dispute','k'),'<span class=m>Review</span>'],['UNT-48210','Mia Tremblay','Summer Stage','$189.00',tag('Refunded'),'<span class=m>View</span>']]
    t=tbl(v,['Order','Customer','Event','Total','Status',''],R,'1fr 1.2fr 1.2fr 1fr 1fr 80px')
    return head(v,'Orders and refunds','Commerce',tag('Today','k')+tag('7 days')+tag('30 days'))+(box(2,t,28) if v==2 else t)
def adminpay(v):
    R=[['Okafor Events','Summer Stage','$6,210.00',tag('Ready','a'),'<span class="btn s a">Release</span>'],['Prairie Sports','Cup Final','$7,480.00',tag('Ready','a'),'<span class="btn s a">Release</span>'],['Stage Left','Open Mic Gala','$2,130.00',tag('Held'),'<span class="btn s o">Inspect</span>'],['Interior Tech','Tech Summit','$2,600.00',tag('Verify bank','k'),'<span class="btn s o">Inspect</span>']]
    t=tbl(v,['Organiser','Event','Amount','Status',''],R,'1.3fr 1.3fr 1fr 1fr 120px')
    return head(v,'Payout approvals','Money',tag('$18,420 ready','a'))+(box(2,t,28) if v==2 else t)
def adminreports(v):
    R=[['Misleading description','Tech Summit','3 reports',tag('Open','k'),'<span class="btn s a">Review</span>'],['Spam account','Sofia Rossi','2 reports',tag('Open','k'),'<span class="btn s a">Review</span>'],['Duplicate event','Lakeside Fest','1 report',tag('New'),'<span class="btn s o">Open</span>'],['Abusive comment','Kofi Mensah','1 report',tag('Closed'),'<span class="btn s o">View</span>']]
    t=tbl(v,['Reason','Subject','Count','Status',''],R,'1.6fr 1.2fr 1fr 1fr 110px')
    return head(v,'Reports and moderation','Safety',tag('7 open','a'))+(box(2,t,28) if v==2 else t)
def adminsettings(v):
    F=lambda a,b:f'<div class="row" style="justify-content:space-between;align-items:center;padding:20px 0;border-top:1px solid {"#0d0d0d" if v==3 else "var(--ln)"}"><div><div style="font-size:17px;font-weight:500">{a}</div><div class="sub" style="font-size:14px">{b}</div></div><div class="in" style="width:200px;height:44px">value</div></div>'
    rows=F('Service fee','Added to every order')+F('Hold timer','Seconds seats are held at checkout')+F('Refund window','Hours before event')+F('Categories','Concert, Sport, Theatre, Conference, Festival')
    return head(v,'Platform settings','Configuration','<span class="btn a">Save changes</span>')+(box(2,rows,32) if v==2 else rows)
def adminaudit(v):
    R=[['10:42','Mia Tremblay','Released payout','Okafor Events · $6,210.00'],['10:31','System','Hold expired','Order UNT-48214 · 3 seats'],['09:58','Mia Tremblay','Suspended user','Kofi Mensah'],['09:12','Noah Patel','Approved event','Lakeside Fest'],['08:40','System','Refund issued','UNT-48210 · $189.00']]
    t=tbl(v,['Time','Actor','Action','Detail'],R,'100px 1.2fr 1.3fr 2fr')
    return head(v,'Audit log','Security',tag('Today','k')+tag('Export'))+(box(2,t,28) if v==2 else t)
seg4.SEGS[:]=[s for s in seg4.SEGS if s[0] not in('P16','P17')]+[
('P16','Admin overview',[('overview','Overview tab',W('Overview',adminkpi)),('events','Events tab',W('Events',adminevents)),('orders','Orders tab',W('Orders',adminorders)),('approvals','Event approvals',W('Events',approvals))]),
('P17','Admin users',[('list','Users tab',W('Users',users)),('detail','User detail',W('Users',userdetail)),('payouts','Payouts tab',W('Payouts',adminpay)),('reports','Reports tab',W('Reports',adminreports)),('settings','Settings tab',W('Settings',adminsettings)),('audit','Audit log tab',W('Audit log',adminaudit))])]
SEGS=seg4.SEGS
