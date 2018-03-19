import numpy as np

from . import sinogramTransformer as ST


def ringArtifactsRemover(image,isSinogram=False,GPU=False,threshold=None,filters=None):
    if isSinogram:
        sinogram = image
    else:
        sinogram = ST.makeSinogram(image,GPU=GPU)

    rings = _detectRings(sinogram,threshold,filters)
    sinogramNoRings = _removeRings(sinogram,rings)
    
    if isSinogram:
        return sinogramNoRings
    else:
        return ST.makeReconstruction(sinogramNoRings,GPU=GPU,algorithm="FBP")


def _detectRings(sinogram,threshold=None,filters=None):
    """ Finds the  by filtering the sinogram, 
        summing along the columns and thresholding the result 
        extract ring positions"""
    import scipy as sp
    import scipy.signal

    # Apply the filter on the sinogram
    if filters==None:
        sinogramFiltered = sp.signal.medfilt(sinogram,3)
    else:
        sinogramFiltered = filters(sinogram)
        
    # Sum along the angles
    sumfiltered = np.sum(sinogramFiltered,0)
    sumOriginal = np.sum(sinogram,0)
    # Find the peaks in difference between the sum of response 
    # to the filter using thresholding.
    if threshold==None:
        threshold = 8*np.median( np.abs(sumfiltered-sumOriginal) )
        
    ringsIndicies = np.where( sumfiltered-sumOriginal>threshold )
    return ringsIndicies

def _removeRings(sinogram,rings,filters=None):
    """ reduce the ring artifact by applying a filter at their position """

    sinogramRingRemoved = np.array(sinogram)
    rings = np.array(rings)
    sinogramRingRemoved[:,rings] = (sinogram[:,rings-1]+sinogram[:,rings+1] )/2
    
    return sinogramRingRemoved