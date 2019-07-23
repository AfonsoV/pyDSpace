import glob

from astropy.table import Table
import matplotlib.pyplot as mpl
import numpy as np

from .info import DeepSpaceInfo, DataFolder
from .errors import deepspaceError
from .image import FitsImage
from .plot import plot_cross


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
        if filter == "det":
            self.info.verify_cluster(cluster)
            fdescr = f"{DataFolder}/{cluster}*/images/detection/*detection.fits*"
            dataFile =  glob.glob(fdescr)
        elif filter == "seg":
            self.info.verify_cluster(cluster)
            fdescr = f"{DataFolder}/{cluster}*/photometry/*detection_seg.fits*"
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

    def load_cutouts(self,ra,dec,size,filters,mode="bcgs_out",img="drz",**kwargs):
        data = {}
        if isinstance(filters,str):
            filters = [filters]
        cluster = self.info.get_cluster_from_coords(ra,dec)

        if filters is not None:
            for fltr in filters:
                imageData = self.load_filter(cluster,fltr,mode=mode,img=img)
                data[fltr] =  imageData.cutout(ra,dec,size,**kwargs)
        else:
            raise deepspaceError("A set of filters must be provided.")
        return data

    def load_all_data_cutouts(self,ra,dec,size,mode="bcgs_out",img="drz",**kwargs):
        cluster = self.info.get_cluster_from_coords(ra,dec)
        fullData = {"img":{},"psf":{}}
        imageData = self.load_segmentation(cluster)
        fullData["img"]["seg"] = imageData.cutout(ra,dec,size,**kwargs)
        for fltr in self.info.availableFilters[cluster]:
            imageData = self.load_filter(cluster,fltr,mode=mode,img=img)
            fullData["img"][fltr] = imageData.cutout(ra,dec,size,**kwargs)
            fullData["psf"][fltr] = self.load_PSF(cluster,fltr)

        imageData = self.load_filter(cluster,"det")
        fullData["img"]["det"] = imageData.cutout(ra,dec,size,**kwargs)
        return fullData

    def display_dict(self,dict,draw_cross=False,draw_cross_params={},\
                     imshow_params={}):
        fig = mpl.figure(figsize=(4*len(dict),5))

        axplaces = np.linspace(0.05,0.95,len(dict)+1)
        ax_width = axplaces[1]-axplaces[0]

        i=0
        ax = []
        sorted_filters = sorted(dict.keys(),key = self.info.sort_filters)
        for fltr in sorted_filters:
            cutout = dict[fltr]
            if i ==0:
                ax0 = fig.add_axes([0.05+i*ax_width,0.05,ax_width,0.9])#,\
                                    # projection = cutout.wcs)
                # projection = cutout.wcs causes a weird offset
                ax.append(ax0)
            else:
                axi = fig.add_axes([0.05+i*ax_width,0.05,ax_width,0.9])#,\
                                    # sharex=ax0,sharey=ax0,\
                                    # projection = cutout.wcs)
                ax.append(axi)

            if fltr == "seg":
                vlims = (0,1)
            else:
                vlims = np.percentile(cutout.data,[1,99])


            ax[i].imshow(cutout.data, vmin=vlims[0], vmax=vlims[1],**imshow_params)

            if draw_cross is True:
                print(draw_cross_params)
                plot_cross(ax[i],**draw_cross_params)

            ax[i].set_title(fltr,fontsize=12+0.3*len(dict))
            if i>0:
            #     ax[i].coords[1].set_ticklabel_visible(False) # works for wcs projection
                ax[i].tick_params(labelleft=False)
            i+=1

        # ax0.set_ylabel(r"DEC [J2000]")# works for wcs projection
        ax0.set_ylabel(r"$\Delta$DEC [${}^{\prime\prime}$]",fontsize=14+0.3*len(dict))
        fig.text(0.5,0.05,r"$\Delta$RA [${}^{\prime\prime}$]",fontsize=14+0.3*len(dict))
        return fig,np.asarray(ax)

    def _set_extent(self,size):
        if isinstance(size,float):
            return (-size/2,+size/2,-size/2,+size/2)
        else:
            return (-size.value/2,+size.value/2,-size.value/2,+size.value/2)

    def display_cutouts(self,ra,dec,size,filters,mode="bcgs_out",img="drz",\
                        draw_cross=False,draw_cross_params={},imshow_params={},\
                        **kwargs):

        cluster = self.info.get_cluster_from_coords(ra,dec)
        data = self.load_cutouts(ra,dec,size,filters,mode=mode,img=img,**kwargs)

        imshow_params["extent"] = self._set_extent(size)
        draw_cross_params["x"]= 0
        draw_cross_params["y"]= 0
        fig,ax = self.display_dict(data,draw_cross=draw_cross,\
                                  draw_cross_params=draw_cross_params,\
                                  imshow_params=imshow_params)
        return fig, ax

    def display_all_cutouts(self,ra,dec,size,mode="bcgs_out",img="drz",\
                            draw_cross=False,draw_cross_params={},\
                            imshow_params={},**kwargs):

        cluster = self.info.get_cluster_from_coords(ra,dec)
        data = self.load_all_data_cutouts(ra,dec,size,mode=mode,img=img,**kwargs)

        imshow_params["extent"] = self._set_extent(size)
        draw_cross_params["x"]= 0
        draw_cross_params["y"]= 0
        fig,ax = self.display_dict(data["img"],draw_cross=draw_cross,\
                                  draw_cross_params=draw_cross_params,\
                                  imshow_params=imshow_params)
        self.display_dict(data["psf"])
        return fig, ax
