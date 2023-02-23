# How to use this server

## Requirements

- Python>=[3.9.0](https://www.python.org/)
- PyTorch>=[1.7](https://pytorch.org/get-started/locally/) is required. For gpu version pytorch, installing from there offficial repository is recommended.
- gdown to download model files from Google Drive :
```bash
  $ pip3 install gdown
```

```bash
# extract the code from the provided zip file.

$ pip install torch tqdm pandas requests torchvision seaborn pyyaml ailia
$ pip install jsonify
$ pip install -r requirements.txt
```

Next, we need to install ailia SDK. Download and Extract the zip file from [here](https://drive.google.com/file/d/1XOUILHyoekz4nBnISGt6J8FREFjzInFP/view?usp=share_link). 

Get an AILIA license trial from [here](https://axinc.jp/en/trial/) and paste it in the downloaded python directory.

Then, while in the root directory, run the following commands.

```bash
$ cd python
$ python bootstrap.py
$ pip install .
```

## Download model files

If it is the first time you open this repo, you've probably not downloaded the model files yet.
To do so, run the following command:

```bash
$ chmod +x download_models.sh
$ ./download_models.sh
```

It will copy the files in appropriate directories.

## Start the server

```bash
$ python manage.py migrate
$ python manage.py runserver
```

The server should start locally at http://127.0.0.1:8000/.

## Image keypoints computing API

Join our Postman Team [here](https://app.getpostman.com/join-team?invite_code=f68903cd9fa0ac4d12f855be1d739719&target_code=7d5682c00f94eb97eb3b67333cf1ddb6) to test this API.

Basically, there is a single POST endpoint that takes in body request a JSON object that contains
the following fields:
- 'clothing': a string that indicates the clothing type on the image (among ['trousers', 'blouse', 'outwear', 'skirt', 'dress'])
- 'image': the base64 data of the JPG image (only the raw data without the 'data:image/...' prefix).

The endpoint is located at http://127.0.0.1:8000/keypoints/execScript.

The response follows this format:
```json
{
    "keypoints": {
        "waistband_left": "array([467, 978,   1], dtype=int16)",
        "waistband_right": "array([2522, 1065,    1], dtype=int16)",
        "crotch": "array([1380, 2616,    1], dtype=int16)",
        "bottom_left_in": "array([1065, 2932,    1], dtype=int16)",
        "bottom_left_out": "array([   2, 2435,    1], dtype=int16)",
        "bottom_right_in": "array([1672, 2861,    1], dtype=int16)",
        "bottom_right_out": "array([2932, 2624,    1], dtype=int16)"
    },
    "cb_box_distance": 52.17978800104307
}
```

For each keypoints, you have an array [x,y,z] for coordinates in pixels.

The *cb_box_distance* field correspond to the size in pixels of 1 centimeter.

To obtain a dimension, you'll have to compute the Euclidian distance between to points (consedering only *x* and *y*)
and then divide this distance in pixels by the *cb_box_distance* value. You will obtain the distance in centimeters.