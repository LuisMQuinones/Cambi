# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 13:02:28 2015

@author: Luimi
"""
from numpy import (array,dot,arccos)
from numpy.linalg import norm
from numpy import clip
from solid import *
from solid.utils import *

import utils
import altHinge
import sys

class Face:
    def __init__(self,vertID=[], vertPos=[] ):
        self.vertID = vertID
        self.vertPos = vertPos
class Fold:

    def __init__(self,startingPos=[], endingPos=[]):
        self.startingPos = startingPos
        self.endingPos = endingPos
    def numFaces(self):
        return len(self.faces)
        
def main(vertices, faces, folds,desiredThickness):
    obj = utils.createFaces(vertices,faces,desiredThickness)
    obj = addHinges(obj, folds)
    #addHinges(obj,folds)
    return obj
def distance(point1,point2):
    return ((point2[0]-point1[0])**2 + (point2[1]-point1[1])**2)**.5
def midpoint(startingPoint, endingPoint):
    return   [(startingPoint[0]+ endingPoint[0])/2, (startingPoint[1]+endingPoint[1])/2.]

def angle(u,v):
    angle = math.degrees(math.atan2(u[1],u[0]) - math.atan2(v[1],v[0]))  
    return angle
    
def addHinges(obj, folds):
    
    for fold in folds:
        startingPoint = fold.startingPos
        endingPoint =  fold.endingPos
        length =  distance(startingPoint, endingPoint)
        midpt = midpoint(startingPoint, endingPoint)
        u = [endingPoint[0] - startingPoint[0], endingPoint[1]-startingPoint[1]]
        
        foldangle = angle(u, [1,0])
        
        midpt.append(0)
        
    
        
        cutout = altHinge.cutout(length+2.5)
        cutout = rotate(a=foldangle, v=[0,0,1])(cutout)
        cutout = translate(midpt)(cutout)
        cutout = translate([0,0,1.5])(cutout)
        
        obj-=cutout
        
        hinge = altHinge.hinge2()
        hinge = rotate(a = foldangle,v=[0,0,1])(hinge)
        hinge = translate(midpt)(hinge)
        hinge = translate([0,0,1.5])(hinge)
        
        obj += hinge 
    return obj
        
def processFaces(vertices, faces):
    facelist = []
    for face in faces:
        vertlist = []
        for vert in face:
            vertlist.append(vertices[vert])
        facelist.append(Face(face,vertlist))
    return facelist
def processFolds(vertoces, folds):
    foldlist = []
    for fold in folds:
        currentFold = Fold(vertices[fold[0]],vertices[fold[1]])
        foldlist.append(currentFold)
    return foldlist

SEGMENTS = 96
if __name__ == '__main__':
    #main()
    
    #coord = sys.argv[1]
    
    defaultFilename = "coord.txt"    
    
    filename = sys.argv[1] if len(sys.argv) >1 else defaultFilename
    
    #vertices = utils.getVertices("coord4.txt")
    vertices = utils.getVertices(filename)
    #faces = utils.getFaces("coord4.txt")
    faces = utils.getFaces(filename)
    faces = processFaces(vertices,faces)
    #folds = processFolds (vertices,utils.getFolds("coord4.txt"))
    folds = processFolds (vertices,utils.getFolds(filename))
    a =  main(vertices,faces,folds, 3.)
    
    out_dir = sys.argv[2] if len(sys.argv) > 2 else os.curdir
    out_filename = sys.argv[3]+".scad" if len(sys.argv) > 3 else "main.scad"
    file_out = os.path.join(out_dir,out_filename)



    print("%(__file__)s: SCAD file written to: \n%(file_out)s" % vars())

    scad_render_to_file(a, file_out, file_header='$fn = %s;' % SEGMENTS)

    