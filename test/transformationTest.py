import numpy as np
from scipy import io
import matplotlib.pyplot as plt

# import the source code
import sys
sys.path.append("..")
import src

def transformationTest():
    """ Show the effect on the standard Shepp-Logan sample using the cpu reconstruction 
        algorithms from astra"""
    reconstruct = src.sinogramTransformer.makeReconstruction
    makeSinogram = src.sinogramTransformer.makeSinogram

    image = io.loadmat("data/phantom512.mat")["X"]    
    image2 = reconstruct(makeSinogram(image),algorithm="FBP")    
    f, ( ax ) = plt.subplots(1,3)
    vmin,vmax = np.min(image),np.max(image)
    ax[0].imshow(image,vmin=vmin,vmax=vmax)    
    ax[1].imshow(image2,vmin=vmin,vmax=vmax)
    ax[2].imshow(image2-image)

transformationTest()