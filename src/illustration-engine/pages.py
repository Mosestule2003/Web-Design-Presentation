import sys; sys.path.insert(0,'/tmp/claude-0/ill/lib')
from untitled_art import *
import random
W,H=1600,1000
IF='/usr/share/fonts/opentype/inter/'
def F(kind,size):
    if kind=='disp': return ImageFont.truetype(IF+'InterDisplay-Medium.otf',size)
    if kind=='light': return ImageFont.truetype(IF+'InterDisplay-Light.otf',size)
    if kind=='sb': return ImageFont.truetype(IF+'Inter-SemiBold.otf',size)
    if kind=='reg': return ImageFont.truetype(IF+'Inter-Regular.otf',size)
    return ImageFont.truetype(L+'GeistMono-Regular.ttf',size)
THEMES={
 'A':dict(name='Peach',card='#FFFFFF',ink='#17130F',mute='#8B7F76',acc='#E4483E',acc2='#D09472',line='#EADFD6',dark=False,
   blobs=lambda r:[(.2,.3,.4,'#D09472',1),(.8,.75,.35,'#F08A5D',1),(.3,.95,.3,'#FFF6EE',1.2),(.95,.05,.35,'#E9D3C5',1),(.6,.4,.25,'#F2B38E',.6)],base='#F7EDE6',flutes=30,k=6.5),
 'B':dict(name='Ember',card='#15110E',ink='#F6EFE8',mute='#9A8C82',acc='#F26A2E',acc2='#F5B83D',line='#2E2622',dark=True,
   blobs=lambda r:[(.15,.95,.38,'#F26A2E',1.1),(.85,.15,.32,'#5B3A8C',.9),(.55,.55,.3,'#E4483E',.5),(.05,.05,.4,'#0D0F05',1.6),(.95,.95,.3,'#F5B83D',.8),(.5,.1,.3,'#2B2025',1)],base='#0D0F05',flutes=34,k=7.2),
 'C':dict(name='Magenta',card='#FFFFFF',ink='#2A0A1B',mute='#9A6B86',acc='#B3125F',acc2='#F04CA8',line='#F6D3E8',dark=False,
   blobs=lambda r:[(.25,.3,.35,'#F04CA8',1),(.8,.7,.35,'#B3125F',1),(.4,.95,.3,'#FFC7EE',1.2),(.9,.1,.3,'#FFE3F5',1),(.1,.8,.3,'#5E0B35',.6)],base='#FFE3F5',flutes=26,k=6.0),
}
class Layer:
    S=2
    def __init__(s,w,h):
        s.w,s.h=w,h; s.im=Image.new('RGBA',(w*s.S,h*s.S),(0,0,0,0)); s.d=ImageDraw.Draw(s.im)
    def _b(s,b): return [v*s.S for v in b]
    def rr(s,b,r,fill=None,outline=None,width=1): s.d.rounded_rectangle(s._b(b),r*s.S,fill=fill,outline=outline,width=max(1,int(round(width*s.S))))
    def ell(s,b,fill=None,outline=None,width=1): s.d.ellipse(s._b(b),fill=fill,outline=outline,width=max(1,int(round(width*s.S))))
    def line(s,pts,fill,width=1): s.d.line([v*s.S for v in pts],fill=fill,width=max(1,int(round(width*s.S))))
    def rect(s,b,fill): s.d.rectangle(s._b(b),fill=fill)
    def text(s,xy,t,font,fill,anchor='la',sp=0):
        f=font.font_variant(size=int(font.size*s.S)) if hasattr(font,'font_variant') else font
        if sp:
            x,y=xy[0]*s.S,xy[1]*s.S
            tot=sum(f.getlength(ch)+sp*s.S for ch in t)-sp*s.S
            if anchor[0]=='r': x-=tot
            elif anchor[0]=='m': x-=tot/2
            a2='l'+anchor[1]
            for ch in t:
                s.d.text((x,y),ch,font=f,fill=fill,anchor=a2); x+=f.getlength(ch)+sp*s.S
        else: s.d.text((xy[0]*s.S,xy[1]*s.S),t,font=f,fill=fill,anchor=anchor)
    def tw(s,t,font):
        f=font.font_variant(size=int(font.size*s.S)); return f.getlength(t)/s.S
    def out(s): return s.im.resize((s.w,s.h),Image.LANCZOS)
