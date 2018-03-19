import numpy as np
import matplotlib.pyplot as plt

# import the source code
import sys
sys.path.append("..")
import src


def ChalkSample():
    """ show the effect on a small chalk sample using the cpu reconstruction 
        algorithms from astra"""
    reconstruct = src.sinogramTransformer.makeReconstruction
    ringRemover =  src.ringArtifactsRemover.ringArtifactsRemover

    sinogram = np.load("data/sino0500.npy")
    sinogram2 = ringRemover(sinogram,True,threshold=0.8)
    
    image = reconstruct(sinogram,algorithm="FBP")
    image2 = reconstruct(sinogram2,algorithm="FBP")    
    zoom = [slice(680,990),slice(560,690)]
   
    f, ( ax ) = plt.subplots(1,3)
    vmin,vmax = np.min(image[zoom]),np.max(image[zoom])
    ax[0].imshow(image[zoom],vmin=vmin,vmax=vmax)    
    ax[1].imshow(image2[zoom],vmin=vmin,vmax=vmax)
    ax[2].imshow(image2[zoom]-image[zoom])


ChalkSample()