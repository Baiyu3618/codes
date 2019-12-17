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

  // creating output directory
  fileName outputDir = mesh.time().path()/"postProcessing";
  mkDir(outputDir);

  // create pointer
  autoPtr<OFstream> filePtr;
  filePtr.reset(new OFstream(outputDir/"fluxData.csv"));

  // writing header data
  filePtr() << "patchName, flux value" << endl;

  // computing total flux per boundary
  word patchName;
  scalar flux(0), globalFlux(0);

  forAll(mesh.boundaryMesh(), patchID)
    {
      // getting patch name
      patchName = mesh.boundary()[patchID].name();

      // setting flux
      flux = sum(phi.boundaryField()[patchID]);
      globalFlux += flux;

      // writing data to file
      filePtr() << patchName << ", " << flux << endl;

      // outputing the display
      Info << nl << "Patch : " << patchName << "; Flux value : " << flux << endl;
    }

  Info << nl << "Global continuity value : " << globalFlux << endl;

  filePtr() << "Global continuity value :, " << globalFlux << endl;

  Info << nl << "End." << endl;
}