def pill(L_,x,y,t,th,filled=False,fnt=None,pad=14,h=30):
    fnt=fnt or F('mono',13); w=L_.tw(t,fnt)+pad*2
    L_.rr((x,y,x+w,y+h),h/2,fill=th['ink'] if filled else None,outline=None if filled else th['line'],width=1.5)
    L_.text((x+pad,y+h/2),t,fnt,th['card'] if filled else th['mute'],anchor='lm'); return w
def backdrop(th,seed,box=None,flutes=None,k=None,w=W,h=H,teeth=1.0):
    r=random.Random(seed)
    bl=[(cx+r.uniform(-.08,.08),cy+r.uniform(-.08,.08),rad,c,wt) for cx,cy,rad,c,wt in th['blobs'](r)]
    m=mesh(w,h,bl,th['base'])
    a=reeded(m,flutes=flutes or th['flutes'],k=k or th['k'],teeth=teeth,seed=seed,shade=0.2 if not th['dark'] else 0.28)
    a=grain(a,0.035,seed); return a
def compose(bg,layers,shadows=True):
    im=toimg(bg).convert('RGBA')
    for lay,(x,y),sh in layers:
        if sh:
            a=lay.split()[3]; big=Image.new('L',im.size,0); big.paste(a,(x,y+sh[0]))
            big=big.filter(ImageFilter.GaussianBlur(sh[1])).point(lambda v:int(v*sh[2]))
            im=Image.composite(Image.new('RGBA',im.size,(20,10,5,255)),im,big)
        im.alpha_composite(lay,(x,y))
    return im.convert('RGB')
def tag(th,page,name,var,dark_on_art=True):
    l=Layer(W,60); t=f'UNT-ILL-{page}  /  {name.upper()}  /  {var}'; f=F('mono',13); w=l.tw(t,f)+len(t)*1.2+36
    l.rr((36,12,36+w,48),18,fill=(10,8,6,120)); l.text((54,30),t,f,(255,255,255,235),anchor='lm',sp=1.2); return l.out()
# ---------- objects ----------
def ticket(th,w=640,h=300,title='SUMMER STAGE',date='SAT 14 JUN',seat='SEC 112  ROW F  SEAT 14',acc=None):
    L_=Layer(w,h); c=th['card']; ink=th['ink']; a=acc or th['acc']
    L_.rr((0,0,w,h),26,fill=c)
    sx=w*0.72
    for yy in range(18,h-10,14): L_.ell((sx-2,yy,sx+2,yy+4),fill=th['line'])
    L_.ell((sx-16,-16,sx+16,16),fill=(0,0,0,0)); 
    L_.text((36,40),'ADMIT ONE',F('mono',13),th['mute'],sp=2)
    L_.text((36,88),title,F('disp',44),ink)
    L_.text((36,150),date+'  ·  20:00',F('mono',17),ink)
    L_.text((36,182),seat,F('mono',14),th['mute'])
    pill(L_,36,226,'GENERAL EVENTS',th,fnt=F('mono',12),h=28)
    # barcode
    r=random.Random(5); x=sx+36
    while x<w-30:
        bw=r.choice([2,3,5]); L_.rect((x,48,x+bw,h-70),ink); x+=bw+r.choice([2,3,4])
    L_.text((sx+36,h-48),'0042  7716  0398',F('mono',12),th['mute'])
    L_.rr((w-54,h-44,w-30,h-20),12,fill=a)
    im=L_.out()
    # punch notches
    px=im.load(); 
    m=Image.new('L',im.size,255); md=ImageDraw.Draw(m); md.ellipse((sx-14,-14,sx+14,14),fill=0); md.ellipse((sx-14,h-14,sx+14,h+14),fill=0)
    im.putalpha(Image.composite(im.split()[3],Image.new('L',im.size,0),m)); return im
