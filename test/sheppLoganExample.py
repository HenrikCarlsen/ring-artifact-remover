import numpy as np
from scipy import io
import matplotlib.pyplot as plt

# import the source code
import sys
sys.path.append("..")
import src

def makeRingArtifact(sinogram,columns,pixelEffeciency=None):
    """ Simulate the effects of ring artifacts by multiplying columns
        in the sinogram by a factor between zero and one, zero being a dead
        pixel"""
    if np.all(pixelEffeciency == None):
        pixelEffeciency = [0]*len(columns)
    
    sinogram = np.array(sinogram)
    
    for c,e in zip(columns,pixelEffeciency):
        sinogram[:,c] = sinogram[:,c]*e
        
    return sinogram


def SheppLogan():
    """ This example show that ring artifact close to each other 
        or many ring artifacts makes the ring removal"""
    ringRemover =  src.ringArtifactsRemover.ringArtifactsRemover
    makeSinogram = src.sinogramTransformer.makeSinogram
    reconstruct = src.sinogramTransformer.makeReconstruction

    image = io.loadmat("data/phantom512.mat")["X"]
    sinogram = makeSinogram(image)
    
    ringsN=10
    
    rings = np.random.randint(sinogram.shape[1],size=ringsN)
    print(rings)
    pixelEffeciency = np.random.rand(ringsN)*0.5
    sinogram = makeRingArtifact(sinogram,rings,pixelEffeciency)

    sinogramDetected = ringRemover(sinogram,
                                   isSinogram=True,threshold=0.8)
    imageDetected = reconstruct(sinogramDetected,algorithm="FBP")    

    f, ( ax ) = plt.subplots(1,3)
    vmin,vmax = np.min(image),np.max(image)
    ax[0].imshow(image,vmin=vmin,vmax=vmax)    
    ax[1].imshow(imageDetected,vmin=vmin,vmax=vmax)
    ax[2].imshow(imageDetected-image)

SheppLogan()