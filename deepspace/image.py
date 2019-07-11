from astropy.io import fits as pyfits
from astropy import wcs as pywcs
from astropy.nddata import Cutout2D

class FitsImage:

    def __init__(self,filename):
        self.data = pyfits.getdata(filename)
        self.header = pyfits.getheader(filename)
        self.wcs = pywcs.WCS(self.header)
        return
