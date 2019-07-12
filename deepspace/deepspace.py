import glob

from astropy.table import Table

from .info import DeepSpaceInfo, DataFolder
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
        self.info.verify_mode(mode)
        if filter == "detection":
            self.info.verify_cluster(cluster)
            fdescr = f"{DataFolder}/{cluster}*/images/detection/*detection.fits*"
            dataFile =  glob.glob(fdescr)
        else:
            self.info.verify_filter(cluster,filter)
            fdescr = f"{DataFolder}/{cluster}*/images/{mode}/*{filter}*{img}*.fits*"
            dataFile =  glob.glob(fdescr)
            if len(dataFile)>1:
                print(f"Warning, more than one file matching descriptor {fdescr}. {dataFile}")
        return FitsImage(dataFile[0])

    def load_PSF(self,cluster,filter):
        self.info.verify_filter(cluster,filter)
        fdescr = f"{DataFolder}/{cluster}*/star_psfs/*{filter}*.fits*"
        dataFile =  glob.glob(fdescr)
        return FitsImage(dataFile[0])

    def load_segmentation(self,cluster):
        self.info.verify_cluster(cluster)
        fdescr = f"{DataFolder}/{cluster}*/photometry/*detection_seg.fits*"
        dataFile =  glob.glob(fdescr)
        return FitsImage(dataFile[0])

    def load_cutouts(self,ra,dec,size,filters,mode="bcgs_out",img="drz",segmentation=False,**kwargs):
        data = {}
        if isinstance(filters,str):
            filters = [filters]
        cluster = self.info.get_cluster_from_coords(ra,dec)
        if segmentation is True:
            imageData = self.load_segmentation(cluster)
            data["seg"] = imageData.cutout(ra,dec,size,**kwargs)

        if filters is None and segmentation is True:
            return data
        elif filters is not None:
            for fltr in filters:
                imageData = self.load_filter(cluster,fltr,mode=mode,img=img)
                data[fltr] =  imageData.cutout(ra,dec,size,**kwargs)
        else:
            raise deepspaceError("Either a set of filters must be provided, ot the segmentaion keyword must be set to True.")
        return data

    def load_all_data_cutout(self,ra,dec,size,mode="bcgs_out",img="drz",**kwargs):
        cluster = self.info.get_cluster_from_coords(ra,dec)
        fullData = {"img":{},"psf":{}}
        imageData = self.load_segmentation(cluster)
        fullData["seg"] = imageData.cutout(ra,dec,size,**kwargs)
        for fltr in self.info.availableFilters[cluster]:
            imageData = self.load_filter(cluster,fltr,mode=mode,img=img)
            fullData["img"][fltr] = imageData.cutout(ra,dec,size,**kwargs)
            fullData["psf"][fltr] = self.load_PSF(cluster,fltr)

        imageData = self.load_filter(cluster,"detection")
        fullData["img"]["det"] = imageData.cutout(ra,dec,size,**kwargs)
        return fullData
