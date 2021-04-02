# HSV-Thresholding
This is a GUI tool to help determine the HSV value needed for thresholding in OpenCV. Keep in mind the program assumes a fixed lighting condition, so it it best to recalibrate the HSV values before deploying your program.  

**[What is HSV?](https://docs.opencv.org/3.4/da/d97/tutorial_threshold_inRange.html)**


## Demo
***You can adjust the upper and lower bounds by using the slider with a mouse, typing the value in the text box, or tapping the keyboard to scrub the slider once it has been highlighted.***  

![Main Preview](./assets/main.gif)

## Fixes 
The default **camera path is set to 2**, if it does not open up or if you have multiple cameras you can try to change this line in the **main python file.**

***Start by using 0 and increase the value by 1 until you see the video feed.***

```
# Set camera path and capture from web cam
cap = cv2.VideoCapture(0)
```
