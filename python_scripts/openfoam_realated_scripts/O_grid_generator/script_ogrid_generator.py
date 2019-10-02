#########################################
# O-grid blockMeshDict generator script #
# developed by Ramkumar                 #
#########################################

import numpy as np

""" Plane of work is X-Y only for now """

# input parameters
op = [0,0,0]        # origin point x y z
ri = 0.015             # inner radius
ro = 0.045             # outer radius
t = 0.001              # thickness of mesh in z direction
bc = [10,10,1]         # cell count in radial, azimuthal and z directions

# custom lambda function definition
cos = lambda x: np.cos(np.deg2rad(x))
sin = lambda x: np.sin(np.deg2rad(x))

# creating coordinate points
X = []; Y = []; Z = []

X.append(ri*cos(45)+op[0]); Y.append(ri*sin(45)+op[1]); Z.append( t/2 +op[2]) # 1
X.append(ro*cos(45)+op[0]); Y.append(ro*sin(45)+op[1]); Z.append( t/2 +op[2]) # 2
X.append(ro*cos(45)+op[0]); Y.append(ro*sin(45)+op[1]); Z.append(-t/2 +op[2]) # 3
X.append(ri*cos(45)+op[0]); Y.append(ri*sin(45)+op[1]); Z.append(-t/2 +op[2]) # 4

X.append(ri*cos(-45)+op[0]); Y.append(ri*sin(-45)+op[1]); Z.append( t/2 +op[2]) # 5
X.append(ro*cos(-45)+op[0]); Y.append(ro*sin(-45)+op[1]); Z.append( t/2 +op[2]) # 6
X.append(ro*cos(-45)+op[0]); Y.append(ro*sin(-45)+op[1]); Z.append(-t/2 +op[2]) # 7
X.append(ri*cos(-45)+op[0]); Y.append(ri*sin(-45)+op[1]); Z.append(-t/2 +op[2]) # 8

X.append(ri*cos(-135)+op[0]); Y.append(ri*sin(-135)+op[1]); Z.append( t/2+op[2]) # 9
X.append(ro*cos(-135)+op[0]); Y.append(ro*sin(-135)+op[1]); Z.append( t/2+op[2]) # 10
X.append(ro*cos(-135)+op[0]); Y.append(ro*sin(-135)+op[1]); Z.append(-t/2+op[2]) # 11
X.append(ri*cos(-135)+op[0]); Y.append(ri*sin(-135)+op[1]); Z.append(-t/2+op[2]) # 12

X.append(ri*cos(135)+op[0]); Y.append(ri*sin(135)+op[1]); Z.append( t/2+op[2]) # 13
X.append(ro*cos(135)+op[0]); Y.append(ro*sin(135)+op[1]); Z.append( t/2+op[2]) # 14
X.append(ro*cos(135)+op[0]); Y.append(ro*sin(135)+op[1]); Z.append(-t/2+op[2]) # 15
X.append(ri*cos(135)+op[0]); Y.append(ri*sin(135)+op[1]); Z.append(-t/2+op[2]) # 16

# creating blockMeshDict File
fid = open("blockMeshDict","w")

