"""Deterministic palette studies. No spatial/temporal blur, no generative resynthesis.
Requires numpy, opencv-python-headless, Pillow and ffmpeg. Does not add XX engravings.
Pass the immutable Dashies static/mascots/motion directory as the first argument.
"""
from pathlib import Path
import cv2,numpy as np,subprocess,json,hashlib,sys
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(__file__).resolve().parents[1]; SOURCE=Path(sys.argv[1]); OUT=ROOT/'static/motion'; REVIEW=ROOT/'static/reviews/motion';OUT.mkdir(parents=True,exist_ok=True);REVIEW.mkdir(parents=True,exist_ok=True)
CLIPS=[('shipping','playful','exports/shipping-playful-alpha-v4.mp4',False),('ads','calm','ads/exports/ads-calm-alpha-v3.mp4',False),('ads','playful','ads/exports/ads-playful-alpha-v4.mp4',False),('token','calm','token/exports/token-calm-alpha-v1.mp4',False),('token','playful','token/exports/token-playful-alpha-v2.mp4',False),('tariff','calm','tariff/exports/tariff-calm-alpha-v1.mp4',False),('tariff','playful','tariff/exports/tariff-seedance-alpha-v14-r7.mp4',False),('tariff','page','tariff/tariff-page-v4.mp4',True)]
def smooth(a,b,x):
 t=np.clip((x-a)/(b-a),0,1);return t*t*(3-2*t)
def grade(rgb,agent):
 hsv=cv2.cvtColor(rgb.astype(np.float32)/255,cv2.COLOR_RGB2HSV);h,s,v=cv2.split(hsv);out=hsv.copy()
 if agent=='shipping':
  mask=smooth(145,165,h)*(1-smooth(193,205,h))*smooth(.08,.30,s)*(1-smooth(.72,.90,v));target=350;scale=.92
 elif agent=='ads':
  mask=smooth(195,220,h)*(1-smooth(250,270,h))*smooth(.1,.30,s);target=214;scale=.68
 elif agent=='token':
  mask=smooth(230,260,h)*(1-smooth(295,320,h))*smooth(.08,.25,s);target=282;scale=.86
 else:
  mask=(1-smooth(38,55,h))*smooth(.10,.35,s)*smooth(.08,.20,v);target=39;scale=.96
 out[:,:,0]=target;out[:,:,1]=s*(.84 if agent in ['ads','token'] else .9);out[:,:,2]=v*scale
 shifted=cv2.cvtColor(out,cv2.COLOR_HSV2RGB);result=rgb/255*(1-mask[:,:,None])+shifted*mask[:,:,None]
 if agent=='token':
  brass=smooth(105,130,h)*(1-smooth(175,190,h))*smooth(.12,.28,s)
  gold=hsv.copy();gold[:,:,0]=43;gold[:,:,1]=s*.95;gold[:,:,2]=np.clip(v*1.08,0,1)
  result=result*(1-brass[:,:,None])+cv2.cvtColor(gold,cv2.COLOR_HSV2RGB)*brass[:,:,None]
 if agent=='tariff':
  # Warm raised lines separate chromatically from the redder copper body.
  brass=smooth(23,29,h)*(1-smooth(40,48,h))*smooth(.28,.45,s)*smooth(.45,.7,v)
  gold=hsv.copy();gold[:,:,0]=43;gold[:,:,1]=s*.9
  result=result*(1-brass[:,:,None])+cv2.cvtColor(gold,cv2.COLOR_HSV2RGB)*brass[:,:,None]
 return np.uint8(np.clip(result*255,0,255))
def encoder(path,w,h,fps,rgba=False):
 args=['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgba' if rgba else 'rgb24','-s',f'{w}x{h}','-r',str(fps),'-i','-','-an']
 args+=['-c:v','libvpx-vp9','-pix_fmt','yuva420p','-b:v','0','-crf','20','-auto-alt-ref','0','-row-mt','1','-threads','2'] if rgba else ['-c:v','libx264','-pix_fmt','yuv420p','-crf','17','-preset','fast','-movflags','+faststart','-threads','2']
 return subprocess.Popen(args+[str(path)],stdin=subprocess.PIPE)
