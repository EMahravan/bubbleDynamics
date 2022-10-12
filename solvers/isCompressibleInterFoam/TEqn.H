{

    mixture.correctThermo();
    mixture.correct();
    //~ volScalarField& psi1_NonConst=const_cast<volScalarField&> (psi1);
    //~ volScalarField& psi2_NonConst=const_cast<volScalarField&> (psi2);
    //~ psi1_NonConst=alpha1*psi1+alpha2*dimensionedScalar(psi1.dimensions(),1e-13);
    //~ psi2_NonConst=alpha2*psi2+alpha1*dimensionedScalar(psi1.dimensions(),1e-13);
}

/*
{
    if(counter<50)
    {
        mass0=gSum(alpha2*rho2*mesh.V());
    }
            
    scalar mass=gSum(alpha2*rho2*mesh.V());
    
    Info<<"mass0="<<mass0<<"   mass="<<mass<<endl;
    
    const_cast<volScalarField&>(rho2)=rho2*mass0/mass;

    IOdictionary dict
    (
        IOobject
        (
            "thermophysicalProperties."+ mixture.phase2Name(),
            runTime.constant(),
            mesh,
            IOobject::MUST_READ_IF_MODIFIED,
            IOobject::NO_WRITE
        )
    );
    const dictionary& mixtureDict=dict.subDict("mixture");
    dimensionedScalar p0   (p.dimensions()   ,mixtureDict.subDict("equationOfState").lookup<scalar>("p0")   );
    dimensionedScalar rho0 (rho1.dimensions(),mixtureDict.subDict("equationOfState").lookup<scalar>("rho0") );
    dimensionedScalar gamma(dimless          ,mixtureDict.subDict("equationOfState").lookup<scalar>("gamma"));
    dimensionedScalar B    (p.dimensions()   ,mixtureDict.subDict("equationOfState").lookup<scalar>("B")    );
    
    p=alpha1*p+alpha2*((p0+B)*Foam::pow(rho2/rho0,gamma));
    p_rgh = p - rho*gh;
    p_rgh.correctBoundaryConditions();
        
    mixture.correctThermo();
    mixture.correct();
    
}
*/