def seatmap(th,w=900,h=620,seed=3):
    L_=Layer(w,h); L_.rr((0,0,w,h),28,fill=th['card'])
    L_.rr((w*0.2,28,w*0.8,56),14,fill=th['line']); L_.text((w/2,42),'STAGE',F('mono',13),th['mute'],anchor='mm',sp=3)
    r=random.Random(seed); rows=11; cols=22; gx=(w-120)/cols; gy=(h-210)/rows
    sel=[(5,9),(5,10),(5,11)]; held=[(3,4),(3,5)]
    for i in range(rows):
        L_.text((46,92+i*gy+gy/2),chr(65+i),F('mono',12),th['mute'],anchor='mm')
        for j in range(cols):
            if j in (7,14): continue
            if (i==0 and (j<3 or j>18)) or (i==rows-1 and (j<2 or j>19)): continue
            x=60+j*gx+(8 if j>14 else 0)+(-4 if j<7 else 0); y=92+i*gy; d=gx*0.62
            b=(x+gx/2-d/2,y+gy/2-d/2,x+gx/2+d/2,y+gy/2+d/2)
            if (i,j) in sel: L_.rr(b,d*0.3,fill=th['acc'])
            elif (i,j) in held: L_.rr(b,d*0.3,outline=th['acc2'],width=2)
            elif r.random()<0.34: L_.rr(b,d*0.3,fill=th['line']); L_.line((b[0]+d*.3,b[1]+d*.3,b[2]-d*.3,b[3]-d*.3),th['mute'],1.2); L_.line((b[0]+d*.3,b[3]-d*.3,b[2]-d*.3,b[1]+d*.3),th['mute'],1.2)
            else: L_.rr(b,d*0.3,fill=th['ink'] if th['dark'] else '#E9E4DE')
    ly=h-70; x=46
    for lab,kind in [('AVAILABLE','a'),('SELECTED','s'),('HELD','h'),('SOLD','x')]:
        b=(x,ly,x+20,ly+20)
        if kind=='s': L_.rr(b,6,fill=th['acc'])
        elif kind=='h': L_.rr(b,6,outline=th['acc2'],width=2)
        elif kind=='x': L_.rr(b,6,fill=th['line']); L_.line((x+6,ly+6,x+14,ly+14),th['mute'],1.2); L_.line((x+6,ly+14,x+14,ly+6),th['mute'],1.2)
        else: L_.rr(b,6,fill=th['ink'] if th['dark'] else '#E9E4DE')
        L_.text((x+30,ly+10),lab,F('mono',12),th['mute'],anchor='lm'); x+=170
    return L_.out()
def summary(th,w=420,h=520):
    L_=Layer(w,h); L_.rr((0,0,w,h),28,fill=th['card'])
    L_.text((32,38),'YOUR SELECTION',F('mono',12),th['mute'],sp=2)
    L_.text((32,84),'3 tickets',F('light',40),th['ink'])
    for i,(a,b) in enumerate([('Sec 112 · Row F · 14','$84.00'),('Sec 112 · Row F · 15','$84.00'),('Sec 112 · Row F · 16','$84.00')]):
        y=160+i*54; L_.text((32,y),a,F('mono',14),th['ink']); L_.text((w-32,y),b,F('mono',14),th['ink'],anchor='ra'); L_.line((32,y+30,w-32,y+30),th['line'],1)
    L_.text((32,340),'Total',F('reg',16),th['mute']); L_.text((w-32,330),'$252.00',F('disp',30),th['ink'],anchor='ra')
    pill(L_,32,376,'HOLD 08:42',th,fnt=F('mono',13),h=32)
    L_.rr((32,h-92,w-32,h-36),28,fill=th['acc']); L_.text((w/2,h-64),'Continue to checkout',F('sb',17),'#FFFFFF',anchor='mm'); return L_.out()
