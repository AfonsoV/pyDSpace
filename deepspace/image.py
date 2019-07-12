from astropy.io import fits as pyfits
from astropy import wcs as pywcs
from astropy.nddata import Cutout2D
from astropy.coordinates import SkyCoord
import astropy.units as u

class FitsImage:

    def __init__(self,filename):
        self.fname = filename
        self.data = pyfits.getdata(filename)
        self.header = pyfits.getheader(filename)
        self.wcs = pywcs.WCS(self.header)
        return

    def __str__(self):
        return f"Data from {self.fname}: image data shape {self.data.shape}"

    def __add__(self,other):
        return self.data + other

    def cutout(self,ra,dec,size,**kwargs):
        if isinstance(ra,str):
            skyPosition = SkyCoord(ra,dec,frame="icrs",unit=(u.hourangle, u.deg))
        else:
            skyPosition = SkyCoord(ra,dec,unit=u.deg,frame="icrs")
        return Cutout2D(self.data, skyPosition, size, wcs=self.wcs, **kwargs)

    
