
# ======================
# Parameters
# ======================

################## GENERAL PARAMS ##################

# set path to image, video or directory containing images.
# SOURCE = "data/images/"
SOURCE = "data/images/trouser"

# set path to results
RESULTS_PATH = "runs"
EXPERIMENT_NAME = "experiment"

CLOTHING_TYPE = 'trousers'
CHECKBOARD_SIZE = (5, 5)
SAVE_IMAGE = True
SAVE_TXT = True
VISUALIZE = False

BENCHMARK = False

########################## LANDMARKS MODELS PARAMS ##########################

WEIGHT_BLOUSE_PATH = 'weights/blouse_100.onnx'
MODEL_BLOUSE_PATH = 'weights/blouse_100.onnx.prototxt'
WEIGHT_DRESS_PATH = 'weights/dress_100.onnx'
MODEL_DRESS_PATH = 'weights/dress_100.onnx.prototxt'
WEIGHT_OUTWEAR_PATH = 'weights/outwear_100.onnx'
MODEL_OUTWEAR_PATH = 'weights/outwear_100.onnx.prototxt'
WEIGHT_SKIRT_PATH = 'weights/skirt_100.onnx'
MODEL_SKIRT_PATH = 'weights/skirt_100.onnx.prototxt'
WEIGHT_TROUSERS_PATH = 'weights/trousers_100.onnx'
MODEL_TROUSERS_PATH = 'weights/trousers_100.onnx.prototxt'
REMOTE_PATH_LANDMARKS = 'https://storage.googleapis.com/ailia-models/fashionai-key-points-detection/'

IMAGE_SIZE = 512

MU = 0.65
SIGMA = 0.25
HM_STRIDE = 4


MODELS = {
    'blouse': {
        'weights_path': WEIGHT_BLOUSE_PATH,
        'model_path': MODEL_BLOUSE_PATH
    },
    'dress': {
        'weights_path': WEIGHT_BLOUSE_PATH,
        'model_path': MODEL_DRESS_PATH
    },    
    'outwear': {
        'weights_path': WEIGHT_OUTWEAR_PATH,
        'model_path': MODEL_OUTWEAR_PATH
    },
    'skirt': {
        'weights_path': WEIGHT_SKIRT_PATH,
        'model_path': MODEL_SKIRT_PATH
    },
    'trousers': {
        'weights_path': WEIGHT_TROUSERS_PATH,
        'model_path': MODEL_TROUSERS_PATH
    },
}

KEYPOINTS = {
        'blouse': ['neckline_left', 'neckline_right', 'center_front', 'shoulder_left', 'shoulder_right',
                   'armpit_left', 'armpit_right', 'cuff_left_in', 'cuff_left_out', 'cuff_right_in',
                   'cuff_right_out', 'top_hem_left', 'top_hem_right'],
        'outwear': ['neckline_left', 'neckline_right', 'shoulder_left', 'shoulder_right', 'armpit_left',
                    'armpit_right', 'waistline_left', 'waistline_right', 'cuff_left_in', 'cuff_left_out',
                    'cuff_right_in', 'cuff_right_out', 'top_hem_left', 'top_hem_right'],
        'trousers': ['waistband_left', 'waistband_right', 'crotch', 'bottom_left_in', 'bottom_left_out',
                     'bottom_right_in', 'bottom_right_out'],
        'skirt': ['waistband_left', 'waistband_right', 'hemline_left', 'hemline_right'],
        'dress': ['neckline_left', 'neckline_right', 'center_front', 'shoulder_left', 'shoulder_right',
                  'armpit_left', 'armpit_right', 'waistline_left', 'waistline_right', 'cuff_left_in',
                  'cuff_left_out', 'cuff_right_in', 'cuff_right_out', 'hemline_left', 'hemline_right']
    }



########################## DETECTOR PARAMS ##########################

#Model Path for YOLOv3 Detector
WEIGHT_PATH_DETECTOR = 'weights/yolov7_deepfashion2_best.pt'

# Thresholds
CONFIDENCE_THRESHOLD = 0.4
IOU_THRESHOLD = 0.45
DETECTOR_IMAGE_SIZE = 416

# classes
DETECTORS_CLASSES = [
  "vest dress",
  "vest",
  "short sleeve dress",
  "trousers",
  "short sleeve top",
  "skirt",
  "long sleeve top",
  "shorts",
  "long sleeve outwear",
  "long sleeve dress",
  "checkerboard",
]


DETECTOR_MAPPING = {
  "vest dress": "dress",
  "vest": "blouse",
  "short sleeve dress": "dress",
  "trousers": "trousers",
  "short sleeve top": "blouse",
  "skirt": "skirt",
  "long sleeve top": "blouse",
  "shorts": "trousers",
  "long sleeve outwear": "outwear",
  "long sleeve dress": "dress",
}


########################## KEYPOINTS CONNECTIONS ##########################

CONNECTIONS = {
    'blouse': {
        "neck": ('neckline_left', 'neckline_right'),
        "shoulders": ('shoulder_left', 'shoulder_right'),
        "left_sleeve": ('shoulder_left', 'cuff_left_out'),
        "right_sleeve": ('shoulder_right', 'cuff_right_out'),
        "left_cuff": ('cuff_left_in', 'cuff_left_out'),
        "right_cuff": ('cuff_right_in', 'cuff_right_out'),
        "chest": ('armpit_left', 'armpit_right'),
        "waist": ('top_hem_left', 'top_hem_right'),
        "length_left": ('shoulder_left', 'top_hem_left'),
        "length_right": ('shoulder_right', 'top_hem_right'),
    }
}
