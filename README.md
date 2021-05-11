# Face-mask-detection
Detect face mask with yolov3

I implemented this project in Google Colab and the model was trained using Colab's GPU.

### Dowload the Dataset
The face mask detection dataset is fetched from [Kaggle](https://www.kaggle.com/andrewmvd/face-mask-detection)

I followed this [tutorial](https://laptrinhx.com/how-to-download-kaggle-datasets-into-google-colab-via-google-drive-1107891156/)  to download and unzip the dataset to my google drive 

### Create a new folder yolov3
The dataset comprises of two folders - images, annotations. Save these in the yolov3 folder. Convert the xml annotations to text files using xml_to_yolo.py and save them to mask_yolo_train. 

Create a new folder mask_yolo_test. Split the dataset into training and testing data. Move some images and their respective annotations to the mask_yolo_test folder for testing.

### Clone the Darknet repo
Locate to **darknet/data** folder.

Create `face_mask.names` file. This files will contain the classes we want to predict for. So in this case our file will look like this :
```
Good
Bad
```


Create `face_mask.data` file. This file will contain some important information and absolute paths to train.txt, test.txt, face_mask.names and the backup folder. 

Make sure that you have copied train.txt and test.txt from yolov3 to darknet/data folder. 

If you don't have a backup folder then create one in order to save the weights. So our file would look like this : 
```
classes = 2
train = data/train.txt
valid  = data/test.txt
names = data/face_mask.names
backup = backup
```


Next locate to **darknet/cfg** folder.
Copy ```yolov3.cfg``` and rename it to ```face_mask.cfg```

Then we make the following changes to ```face_mask.cfg``` :
* Change ```batch``` to ```batch = 64```
* Change ```subdivisions``` to ```subdivisions = 16```
* Change the input dimensions
  -  ```width = 416```
  -  ```height = 416```
* Change ```max_batches``` to ```max_batches = 4000```
* Change ```steps``` to ```steps = 3200,3600```
* At lines ```610```, ```696``` and ```783``` 
  - change ```classes``` to ```classes = 2```
* At lines ```603```, ```689``` and ```776``` 
  - change ```filters``` to ```filters = 21```

