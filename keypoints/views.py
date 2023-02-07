import base64
import json
import os
import re
import subprocess

from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt


# @csrf_exempt
def exec_script(request):
    res = {}
    if request.method == 'POST':
        body_json = json.loads(request.body)
        clothing = body_json['clothing']
        img_data = body_json['image'] # base64 raw data (without prefix data:image/...)
        wd = os.getcwd() + '/keypoints/code'

        with open(wd + '/tmp.jpg', 'wb') as f:
            f.write(base64.b64decode(img_data)) # Valid only for jpg data
            f.close()

        ai_exec = subprocess.Popen(['python', 'run_no_det.py',
                                    '--clothing', clothing,
                                    '--source', wd + '/tmp.jpg'],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT,
                                   cwd=wd)
        res = ai_exec.communicate()[0]
        os.remove(os.getcwd() + '/keypoints/code/tmp.jpg')

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

    return JsonResponse(res)
