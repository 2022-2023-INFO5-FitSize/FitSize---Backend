# How to use this server

## Requirements

- Python>=[3.9.0](https://www.python.org/)
- PyTorch>=[1.7](https://pytorch.org/get-started/locally/) is required. For gpu version pytorch, installing from there offficial repository is recommended.

```bash
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

## Start RabbitMQ broker for Celery

```bash
# Make sure you have docker installed and the daemon running

$ docker run -d -p 5672:5672 rabbitmq
```

## Start the server

```bash
$ python manage.py migrate
$ daphne fitsize.asgi:application 
```

In a separate terminal, start the celery worker:
```bash
$ celery -A fitsize worker -l info
```

The server should start locally at http://127.0.0.1:8000/.

## Image keypoints computing API

Join our Postman Team [here](https://app.getpostman.com/join-team?invite_code=f68903cd9fa0ac4d12f855be1d739719&target_code=7d5682c00f94eb97eb3b67333cf1ddb6) to test this API.

Basically, the AI keypoints computing API is made of 2 endpoints:
- POST /keypoints/execScript: this endpoint takes in input a JSON object that contains the clothing type and the image (base64 raw data of a JPG: only the raw data without the 'data:image/...' prefix).
  
  The response follows this format:
  ```json
  {
      "task_id": "e6b0b5e0-5e1a-4b5e-9c1a-7c5f1b2e3f4a"
  }
  ```


- GET /keypoints/taskStatus/<task_id>: this endpoint takes in input the task_id returned by the previous endpoint and returns the status of the task (among ['PENDING', 'STARTED', 'SUCCESS', 'FAILURE']). If the task is completed, the response will also contain the keypoints and the cb_box_distance value.

  An exemple of response with SUCCESS:
  ```json
  {
    "status": "SUCCESS",
    "result": {
        "keypoints": {
            "waistband_left": "array([ 73, 157,   1], dtype=int16)",
            "waistband_right": "array([403, 172,   1], dtype=int16)",
            "crotch": "array([221, 417,   1], dtype=int16)",
            "bottom_left_in": "array([172, 466,   1], dtype=int16)",
            "bottom_left_out": "array([  2, 391,   1], dtype=int16)",
            "bottom_right_in": "array([267, 453,   1], dtype=int16)",
            "bottom_right_out": "array([467, 418,   1], dtype=int16)"
        },
        "cb_box_distance": 8.792742391172574
    }
  }
  ```

For each keypoints, you have an array [x,y,z] for coordinates in pixels.

The *cb_box_distance* field correspond to the size in pixels of 1 centimeter.

To obtain a dimension, you'll have to compute the Euclidian distance between to points (consedering only *x* and *y*)
and then divide this distance in pixels by the *cb_box_distance* value. You will obtain the distance in centimeters.