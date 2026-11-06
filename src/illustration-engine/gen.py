import sys,os; sys.path.insert(0,'lib')
from pages import *
OUT='out/final'; os.makedirs(OUT,exist_ok=True)
def P(layer,x,y,sh=(26,34,0.30)): return (layer,(int(x),int(y)),sh)
def split(th,var,seed,kind,art='reeded'):
    left=Image.new('RGB',(W,H),'#FFFFFF' if not th['dark'] else '#0F0C0A')
    bg=backdrop(th,seed,flutes=th['flutes']-6)
    art_im=toimg(bg).crop((W//2-80,0,W,H)).resize((W//2+80,H))
    left.paste(art_im,(W//2-80,0))
    base=left.convert('RGBA')
    f=formcard(th,560,700,kind); 
    if th['dark']:
        pass
    base.alpha_composite(f,(110,150-40))
    return base.convert('RGB')
def page(code,name,var,fn):
    th=THEMES[var]; im=fn(th,var); 
    t=tag(th,code,name,var); im=im.convert('RGBA'); im.alpha_composite(t,(0,H-70)); im=im.convert('RGB')
    d=f'{OUT}/{code}_{name.lower().replace(" ","-").replace("&","and")}'; os.makedirs(d,exist_ok=True)
    im.save(f'{d}/UNT-ILL-{code}_{name.lower().replace(" ","-").replace("&","and")}_{var}.png',optimize=True)
S={'A':1,'B':2,'C':3}
def p01(th,v):
    bg=backdrop(th,10+S[v]); L=[]
    # nav pill
    n=Layer(900,64); n.rr((0,0,900,64),32,fill=th['card'])
    n.text((32,32),'UNTITLED',F('mono',14),th['ink'],anchor='lm',sp=4)
    for i,t in enumerate(['Discover','Concerts','Sport','Theatre','Sign in']): n.text((250+i*128,32),t,F('reg',15),th['ink'] if i<4 else th['acc'],anchor='lm')
    L.append(P(n.out(),350,56,(10,16,.18)))
    ttl=Layer(1100,300); ttl.text((0,80),'Every stage,',F('light',104),(255,255,255,255) if True else th['ink']); ttl.text((0,200),'one ticket away.',F('light',104),(255,255,255,255))
    L.append(P(ttl.out(),90,230,(8,22,.25)))
    L.append(P(eventcards(th,1100,330),90,590,(20,30,.28)))
    L.append(P(rot(ticket(th,480,224),-8),1030,230))
    return compose(bg,L)
def p0x_auth(kind,seed):
    def f(th,v):
        return split(th,v,seed+S[v],kind)
    return f
def p05(th,v):
    bg=backdrop(th,50+S[v]); cal=calendar(th); cal=cal.resize((760,591),Image.LANCZOS)
    L=[P(cal,80,130),P(eventcards(th,700,330),840,130)]
    f=Layer(700,200); f.rr((0,0,700,200),28,fill=th['card']); f.text((30,40),'FILTERS',F('mono',12),th['mute'],sp=2)
    x=30
    for c in ['All','Concert','Sport','Theatre','Conference','Festival']: x+=pill(f,x,70,c,th,filled=(c=='All'),fnt=F('mono',13),h=36,pad=16)+8
    f.text((30,150),'This week · Kamloops · Any price',F('reg',17),th['ink'])
    L.append(P(f.out(),840,520))
    return compose(bg,L)
def p06(th,v):
    s=1 if th['dark'] else 0
    g=arena_scene(W,H,seed=S[v]*7,lights=5); d=dither(g,3,paper='#F4F4F4' if not th['dark'] else '#F5B83D',ink='#0E0E0E',contrast=1.3)
    bg=d*0.9+0.05
    im=toimg(bg).convert('RGBA'); L=Layer(700,420); L.rr((0,0,700,420),30,fill=th['card'])
    L.text((40,50),'SAT 14 JUN  ·  20:00',F('mono',13),th['mute'],sp=2); L.text((40,130),'Summer Stage',F('light',66),th['ink']); L.text((40,184),'Open-air concert  ·  Riverside Arena  ·  All ages',F('reg',16),th['mute'])
    pill(L,40,236,'FROM $45',th,filled=True,fnt=F('mono',13),h=34); pill(L,150,236,'482 LEFT',th,fnt=F('mono',13),h=34)
    L.rr((40,320,300,380),30,fill=th['acc']); L.text((170,350),'Choose seats',F('sb',17),'#FFFFFF',anchor='mm')
    im.alpha_composite(L.out(),(90,490)); return im.convert('RGB')
def p07(th,v):
    bg=backdrop(th,70+S[v]); return compose(bg,[P(seatmap(th,900,620,S[v]),110,150),P(summary(th),1060,100)])
def p08(th,v):
    bg=backdrop(th,80+S[v]); L=[P(rot(ticket(th,640,300),6),160,260),P(summary(th,460,560),980,170)]
    return compose(bg,L)
def p09(th,v):
    bg=backdrop(th,90+S[v]); return compose(bg,[P(checkmark(th),150,190),P(rot(ticket(th,640,300),-6),780,300)])
def p10(th,v):
    bg=backdrop(th,100+S[v]); ts=tickets_stack(th)
    L=[P(rot(ts[2],-9),180,420),P(rot(ts[1],-3),300,300),P(ts[0],440,150),P(profile(th,420,200) if False else rot(ts[0],0),9999,9999)]
    L=[P(rot(ts[2],-7),200,500),P(rot(ts[1],-3),340,330),P(rot(ts[0],2),480,150)]
    return compose(bg,L)
def p11(th,v):
    sph=dotsphere(W,H,['#5E0B35','#B3125F','#F04CA8','#FFC7EE'] if v=='C' else (['#2B2025','#E4483E','#F26A2E','#F5B83D'] if v=='B' else ['#8E6A55','#D09472','#F08A5D','#FFF3E8']),cs=44,cx=.28,cy=.5,bg='#EDEDED' if not th['dark'] else '#0D0F05')
    return compose(sph,[P(profile(th),740,170)])
def p12(th,v):
    bg=backdrop(th,120+S[v],flutes=th['flutes']+4); return compose(bg,[P(createform(th),310,140)])
def p13(th,v):
    bg=backdrop(th,130+S[v]); return compose(bg,[P(tiers(th),250,200)])
def p14(th,v):
    bg=backdrop(th,140+S[v]); return compose(bg,[P(stats(th),300,150)])
def p15(th,v):
    bg=backdrop(th,150+S[v]); return compose(bg,[P(ledger(th),300,150)])
def p16(th,v):
    bg=backdrop(th,160+S[v]); return compose(bg,[P(heat(th),300,150)])
def p17(th,v):
    g=np.zeros((H,W),np.float32); r=np.random.default_rng(S[v])
    for i in range(0,H,6): g[i:i+r.integers(1,5),:]=r.uniform(.05,.9)
    d=dither(cv2.GaussianBlur(g,(0,0),2)*np.linspace(.3,1,W)[None,:],3,paper='#EDEDED' if not th['dark'] else '#F26A2E',ink='#0B0B0C',contrast=1.1)
    return compose(d,[P(userlist(th),300,150)])
PAGES=[('P01','Landing',p01),('P02','Login',p0x_auth('login',20)),('P03','Sign up',p0x_auth('signup',30)),('P04','Password reset',p0x_auth('reset',40)),('P05','Discover events',p05),('P06','Event details',p06),('P07','Seat selection',p07),('P08','Checkout',p08),('P09','Order confirmation',p09),('P10','My tickets',p10),('P11','Profile',p11),('P12','Create event',p12),('P13','Ticket types',p13),('P14','Event dashboard',p14),('P15','Payout details',p15),('P16','Admin overview',p16),('P17','Admin users',p17)]
if __name__=='__main__':
    only=sys.argv[1:] 
    for code,name,fn in PAGES:
        if only and code not in only: continue
        for v in 'ABC':
            try: page(code,name,v,fn)
            except Exception as e:
                import traceback; print('FAIL',code,v); traceback.print_exc(); break
    print('done')
