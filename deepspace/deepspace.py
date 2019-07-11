import glob

from astropy.table import Table
from astropy.coordinates import SkyCoord

from .info import DeepSpaceInfo
from .errors import deepspaceError
from .image import FitsImage


class DeepSpaceData:

    def __init__(self):
        self.info = DeepSpaceInfo()
        return

    def load_photometry_catalog(self,cluster):
        self.info.verify_cluster(cluster)
        fileAscii = glob.glob(f"{DataFolder}/{cluster}*/*.cat")
        return Table.read(fileAscii[0],format="ascii")

    def load_eazy_catalog(self,cluster):
        self.info.verify_cluster(cluster)
        fileAscii = glob.glob(f"{DataFolder}/{cluster}*/eazy/*/*.zout")
        return Table.read(fileAscii[0],format="ascii")

    def load_fast_catalog(self,cluster):
        self.info.verify_cluster(cluster)
        fileAscii = glob.glob(f"{DataFolder}/{cluster}*/fast/*/*.fout")
        return Table.read(fileAscii[0],format="ascii")

    def load_filter(self,cluster,filter,mode="bcgs_out",img="drz"):
        if filter == "detection":
            self.info.verify_cluster(cluster)
            fdescr = f"{DataFolder}/{cluster}*/images/detection/*detection.fits.gz"
            dataFile =  glob.glob(fdescr)
        else:
            self.info.verify_filter(cluster,filter)
            fdescr = f"{DataFolder}/{cluster}*/images/{mode}/*{filter}*{img}*.fits.gz"
            dataFile =  glob.glob(fdescr)
            if len(dataFile)>1:
                print(f"Warning, more than one file matching descriptor {fdescr}. {dataFile}")
        return FitsImage(dataFile[0])

    def load_PSF(self,cluster,filter):
        self.info.verify_filter(cluster,filter)
        fdescr = f"{DataFolder}/{cluster}*/star_psfs/*{filter}*.fits.gz"
        dataFile =  glob.glob(fdescr)
        return FitsImage(dataFile[0])

    def load_segmentation(self,cluster):
        self.info.verify_cluster(cluster)
        fdescr = f"{DataFolder}/{cluster}*/photometry/*detection_seg.fits.gz"
        dataFile =  glob.glob(fdescr)
        return FitsImage(dataFile[0])

        
