FoamFile
{
    version     2.0;
    format      ascii;
    class       volScalarField;
    location    "0";
    object      p;
}
dimensions      [1 -1 -2 0 0 0 0];
internalField   uniform 101325;
boundaryField
{
    inlet
    {
        type            totalPressure;
        p0              uniform 1013250; // adjust per target Mach
        gamma           1.4;
        value           uniform 101325;
    }
    farfield
    {
        type            zeroGradient;
    }
    body
    {
        type            zeroGradient;
    }
    axis
    {
        type            wedge;
    }
    symmetryPlane
    {
        type            wedge;
    }
}
