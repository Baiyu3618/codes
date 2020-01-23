# Fluent Mesh Reader Programme for Meshless Method computation
# type of mesh read : 2D
# B.C.s supported   : inlet,outlet,wall

import numpy as np
import matplotlib.pyplot as plt
from copy import copy as cp

# opening the mesh file
fid = open("rect_structured.msh")

# reading number of dimensions in mesh file-------------------------------------
while True:
    txt = fid.readline().split()
    if np.size(txt) != 0:
        if txt[0] == "(2":
            ND = txt[1]
            break
        else:
            continue
        if ND != "2)":
            raise RuntimeError("Only 2D Meshes are read!!")
    else:
        continue

# reading nodes section---------------------------------------------------------
while True:
    txt = fid.readline().split()
    if txt[0] == "(10" and txt[1] == "(0":
        Nstart = int(txt[2],16)
        Nnodes = int(txt[3],16)-Nstart+1
        break
    else:
        continue

# reading nodes from file-------------------------------------------------------
X = np.zeros(Nnodes, dtype = float); Y = cp(X)
while True:
    txt = fid.readline().split()
    try:
        if np.isreal(float(txt[0])):
            break
    except ValueError:
        continue
for i in range(Nnodes):
    X[i],Y[i] = float(txt[0]),float(txt[1])
    txt = fid.readline().split()

# reading faces-----------------------------------------------------------------
while True:
    if txt[0] == "(13" and txt[1] == "(0":
        Total_Nfaces = int(txt[3],16)       # total no of faces in domain
        break
    else:
        txt = fid.readline().split()

ID = list([])             # dummy zone id
N_start = list([])         # dummy face zone start node of correspondin zone id
N_end = list([])           # dummy face zone end node of correspondin zone id
Faces = np.zeros([Total_Nfaces+1,4],dtype = int) # faces array +1 for adjusting

while True:

    if txt[0] == "(39":
        break
    if txt[0] == "(13" and txt[1] != "(0":
        # assigning zone id to the list
        tmptxt = list(txt[1])
        ZoneID = int(''.join(tmptxt[1:]),16)
        # F.ID = np.array([list([F.ID]) + list([ZoneID])])
        ID = list(ID) + list([ZoneID])

        # getting Nstart and Nend face numbers and assigning variables
        Nstart = int(txt[2],16)
        Nend = int(txt[3],16)
        Nfaces = Nend - Nstart +1
        N_start = list(N_start) + list([Nstart])
        N_end = list(N_end) + list([Nend])

        # reading face values
        for i in range(Nstart,Nend+1):      # +1 is 1st index shift from 0 to 1
            txt = fid.readline().split()
            Faces[i,0] = int(txt[0],16)
            Faces[i,1] = int(txt[1],16)
            Faces[i,2] = int(txt[2],16)
            Faces[i,3] = int(txt[3],16)

        continue
    else:
        txt = fid.readline().split()
        continue

# assigning faces to correct BCs------------------------------------------------
INLET = list()
OUTLET = list()
WALL = list()
INTERIOR = list()

txt = fid.readline().split()

while True:
    if txt == []:
        break

    if txt[0] == '(39':
        tmptxt = list(txt[1])
        id = int(''.join(tmptxt[1:]),10)        # getting id from file
    else:
        txt = fid.readline().split()
        continue

    for i in range(np.max(np.shape(ID))):
        if ID[i] == id:
            tmpmat = cp(Faces[N_start[i]:N_end[i]+1,0:2])
            if txt[2] == 'wall':
                WALL = np.array(list(WALL) + list(tmpmat))
            elif txt[2] == 'interior':
                INTERIOR = np.array(list(INTERIOR) + list(tmpmat))
            elif txt[2] == 'pressure-outlet' or txt[2] == 'outlet-vent':
                OUTLET = np.array(list(OUTLET) + list(tmpmat))
            elif txt[2] == 'velocity-inlet' or txt[2] == 'pressure-inlet':
                INLET = np.array(list(INLET) + list(tmpmat))
    txt = fid.readline().split()

# removing repeated nodes on boundaries-----------------------------------------
INLET -= 1
OUTLET -= 1
WALL -= 1
INTERIOR -= 1

INODES = []
ONODES = []
WNODES = []
INTNODES = []

for i in range(np.max(np.shape(INLET))):
    if (INLET[i,0] != INLET[:,1]).all():
        INODES = np.array(list(INLET[:,1]) + list([INLET[i,0]]))
        break

for i in range(np.max(np.shape(OUTLET))):
    if (OUTLET[i,0] != OUTLET[:,1]).all():
        ONODES = np.array(list(OUTLET[:,1]) + list([OUTLET[i,0]]))
        break

for i in range(np.max(np.shape(WALL))):
    if (WALL[i,0] != WALL[:,1]).all():
        WNODES = np.array(list(WALL[:,1]) + list([WALL[i,0]]))
        break

# removing inter-occuring nodes i.e having been into interior from boundary-----
INT = list(INTERIOR[:,0]) + list(INTERIOR[:,1])
for i in range(np.max(np.shape(INT))):
    if (INT[i] == INODES).any() or (INT[i] == ONODES).any() \
        or (INT[i] == WNODES).any():
        INT[i] = np.nan             # making a mark to remove

for i in range(np.max(np.shape(INT))):
    if not(np.isnan(INT[i])) and not((INT[i] == INTNODES).any()):
        INTNODES = np.array(list(INTNODES) + list([INT[i]]))

INODES += 1             # changing indexing back from 1
ONODES += 1
WNODES += 1
INTNODES += 1

# exporting nodes to .nod files-------------------------------------------------
fi = open("INODES.nod","w")         # INODES export
Ni = np.max(np.shape(INODES))
fi.writelines("%d \n" %(Ni))
for i in INODES:
    fi.writelines("%d \n" %(i))
fi.close()

fo = open("ONODES.nod","w")         # ONODES export
No = np.max(np.shape(ONODES))
fo.writelines("%d \n" %(No))
for i in ONODES:
    fo.writelines("%d \n" %(i))
fo.close()

fw = open("WNODES.nod","w")         # WNODES export
Nw = np.max(np.shape(WNODES))
fw.writelines("%d \n" %(Nw))
for i in WNODES:
    fw.writelines("%d \n" %(i))
fw.close()

fint = open("INTNODES.nod","w")     # INTNODES export
Nint = np.max(np.shape(INTNODES))
fint.writelines("%d \n" %(Nint))
for i in INTNODES:
    fint.writelines("%d \n" %(i))
fint.close()

fpnt = open("COORD.xy","w")       # coordinate export
fpnt.writelines("%f,%f\n" %(Nnodes,0))
for i in range(Nnodes):
    fpnt.writelines("%f,%f\n" %(X[i],Y[i]))
fpnt.close()

# plotting mesh points----------------------------------------------------------
plt.plot(X[INODES-1],Y[INODES-1],'ob',label = 'inlet')
plt.plot(X[ONODES-1],Y[ONODES-1],'or', label = 'outlet')
plt.plot(X[WNODES-1],Y[WNODES-1],'og', label = 'wall')
plt.plot(X[INTNODES-1],Y[INTNODES-1],'ok', label = 'interior')
plt.axis('image'); plt.legend()
plt.show()

print("Done\n")
