



import numpy as np
import re

from solid import *
from solid.utils import *



    


def verticesfromface(face,vertices):
    faceVert = []
    for point in face:
        faceVert.append(vertices[point])
        
    return faceVert
    
def createFaces(vertices,faces,desiredThickness):
     listoffaces =(linear_extrude(height=desiredThickness,center=False)(polygon(verticesfromface(faces[0].vertID,vertices))))
     i = 1
     for face in faces[1:]:
        # if i==6 or i==7 or i==14 or i==15 or i==22 or i==23 or i==30 or i==31 or i==38 or i==39 or i==46 or i==47 or i==54 or i==55 or i==62 or i==63: 
           #  i+=1
          #   continue
         listoffaces+=(linear_extrude(height=desiredThickness,center=False)(polygon(verticesfromface(face.vertID,vertices))))

         i+=1
     return listoffaces
     
     
def centroid(vertices):
    areasum = 0
    
    for i in range(0, len(vertices)):
        iplus1= i+1
        if (i == len(vertices)-1):
            iplus1 =0
        areasum+=(vertices[i][0]*vertices[iplus1][1] - vertices[iplus1][0]*vertices[i][1])
    area = areasum * .5
    
    CxSum = 0
    
    for i in range(0, len(vertices)):
        iplus1= i+1
        if (i == len(vertices)-1):
            iplus1 =0
        same=(vertices[i][0]*vertices[iplus1][1] - vertices[iplus1][0]*vertices[i][1])
      
        CxSum+= (vertices[i][0] + vertices[iplus1][0])*same
    Cx = 1/(6. * area) * CxSum
    
    CySum = 0
    
    for i in range(0, len(vertices)):
        iplus1= i+1
        if (i == len(vertices)-1):
            iplus1 =0
        same=(vertices[i][0]*vertices[iplus1][1] - vertices[iplus1][0]*vertices[i][1]) 
       
        CySum+= (vertices[i][1] + vertices[iplus1][1])*same
   
    Cy = 1/(6. * area) * CySum
    
    return [Cx,Cy]
    
def scalePolygon(vertices, centroid, scaleFactor):
    workedVertices = []
        
    for vert in vertices:
        vector = [ vert[0]-centroid[0],vert[1]- centroid[1]]
        scaledvector = np.multiply(scaleFactor, vector).tolist()
        
        workedVertices.append([centroid[0]+ scaledvector[0], centroid[1] + scaledvector[1]])
    return workedVertices
    
def getVertices(filename):
    p = re.compile('(v\d*)+\s*? \[\s*?(\-?\d+\.?\d*?),\s*?(\-?\d+?\.?\d*?)\]')
    textfile = open(filename, 'r')
    filetext = textfile.read()
    textfile.close()
    matches = re.findall(p,filetext)
    vert = []
   # print "filetext",filetext
    for i in matches:
        v = [float(i[1]), float(i[2])]

        vert.append(v)
        
   
    return vert
def getFaces(filename):
    p = re.compile('f\d*\s*\[(.*)\]')
    textfile = open(filename, 'r')
    filetext = textfile.read()
    textfile.close()
    matches = re.findall(p,filetext)
    faces = []
    for i in matches:
        f = re.split('[,]',i)
        for j in range(0,len(f)):
            f[j] = int(f[j])
        faces.append(f)
    return faces

def getFolds(filename):
    p = re.compile('e\d*\s*\[(\d+),(\d+)\]\s*\[(.*)\]')
    textfile = open(filename, 'r')
    filetext = textfile.read()
    textfile.close()
    matches = re.findall(p,filetext)
    folds = []
    for i in matches:
        v1 = int(i[0])
        v2 = int(i[1])
        
       
        e = [v1,v2]
        folds.append(e)
    return folds  
