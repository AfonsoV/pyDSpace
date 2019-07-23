import os

from .errors import deepspaceError


DataFolder = os.getenv("DEEPSPACE")

if DataFolder is None:
    raise deepspaceError("DEEPSPACE environment variable not set.")


class DeepSpaceInfo:

    def __init__(self):
        return None


    filter_order = ['f225w','f275w','f336w','f390w','f435w','f475w','f555w',\
                    'f606w','f625w','f775w','f814w','f850lp','f105w',\
                    'f110w','f125w','f140w','f160w','Ks','ch1','ch2',\
                    'ch3','ch4','det','seg']

    clusters = ["abell1063","abell2744","abell370","macs0416","macs0717","macs1149"]

    availableFilters = {"abell1063":['Ks', 'ch1', 'ch2', 'ch3', 'ch4', 'f105w',\
                                    'f110w', 'f125w', 'f140w', 'f160w', 'f225w',\
                                    'f275w', 'f336w', 'f390w', 'f435w', 'f475w',\
                                    'f606w', 'f625w', 'f775w', 'f814w', 'f850lp'],\
                        "abell2744":['Ks', 'ch1', 'ch2', 'ch3', 'ch4', 'f105w',\
                                     'f125w', 'f140w', 'f160w', 'f275w', 'f336w',\
                                     'f435w', 'f606w', 'f814w'],\
                        "abell370":['Ks', 'ch1', 'ch2', 'ch3', 'ch4', 'f105w',\
                                    'f110w', 'f125w', 'f140w', 'f160w', 'f275w',\
                                    'f336w', 'f435w', 'f475w', 'f606w', 'f625w',\
                                    'f814w'],\
                        "macs0416":['Ks', 'ch1', 'ch2', 'f105w', 'f110w',\
                                    'f125w', 'f140w', 'f160w', 'f225w', 'f275w',\
                                    'f336w', 'f390w', 'f435w', 'f475w', 'f606w',\
                                    'f625w', 'f775w', 'f814w', 'f850lp'],\
                        "macs0717":['Ks', 'ch1', 'ch2', 'f105w', 'f110w', 'f125w',\
                                    'f140w', 'f160w', 'f225w', 'f275w', 'f336w',\
                                     'f390w', 'f435w', 'f475w', 'f555w', 'f606w',\
                                     'f625w', 'f775w', 'f814w', 'f850lp'],\
                        "macs1149":['Ks', 'ch1', 'ch2', 'f105w', 'f110w',\
                                    'f125w', 'f140w', 'f160w', 'f225w', 'f275w',\
                                    'f336w', 'f390w', 'f435w', 'f475w', 'f555w',\
                                    'f606w', 'f625w', 'f775w', 'f814w', 'f850lp']}


    zeropoints = {"f105w":26.26892,\
                    "f110w":26.82222,\
                    "f125w":26.23032,\
                    "f140w":26.45242,\
                    "f160w":25.94633,\
                    "f225w":24.07782,\
                    "f275w":24.01411,\
                    "f336w":24.58160,\
                    "f390w":25.36151,\
                    "f435w":25.66559,\
                    "f475w":26.05643,\
                    "f606w":26.49342,\
                    "f625w":25.89953,\
                    "f775w":25.66206,\
                    "f814w":25.94672,\
                    "f850lp":24.85725}

    image_modes = ["bcgs_models","bcgs_out","psf_matched","original"]

    cluster_coords = {"macs0717":(109.43863048556054, 109.33323737580649, 37.708234125318704, 37.791567413408224),\
                      "abell2744":(3.6349786790793948, 3.531611340899466, -30.439247968007468, -30.336748088394312),\
                      "abell370":(40.00302643255294, 39.92299569762585, -1.6432928825364999, -1.5332929431505387),\
                      "macs1149":(177.44326387785338, 177.34591790002193, 22.356309256746993, 22.446309208248984),\
                      "abell1063":(342.23815044338255, 342.12452654293924, -44.57507016811651, -44.48856837273851),\
                      "macs0416":(64.08056990070776, 63.989300170823576, -24.114107728713556, -24.030773153403377)}

    def get_cluster_from_coords(self,ra,dec):
        for cluster,limits in DeepSpaceInfo.cluster_coords.items():
            if (ra>limits[1]) and (ra<limits[0]):
                return cluster
        raise deepspaceError(f"Coordinates {ra},{dec} outside cluster boundaries.")
        return None

    def verify_mode(self,mode):
        if mode not in DeepSpaceInfo.image_modes:
            raise deepspaceError(f"{mode} not available. Choice of {DeepSpaceInfo.image_modes}")

    def verify_cluster(self,cluster):
        if cluster not in DeepSpaceInfo.clusters:
            raise deepspaceError(f"{cluster} not available. Choice of {DeepSpaceInfo.clusters}")

    def verify_filter(self,cluster,filter):
        self.verify_cluster(cluster)
        if filter not in DeepSpaceInfo.availableFilters[cluster]:
            raise deepspaceError(f"{filter} not available for cluster {cluster}.\nChoice of {DeepSpaceInfo.availableFilters[cluster]}")

    def available_image_modes(self):
        for mode in DeepSpaceInfo.image_modes:
            print(mode)
        return None

    def available_data(self):
        for clst in DeepSpaceInfo.clusters:
            print(clst)
        return None

    def available_filters(self,cluster):
        self.verify_cluster(cluster)
        for flt in DeepSpaceInfo.availableFilters[cluster]:
            print(flt)
        return None

    def sort_filters(self,fltr):
        return DeepSpaceInfo.filter_order.index(fltr)
