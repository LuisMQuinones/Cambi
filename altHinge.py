# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 11:03:09 2015

@author: Luimi
"""

import os
import sys
import re

from solid import *
from solid.utils import *

SEGMENTS = 48

'''
rough construction of a hinge. only paramater that can be controlled is the height of the hinge and the tolerance,
    - radius of small cylinder is held constant at 1.5 mm
    - thickness of the hinge is held constant at 6.0 mm
'''

def cutout(length):
  #  cut= cube(size=[5.0,10.5, 6.0], center=True)
    #cut= cube(size=[5.0,9., 6.0], center=True)
    cut= cube(size=[5.0,9.+1.5, 6.0], center=True)
    cut = rotate(a=90, v=[0,1,0])(cut)
    cut =rotate(a=90,v=[0,0,1])(cut)
    
    edgeCut = cube(size=[length,3.,5.0],center = True)
   # edgeCut = cube(size=[length,.5,5.0],center = True)
    #edgeCut = translate([0,-1.5-.75,0])(edgeCut)
    return cut+edgeCut
    
def hinge():
    base = cube(size = [3.,2.,3.], center=True)
    base += translate([0,0,-2.25])(cube(size=[3.,2,1.5],center=True))
    
    male = cylinder(h=3,r1=1.5,r2=0.)    
    male = rotate(a=90,v=[180,1,0])(male)
    male = translate([0,-1.,0])(male)
    
    female = cube(size = [3.,3.,3.5],center=True)
    female = translate([0,-3.,0])(female)
    
    femaleCut = cylinder(h=3,r1=1.5+.35,r2=0.)
    femaleCut = rotate(a=90,v=[180,1,0])(femaleCut)
    femaleCut = translate([0,-1.,0])(femaleCut)
    
    female-=femaleCut
    
    topSupport = cube(size=[3.0,9.,2.], center=True)
    topSupport = translate([0,0,1.+1.75 + 1.5])(topSupport)  

    connector =  translate([0,-3.,3])(cube(size = [3.,3.,3.5],center=True))
    
    
    bottomSupport= cube(size=[3.,9.,3.], center=True)
    bottomSupport = translate([0,0,-1.5 -3.])(bottomSupport)
    hinge= base+male + mirror([0,1,0])(male) + female + mirror([0,1,0])(female) + topSupport+ connector + mirror([0,1,0])(connector)+bottomSupport
    
    hinge = rotate(a=90, v=[0,1,0])(hinge)
    hinge =rotate(a=90,v=[0,0,1])(hinge)
    return hinge
def hinge2():
    base = cube(size = [3.,2.,3.], center=True)
    base += translate([0,0,-2.25])(cube(size=[3.,2,1.5],center=True))
    
    male = cylinder(h=3,r1=1.5,r2=0.)    
    male = rotate(a=90,v=[180,1,0])(male)
    male = translate([0,-1.,0])(male)
    
    female = cube(size = [3.,3.,3.5],center=True)
    female = translate([0,-3.,0])(female)
    
    femaleCut = cylinder(h=3,r1=1.5+.35,r2=0.)
    femaleCut = rotate(a=90,v=[180,1,0])(femaleCut)
    femaleCut = translate([0,-1.,0])(femaleCut)
    
    female-=femaleCut
    
    topSupport = cube(size=[3.0,9.,2.], center=True)
    topSupport = translate([0,0,1.+1.75 + 1.5])(topSupport)  

    connector =  translate([0,-3.,3])(cube(size = [3.,3.,3.5],center=True))
    
    
    bottomSupport= cube(size=[3.,9.,3.], center=True)
    bottomSupport = translate([0,0,-1.5 -3.])(bottomSupport)
    hinge= base+male + mirror([0,1,0])(male) + female + mirror([0,1,0])(female)+ connector + mirror([0,1,0])(connector)
    
    hinge = rotate(a=90, v=[0,1,0])(hinge)
    hinge =rotate(a=90,v=[0,0,1])(hinge)
    return hinge
    
def hingeDesign(radtol,ztol):
    base = cube(size = [3.,2.,3.], center=True)
    base += translate([0,0,-2.25])(cube(size=[3.,2,1.5],center=True))
    
    male = cylinder(h=3,r1=1.5,r2=0.)    
    male = rotate(a=90,v=[180,1,0])(male)
    male = translate([0,-1.,0])(male)
    
    female = cube(size = [3.,3.,3.5],center=True)
    female = translate([0,-3.,0])(female)
    
    connector =  translate([0,-3.,3])(cube(size = [3.,3.,3.5],center=True))    
    
    female+=connector    
    
    femaleCut = cylinder(h=3+ztol,r1=1.5+radtol,r2=0.)
    femaleCut = rotate(a=90,v=[180,1,0])(femaleCut)
    femaleCut = translate([0,-1.,0])(femaleCut)
    
    female-=femaleCut
    
    topSupport = cube(size=[3.0,9.,2.], center=True)
    topSupport = translate([0,0,1.+1.75 + 1.5])(topSupport)  

    
    
    
    bottomSupport= cube(size=[3.,9.,3.], center=True)
    bottomSupport = translate([0,0,-1.5 -3.])(bottomSupport)
    hinge= base+male + mirror([0,1,0])(male) + female + mirror([0,1,0])(female) + topSupport+bottomSupport
    
    hinge = rotate(a=90, v=[0,1,0])(hinge)
    hinge =rotate(a=90,v=[0,0,1])(hinge)
    return hinge
    

    
if __name__ == '__main__':
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.curdir
    file_out = os.path.join(out_dir, 'althinge.scad')

  
    #a = hinge()
    #a +=cutout(25)
    
    a = hingeDesign(.4,.35)
    print("%(__file__)s: SCAD file written to: \n%(file_out)s" % vars())

    # Adding the file_header argument as shown allows you to change
    # the detail of arcs by changing the SEGMENTS variable.  This can
    # be expensive when making lots of small curves, but is otherwise
    # useful.
    scad_render_to_file(a, file_out, file_header='$fn = %s;' % SEGMENTS)