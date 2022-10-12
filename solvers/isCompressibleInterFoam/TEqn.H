{

    mixture.correctThermo();
    mixture.correct();
    //~ volScalarField& psi1_NonConst=const_cast<volScalarField&> (psi1);
    //~ volScalarField& psi2_NonConst=const_cast<volScalarField&> (psi2);
    //~ psi1_NonConst=alpha1*psi1+alpha2*dimensionedScalar(psi1.dimensions(),1e-13);
    //~ psi2_NonConst=alpha2*psi2+alpha1*dimensionedScalar(psi1.dimensions(),1e-13);
}
