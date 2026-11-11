import sys,time
V=(0,100,320,330,500,900,20000)
KN=(-21,-19,-12,-8,8,12,19,21)
KD=(-11,-10,-9,-1,1,9,10,11)
CR={91:2,98:1,21:8,28:4,95:3,25:12}
SF="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -"
RG=range(21,99)
def D(s):return[(ord(s[(i//8)*4+min(i&7,7-i&7)])-107)*5 for i in range(64)]
T=[D(s)for s in("kkkkuuuummoqllmpkkkoljiklmmgkkkk","eccaeccaeccaeccageecigggookkoqmk")]
T[1:1]=[[0]*64]*4
B=bytearray(120);W=1;C=0;E=0
U=[]
class TO(Exception):pass
def sq(s):return(10-int(s[1]))*10+ord(s[0])-96
def setfen(f):
 global B,W,C,E
 p=f.split();B=bytearray([13]*20+([13]+[0]*8+[13])*8+[13]*20)
 i=21
 for ch in p[0]:
  if ch=="/":i+=2
  elif ch.isdigit():i+=int(ch)
  else:B[i]="PNBRQKpnbrqk".find(ch)+1;i+=1
 W=len(p)<2 or p[1]=="w"
 C=sum(1<<x for x,ch in enumerate("KQkq")if len(p)>2 and ch in p[2])
 E=0 if len(p)<4 or p[3]=="-" else sq(p[3])
def gen(cap=0):
 ms=[];ap=ms.append
 for i in RG:
  p=B[i]
  if p%13==0 or(p<7)-W:continue
  if(t:=(p-1)%6+1)==1:
   st=10-20*W;pr2=(5,4,3,2)if(i+st)//10 in(2,9)else(0,)
   for d in(st-1,st,st+1):
    j=i+d;c=B[j]
    if d==st:
     if c:continue
     [ap((i,j,pr,0))for pr in pr2 if pr or not cap]
     if not cap and i//10==3+5*W and B[i+2*st]==0:ap((i,i+2*st,0,0))
    elif c and c!=13 and(c<7)-W:
     for pr in pr2:ap((i,j,pr,c))
    elif E and j==E:ap((i,j,0,B[j-st]))
  else:
   for d in(0,0,KN,(-11,-9,9,11),(-10,-1,1,10),KD,KD)[t]:
    j=i
    while(j:=j+d):
     c=B[j]
     if c==13 or c and(c<7)==W:break
     if c:ap((i,j,0,c));break
     if not cap:ap((i,j,0,0))
     if t in(2,6):break
   if t==6 and not cap and i==25+70*W:
    for j in(i+2,i-2):
     if C&((1,2),(4,8))[not W][j<i]and all(B[s]==0 for s in(range(i+1,j+1)if j>i else range(j-1,i)))and not any(atkd(s,not W)for s in(i,(i+j)//2,j)):ap((i,j,0,0))
 return ms
def atkd(s,w):
 global W
 o=W;W=w;v=B[s];B[s]=v or 6+6*w
 r=any(m[1]==s and m[3]for m in gen(1))
 B[s]=v;W=o;return r
def mk(m):
 global W,C,E
 i,j,pr,cap=m;p=B[i];t=(p-1)%6+1
 U.append((B.copy(),C,E))
 if t==1 and cap and B[j]==0:B[j+10-20*(p>6)]=0
 B[j]=pr+6*(p>6)if pr else p
 B[i]=0
 if t==6 and abs(j-i)==2:
  r1,r2=(j+1,j-1)if j>i else(j-2,j+1);B[r2]=B[r1];B[r1]=0
 C&=~(CR.get(i,0)|CR.get(j,0))
 E=(i+j)//2 if t==1 and abs(j-i)==20 else 0
 W=not W
def un():
 global W,C,E
 b,C,E=U.pop();B[:]=b;W=not W
def ev():
 s=sum((V[(t:=(p-1)%6+1)]+T[t-1][(i-2*(i//10)-17)^56*(p>6)])*(1-(p>6)*2)for i in RG if(p:=B[i])%13)
 return s if W else -s
def srt(ms):return sorted(ms,key=lambda m:V[(m[3]-1)%6+1]*16-V[(B[m[0]]-1)%6+1]+V[m[2]]if m[3]else V[m[2]],reverse=True)
def sr(d,a,b):
 global NN
 NN+=1
 if NN&1023==0 and time.time()>DL:raise TO
 if d<=0:
  s=ev()
  if s>=b:return s
  if s>a:a=s
 n=0
 for m in srt(gen(d<=0)):
  mk(m)
  if atkd(B.index(6+6*W),W):un();continue
  n+=1;sc=-sr(d-1,-b,-a);un()
  if sc>a:a=sc
  if a>=b:break
 if d>0 and n==0:return-100000-d if atkd(B.index(12-6*W),not W)else 0
 return a
def think(D,ms):
 global DL,NN
 NN=0;DL=1e18;bm=None;DL0=time.time()+ms/1000
 for d in range(1,D+1):
  a=-10**7
  try:
   for m in srt(gen()):
    mk(m)
    if atkd(B.index(6+6*W),W):un();continue
    sc=-sr(d-1,-10**7,-a);un()
    if sc>a:a=sc;bm=m
  except TO:break
  DL=DL0
 return bm
setfen(SF)
if __name__=="__main__":
 for line in iter(sys.stdin.readline,""):
  t=line.split()
  if not t:continue
  c=t[0]
  if c=="uci":print("id name Tiny4K\nuciok",flush=True)
  elif c=="isready":print("readyok",flush=True)
  elif c=="position":
   z=t.index("moves")if"moves"in t else 99
   setfen(SF if t[1]=="startpos"else" ".join(t[2:z]))
   for s in t[z+1:]:
    i=sq(s);j=sq(s[2:]);pr="nbrq".find(s[4])+2 if len(s)>4 else 0
    for m in gen():
     if m[:3]==(i,j,pr):mk(m);break
  elif c=="go":
   D=int(t[t.index("depth")+1])if"depth"in t else 99
   ms=int(t[t.index("movetime")+1])*0.95 if"movetime"in t else(1e7 if D<99 else 1000)
   m=think(D,int(ms))
   print("bestmove "+(chr(96+m[0]%10)+str(10-m[0]//10)+chr(96+m[1]%10)+str(10-m[1]//10)+("nbrq"[m[2]-2]if m[2]else"")if m else"0000"),flush=True)
  elif c=="quit":break
