import json,os,sys,urllib.request,urllib.error
A=os.environ.get("MAKEFUN_ENV_URL")or sys.exit("MAKEFUN_ENV_URL is not set")
V=(0,100,320,330,500,900,20000)
KN=(-21,-19,-12,-8,8,12,19,21)
KD=(-11,-10,-9,-1,1,9,10,11)
CR={91:2,98:1,21:8,28:4,95:3,25:12}
def D(s):return[(ord(s[(i//8)*4+min(i&7,7-i&7)])-107)*5 for i in range(64)]
T=[D(s)for s in("kkkkuuuummoqllmpkkkoljiklmmgkkkk","aceecgkkekmnelnoeknoelmncgklacee","giiiikkkiklmillmikmmimmmilkkgiii","eccaeccaeccaeccageecigggookkoqmk")]
T[3:3]=[[0]*64]*2
B=bytearray(120);W=1;C=0;E=0;S=[]
class X(Exception):pass
def F(f):
 global B,W,C,E
 p=f.split();B=bytearray([13]*20+([13]+[0]*8+[13])*8+[13]*20)
 i=21
 for c in p[0]:
  if c=="/":i+=2
  elif c.isdigit():i+=int(c)
  else:B[i]="PNBRQKpnbrqk".find(c)+1;i+=1
 W=len(p)<2 or p[1]=="w"
 C=sum(1<<x for x,c in enumerate("KQkq")if len(p)>2 and c in p[2])
 E=0 if len(p)<4 or p[3]=="-" else(10-int(p[3][1]))*10+ord(p[3][0])-96
def G(c=0):
 m=[];a=m.append
 for i in range(21,99):
  p=B[i]
  if p%13==0 or(p<7)-W:continue
  if(t:=(p-1)%6+1)==1:
   s=10-20*W;q=(5,4,3,2)if(i+s)//10 in(2,9)else(0,)
   for d in(s-1,s,s+1):
    j=i+d;v=B[j]
    if d==s:
     if v:continue
     [a((i,j,r,0))for r in q if r or not c]
     if not c and i//10==3+5*W and B[i+2*s]==0:a((i,i+2*s,0,0))
    elif v and v!=13 and(v<7)-W and(c==2 or v%6):
     for r in q:a((i,j,r,v))
    elif E and j==E:a((i,j,0,B[j-s]))
  else:
   for d in(0,0,KN,(-11,-9,9,11),(-10,-1,1,10),KD,KD)[t]:
    j=i
    while(j:=j+d):
     v=B[j]
     if v==13 or v and(v<7)==W:break
     if v:a((i,j,0,v))if c==2 or v%6 else 0;break
     if not c:a((i,j,0,0))
     if t in(2,6):break
   if t==6 and not c and i==25+70*W:
    for j in(i+2,i-2):
     if C&((1,2),(4,8))[not W][j<i]and all(B[x]==0 for x in(range(i+1,j+1)if j>i else range(j-1,i)))and not any(K(x,not W)for x in(i,(i+j)//2,j)):a((i,j,0,0))
 return m
def K(s,w):
 global W
 o=W;W=w;v=B[s];B[s]=v or 6+6*w
 r=any(m[1]==s and m[3]for m in G(2))
 B[s]=v;W=o;return r
def M(m):
 global W,C,E
 i,j,r,v=m;p=B[i];t=(p-1)%6+1
 S.append((B.copy(),C,E))
 if t==1 and v and B[j]==0:B[j+10-20*(p>6)]=0
 B[j]=r+6*(p>6)if r else p
 B[i]=0
 if t==6 and abs(j-i)==2:
  r1,r2=(j+1,j-1)if j>i else(j-2,j+1);B[r2]=B[r1];B[r1]=0
 C&=~(CR.get(i,0)|CR.get(j,0))
 E=(i+j)//2 if t==1 and abs(j-i)==20 else 0
 W=not W
def N():
 global W,C,E
 b,C,E=S.pop();B[:]=b;W=not W
def P():
 s=sum((V[(t:=(p-1)%6+1)]+T[t-1][(i-2*(i//10)-17)^56*(p>6)])*(1-(p>6)*2)for i in range(21,99)if(p:=B[i])%13)
 return s if W else -s
def O(m):return sorted(m,key=lambda m:V[(m[3]-1)%6+1]*16-V[(B[m[0]]-1)%6+1]+V[m[2]]if m[3]else V[m[2]],reverse=True)
NN=0;NB=40000
def R(d,a,b):
 global NN
 NN+=1
 if NN>NB:raise X
 if d<=0:
  s=P()
  if s>=b:return s
  if s>a:a=s
 n=0
 for m in O(G(d<=0)):
  M(m)
  if K(B.index(6+6*W),W):N();continue
  n+=1;z=-R(d-1,-b,-a);N()
  if z>a:a=z
  if a>=b:break
 if d>0 and n==0:return-100000-d if K(B.index(12-6*W),not W)else 0
 return a
def H():
 global NN
 NN=0;bm=None
 for d in range(1,21):
  a=-10**7;cur=None
  try:
   for m in O(G()):
    M(m)
    if K(B.index(6+6*W),W):N();continue
    z=-R(d-1,-10**7,-a);N()
    if z>a:a=z;cur=m
  except X:break
  bm=cur
 return bm
def post(p,b):
 q=urllib.request.Request(A+p,data=json.dumps(b).encode(),headers={"content-type":"application/json"})
 try:
  with urllib.request.urlopen(q)as r:return json.load(r)
 except urllib.error.HTTPError as e:sys.exit(f"{p}: HTTP {e.code}")
def u(m):
 return chr(96+m[0]%10)+str(10-m[0]//10)+chr(96+m[1]%10)+str(10-m[1]//10)+("nbrq"[m[2]-2]if m[2]else"")
while 1:
 g=post("/game",{})
 if g["status"]=="done":break
 while g["status"]=="your_move":
  L=g["legal_moves"]
  if L:
   F(g["fen"]);m=H();v=u(m)if m else""
   g=post("/move",{"game":g["game"],"move":v if v in L else L[0]})
  else:g=post("/resign",{"game":g["game"]})
