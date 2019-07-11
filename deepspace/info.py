from .errors import deepspaceError

class DeepSpaceInfo:

    def __init__(self):
        return None

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
