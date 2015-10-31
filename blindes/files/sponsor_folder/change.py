#!/usr/bin/python
import time, os
imageName="sponsor.png"
stime=10
images=[]
for i in os.listdir("."):
  if i[-4:].find(".png")>-1:
    images.append(i)
print images
while not ".kill_change_sponsor" in os.listdir("."):
  for im in images:
    os.system("cp %s ../%s"%(im,imageName))
    print "Moved %s to ../%s"%(im,imageName)
    time.sleep(stime)

