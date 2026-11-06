"""Untitled illustration engine: reeded glass, mesh gradients, dot-matrix, halftone, seat maps, tickets."""
import numpy as np, cv2, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
L='/tmp/claude-0/ill/lib/'
def font(name,size): return ImageFont.truetype(L+name+'.ttf',size)
def hexrgb(h): h=h.lstrip('#'); return np.array([int(h[i:i+2],16) for i in (0,2,4)],dtype=np.float32)/255
PAL={
 'ember':['#0D0F05','#2B2025','#5B3A8C','#E4483E','#F26A2E','#F5B83D'],
 'sunset':['#FFB03B','#F05A4E','#B07BC8','#F4D8A8','#E5486C','#FFE7C2'],
 'peach':['#F7EDE6','#E9D3C5','#D09472','#F08A5D','#FFF6EE','#F2B38E'],
 'magenta':['#FFFFFF','#FFC7EE','#F04CA8','#B3125F','#5E0B35','#FFE3F5'],
 'ink':['#0B0B0C','#1A1A1C','#3B3B40','#8A8A90','#D8D8DC','#FFFFFF'],
}
def rng(seed): return np.random.default_rng(seed)
def smooth(e0,e1,x):
    t=np.clip((x-e0)/(e1-e0+1e-9),0,1); return t*t*(3-2*t)
def mesh(w,h,blobs,base,seed=0,scale=4):
    """blobs: (cx,cy,r,color,weight) in 0..1 units; returns float HxWx3"""
    sw,sh=w//scale,h//scale
    yy,xx=np.mgrid[0:sh,0:sw].astype(np.float32); xx/=sw; yy/=sh
    num=np.zeros((sh,sw,3),np.float32)+hexrgb(base)*0.02; den=np.zeros((sh,sw,1),np.float32)+0.02
    asp=w/h
    for cx,cy,r,col,wt in blobs:
        d2=((xx-cx)*asp)**2+(yy-cy)**2
        g=np.exp(-d2/(2*r*r))*wt
        num+=g[...,None]*hexrgb(col); den+=g[...,None]
    img=num/den
    return cv2.resize(img,(w,h),interpolation=cv2.INTER_CUBIC)
def grain(img,amt=0.04,seed=1,mono=False):
    r=rng(seed); h,w=img.shape[:2]
    n=r.normal(0,amt,(h,w,1) if mono else (h,w,3)).astype(np.float32)
    return np.clip(img+n,0,1)
def vignette(img,amt=0.25):
    h,w=img.shape[:2]; yy,xx=np.mgrid[0:h,0:w].astype(np.float32)
    d=np.sqrt(((xx/w-.5)*1.1)**2+((yy/h-.5)*1.1)**2)
    return np.clip(img*(1-amt*smooth(0.25,0.8,d))[...,None],0,1)