def run(spec):
 agent,variant,rel,opaque=spec;id=f'{agent}-{variant}-v2';src=SOURCE/rel;cap=cv2.VideoCapture(str(src));fps=cap.get(cv2.CAP_PROP_FPS);count=int(cap.get(cv2.CAP_PROP_FRAME_COUNT));W=int(cap.get(3));H=int(cap.get(4));w=W if opaque else W//2
 # A fixed union crop protects the full motion envelope without changing placement frame-to-frame.
 if opaque:x0,y0,x1,y1=0,0,w,H
 else:
  x0,y0,x1,y1=w,H,0,0
  while True:
   ok,f=cap.read()
   if not ok:break
   ys,xs=np.where(f[:,:w,0]>24)
   if len(xs):x0=min(x0,int(xs.min()));x1=max(x1,int(xs.max())+1);y0=min(y0,int(ys.min()));y1=max(y1,int(ys.max())+1)
  margin=round(max(x1-x0,y1-y0)*.09);x0=max(0,(x0-margin)//2*2);y0=max(0,(y0-margin)//2*2);x1=min(w,((x1+margin+1)//2)*2);y1=min(H,((y1+margin+1)//2)*2)
 cap.set(cv2.CAP_PROP_POS_FRAMES,0);ow=x1-x0;oh=y1-y0;ow-=ow%2;oh-=oh%2
 page=encoder(OUT/(id+'-ivory.mp4'),ow,oh,fps);packed=None if opaque else encoder(OUT/(id+'-packed.mp4'),ow*2,oh,fps);webm=None if opaque else encoder(OUT/(id+'.webm'),ow,oh,fps,True)
 thumbs=[];metrics=[];index=0
 while True:
  ok,f=cap.read()
  if not ok:break
  rgb=cv2.cvtColor(f if opaque else f[:,w:],cv2.COLOR_BGR2RGB)[y0:y0+oh,x0:x0+ow];alpha=np.full((oh,ow),255,np.uint8) if opaque else f[y0:y0+oh,x0:x0+ow,0].copy();new=grade(rgb,agent)
  if opaque:
   # Neutral source page (#FAF9F5) shifts to Jaxxton ivory, preserving texture and local contrast.
   hsv=cv2.cvtColor(rgb,cv2.COLOR_RGB2HSV);m=(1-smooth(8,25,hsv[:,:,1]))*smooth(215,245,hsv[:,:,2]);new=np.uint8(np.clip(new.astype(float)+m[:,:,None]*np.array([-3,-3,-1]),0,255))
  rgba=np.dstack([new,alpha]);a=alpha[:,:,None]/255
  ivory=np.uint8(new*a+np.array([247,246,244])*(1-a));page.stdin.write(ivory.tobytes())
  if packed:packed.stdin.write(np.concatenate([np.repeat(alpha[:,:,None],3,axis=2),new],axis=1).tobytes());webm.stdin.write(rgba.tobytes())
  if index==0:
   from PIL import Image
   Image.fromarray(rgba if not opaque else new).save(OUT/(id+'.webp'),lossless=True)
  # Every frame appears on a light/dark split, with an exact frame number.
  bg=np.full_like(new,[247,246,244]);bg[:,ow//2:]=[28,9,12];composite=np.uint8(new*a+bg*(1-a));thumb=cv2.resize(composite,(240,200),interpolation=cv2.INTER_AREA);cv2.putText(thumb,f'{index:03d}',(8,18),cv2.FONT_HERSHEY_SIMPLEX,.4,(130,130,130),1);thumbs.append(thumb)
  metrics.append({'frame':index,'visiblePixels':int((alpha>24).sum()),'borderAlphaMax':int(max(alpha[0].max(),alpha[-1].max(),alpha[:,0].max(),alpha[:,-1].max())),'alphaPreservedBeforeEncoding':True});index+=1
 for proc in [page,packed,webm]:
  if proc:proc.stdin.close();assert proc.wait()==0
 assert index==count,(id,index,count)
 for start in range(0,len(thumbs),30):
  board=np.full((6*200,5*240,3),247,np.uint8)
  for n,t in enumerate(thumbs[start:start+30]):board[(n//5)*200:(n//5+1)*200,(n%5)*240:(n%5+1)*240]=t
  cv2.imwrite(str(REVIEW/f'{id}-{start//30+1:02d}.jpg'),cv2.cvtColor(board,cv2.COLOR_RGB2BGR),[cv2.IMWRITE_JPEG_QUALITY,92])
 record={'id':id,'agent':agent,'variant':variant,'source':rel,'sourceSha256':hashlib.sha256(src.read_bytes()).hexdigest(),'sourceRevision':'dc1319d1beeb0d00b85eeec85b1e5cb179fa2e3e','status':'palette-study','width':ow,'height':oh,'fps':fps,'frames':count,'duration':count/fps,'crop':[x0,y0,ow,oh],'opaque':opaque,'poster':f'/motion/{id}.webp','page':f'/motion/{id}-ivory.mp4','packed':None if opaque else f'/motion/{id}-packed.mp4','webm':None if opaque else f'/motion/{id}.webm','reviewSheets':[f'/reviews/motion/{id}-{i+1:02d}.jpg' for i in range((count+29)//30)],'limitations':['Palette study, not an approved final animation.','Original motion/edge artifacts remain.','XX tool engravings not tracked into motion; still masters remain identity authority.']}
 (REVIEW/(id+'.json')).write_text(json.dumps({'clip':record,'frameMetrics':metrics},indent=2)+'\n');print(id,count,'frames',flush=True);return record
if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=2) as pool:records=list(pool.map(run,CLIPS))
 (OUT/'manifest.json').write_text(json.dumps(records,indent=2)+'\n')
