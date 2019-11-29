/*---------------------------------------------------------------------------*\
 =========                   |
 \\      /   F ield          | OpenFOAM: The Open Source CFD Toolbox
  \\    /    O peration      |
   \\  /     A nd            | Copyright (C) 1991-2005 OpenCFD Ltd.
    \\/      M anipulation   |
-------------------------------------------------------------------------------
License
    This file is part of OpenFOAM.

    OpenFOAM is free software; you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation; either version 2 of the License, or (at your
    option) any later version.

    OpenFOAM is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License
    along with OpenFOAM; if not, write to the Free Software Foundation,
    Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

Application
    calcMassFlow

Description
    calculates Massflow through selected face sets and boundary patches

\*---------------------------------------------------------------------------*/

/**
 * Basic OpenFOAM Finite Volume CFD Library
 */
#include "fvCFD.H"

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
// Main program:

int main(int argc, char *argv[])
{
#   include "addTimeOptions.H"

#   include "setRootCase.H"
#   include "createTime.H"
#   include "createMesh.H"

    /**
     * IODictionary: calcMassFlowDict
     * Purpose: Parameters and settings dictionary for Mass Flow calculations
     */
	IOdictionary calcMassFlowDict
    (
        IOobject
        (
            "calcMassFlowDict",
            runTime.system(),
            mesh,
            IOobject::MUST_READ,
            IOobject::NO_WRITE
        )
    );

	/**
	 * Word list for the names of the patches to consider
	 */
    const wordList bcNames(calcMassFlowDict.lookup("patchNames"));

    /**
     * Density of the medium used for the simulation
     */
    dimensionedScalar rho=dimensionedScalar("noRho",dimensionSet(0,0,0,0,0,0,0),1);

    /** 
     * Reset the density to the value specified in the dictionary
     */
    if(calcMassFlowDict.found("rho")) 
    {
      dimensionedScalar tmp=dimensionedScalar(calcMassFlowDict.lookup("rho"));
      rho.value()=tmp.value();
      rho.dimensions().reset(tmp.dimensions());

      Info << "Reseting rho to " << rho << " (Assuming incompressible case)\n" << endl;
    }

    /** 
     * Scaling factor used to convert the mass flow to relevant units
     */
    scalar scaleFactor=1;
    if(calcMassFlowDict.found("scaleFactor")) 
    {
        scaleFactor=readScalar(calcMassFlowDict.lookup("scaleFactor"));
    }

    /**
     * Check if the case in question is a parallel one
     */
    Info << "Checking for multiple processor directories...." << endl;

    int nProcs = 0;
    PtrList<Time> procDBs;

    while
    (
       exists
       ( args.rootPath()
         / args.caseName()
         / fileName(word("processor") + name(nProcs))
       )
    )
    {
       nProcs++;
    }

    if(nProcs > 0)
    {
       Info << "Number of processor directories found: " << nProcs << endl << endl;

       // Create a separate database for each processor
       procDBs.setSize(nProcs);

       forAll (procDBs,procI)
       {
          Info << "Creating database: "
               << args.caseName()/fileName(word("processor") + name(procI))
               << endl;

          procDBs.set
          (
             procI,
             new Time
             (
                Time::controlDictName,
                args.rootPath(),
                args.caseName()/fileName(word("processor") + name(procI))
             )
          );
       }
       Info << endl;
    }
    else
    {
       Info << "No processor directories found" << endl << endl;
       nProcs = 1;

       procDBs.setSize(1);
       forAll (procDBs,procI)
       {
          procDBs.set
          (
             procI,
             new Time
             (
                 Time::controlDictName,
                 args.rootPath(),
                 args.caseName()
             )
          );
       }
    }

    // Get times list
    instantList Times = procDBs[0].times();

    // set startTime and endTime depending on -time and -latestTime options
#   include "checkTimeOptions.H"

    for (label i=startTime; i<endTime; i++)
    {
        forAll(procDBs,procI)
        {
           procDBs[procI].setTime(Times[i],i);
        }

        Info<< "Time = " << procDBs[0].timeName() << endl << endl;

        forAll(bcNames,bcI)
        {
           scalar flux=0;
           scalar fluxFound = 0;
           bool fluxOK = true;

           // Cycle through each processor database
           forAll(procDBs,procI)
           {
              // Create the mesh for the current processor
              fvMesh procMesh
              (
                 IOobject
                 (
                    fvMesh::defaultRegion,
                    procDBs[procI].timeName(),
                    procDBs[procI]
                 )
              );

#             include "createPhi.H"

              label patchIndex=procMesh.boundaryMesh().findPatchID(bcNames[bcI]);

              if ((patchIndex >= 0) && (phi.boundaryField()[patchIndex].size())) 
              {
                 flux += gSum(phi.boundaryField()[patchIndex]);
                 fluxFound++;
              }
           }

           if(fluxFound == 0)
           {
              Info << "Error....Patch: " << bcNames[bcI] << " not found!" << endl;
              fluxOK = false;
           }
           else
           {
              Info << "Patch: " << bcNames[bcI] << " found on " 
                   << fluxFound << "/" << nProcs << " processor(s)" 
                   << endl;
              fluxOK = true;
           }

           scalar fluxOut = scaleFactor * flux * rho.value();

           if(fluxOK)
           {
			  if(rho.value() > 1.0)
			  {
			     Info << "Massflow at "<< bcNames[bcI]
                      << " = " << fluxOut << "kg/s"
                      << endl;
              }
              else
              {			  
                 Info << "Flux at "<< bcNames[bcI] 
                      << " = " << fluxOut << "m^3/s [" 
                      << fluxOut*60000 << " l/min]" 
                      << endl;
			  }
           }
        }
        Info << endl;
    }

    Info << "End\n" << endl;

    return 0;
}


// ************************************************************************* //