def reeded(img,flutes=36,k=7.0,teeth=0.0,seed=0,shade=0.22,chroma=1.5):
    h,w=img.shape[:2]; p=w/flutes
    yy,xx=np.mgrid[0:h,0:w].astype(np.float32)
    f=np.floor(xx/p); u=(xx-f*p)/p
    srcx=(f+0.5)*p+(u-0.5)*p*k
    r=rng(seed); nz=r.normal(0,1,(flutes+2,)).astype(np.float32)
    nzy=cv2.GaussianBlur(r.normal(0,1,(h,1)).astype(np.float32),(0,0),sigmaX=0.1,sigmaY=h/18)[:,0]
    srcy=yy+(u-0.5)*teeth*h*0.12*(nz[f.astype(int)]*0.6+nzy[:,None]*1.2)
    out=np.zeros_like(img)
    for c,off in enumerate((-chroma,0,chroma)):
        out[...,c]=cv2.remap(img[...,c],np.clip(srcx+off*(u-0.5),0,w-1).astype(np.float32),np.clip(srcy,0,h-1).astype(np.float32),cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
    ridge=1-shade+shade*1.6*(1-np.abs(2*u-1))**1.4
    return np.clip(out*ridge[...,None],0,1)
def toimg(a): return Image.fromarray((np.clip(a,0,1)*255).astype(np.uint8))
def arr(im): return np.asarray(im.convert('RGB'),dtype=np.float32)/255
def ramp(colors,t):
    cs=np.array([hexrgb(c) for c in colors]); t=np.clip(t,0,1)*(len(cs)-1)
    i=np.clip(np.floor(t).astype(int),0,len(cs)-2); f=(t-i)[...,None]
    return cs[i]*(1-f)+cs[i+1]*f
def dotsphere(w,h,colors,cs=52,seed=0,cx=0.5,cy=0.5,power=1.0,bg='#EDEDED'):
    S=2; W,H=w*S,h*S; c=cs*S
    yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
    ci=np.floor(xx/c); cj=np.floor(yy/c)
    lx=((xx-ci*c)/c)*2-1; ly=((yy-cj*c)/c)*2-1
    ccx=(ci+.5)*c/W; ccy=(cj+.5)*c/H
    d=np.sqrt(((ccx-cx)*W/H)**2+(ccy-cy)**2); t=1-np.clip(d/0.62,0,1)**power
    base=ramp(colors,t)
    rr=np.sqrt(lx*lx+ly*ly); mask=smooth(1.0,0.9,rr)
    light=np.clip(0.78+0.30*(-0.55*lx-0.7*ly)+0.18*(1-rr),0.35,1.25)
    col=np.clip(base*light[...,None],0,1)
    out=col*mask[...,None]+hexrgb(bg)*(1-mask[...,None])
    return cv2.resize(out,(w,h),interpolation=cv2.INTER_AREA)
BAYER=np.array([[0,32,8,40,2,34,10,42],[48,16,56,24,50,18,58,26],[12,44,4,36,14,46,6,38],[60,28,52,20,62,30,54,22],[3,35,11,43,1,33,9,41],[51,19,59,27,49,17,57,25],[15,47,7,39,13,45,5,37],[63,31,55,23,61,29,53,21]],np.float32)/64
def dither(gray,px=3,paper='#F4F4F4',ink='#0E0E0E',contrast=1.0):
    h,w=gray.shape; sh,sw=h//px,w//px
    g=cv2.resize(gray,(sw,sh),interpolation=cv2.INTER_AREA)
    g=np.clip((g-.5)*contrast+.5,0,1)
    th=np.tile(BAYER,(sh//8+1,sw//8+1))[:sh,:sw]
    b=(g>th).astype(np.float32)
    big=cv2.resize(b,(sw*px,sh*px),interpolation=cv2.INTER_NEAREST)
    big=cv2.copyMakeBorder(big,0,h-big.shape[0],0,w-big.shape[1],cv2.BORDER_REPLICATE)
    return big[...,None]*hexrgb(paper)+(1-big[...,None])*hexrgb(ink)
def arena_scene(w,h,seed=0,lights=5):
    """grayscale arena: spotlight beams from top, stage glow, crowd silhouettes"""
    r=rng(seed); yy,xx=np.mgrid[0:h,0:w].astype(np.float32); X=xx/w; Y=yy/h
    g=np.full((h,w),0.08,np.float32)
    for i in range(lights):
        ox=0.12+0.76*(i+r.uniform(-.15,.15))/(lights-1); tx=0.5+r.uniform(-.28,.28)
        ang=np.arctan2(X-ox,Y+0.05); tgt=np.arctan2(tx-ox,0.85+0.05)
        beam=np.exp(-((ang-tgt)/0.085)**2)*smooth(0,0.6,Y+0.1)*(0.75-0.25*Y)
        g+=beam*0.55
    glow=np.exp(-(((X-0.5)*1.7)**2+((Y-0.82)*3.4)**2)); g+=glow*0.55
    # crowd
    for row,(base,amp,sz) in enumerate([(0.80,0.05,0.020),(0.88,0.06,0.028),(0.97,0.07,0.04)]):
        n=int(1/sz*1.2); 
        for k in range(n):
            cx=(k+r.uniform(-.2,.2))*sz; cy=base+r.uniform(-amp,amp)*0.4
            rad=sz*r.uniform(.42,.55)
            m=((X-cx)*w/h)**2+(Y-cy)**2<(rad*1.0)**2
            m2=(np.abs(X-cx)<sz*0.55)&(Y>cy)&(Y<cy+0.35)
            g[m|m2]=0.03+0.015*row
    g=cv2.GaussianBlur(g,(0,0),1.2)
    return np.clip(g,0,1)
def rrect(d,box,rad,fill=None,outline=None,width=1): d.rounded_rectangle(box,rad,fill=fill,outline=outline,width=width)
def shadow(im,mask,off=(0,24),blur=40,alpha=0.28):
    sh=Image.new('L',im.size,0); sh.paste(mask,off,mask) if mask.mode=='L' else None
    sh=sh.filter(ImageFilter.GaussianBlur(blur)); black=Image.new('RGB',im.size,(0,0,0))
    return Image.composite(black,im,sh.point(lambda v:int(v*alpha)))
def save(im,path,q=92):
    if path.endswith('.png'): im.save(path,optimize=True)
    else: im.save(path,quality=q)
