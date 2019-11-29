
//Info<< "Reading/calculating face flux field phi\n" << endl;


IOobject testPhi(
		 "phi",
		 procDBs[procI].timeName(),
		 procMesh,
		 IOobject::NO_READ,
		 IOobject::NO_WRITE
		 );

if(!exists(testPhi.objectPath()) && !exists(testPhi.objectPath()+".gz")) {
  Info << "No phi for Time = " << runTime.timeName() << " -> Skipping\n" << endl; 
  continue;
 }

surfaceScalarField phi
(
    IOobject
    (
        "phi",
        procDBs[procI].timeName(),
        procMesh,
        IOobject::READ_IF_PRESENT
    ),
    procMesh
);

