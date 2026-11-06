import sys; sys.path.insert(0,'/tmp/claude-0/ill/lib')
from untitled_art import *
import random
def reed(blobs,base,w,h,seed,fl=30,k=6.5): return grain(reeded(mesh(w,h,blobs,base),flutes=fl,k=k,teeth=1,seed=seed,shade=.2),.03,seed)
EM=[(.15,.95,.4,'#F26A2E',1.1),(.85,.15,.35,'#5B3A8C',.9),(.55,.55,.3,'#E4483E',.5),(.05,.05,.4,'#0D0F05',1.4),(.95,.95,.3,'#F5B83D',.8)]
PE=[(.2,.3,.4,'#D09472',1),(.8,.75,.35,'#F08A5D',1),(.3,.95,.3,'#FFF6EE',1.2),(.95,.05,.35,'#E9D3C5',1)]
MG=[(.25,.3,.35,'#F04CA8',1),(.8,.7,.35,'#B3125F',1),(.4,.95,.3,'#FFC7EE',1.2),(.9,.1,.3,'#FFE3F5',1)]
SU=[(.2,.2,.4,'#FFB03B',1),(.8,.3,.35,'#F05A4E',1),(.5,.95,.35,'#B07BC8',1),(.95,.9,.3,'#E5486C',.8)]
def sv(a,n): toimg(a).save(f'assets/{n}.jpg',quality=88)
sv(reed(EM,'#0D0F05',900,900,1,28),'a0'); sv(reed(PE,'#F7EDE6',900,900,2,24),'a1')
sv(grain(mesh(900,900,MG+[(.5,.5,.3,'#FFFFFF',.4)],'#FFE3F5'),.03),'a2')
sv(dotsphere(900,900,['#2B2025','#E4483E','#F26A2E','#F5B83D'],cs=60,cx=.5,cy=.5,bg='#FFFFFF'),'a3')
sv(reed(SU,'#F4D8A8',900,900,5,22),'a4')
sv(dither(arena_scene(900,900,seed=4,lights=5),3,paper='#F4F4F4',ink='#0E0E0E',contrast=1.3),'a5')
sv(reed(EM,'#0D0F05',1600,900,11,40),'w_ember'); sv(reed(PE,'#F7EDE6',1600,900,12,34),'w_peach'); sv(reed(MG,'#FFE3F5',1600,900,13,30),'w_mag')
sv(dither(arena_scene(1600,900,seed=7,lights=5),3,paper='#F4F4F4',ink='#0E0E0E',contrast=1.3),'w_half')
sv(dotsphere(1200,1200,['#5E0B35','#B3125F','#F04CA8','#FFC7EE'],cs=60,cx=.5,cy=.5,bg='#FFFFFF'),'sph_mag')
sv(dotsphere(1200,1200,['#8E6A55','#D09472','#F08A5D','#FFF3E8'],cs=60,cx=.5,cy=.5,bg='#FFFFFF'),'sph_peach')
sv(dotsphere(1200,1200,['#2B2025','#E4483E','#F26A2E','#F5B83D'],cs=60,cx=.5,cy=.5,bg='#FFFFFF'),'sph_ember')
sv(reed(PE,'#F7EDE6',700,1100,21,16),'tall_peach'); sv(reed(MG,'#FFE3F5',700,1100,22,16),'tall_mag'); sv(reed(EM,'#0D0F05',700,1100,23,16),'tall_ember')
