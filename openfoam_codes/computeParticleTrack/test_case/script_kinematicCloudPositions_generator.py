###################################################################################
# script to compute the particle positions in lagrangian flow physicis simulation #
###################################################################################

import pandas as pd
import numpy as np
from copy import copy as cp

# reading the datafile
fid = pd.read_csv("doorLocations.csv")
NX = 10; NY = 10

def planeFunction(doorName,nx,ny):
    # point definitions
    width = fid["width"][fid["doorName"]==doorName].values[0]
    height = fid["height"][fid["doorName"]==doorName].values[0]
    Xd = fid["Xd"][fid["doorName"]==doorName].values[0]
    Yd = fid["Yd"][fid["doorName"]==doorName].values[0]
    Zd = fid["Zd"][fid["doorName"]==doorName].values[0]

    Xs = fid["Xs"][fid["doorName"]==doorName].values[0] + Yd*0.1
    Ys = fid["Ys"][fid["doorName"]==doorName].values[0] - Xd*0.1
    Zs = fid["Zs"][fid["doorName"]==doorName].values[0] + Zd*0.1 + 0.001

    p1 = [Xs,Ys,Zs]
    p2 = [Xs + Xd*width + 0,
          Ys + Yd*width + 0,
          Zs + Zd*width + height]

    X = np.zeros([ny,nx]); Y = cp(X); Z = cp(X)

    xl = np.linspace(p1[0],p2[0],nx)
    yl = np.linspace(p1[1],p2[1],nx)
    zl = np.linspace(p1[2],p2[2],ny)

    for i in range(nx):
        for j in range(ny):
            X[j,i] = xl[i];
            Y[j,i] = yl[i];
            Z[j,i] = zl[j];

    return X,Y,Z

# creating cloud file
fname = "kinematicCloudPositions"
fidtxt = open(fname,"w")

# writing the file
fidtxt.writelines("/*--------------------------------*- C++ -*----------------------------------*\ \n")
fidtxt.writelines("| =========                 |                                                 | \n")
fidtxt.writelines("| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           | \n")
fidtxt.writelines("|  \\    /   O peration     | Version:  v1806                                 | \n")
fidtxt.writelines("|   \\  /    A nd           | Web:      www.OpenFOAM.com                      | \n")
fidtxt.writelines("|    \\/     M anipulation  |                                                 | \n")
fidtxt.writelines("\*---------------------------------------------------------------------------*/ \n")
fidtxt.writelines("FoamFile \n")
fidtxt.writelines("{ \n")
fidtxt.writelines("    version     2.0; \n")
fidtxt.writelines("    format      ascii; \n")
fidtxt.writelines("    class       vectorField; \n")
fidtxt.writelines("    object      particlePositions; \n")
fidtxt.writelines("} \n")
fidtxt.writelines("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * // \n")
fidtxt.writelines(" \n")
fidtxt.writelines(" \n")
fidtxt.writelines("( \n")
# going through doors
count = 0
for name in fid["doorName"]:
    X,Y,Z = planeFunction(name,NX,NY)
    fidtxt.writelines("// "+name+"\n")
    for i in range(NX):
        for j in range(NY):
            fidtxt.writelines("("+str(X[j,i])+" "+str(Y[j,i])+" "+str(Z[j,i])+") //"+str(count)+"\n")
            count += 1
fidtxt.writelines(") \n")
fidtxt.writelines(" \n")
fidtxt.writelines("// ************************************************************************* // \n")
fidtxt.writelines("\n")

print("wrote the kinematicCloudPositions file")