fid.writelines("/*--------------------------------*- C++ -*----------------------------------*\\n")
fid.writelines("| =========                 |                                                 |\n")
fid.writelines("| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |\n")
fid.writelines("|  \\    /   O peration     | Version:  v1806                                 |\n")
fid.writelines("|   \\  /    A nd           | Web:      www.OpenFOAM.com                      |\n")
fid.writelines("|    \\/     M anipulation  |                                                 |\n")
fid.writelines("\*---------------------------------------------------------------------------*/\n")
fid.writelines("FoamFile\n")
fid.writelines("{\n")
fid.writelines("    version     2.0;\n")
fid.writelines("    format      ascii;\n")
fid.writelines("    class       dictionary;\n")
fid.writelines("    object      blockMeshDict;\n")
fid.writelines("}\n")
fid.writelines("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n")
fid.writelines("\n")
fid.writelines("scale   1;\n")
fid.writelines("\n")
fid.writelines("vertices\n")
fid.writelines("(\n")
fid.writelines(" name v1 ("+str(X[0])+" "+str(Y[0])+" "+str(Z[0])+")\n")
fid.writelines(" name v2 ("+str(X[1])+" "+str(Y[1])+" "+str(Z[1])+")\n")
fid.writelines(" name v3 ("+str(X[2])+" "+str(Y[2])+" "+str(Z[2])+")\n")
fid.writelines(" name v4 ("+str(X[3])+" "+str(Y[3])+" "+str(Z[3])+")\n")
fid.writelines("\n")
fid.writelines(" name v5 ("+str(X[4])+" "+str(Y[4])+" "+str(Z[4])+")\n")
fid.writelines(" name v6 ("+str(X[5])+" "+str(Y[5])+" "+str(Z[5])+")\n")
fid.writelines(" name v7 ("+str(X[6])+" "+str(Y[6])+" "+str(Z[6])+")\n")
fid.writelines(" name v8 ("+str(X[7])+" "+str(Y[7])+" "+str(Z[7])+")\n")
fid.writelines("\n")
fid.writelines(" name v9 ("+str(X[8])+" "+str(Y[8])+" "+str(Z[8])+")\n")
fid.writelines(" name v10 ("+str(X[9])+" "+str(Y[9])+" "+str(Z[9])+")\n")
fid.writelines(" name v11 ("+str(X[10])+" "+str(Y[10])+" "+str(Z[10])+")\n")
fid.writelines(" name v12 ("+str(X[11])+" "+str(Y[11])+" "+str(Z[11])+")\n")
fid.writelines("\n")
fid.writelines(" name v13 ("+str(X[12])+" "+str(Y[12])+" "+str(Z[12])+")\n")
fid.writelines(" name v14 ("+str(X[13])+" "+str(Y[13])+" "+str(Z[13])+")\n")
fid.writelines(" name v15 ("+str(X[14])+" "+str(Y[14])+" "+str(Z[14])+")\n")
fid.writelines(" name v16 ("+str(X[15])+" "+str(Y[15])+" "+str(Z[15])+")\n")
fid.writelines(");\n")
fid.writelines("\n")
fid.writelines("blocks\n")
fid.writelines("(\n")
fid.writelines("    hex (v1 v4 v3 v2 v5 v8 v7 v6) movingZone ("+str(bc[2])+" "+str(bc[0])+" "+str(bc[1])+") simpleGrading (1 1 1)\n")
fid.writelines("    hex (v5 v8 v7 v6 v9 v12 v11 v10) movingZone ("+str(bc[2])+" "+str(bc[0])+" "+str(bc[1])+") simpleGrading (1 1 1)\n")
fid.writelines("    hex (v9 v12 v11 v10 v13 v16 v15 v14) movingZone ("+str(bc[2])+" "+str(bc[0])+" "+str(bc[1])+") simpleGrading (1 1 1)\n")
fid.writelines("    hex (v13 v16 v15 v14 v1 v4 v3 v2) movingZone ("+str(bc[2])+" "+str(bc[0])+" "+str(bc[1])+") simpleGrading (1 1 1)\n")
fid.writelines(");\n")
fid.writelines("\n")
fid.writelines("edges\n")
fid.writelines("(\n")
fid.writelines(" arc v1 v5 ("+str(op[0]+ri)+" 0 "+str(op[2]+t/2)+")\n")
fid.writelines(" arc v4 v8 ("+str(op[0]+ri)+" 0 "+str(op[2]-t/2)+")\n")
fid.writelines("\n")
fid.writelines(" arc v2 v6 ("+str(op[0]+ro)+" 0 "+str(op[2]+t/2)+")\n")
fid.writelines(" arc v7 v3 ("+str(op[0]+ro)+" 0 "+str(op[2]-t/2)+")\n")
fid.writelines("\n")
fid.writelines(" arc v5 v9 (0 "+str(op[1]-ri)+" "+str(op[2]+t/2)+")\n")
fid.writelines(" arc v8 v12 (0 "+str(op[1]-ri)+" "+str(op[2]-t/2)+")\n")
fid.writelines("\n")
fid.writelines(" arc v6 v10 (0 "+str(op[1]-ro)+" "+str(op[2]+t/2)+")\n")
fid.writelines(" arc v7 v11 (0 "+str(op[1]-ro)+" "+str(op[2]-t/2)+")\n")
fid.writelines("\n")
fid.writelines(" arc v13 v9 ("+str(op[0]-ri)+" 0 "+str(op[2]+t/2)+")\n")
fid.writelines(" arc v16 v12 ("+str(op[0]-ri)+" 0 "+str(op[2]-t/2)+")\n")
fid.writelines("\n")
fid.writelines(" arc v10 v14 ("+str(op[0]-ro)+" 0 "+str(op[2]+t/2)+")\n")
fid.writelines(" arc v11 v15 ("+str(op[0]-ro)+" 0 "+str(op[2]-t/2)+")\n")
fid.writelines("\n")
fid.writelines(" arc v14 v2 (0 "+str(op[1]+ro)+" "+str(op[2]+t/2)+")\n")
fid.writelines(" arc v3 v15 (0 "+str(op[1]+ro)+" "+str(op[2]-t/2)+")\n")
fid.writelines("\n")
fid.writelines(" arc v1 v13 (0 "+str(op[1]+ri)+" "+str(op[2]+t/2)+")\n")
fid.writelines(" arc v4 v16 (0 "+str(op[1]+ri)+" "+str(op[2]-t/2)+")\n")
fid.writelines(");\n")
fid.writelines("\n")
fid.writelines("defaultPatch\n")
fid.writelines("{\n")
fid.writelines("  type wall;\n")
fid.writelines("  name innerCylinder;\n")
fid.writelines("}\n")
fid.writelines("\n")
fid.writelines("boundary\n")
fid.writelines("(\n")
fid.writelines(" frontCylinder\n")
fid.writelines(" {\n")
fid.writelines("   type empty;\n")
fid.writelines("   faces\n")
fid.writelines("     (\n")
fid.writelines("      (v13 v14 v2 v1)\n")
fid.writelines("      (v1 v2 v6 v5)\n")
fid.writelines("      (v5 v6 v10 v9)\n")
fid.writelines("      (v9 v10 v14 v13)\n")
fid.writelines("      );\n")
fid.writelines(" }\n")
fid.writelines("\n")
fid.writelines(" backCylinder\n")
fid.writelines(" {\n")
fid.writelines("   type empty;\n")
fid.writelines("   faces\n")
fid.writelines("     (\n")
fid.writelines("      (v16 v15 v3 v4)\n")
fid.writelines("      (v4 v3 v7 v8)\n")
fid.writelines("      (v8 v7 v11 v12)\n")
fid.writelines("      (v12 v11 v15 v16)\n")
fid.writelines("      );\n")
fid.writelines(" }\n")
fid.writelines("\n")
fid.writelines(" oversetCylinder\n")
fid.writelines(" {\n")
fid.writelines("   type overset;\n")
fid.writelines("   faces\n")
fid.writelines("     (\n")
fid.writelines("      (v14 v15 v3 v2)\n")
fid.writelines("      (v2 v3 v7 v6)\n")
fid.writelines("      (v6 v7 v11 v10)\n")
fid.writelines("      (v10 v11 v15 v14)\n")
fid.writelines("      );\n")
fid.writelines(" }\n")
fid.writelines(");\n")
fid.writelines("\n")
fid.writelines("// ************************************************************************* //\n")

fid.close()

print("\n total cell count : "+str(bc[0]*bc[1]*bc[2]*4))
print("blockMeshDict file written successfully .. ")
