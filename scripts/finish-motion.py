"""Export reviewed Seedance sources without filtering character texture.
Key the chroma stage using a narrow edge-only color-unmixing band; export fixed framing.
Usage: python scripts/finish-motion.py [agent-variant ...]
"""
from pathlib import Path
import cv2, numpy as np, subprocess, json, hashlib, sys, os
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'output/final-v1';OUT=ROOT/'static/motion';REVIEW=ROOT/'static/reviews/final-v1'
OUT.mkdir(exist_ok=True,parents=True);REVIEW.mkdir(exist_ok=True,parents=True)
SIZE=1200
VERSION=os.environ.get('MOTION_VERSION','v3')
SOURCE_VERSION=os.environ.get('SOURCE_VERSION','v1')

def matte(bgr):
 rgb=cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB).astype(np.float32)
 r,g,b=cv2.split(rgb); excess=g-np.maximum(r,b)
 core=(excess<18).astype(np.uint8)
 # A one-pixel interior gives the unmixing solver a clean foreground sample.
 core=cv2.erode(core,np.ones((3,3),np.uint8),iterations=1)
 count,labels,stats,centroids=cv2.connectedComponentsWithStats(core,8)
 for i in range(1,count):
  if stats[i,cv2.CC_STAT_AREA]<12:core[labels==i]=0
 dist,lbl=cv2.distanceTransformWithLabels(1-core,cv2.DIST_L2,5,labelType=cv2.DIST_LABEL_PIXEL)
 lut=np.zeros((lbl.max()+1,3),np.float32);lut[lbl[core>0]]=rgb[core>0]
 near=lut[lbl]
 # Corner median is stable against source compression and mild lighting variations.
 h,w=core.shape;sample=np.concatenate([rgb[:40,:40].reshape(-1,3),rgb[:40,-40:].reshape(-1,3),rgb[-40:,:40].reshape(-1,3),rgb[-40:,-40:].reshape(-1,3)])
 bg=np.median(sample,axis=0)
 direction=near-bg
 alpha=np.clip(np.sum((rgb-bg)*direction,axis=2)/np.maximum(np.sum(direction*direction,axis=2),1),0,1)
 alpha[core>0]=1;alpha[dist>6]=0
 alpha[alpha<.015]=0
 clean=np.clip((rgb-(1-alpha[:,:,None])*bg)/np.maximum(alpha[:,:,None],.03),0,255)
 clean=np.where((alpha<.12)[:,:,None],near,clean)
 clean[alpha==0]=0
 return clean.astype(np.uint8),np.uint8(alpha*255),bg.tolist()

def enc(path,rgba=False):
 pix='rgba' if rgba else 'rgb24';w=SIZE*2 if 'packed' in path.name else SIZE
 args=['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt',pix,'-s',f'{w}x{SIZE}','-r','24','-i','-','-an']
 args+=['-c:v','libvpx-vp9','-pix_fmt','yuva420p','-b:v','0','-crf','16','-auto-alt-ref','0','-row-mt','1','-threads','2'] if rgba else ['-c:v','libx264','-pix_fmt','yuv420p','-crf','14','-preset','fast','-movflags','+faststart','-threads','2']
 return subprocess.Popen(args+[str(path)],stdin=subprocess.PIPE)

