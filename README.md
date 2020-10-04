# **Quick Faces**

It is a **framework for experiments with computer vision** algorithms.

It is designed for working with faces, but can be use for other types of tasks.


## Idea
The idea is to choose for your own experiment:
1) any of the **inputs** (directory with pictures, camera, video),
2) any of the **outputs** (directory, video, a window on the screen)
3) any of the **processors** (programs) or a combination of them that will process the images

(The framework was designed especially for different algorithms searching faces and landmarks in these faces).

## Debugging

For each process, **the processing time is recorded**, both for individual images and as a whole as **statistics** for the entire process.

## Purpose
There are many published algorithms and here everyone will be able to test them on their data.
Gradually, I will expand the list of usable processes.
I hope that it can be useful for testing different algorithms.

## Usage
For now, just modify main_example.py and run it:

`python3 main_example.py`


## Todo list (for the near future):
- Wrap the entire process to a **command line** with parameters and/or with a configuration file.
- Improve this documentation
    - command-line examples
    - configuration file examples
    - How to write your own image processor
- add **input source**
    - **video**
- add **output source**
    - **video**
- add different types **of face detectors**
    - **yolo v3**
    - **tracking face detecor** 
    Estimates the position of the face based on the previous location of the landmarks and the direction and speed of movement of these landmarks in history. Either a simple estimate or learning from examples in history. If the history is not known, the classic (and slower) face detector is used.
- add different types **of landmarks predictors (detectors)**
    - **Combination of 3 shape predictors from library dlib** 
    From models for the whole face and separately user-trained models for the left and right part of the face Select the best in each image.
- add image processor, wicht adds legend (information about all processes) to the each image    
    