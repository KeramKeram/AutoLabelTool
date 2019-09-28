# AutoLabelTool

From time to time there is need to create database of images for machine learning. In order to create bigger base we use
some kind of augumentator. Sometimes we only want to one element to be augmented and rest of background should be intact.
Problem here is to generate new labels(Pascal VOC Format) for such images. this small tool can do this for you.

### Example
This example is not the same like this in example and out folder.
First Image:
Original file.

![alt text](https://github.com/KeramKeram/AutoLabelTool/blob/master/original.png)

We are extracting blue rectangle from background and next we generate many variants of this object. Now we want to:
Add this generated images to template image with background only. We are adding this images in some specific 
area(rectangle area) on template(we randomly generating coordinates in specific are). In the end we want to generate xml
file with label data(Pascal VOC Format)
On this image we have only background. Green dot rectangle it is area when we want to put images.
![alt text](https://github.com/KeramKeram/AutoLabelTool/blob/master/background.png)

This is example output:
![alt text](https://github.com/KeramKeram/AutoLabelTool/blob/master/example_out.png)

### End information
More information about configuring script is on wiki.