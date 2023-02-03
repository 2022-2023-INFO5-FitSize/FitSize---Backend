# Clothes Key Points Detection and Measurement

<img src="gallery/outline.jpg">

<br>
This code uses [Cascaded Pyramid Network for Multi-Person Pose Estimation](https://arxiv.org/abs/1711.07319) to detect key points of clothing including five types: blouse, dress, outwear, skirt and trousers by the help of [ailia SDK](https://axinc.jp/en/solutions/ailia_sdk.html). These keypoints are then used to measure parts of clothes.

Ailia SDK is a self-contained cross-platform high speed inference SDK. The ailia SDK provides a consistent C++ API on Windows and supports Python for efficient AI implementation. 

## <div>General Capabilities</div>

For every cloth category, a sperate model has been trained which means we need to specify the cloth type before we perform inference. But sometimes, we need a fully automated solution to work with all types of clothes. For this to handle, we have added an extra layer on the top of keypoints detection models. We have trained YOLOv7 detector on DeepFashion2 dataset for clothes detection which helps in categorizing the clothes first, then the code smartly select the best model for ketpoints detection.

The main goal of the project is to measure the clothes. To handle this, we needed to add some reference object with known dimensions in real-world units e.g. centimeters. For this, we used a checkerboard of size (n, m) for calibiration. The YOLOv7 detector model has an extra class for checkerboard which detects and crops the checkerboard. The crop is then processed with open CV to detect checkerboard corners for measuring the pixelate distance between corners.

## <div>Quick Start Examples</div>

<summary><h3>Install</h3></summary>

Python>=[3.7.0](https://www.python.org/) is required with all
packaged listed in the requirements.txt.

PyTorch>=[1.7](https://pytorch.org/get-started/locally/) is required. For gpu version pytorch, installing from there offficial repository is recommended.

```bash
# extract the code from the provided zip file.

$ cd code
$ pip install -r requirements.txt

```

Next, we need to install ailia SDK. Download and Extract the zip file from [here](https://drive.google.com/file/d/1nnYp_jQKCJO1z18WFFuXiDqsPUKWLC85/view?usp=sharing). While in the root directory, run the following commands.

```bash

$ cd python
$ python bootstrap.py
$ pip install .

```

Finaly, we need to download pre-trained weights for 5 keypoints detection models and YOLOv7 clothes detection. Download the zip file from [here](https://drive.google.com/file/d/1IWJm5-P_Ncal6-0Aj0kATVhPxlDkdSbI/view?usp=sharing) and paste it in the weights directory in the root directory.

<br >

<summary><h3>Inference</h3></summary>

There are two different scripts for performing inference. We can perfrom inference with using the YOLOv7 clothes detector as well without the detector. But if we are to do inference without the detector, we will need to specify the CLOTHING_TYPE in the CONFIG.py accordingly. 

```bash
# performing inference using the clothes detector
$ python run_det.py

# performing inference without clothes detector
$ python run_no_det.py
```

<img src="gallery/011975.jpg">

<br>

## <div>Configuration File</div>
The project configurations have been defined in the CONFIG.py file. Some of the configurations need to be set according to the source video or images but most of them remains constant. Following is the breif explaination for every parameter:


<h3>General Configurations</h3>

* <b>SOURCE: </b>Path to input image, video or directory containing images/videos for inference. It can be set to 0 for running the code on webcam.
* <b>RESULTS_PATH: </b>Path to which the results will be exported.
* <b>CLOTHING_TYPE: </b>Set the type of cloth for which keypoints are to be detected. This is only applicable if we run inference without clothes detector.
* <b>CHECKBOARD_SIZE: </b>Size of the checkerboard (number of squares in rows and cols) to be used for callibiration. 
* <b>VISUALIZE: </b>Visualize detections during inference if True

<br>
<h3>YOLOv7 Detector Configurations</h3>
    These configurations are YOLOv7 model specific. Changing these params may effect the results.

* <b>DETECTORS_CLASSES: </b>list of classes on which the detector was trained.
* <b>DETECTOR_MAPPING: </b>dictionary which maps the detector classes to the keypoints detection models.
* <b>WEIGHT_PATH_DETECTOR: </b>path to the pre-trained weights file.
* <b>IMAGE_SIZE: </b>model input image size on which it was trained.
* <b>CONFIDENCE_THRESHOLD: </b>confidence threshold used while NMS.
* <b>IOU_THRESHOLD: </b>IoU threshold used while NMS.


## <div>Author</div>

Muhammad Nouman Ahsan

## <div>References</div>

* Ailia SDK https://github.com/axinc-ai/ailia-models
* Cascaded Pyramid Network for FashionAI Key Points Detection https://github.com/gathierry/FashionAI-KeyPointsDetectionOfApparel
* YOLOv7 https://github.com/WongKinYiu/yolov7
