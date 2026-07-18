#!/usr/bin/env python3
"""Neutral UV-style plate from a folio scan (the look used in our tooling).

Usage: python3 gen_uv_plate.py scan.jpg out.jpg
Recipe: gaussian background-subtract (sigma = 3.5% of width), normalize,
sharpen x1.4, dark floor 18, grayscale. Get the scan yourself from the
Beinecke Digital Library (MS 408, public domain).  Requires opencv-python.
"""
import sys, cv2, numpy as np
src,dst=sys.argv[1],sys.argv[2]
img=cv2.imread(src); gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
sigma=max(45,int(gray.shape[1]*0.035))
blur=cv2.GaussianBlur(gray,(0,0),sigmaX=sigma,sigmaY=sigma)
diff=cv2.normalize(cv2.subtract(blur,gray),None,0,255,cv2.NORM_MINMAX)
t=cv2.convertScaleAbs(cv2.GaussianBlur(diff,(3,3),0),alpha=1.4,beta=0)
blended=np.clip(cv2.addWeighted(np.full_like(t,18),1.0,t,1.0,0),0,255).astype(np.uint8)
cv2.imwrite(dst,cv2.merge([blended]*3),[cv2.IMWRITE_JPEG_QUALITY,85])
print("saved",dst)
