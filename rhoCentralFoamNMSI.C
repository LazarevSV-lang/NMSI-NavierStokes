/*---------------------------------------------------------------------------*\
  Hypersonic compressible solver with NMSI π*, γ_diss, optional e* clamp
  Base: rhoCentralFoam (density-based, shock-capturing)
\*---------------------------------------------------------------------------*/

#include "fvCFD.H"
#include "psiThermo.H"
#include "turbulenceModel.H"
#include "fvcGrad.H"
#include "fvcDiv.H"
#include "fvcCurl.H"

#include "NMSI/PiStarForce.H"
#include "NMSI/GammaDissSource.H"

int main(int argc, char *argv[])
{
    #include "setRootCase.H"
    #include "createTime.H"
    #include "createMesh.H"

    Info<< "\nCreating thermodynamics\n" << endl;
    autoPtr<psiThermo> pThermo(psiThermo::New(mesh));
    psiThermo& thermo = pThermo();
    volScalarField& p = thermo.p();
    volScalarField& T = thermo.T();
    volScalarField& rho = thermo.rho();

    Info<< "Creating fields\n" << endl;
    volVectorField U
    (
        IOobject("U", runTime.timeName(), mesh, IOobject::MUST_READ, IOobject::AUTO_WRITE),
        mesh
    );

    surfaceScalarField phi
    (
        IOobject("phi", runTime.timeName(), mesh, IOobject::READ_IF_PRESENT, IOobject::AUTO_WRITE),
        linearInterpolate(rho*U) & mesh.Sf()
    );

    #include "createFields.H" // optional extras for central schemes if needed

    // Read NMSI dictionary
    IOdictionary NMSIProps
    (
        IOobject("NMSIProperties", runTime.system(), mesh, IOobject::MUST_READ_IF_MODIFIED, IOobject::NO_WRITE)
    );

    // Build NMSI operators
    PiStarForce piStar(mesh, U, rho, NMSIProps);
    GammaDissSource gammaDiss(mesh, U, rho, NMSIProps);

    // e* clamp?
    const dictionary& NMSI = NMSIProps.subDict("NMSI");
    const dictionary& eClampDict = NMSI.subDict("expClamp");
    const bool eActive = eClampDict.lookupOrDefault<bool>("active", true);
    const scalar lambda = eClampDict.lookupOrDefault<scalar>("lambda", 0.35);
    const scalar alpha  = eClampDict.lookupOrDefault<scalar>("alpha", 0.20);

    Info<< "\nStarting time loop\n" << endl;
    while (runTime.loop())
    {
        // Flux update (very simplified sketch; adapt to your central scheme template)
        phi = linearInterpolate(rho*U) & mesh.Sf();

        // Momentum equation
        fvMatrix<vector> UEqn
        (
            fvm::ddt(rho, U) // + convective + viscous terms as in rhoCentralFoam
        );

        // Add NMSI sources
        piStar.addMomentumSource(phi, UEqn);
        gammaDiss.addMomentumSource(phi, UEqn);

        if (eActive)
        {
            const scalar t = runTime.value();
            const scalar Le = lambda*exp(-alpha*t);
            UEqn.source() -= rho * (Le) * U;
        }

        UEqn.solve();

        // Update thermodynamics, pressure, etc. (use the appropriate central scheme updates)
        // Placeholder:
        p.correctBoundaryConditions();
        T.correctBoundaryConditions();

        runTime.write();
    }

    Info<< "End\n" << endl;
    return 0;
}
