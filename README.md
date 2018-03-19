# RingArtifactRemover
A simple ring artifact remover for tomography

# Introduction
Ring artifacts in tomogram reconstructions are high frequency features shaped like rings  due to dead or damaged detector pixels. We purpose a simple but effective algorithm for remove these artifacts using the sinogram of the reconstructions based on median filters and thresholding.
The purpose is not to make the best ring removal but to show how intuitive and easy the process can be done while still remaining a very effective tool, as seen in the Chalk sample image below.

<img src="resources/picturesForReadme/ChalkSampleReconstruction.png" width="30%"> <img src="resources/picturesForReadme/ChalkSampleReconstructionWithoutRingArtifacts.png" width="30%"> <img src="resources/picturesForReadme/ChalkSampleReconstructionsDifference.png" width="30%">

# Algorithm
First we sinogram of the image using the radon transformation as the rings form lines in this domain. The sinogram is summed along the angle of projection axis to amplify the rings.
This sum is median filtered and subtracted from the original summed sinogram.
This difference magnify the ring artifacts, which now can be thresholded out. To compensate for the damage pixel it was found to be best to interpolate using nearest neighbour methods, as long are there are no ring artifacts next to each other.

# Credits
This code is based on the presentation project written in cooperation between Emma Mellhammar and Henrik Hoffmann Carlsen during the PhD Summer school Cinemax iii.