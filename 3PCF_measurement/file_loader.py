import numpy as np
from astropy.io import fits
import sys

class file_loader:
    """ class for reading in galaxy files and ellipticities from MICE in FITS format

        TODO: implement other filetypes, e.g. parquet
    """
    def __init__(self, filetype="FITS"):
        """Constructor of class
        Args:
            filetype (str, optional): What kind of file is read in. Currently only "FITS" implemented.
        """
        self.filetype=filetype

        
    def read_gamma(self, filename):
        """Reads in a MICE galaxy catalog and gives out shears and ellipticity, flipped to be used with treecorr

        Args:
            filename (str): Path to file

        Returns:
            Xs, Ys, shears1, shears2, eps_int1, eps_int2: Positions [arcmin], shear, and intrinsic ellipticites as np.arrays
        """
        if self.filetype=="FITS":
            hdul=fits.open(filename)
            data=hdul[1].data
            Xs = data['ra_gal']*60
            Ys = data['dec_gal']*60
            ## Following flips are to get shears/ellipticities consistent with Treecorr!
            shears1 = data['gamma1']
            shears2 = -data['gamma2']
            eps_int1 = -data['eps1_gal']
            eps_int2 = data['eps2_gal']
        else:
            sys.exit("file_loader: filetype "+self.filetype+" not implemented. Possible values: FITS")

        return Xs,Ys,shears1,shears2, eps_int1, eps_int2
