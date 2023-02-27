import json
import os
import re
import subprocess

from fitsize.celery import app

@app.task
def process_image(image_path, clothing):
    wd = os.getcwd() + '/keypoints/code'
    ai_exec = subprocess.Popen(['python', 'run_no_det.py',
                                '--clothing', clothing,
                                '--source', wd + image_path],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               cwd=wd)
    res = ai_exec.communicate()[0]
    os.remove(os.getcwd() + '/keypoints/code/' + image_path)

    print(res)
    # Extract keypoints and checkerboard size
    split_res = res.split(b'\n')
    keypoints = json.loads(
        re.sub(
            r"array\([^)]*\)",
            lambda s: '"' + s.group(0) + '"',
            split_res[3].decode("utf-8").replace("'", '"')
        )
    )
    cb_box_distance = float(split_res[4].decode("utf-8"))
    res = {
        'keypoints': keypoints,
        'cb_box_distance': cb_box_distance,
    }

    return res