def tiers(th,w=1100,h=520):
    L_=Layer(w,h); cw=(w-48)/3
    data=[('General','$45','Standing, all ages','AVAILABLE'),('Reserved','$84','Numbered seat','FEW LEFT'),('VIP','$220','Lounge + early entry','SOLD OUT')]
    for i,(n,p,d,s) in enumerate(data):
        x=i*(cw+24); mid=i==1
        L_.rr((x,0,x+cw,h),28,fill=th['ink'] if mid and not th['dark'] else th['card'])
        fg=th['card'] if mid and not th['dark'] else th['ink']; mu=th['line'] if mid and not th['dark'] else th['mute']
        L_.text((x+30,44),n.upper(),F('mono',13),mu,sp=2)
        L_.text((x+30,170),p,F('light',76),fg,anchor='ls')
        L_.text((x+30,208),d,F('reg',16),mu)
        for k,f in enumerate(['Mobile + print ticket','Free transfer','Refund to 48h']):
            L_.ell((x+30,252+k*38,x+42,264+k*38),outline=mu,width=1.5); L_.text((x+56,258+k*38),f,F('reg',15),fg,anchor='lm')
        pill(L_,x+30,h-122,s,th,filled=(s!='AVAILABLE'),fnt=F('mono',12),h=30) if False else None
        L_.rr((x+30,h-100,x+cw-30,h-48),26,fill=th['acc'] if not s=='SOLD OUT' else th['line'])
        L_.text((x+cw/2,h-74),'Select' if s!='SOLD OUT' else 'Sold out',F('sb',16),'#FFFFFF' if s!='SOLD OUT' else th['mute'],anchor='mm')
        pill(L_,x+cw-30-L_.tw(s,F('mono',11))-28,34,s,th,fnt=F('mono',11),h=26,pad=12)
    return L_.out()
