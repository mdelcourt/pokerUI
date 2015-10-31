#!/usr/bin/python
import os
imageName="sponsor.png"
time=10
#os.chdir("files/sponsor_folder")
images=[]
for i in os.listdir("."):
  if i[-4:].find(".png")>-1:
    images.append(i)
print images
while True:
  for im in images:
    os.system("cp %s ../%s"%(im,imageName))
    print "Moved %s to ../%s"%(im,imageName)
    os.system("sleep %ss"%time)
  
