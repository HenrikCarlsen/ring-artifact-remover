import numpy as np

def makeSinogram(image,
                 num_angles=1024,
                 num_detector_pixels=512,
                 GPU=False):
    """ Compute the sinogram of the image from a uniform
        distibution of projections using astra"""
    import astra

    angles = np.linspace(0,np.pi,num_angles,False)
    
    rel_detector_size = 1.0
    
    vol_geom = astra.create_vol_geom(num_detector_pixels,
                                     num_detector_pixels)
    proj_geom = astra.create_proj_geom('parallel',
                                       rel_detector_size, 
                                       num_detector_pixels,
                                       angles)
    if GPU:
        proj_id = astra.create_projector('cuda',proj_geom,vol_geom)
    else:
        proj_id = astra.create_projector('line',proj_geom,vol_geom)
    
    sino_id, sinogram = astra.create_sino(image,proj_id)
    return sinogram

def makeReconstruction(sinogram,GPU=False,algorithm=None,iterations=1):
    """ Construct image from a sinogram using astra """
    import astra

    # select astra algorithm
    if algorithm == None:
        if GPU:
            algString='SIRT_CUDA'    
        else:
            algString='SIRT'
    else:
        algString=algorithm
     
    num_angles,num_detector_pixels = sinogram.shape    
    rel_detector_size = 1.0    
    angles = np.linspace(0,np.pi,num_angles,False)
    
    
    vol_geom = astra.create_vol_geom(num_detector_pixels,num_detector_pixels)
    proj_geom = astra.create_proj_geom('parallel',rel_detector_size, 
                                       num_detector_pixels,angles)
    rec_id = astra.data2d.create('-vol', vol_geom)
    
        
    cfg = astra.astra_dict(algString)
    cfg['ProjectorId'] = astra.create_projector('line',proj_geom,vol_geom)
    cfg['ProjectionDataId'] = astra.data2d.create('-sino',proj_geom, data=sinogram)
    cfg['ReconstructionDataId'] = rec_id
    cfg['FilterType'] = 'Ram-Lak' # only used if gpu is True
    
    alg_id = astra.algorithm.create(cfg)
    astra.algorithm.run(alg_id,iterations)

    return astra.data2d.get(rec_id)