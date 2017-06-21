## Project: Search and Sample Return
---


**The goals / steps of this project are the following:**  

**Training / Calibration**  

* Download the simulator and take data in "Training Mode"
* Test out the functions in the Jupyter Notebook provided
* Add functions to detect obstacles and samples of interest (golden rocks)
* Fill in the `process_image()` function with the appropriate image processing steps (perspective transform, color threshold etc.) to get from raw images to a map.  The `output_image` you create in this step should demonstrate that your mapping pipeline works.
* Use `moviepy` to process the images in your saved dataset with the `process_image()` function.  Include the video you produce as part of your submission.

**Autonomous Navigation / Mapping**

* Fill in the `perception_step()` function within the `perception.py` script with the appropriate image processing functions to create a map and update `Rover()` data (similar to what you did with `process_image()` in the notebook). 
* Fill in the `decision_step()` function within the `decision.py` script with conditional statements that take into consideration the outputs of the `perception_step()` in deciding how to issue throttle, brake and steering commands. 
* Iterate on your perception and decision function until your rover does a reasonable (need to define metric) job of navigating and mapping.  

[//]: # (Image References)

[image1]: ./calibration_images/example_grid_rock.png
[image2]: ./calibration_images/rock_transformed.png
[image3]: ./calibration_images/threshold.png

### Jupyter notebook Data Analysis

In the notebook, I first take a quick look at the grid and rock sample calibration images. The grid is used for perspective transform, which utilize `cv2.getPerspectiveTransform(src, dst)` and `cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]))`.
![alt text][image1]

####1. **Perspective transform:** 
The up right rock image is showed below after the perspective transform:
![alt text][image2]

We can see fair amount of distortion with the yellow rock setting at y=145, x=155.

####2. **Color threshold:** 
There are three categories we need to distinguish: movable terrain, not movable terrain and rock. For movable terrain, the rgb color threshold is > `rgb_thresh=(160, 160, 160)`. The opposite is not movable terrain. The threshold for rock is set by looking at the rock's rgb value and the coordinates is calculated by `cv2.inRange(img, lower_yellow, upper_yellow)`. We can see the outcome of the thresholded image below, respectively.

![alt text][image3]

####3.**Convert to rover coordinate:** 
This is achieved by the function `rover_coords(binary_img)`, which rotate the x coordinate to the direction of rover's heading and y at the left if the x.

####4.**Convert to world coordinate:** 
Given the information of rover's x,y value, yaw, world size and scale, we can convert the rover's coordinate movable terrain, not movable terrain and rock to world coordinate and draw on the Rover worldmap (to be displayed on right side of screen).

### Autonomous Navigation and Mapping

#### 1. Fill in the `perception_step()` and `decision_step`:
`perception_step():`

 The functions is almost the same as that in jupyter notebook with minor modifications: if a rock is detected, set a flag 		`Rover.detected = True` and `Rover.measured_samples_pos = (rock_x, rock_y)` for the `decision.py` to determine whether a rock is encountered.
 
 `decision_step():`
 
 I retain most of the starter code and add the function of picking up the sample when rover sees one. `Rover.mode=pickup` is trigered when `Rover.detected`. At the next cycle, function `drive_toward_sample` is activated: the rover first fully stops, then slowly drive towards the sample until `Rover.near_sample==True`, which sets `Rover.pick_up = True` and samples is picked up. Finally, all the flags are set to their initial value and `Rover.mode=forward`.


#### 2. Launching in autonomous mode your rover can navigate and map autonomously.  Explain your results and how you might improve them in your writeup.  

The result is OK when the rover does not encounter obstacles on its way, otherwise it will get stuck. I tried to add `is_clear()` function to check if obstacles is at the front, but it introduced another issue: the rover stopped when it went through narrow path. Another issus is the rover turn based on the threshold of the image, and the threshold can vary based on different light conditions.






