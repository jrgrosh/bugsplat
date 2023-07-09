This repository documents my project of using YOLOv5 to detect dead bugs on my Honda Accord's windshield. I took pictures using my iPhone, labeled them with Labelme, and created a script to converting Labelme's output into darknet format.

A frequently cited statistic is that 80% of time and effort in a machine learning project is spent on data preparation. For this project, this statement was true and also an understatement. I took 178 pictures of my car and created 12,693 annotations (bounding box labels) of splats by hand. I spent about two months gathering and annotating the data. In an effort to simply the problem, I only took pictures of my car. I also frequently took pictures of the same splats, from different angles, to decrease the time spent acquiring data.

Many of the splats are small. I eventually accepted the fact that I could not, in a reasonable amount of time and effort for a hobbyist, label them all. 

This created a problem. If splats of a certain size had both many labeled and unlabeled examples in the data, the model would become confused. To solve this issue, I decided to remove labels from the dataset that had less width or height than a certain percentage of the image's respective width or height.

* 27 samples are at least 10% of width and height of image
* 152 samples are at least 5% of width and height of image
* 952 samples are at least 2.5% of width and height of image
* 2392 samples are at least 1.75% of width and height of image
* 6225 samples are at least 1% of width and height of image
* 12693 samples are at least 0% of width and height of image

After overfitting (making train and validation datasets the same) on data using thresholds of 2.5%, 1.75%, and 1% for twenty epochs, I saw that using the 1% threshold overfit the best.

Overfitting: filtering small labels
<2.5% thrown out (batch size 16)
Image size 640
20 epochs,  Precision: 0.398      Recall: 0.463       mAP50: 0.37

<1.75% thrown out (batch size 2)
Image size 640
20 epochs, Precision: 0.452      Recall: 0.454      mAP50:0.418

<1% thrown out (batch size 2)
Image size 640
20 epochs, Precision: 0.5      Recall: 0.489      maP50:0.449

Using the entire dataset might have resulted in greater capacity to overfit, but that would have required a larger input image size to YOLO and slowed down training. Therefore, I chose to procede with the 1% and 640 input image dimension.

I split the data into train, validation, and test sets. 

Train / Val / Test (85% train, 10% val, 5% test, batch size 2)
Image size 640
20 epochs, Precision: 0.449     Recall: 0.382    maP50:0.366     maP50-95:0.126

Suprisingly, the results were good! Much better than I expected.

In the detect folder you can see some the detector performed on the test set.

The detector is able to localize many of the bigger splats.

The detector struggled with non-traditional angled pictures, suggesting that the model would benefit from augmented data that rotated images. The other gamut of usual augmentations would also likely help and make this detector more applicable various conditions.

As of July 2023, this is as far as I'd like to take this project for now. This was a learning experience, and taught me that for future machine learning projects - unless I end up designing algorithms somewhere - most of the time will be spent processing the data and not doing "mathy" number crunching and scientific calculations.
