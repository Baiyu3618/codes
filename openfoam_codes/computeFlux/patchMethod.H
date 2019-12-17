//////////////////////////////////////////////////
// creating coordinates based on cells on patch //
// using patch name			        //
//////////////////////////////////////////////////


// reading patch name
word patchName;
propDict.lookup("patchName") >> patchName;

// reading number of random points to be taken on patch
label nRandomPoints;
propDict.lookup("nRandomPoints") >> nRandomPoints;

// retriving patch id
label patchID(mesh.boundaryMesh().findPatchID(patchName));

// getting the cell ids
List<label> faceCells(mesh.boundary()[patchID].patch().faceCells());

// declaring chosen cells list
List<label> chosenCells;

label count(0), randNum, startCell(faceCells[0]), endCell(faceCells[faceCells.size()-1]);

bool foundFlag;

while(count < nRandomPoints)
  {
    randNum = startCell + std::rand()%(endCell - startCell + 1);

    foundFlag = false;

    for(int i = 0; i < chosenCells.size(); i++)
      {
	if(randNum == chosenCells[i])
	  {
	    foundFlag = true;
	    break;
	  }
      }

    if(foundFlag)
      continue;
    else
      {
	chosenCells.append(randNum);
	count++;
      }
  }


// assembling the cell center coordinates as particle starting points
for(int i = 0; i < chosenCells.size(); i++)
  {
    label pos(chosenCells[i]);
    particlePositions.append(mesh.C()[pos]);
  }

// reading phi field value
surfaceScalarField phi
(
 IOobject
 (
  "phi",
  mesh.time().timeName(),
  mesh,
  IOobject::MUST_READ
  ),
 mesh
 );

// determining inlet or outlet patch
if(sum(phi.boundaryField()[patchID]) < 0)
  Info << nl << "Patch: " << patchName << " is of InFlow type.. Enabling advanceTrack.." << endl;
 else
   {
     Info << nl << "Patch: " << patchName << " is of OutFlow type.. Enabling backTrack.." << endl;
     backTrackFlag = true;
   }
