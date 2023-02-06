import json
import os
import re
import subprocess

from django.http import JsonResponse


def exec_script(request):
    wd = os.getcwd() + '/keypoints/code'
    ai_exec = subprocess.Popen(['python3.9', 'run_no_det.py'],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               cwd=wd)
    res = ai_exec.communicate()[0]

    # Extract keypoints and checkerboard size
    split_res = res.split(b'\n')
    keypoints = json.loads(
        re.sub(
            r"array\([^)]*\)",
            lambda s: '"' + s.group(0) + '"',
            split_res[3].decode("utf-8").replace("'", '"')
        )
    )
    cb_box_distance = split_res[4].decode("utf-8")

    return JsonResponse({
        'keypoints': keypoints,
        'cb_box_distance': cb_box_distance,
    })
