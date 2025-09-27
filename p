FoamFile{version 2.0; format ascii; class volScalarField; location "0"; object p;}
dimensions [1 -1 -2 0 0 0 0];
internalField uniform 101325;
boundaryField
{ inlet{ type freestreamPressure; freestreamValue uniform 101325; } 
  outlet{ type inletOutlet; inletValue uniform 101325; value uniform 101325;} 
  wall{ type zeroGradient;} wedgeMin{ type wedge;} wedgeMax{ type wedge;} }
