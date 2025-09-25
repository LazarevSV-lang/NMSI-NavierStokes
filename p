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
        p0              uniform 101325;
        gamma           1.4;
        value           uniform 101325;
    }
    outlet
    {
        type            fixedValue;
        value           uniform 101325;
    }
    plate
    {
        type            zeroGradient;
    }
    farfield
    {
        type            zeroGradient;
    }
    frontAndBack
    {
        type            empty;
    }
}
