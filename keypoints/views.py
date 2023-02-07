import json
import os
import re
import subprocess

from django.http import JsonResponse


def exec_script(request):
    # TODO: take base64 in the request, save tmp img and give its path to the script
    wd = os.getcwd() + '/keypoints/code'
    ai_exec = subprocess.Popen(['python', 'run_no_det.py',
                                '--clothing', 'trousers'],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               cwd=wd)
    res = ai_exec.communicate()[0]
    print(res)
    # os.remove(os.getcwd() + '/keypoints/code/tmp.jpg')

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

    return JsonResponse({
        'keypoints': keypoints,
        'cb_box_distance': cb_box_distance,
    })