def stats(th,w=1000,h=640,seed=1):
    L_=Layer(w,h); r=random.Random(seed)
    items=[('TICKETS SOLD','4,812','+12.4%'),('GROSS REVENUE','$218k','+8.1%'),('CHECK-INS','3,206','67%'),('REFUNDS','1.2%','-0.3%')]
    tw_=(w-24)/2
    for i,(a,b,c) in enumerate(items):
        x=(i%2)*(tw_+24); y=(i//2)*150
        L_.rr((x,y,x+tw_,y+132),26,fill=th['card']); L_.text((x+28,y+34),a,F('mono',12),th['mute'],sp=2); L_.text((x+28,y+108),b,F('light',48),th['ink'],anchor='ls'); pill(L_,x+tw_-110,y+26,c,th,fnt=F('mono',12),h=26,pad=10)
    L_.rr((0,324,w,h),28,fill=th['card']); L_.text((30,360),'SALES · LAST 14 DAYS',F('mono',12),th['mute'],sp=2)
    n=14; bw=(w-80)/n
    for i in range(n):
        v=0.25+0.7*(0.5+0.5*math.sin(i*0.7+seed))*(0.6+0.4*r.random()); top=h-40-(h-460)*v-0
        for q in range(int(v*9)):
            yy=h-48-q*17; L_.ell((40+i*bw+bw*0.2,yy-10,40+i*bw+bw*0.2+bw*0.55,yy+4),fill=th['acc'] if i==9 else (th['acc2'] if q>5 else th['line'] if not th['dark'] else '#3A302B'))
    return L_.out()
def calendar(th,w=900,h=700,seed=2):
    L_=Layer(w,h); L_.rr((0,0,w,h),30,fill=th['card']); L_.text((36,70),'NOVEMBER',F('light',40),th['ink'],anchor='ls')
    for i,dn in enumerate('MTWTFSS'): L_.text((60+i*118,112),dn,F('mono',13),th['mute'],anchor='mm')
    r=random.Random(seed); ev={4,7,11,14,15,18,21,22,25,28}
    for d in range(1,31):
        k=d+1; col=k%7; row=k//7; x=60+col*118; y=170+row*88
        has=d in ev; hot=d in (14,15)
        if hot: L_.rr((x-44,y-30,x+44,y+30),30,fill=th['acc']); 
        L_.text((x,y-4),str(d),F('disp',20),'#FFFFFF' if hot else th['ink'],anchor='mm')
        if has and not hot: L_.ell((x-3,y+20,x+3,y+26),fill=th['acc'])
        if has and hot: L_.ell((x-3,y+20,x+3,y+26),fill='#FFFFFF')
    return L_.out()
def eventcards(th,w=1100,h=420):
    L_=Layer(w,h); cw=(w-48)/3
    ev=[('14','JUN','Summer Stage','Concert · Kamloops'),('21','JUN','Cup Final','Sport · Vancouver'),('02','JUL','Open Mic Gala','Theatre · Victoria')]
    for i,(d,m,t,s) in enumerate(ev):
        x=i*(cw+24); L_.rr((x,0,x+cw,h),28,fill=th['card'])
        L_.rr((x+22,22,x+cw-22,h-130),20,fill=th['line'] if not th['dark'] else '#2A2320')
        L_.text((x+44,48),d,F('light',64),th['ink'] if th['dark'] is False else th['ink']); L_.text((x+46,122),m,F('mono',14),th['mute'],sp=2)
        L_.text((x+30,h-88),t,F('sb',20),th['ink']); L_.text((x+30,h-54),s,F('mono',13),th['mute']); pill(L_,x+cw-96,30,'$45',th,fnt=F('mono',11),h=26,pad=10)
    return L_.out()
def formcard(th,w=560,h=700,kind='login'):
    L_=Layer(w,h); ink=th['ink']
    L_.text((0,40),'UNTITLED',F('mono',14),ink,sp=4)
    ttl={'login':'Welcome back','signup':'Create account','reset':'Reset password'}[kind]
    sub={'login':'Sign in to manage your tickets.','signup':'Tickets, orders and events in one place.','reset':'We will email you a secure link.'}[kind]
    L_.text((0,170),ttl,F('light',54),ink,anchor='ls'); L_.text((0,236),sub,F('reg',17),th['mute'])
    fields={'login':['Email','Password'],'signup':['Full name','Email','Password'],'reset':['Email']}[kind]
    y=290
    for f in fields:
        L_.text((0,y),f.upper(),F('mono',12),th['mute'],sp=2); L_.rr((0,y+26,w,y+84),14,fill=th['card'],outline=th['line'],width=1.5); y+=112
    L_.rr((0,y+10,w,y+70),30,fill=ink); L_.text((w/2,y+40),{'login':'Sign in','signup':'Create account','reset':'Send reset link'}[kind],F('sb',17),th['card'],anchor='mm')
    L_.text((w/2,y+112),{'login':'Forgot password?  ·  Create account','signup':'Already registered?  Sign in','reset':'Back to sign in'}[kind],F('mono',13),th['mute'],anchor='mm')
    return L_.out()
def ledger(th,w=1000,h=640):
    L_=Layer(w,h); L_.rr((0,0,w,h),30,fill=th['card'])
    L_.text((36,48),'PAYOUT DETAILS',F('mono',12),th['mute'],sp=2); L_.text((36,122),'$18,420.00',F('light',60),th['ink'],anchor='ls'); L_.text((36,160),'Next payout  ·  Fri 07 Nov  ·  to account ending 4821',F('mono',14),th['mute'])
    pill(L_,w-190,40,'VERIFIED',th,fnt=F('mono',12),h=28)
    hdr=['EVENT','DATE','STATUS','AMOUNT']; xs=[36,430,620,w-36]
    for i,hh in enumerate(hdr): L_.text((xs[i],214),hh,F('mono',11),th['mute'],anchor='ra' if i==3 else 'la',sp=2)
    rows=[('Summer Stage','02 Nov','PAID','$6,210.00'),('Cup Final','26 Oct','PAID','$7,480.00'),('Open Mic Gala','19 Oct','PENDING','$2,130.00'),('Tech Summit','12 Oct','PAID','$2,600.00')]
    for i,rw in enumerate(rows):
        y=246+i*62; L_.line((36,y,w-36,y),th['line'],1.5)
        for j,t in enumerate(rw): L_.text((xs[j],y+30),t,F('mono',15) if j else F('sb',17),th['ink'],anchor='rm' if j==3 else 'lm')
        L_.rr((xs[2]-12+0,y+18,xs[2]-12+0,y+18),0)
    # dot-matrix bars
    for i in range(24):
        v=0.3+0.65*abs(math.sin(i*0.55)); 
        for q in range(int(v*5)): L_.ell((36+i*38,h-30-q*16-10,36+i*38+20,h-30-q*16+6),fill=th['acc'] if q>=3 else th['line'])
    return L_.out()
def userlist(th,w=1000,h=640,seed=4):
    L_=Layer(w,h); L_.rr((0,0,w,h),30,fill=th['card']); L_.text((36,48),'USERS & MODERATION',F('mono',12),th['mute'],sp=2)
    L_.rr((w-336,28,w-36,68),20,outline=th['line'],width=1.5); L_.text((w-316,48),'Search users',F('reg',15),th['mute'],anchor='lm')
    r=random.Random(seed); names=['Amara Okafor','Liam Chen','Sofia Rossi','Noah Patel','Mia Tremblay','Kofi Mensah','Eli Park']; roles=['ORGANISER','CUSTOMER','CUSTOMER','ORGANISER','ADMIN','CUSTOMER','CUSTOMER']; st=['ACTIVE','ACTIVE','FLAGGED','ACTIVE','ACTIVE','SUSPENDED','ACTIVE']
    for i,n in enumerate(names):
        y=100+i*72; L_.line((36,y,w-36,y),th['line'],1.5)
        L_.ell((36,y+14,80,y+58),fill=[th['acc'],th['acc2'],th['line'],th['ink']][i%4])
        L_.text((98,y+28),n,F('sb',17),th['ink'],anchor='lm'); L_.text((98,y+50),n.split()[0].lower()+'@mail.com',F('mono',12),th['mute'],anchor='lm')
        L_.text((560,y+36),roles[i],F('mono',12),th['mute'],anchor='lm',sp=1.5)
        pill(L_,w-190,y+20,st[i],th,filled=(st[i]!='ACTIVE'),fnt=F('mono',11),h=28,pad=12)
    return L_.out()
def heat(th,w=1000,h=640,seed=6):
    L_=Layer(w,h); L_.rr((0,0,w,h),30,fill=th['card']); L_.text((36,48),'PLATFORM ACTIVITY · 12 WEEKS',F('mono',12),th['mute'],sp=2)
    r=random.Random(seed); cols=24; rows=7; cw=(w-72)/cols; chh=(h-200)/rows
    for i in range(rows):
        for j in range(cols):
            v=min(1,max(0,0.5+0.45*math.sin(j*0.4+i*0.3)+r.uniform(-.3,.3))); c=ramp([th['line'],th['acc2'],th['acc']],np.array(v)); col='#%02x%02x%02x'%tuple(int(x*255) for x in c)
            L_.rr((36+j*cw+2,90+i*chh+2,36+(j+1)*cw-2,90+(i+1)*chh-2),6,fill=col)
    for i,(a,b) in enumerate([('ORDERS','12,481'),('NEW USERS','1,204'),('OPEN FLAGS','7')]):
        x=36+i*300; L_.text((x,h-92),a,F('mono',11),th['mute'],sp=2); L_.text((x,h-34),b,F('light',38),th['ink'],anchor='ls')
    return L_.out()
def profile(th,w=760,h=640):
    L_=Layer(w,h); L_.rr((0,0,w,h),30,fill=th['card']); L_.ell((40,40,140,140),fill=th['acc']); L_.text((90,90),'KT',F('sb',30),'#FFFFFF',anchor='mm')
    L_.text((166,70),'Kpughur Tule',F('disp',30),th['ink']); L_.text((166,108),'CUSTOMER  ·  MEMBER SINCE 2026',F('mono',12),th['mute'],sp=1.5)
    for i,(a,b) in enumerate([('EMAIL','member@mail.com'),('PHONE','+1 250 555 0142'),('CITY','Kamloops, BC'),('NOTIFICATIONS','Order updates on')]):
        y=190+i*84; L_.text((40,y),a,F('mono',11),th['mute'],sp=2); L_.text((40,y+26),b,F('reg',19),th['ink']); L_.line((40,y+66,w-40,y+66),th['line'],1.5)
    L_.rr((40,h-90,300,h-38),26,fill=th['ink']); L_.text((170,h-64),'Save changes',F('sb',16),th['card'],anchor='mm')
    return L_.out()
def createform(th,w=980,h=700):
    L_=Layer(w,h); L_.rr((0,0,w,h),30,fill=th['card'])
    for i,s in enumerate(['Basics','Date & venue','Tickets','Publish']):
        x=36+i*232; on=i==0
        L_.ell((x,36,x+30,66),fill=th['acc'] if on else None,outline=None if on else th['line'],width=1.5); L_.text((x+15,51),str(i+1),F('mono',13),'#FFFFFF' if on else th['mute'],anchor='mm'); L_.text((x+42,51),s,F('sb',15),th['ink'] if on else th['mute'],anchor='lm')
    L_.text((36,170),'Tell us about your event',F('light',44),th['ink'],anchor='ls')
    for i,(a,b) in enumerate([('EVENT NAME','Summer Stage 2026'),('CATEGORY','Concert'),('DESCRIPTION','')]):
        y=210+i*0; 
    L_.text((36,214),'EVENT NAME',F('mono',11),th['mute'],sp=2); L_.rr((36,238,w-36,296),14,outline=th['line'],width=1.5); L_.text((56,267),'Summer Stage 2026',F('reg',18),th['ink'],anchor='lm')
    L_.text((36,330),'CATEGORY',F('mono',11),th['mute'],sp=2); x=36
    for c in ['Concert','Sport','Theatre','Conference','Festival']: x+=pill(L_,x,356,c,th,filled=(c=='Concert'),fnt=F('mono',13),h=36,pad=16)+10
    L_.text((36,430),'DESCRIPTION',F('mono',11),th['mute'],sp=2); L_.rr((36,454,w-36,570),14,outline=th['line'],width=1.5)
    for k in range(3): L_.rr((56,478+k*26,56+(w-150)*(1-k*0.22),490+k*26),6,fill=th['line'])
    L_.rr((w-246,h-82,w-36,h-28),27,fill=th['acc']); L_.text((w-141,h-55),'Continue',F('sb',16),'#FFFFFF',anchor='mm')
    return L_.out()
def tickets_stack(th):
    ts=[ticket(th,600,280,'SUMMER STAGE','SAT 14 JUN','SEC 112  ROW F  SEAT 14',acc=th['acc']),
        ticket(th,600,280,'CUP FINAL','SAT 21 JUN','SEC 204  ROW B  SEAT 3',acc=th['acc2']),
        ticket(th,600,280,'OPEN MIC GALA','WED 02 JUL','GENERAL ADMISSION',acc=th['ink'])]
    return ts
def checkmark(th,w=520,h=520):
    L_=Layer(w,h); L_.rr((0,0,w,h),34,fill=th['card']); L_.ell((w/2-52,70,w/2+52,174),fill=th['acc']); L_.line((w/2-24,124,w/2-6,144,w/2+28,102),'#FFFFFF',6)
    L_.text((w/2,236),'You are going',F('light',40),th['ink'],anchor='mm'); L_.text((w/2,286),'ORDER  UNT-48213',F('mono',14),th['mute'],anchor='mm',sp=2)
    L_.line((50,330,w-50,330),th['line'],1.5); L_.text((60,370),'3 tickets',F('reg',17),th['ink']); L_.text((w-60,370),'$252.00',F('mono',17),th['ink'],anchor='ra')
    L_.rr((50,h-100,w-50,h-44),28,fill=th['ink']); L_.text((w/2,h-72),'Add to wallet',F('sb',16),th['card'],anchor='mm'); return L_.out()
def rot(im,ang): return im.rotate(ang,resample=Image.BICUBIC,expand=True)