def finish(name):
 agent,variant=name.split('-',1);src=SOURCE/(name+'-source'+('' if SOURCE_VERSION=='v1' else '-'+SOURCE_VERSION)+'.mp4');cap=cv2.VideoCapture(str(src));frames=int(cap.get(7));fps=cap.get(5);w=int(cap.get(3));h=int(cap.get(4));assert fps==24
 cache=SOURCE/(name+'-'+VERSION);cache.mkdir(exist_ok=True)
 bounds=[];metrics=[]
 for n in range(frames):
  ok,f=cap.read();assert ok
  rgb,a,bg=matte(f);ys,xs=np.where(a>32);bounds.append([int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)])
  np.savez_compressed(cache/f'{n:04d}.npz',rgb=rgb,alpha=a)
  metrics.append({'frame':n,'bbox':bounds[-1],'visiblePixels':int((a>32).sum()),'backgroundEstimate':bg,'sourceBorderAlphaMax':int(max(a[0].max(),a[-1].max(),a[:,0].max(),a[:,-1].max()))})
  if n%36==0:print(name,'matte',n,flush=True)
 box=np.array(bounds);x0,y0=box[:,:2].min(0);x1,y1=box[:,2:].max(0)
 side=int(np.ceil(max(x1-x0,y1-y0)*1.15/2)*2);cx=(x0+x1)/2;cy=(y0+y1)/2;left=int(cx-side/2);top=int(cy-side/2)
 id=name+'-'+VERSION;paths={'packed':f'/motion/{id}-packed.mp4','webm':f'/motion/{id}.webm','page':f'/motion/{id}-ivory.mp4','dark':f'/motion/{id}-dark.mp4','poster':f'/motion/{id}.webp'}
 procs={k:enc(ROOT/('static'+paths[k]),k=='webm') for k in ['packed','webm','page','dark']}
 thumbs=[];details=[]
 for n in range(frames):
  with np.load(cache/f'{n:04d}.npz') as d:rgb=d['rgb'];a=d['alpha']
  canvas=np.zeros((side,side,4),np.uint8)
  sx0=max(0,left);sy0=max(0,top);sx1=min(w,left+side);sy1=min(h,top+side)
  canvas[sy0-top:sy1-top,sx0-left:sx1-left]=np.dstack([rgb,a])[sy0:sy1,sx0:sx1]
  # Resample premultiplied color and alpha together to avoid dark edge contamination.
  premul=canvas[:,:,:3].astype(np.float32)*(canvas[:,:,3:4]/255)
  aa=cv2.resize(canvas[:,:,3].astype(np.float32)/255,(SIZE,SIZE),interpolation=cv2.INTER_AREA)
  cc=cv2.resize(premul,(SIZE,SIZE),interpolation=cv2.INTER_AREA)
  cc=np.uint8(np.clip(cc/np.maximum(aa[:,:,None],.001),0,255));a8=np.uint8(np.clip(aa*255,0,255));rgba=np.dstack([cc,a8])
  procs['webm'].stdin.write(rgba.tobytes())
  procs['packed'].stdin.write(np.concatenate([np.repeat(a8[:,:,None],3,axis=2),cc],axis=1).tobytes())
  light=np.uint8(cc*aa[:,:,None]+np.array([247,246,244])*(1-aa[:,:,None]));dark=np.uint8(cc*aa[:,:,None]+np.array([28,9,12])*(1-aa[:,:,None]))
  procs['page'].stdin.write(light.tobytes());procs['dark'].stdin.write(dark.tobytes())
  if n==0:Image.fromarray(rgba).save(ROOT/('static'+paths['poster']),lossless=True)
  # 24 consecutive frames per board; preserved aspect ratio with full silhouette.
  combo=light.copy();combo[:,SIZE//2:]=dark[:,SIZE//2:]
  thumb=cv2.resize(combo,(300,300),interpolation=cv2.INTER_AREA);cv2.putText(thumb,f'{n:03d}',(8,20),0,.5,(135,135,135),1);thumbs.append(thumb)
  # 1:1 detail review around head/prop regions on the light composite.
  if n%12==0:
   small=cv2.resize(light,(600,600));cv2.imwrite(str(REVIEW/f'{id}-detail-{n:03d}.jpg'),cv2.cvtColor(small,cv2.COLOR_RGB2BGR),[cv2.IMWRITE_JPEG_QUALITY,96])
  ys,xs=np.where(a8>32);metrics[n]['exportMargins']=[int(xs.min()),int(ys.min()),int(SIZE-xs.max()-1),int(SIZE-ys.max()-1)]
 for p in procs.values():p.stdin.close()
 for p in procs.values():assert p.wait()==0
 sheets=[]
 for start in range(0,frames,24):
  board=np.full((4*300,6*300,3),247,np.uint8)
  for k,t in enumerate(thumbs[start:start+24]):board[k//6*300:(k//6+1)*300,k%6*300:(k%6+1)*300]=t
  path=f'/reviews/final-v1/{id}-{start//24+1:02d}.jpg';cv2.imwrite(str(ROOT/('static'+path)),cv2.cvtColor(board,cv2.COLOR_RGB2BGR),[cv2.IMWRITE_JPEG_QUALITY,93]);sheets.append(path)
 record={'id':id,'agent':agent,'variant':variant,'source':f'/motion/sources/{name}-seedance-{SOURCE_VERSION}.mp4','sourceSha256':hashlib.sha256(src.read_bytes()).hexdigest(),'status':'pending-review','width':SIZE,'height':SIZE,'fps':fps,'frames':frames,'duration':frames/fps,'crop':[left,top,side,side],'opaque':False,**paths,'reviewSheets':sheets,'reviewFramesPerSheet':24,'reviewReport':f'/reviews/final-v1/{id}.json','model':'Seedance 2.5','limitations':[]}
 (REVIEW/(id+'.json')).write_text(json.dumps({'clip':record,'frameMetrics':metrics},indent=2)+'\n')
 (SOURCE/(name+'-record.json')).write_text(json.dumps(record,indent=2)+'\n')
 print(name,'EXPORTED',frames,'frames',flush=True)
 return record
if __name__=='__main__':
 for name in sys.argv[1:]:finish(name)
