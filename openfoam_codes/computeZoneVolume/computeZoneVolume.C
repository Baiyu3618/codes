#include "fvCFD.H"
#include "meshSearch.H"

int main(int argc, char *argv[])
{
  #include "setRootCase.H"
#include "createTime.H"

  Info << "Reading Mesh .. " << nl << endl;
#include "createMesh.H"
  Info << "Done .. " << endl;

  // total timesteps present in the case
  instantList Times = runTime.times();

  #include "checkTimeOptions.H"	// this gives the startTime of computation.

  // setting the simulation time
  runTime.setTime(Times.last(),0);

  // reading U value
  volVectorField U
    (
     IOobject
     (
      "U",
      mesh.time().timeName(),
      mesh,
      IOobject::MUST_READ
      ),
     mesh
     );

  // creating output directory
  fileName outputDir = mesh.time().path()/"postProcessing";
  mkDir(outputDir);

  // create pointer
  autoPtr<OFstream> filePtr;
  filePtr.reset(new OFstream(outputDir/"zoneVolumeData.csv"));

  // writing header data
  filePtr() << "volume of zones with different velocity ranges : " << endl;

  // declaring volumeVariables
  scalar v01(0), v12(0), v23(0), v34(0), v45(0), v56(0), v6a(0), sumVolume(0);

  forAll(mesh.cells(),cellid)
    {
      // reading velocity value
      scalar vmag = mag(U[cellid]);

      sumVolume += mesh.V()[cellid];

      if (vmag >= 0 && vmag < 1)
	  v01 += mesh.V()[cellid];
      else if (vmag >= 1 && vmag < 2)
	  v12 += mesh.V()[cellid];
      else if (vmag >= 2 && vmag < 3)
	  v23 += mesh.V()[cellid];
      else if (vmag >=3 && vmag < 4)
	  v34 += mesh.V()[cellid];
      else if (vmag >= 4 && vmag < 5)
	  v45 += mesh.V()[cellid];
      else if (vmag >= 5 && vmag < 6)
	  v56 += mesh.V()[cellid];
      else if (vmag >= 6)
	  v6a += mesh.V()[cellid];
    }

  Info << nl << "zone Volume with V(0 - 1) = " << v01 << " (" << v01/gSum(mesh.V())*100.0 << "%)" << endl;
  Info << nl << "zone Volume with V(1 - 2) = " << v12 << " (" << v12/gSum(mesh.V())*100.0 << "%)" << endl;
  Info << nl << "zone Volume with V(2 - 3) = " << v23 << " (" << v23/gSum(mesh.V())*100.0 << "%)" << endl;
  Info << nl << "zone Volume with V(3 - 4) = " << v34 << " (" << v34/gSum(mesh.V())*100.0 << "%)" << endl;
  Info << nl << "zone Volume with V(4 - 5) = " << v45 << " (" << v45/gSum(mesh.V())*100.0 << "%)" << endl;
  Info << nl << "zone Volume with V(5 - 6) = " << v56 << " (" << v56/gSum(mesh.V())*100.0 << "%)" << endl;
  Info << nl << "zone Volume with V(6 and above) = " << v6a << " (" << v6a/gSum(mesh.V())*100.0 << "%)" << endl;

  Info << nl << "Sum Volume = " << sumVolume << endl;
  Info << nl << "Total Volume = " << gSum(mesh.V()) << endl;
  Info << nl << "Difference = " << sumVolume - gSum(mesh.V()) << endl;

  // writing to file
  filePtr() << nl << "zone Volume with V(0 - 1) = " << v01 << " (" << v01/gSum(mesh.V())*100.0 << "%)" << endl;
  filePtr() << nl << "zone Volume with V(1 - 2) = " << v12 << " (" << v12/gSum(mesh.V())*100.0 << "%)" << endl;
  filePtr() << nl << "zone Volume with V(2 - 3) = " << v23 << " (" << v23/gSum(mesh.V())*100.0 << "%)" << endl;
  filePtr() << nl << "zone Volume with V(3 - 4) = " << v34 << " (" << v34/gSum(mesh.V())*100.0 << "%)" << endl;
  filePtr() << nl << "zone Volume with V(4 - 5) = " << v45 << " (" << v45/gSum(mesh.V())*100.0 << "%)" << endl;
  filePtr() << nl << "zone Volume with V(5 - 6) = " << v56 << " (" << v56/gSum(mesh.V())*100.0 << "%)" << endl;
  filePtr() << nl << "zone Volume with V(6 and above) = " << v6a << " (" << v6a/gSum(mesh.V())*100.0 << "%)" << endl;
  filePtr() << nl << "Sum Volume = " << sumVolume << endl;
  filePtr() << nl << "Total Volume = " << gSum(mesh.V()) << endl;
  filePtr() << nl << "Difference = " << sumVolume - gSum(mesh.V()) << endl;

  Info << nl << "End." << endl;
}
