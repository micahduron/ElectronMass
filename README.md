# ElectronMass

This is a script that calculates the mass of an electron given
experimental data collected from the emission spectra of
Hydrogen and Mercury. In addition to calculating the mass,
this script also calculates the total experimental error
of the mass calculation.

This script was written for my General Physics III course
in community college.

## How it works

The mass calculation involves plugging the collected values
into derived equations. The experimental error is calculated
via standard propagation of errors, for which each partial
derivative of the mass function must be known. A numerical
differentiation technique is used to calculate these derivatives.

## License

MIT License
