"""
    Script that measures all possible 2- and 3-PCF of shear and intrinsic ellipticity for MICE galaxies
"""
from file_loader import file_loader
import treecorr


def measureAllCorrFunc(dir, files, min_sep=2, max_sep=100, nbins=10, nubins=10, nvbins=10):
    # File loader
    loader=file_loader()


    # Go through all files
    for file in files:

        print("Working on ", file)
        # Read in
        path=dir+file
        Xs, Ys, shears1, shears2, eps1, eps2 = loader.read_gamma(path)

        print("Finished read in")

        # Create Catalogs
        shear_cat=treecorr.Catalog(x=Xs, y=Ys, g1=shears1, g2=shears2, x_units="arcmin", y_units="arcmin")
        eps_cat=treecorr.Catalog(x=Xs, y=Ys, g1=eps1, g2=eps2, x_units="arcmin", y_units="arcmin")

        # Treecorr correlation calculators
        TwoPoint=treecorr.GGCorrelation(min_sep=min_sep, max_sep=max_sep, nbins=nbins, sep_units='arcmin')
        ThreePoint=treecorr.GGGCorrelation(min_sep=min_sep, max_sep=max_sep, nbins=nbins, nubins=nubins, nvbins=nvbins, sep_units='arcmin')


        # Shear-Shear
        print("Starting Shear-Shear Correlation")

        TwoPoint.process(shear_cat)
        fn=dir+file[:-5]+"_GG.dat"
        TwoPoint.write(fn)
        print("Finished Shear-Shear Correlation")

        # Int-Int
        print("Starting Eps-Eps Correlation")

        TwoPoint.process(eps_cat)
        fn=dir+file[:-5]+"_II.dat"

        TwoPoint.write(dir+file[:-5]+"_II.dat")
        print("Finished Eps-Eps Correlation")


        # Shear-Int
        print("Starting Shear-Eps Correlation")

        TwoPoint.process(shear_cat, eps_cat)
        fn=dir+file[:-5]+"_GI.dat"

        TwoPoint.write(dir+file[:-5]+"_GI.dat")
        print("Finished Shear-Eps Correlation")


        # Shear-Shear-Shear
        print("Starting Shear-Shear-Shear Correlation")

        ThreePoint.process(shear_cat)
        fn=dir+file[:-5]+"_GGG.dat"

        ThreePoint.write(dir+file[:-5]+"_GGG.dat")

        print("Finished Shear-Shear-Shear Correlation")

        # Shear-Int-Int
        print("Starting Shear-Eps-Eps Correlation")

        ThreePoint.process(shear_cat, eps_cat)
        fn=dir+file[:-5]+"_GII.dat"

        ThreePoint.write(dir+file[:-5]+"_GII.dat")

        print("Finished Shear-Eps-Eps Correlation")

        # Shear-Shear-Int
        print("Starting Shear-Shear-Eps Correlation")

        ThreePoint.process(eps_cat, shear_cat)
        fn=dir+file[:-5]+"_GGI.dat"

        ThreePoint.write(dir+file[:-5]+"_GGI.dat")
        print("Finished Shear-Shear-Eps Correlation")


        # Int-Int-Int
        print("Starting Eps-Eps-Eps Correlation")

        ThreePoint.process(eps_cat)
        fn=dir+file[:-5]+"_III.dat"

        ThreePoint.write(dir+file[:-5]+"_III.dat")

        print("Finished Eps-Eps-Eps Correlation")

    print("All done!")