import numpy as np

from . import sinogramTransformer as ST


def ringArtifactsRemover(image,isSinogram=False,GPU=False,threshold=None,filters=None):
    """
    Simple ring artifact removal for tomograms using threshold for detecting 
    and median filter for interpolation 

    Parameters
    ----------
    image : ndarray
        The image can be the data in real space or if isSinogram is true 
        in the radon domain
    isSinogram : bool, optional
        see image
    GPU : bool, optional
        Enable ASTRA algorithm SIRT_CUDA which gives a significant 
        better reconstruction but requires specific graphic cards
    threshold : float, optional
        Value to detect the ring artifact, lower means more rings are detect, 
        but also higher error rate due to noise, if None the threshold will 
        be calculated based on the noise
    filters : function, optional
        the filter used to smooth out the ring artifact, if set to None a 
        median filter with size 3 is used.
    Returns
    -------
    result : ndarray
        The image or sinogram with ring artifact interpolated out
    """
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