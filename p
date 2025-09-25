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
    walls
    {
        type zeroGradient;
    }
    frontAndBack
    {
        type empty;
    }
    inletOutlet
    {
        type zeroGradient;
    }
}
