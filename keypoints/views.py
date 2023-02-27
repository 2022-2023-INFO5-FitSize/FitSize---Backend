import base64
import json
import os
import uuid

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .tasks import process_image


@csrf_exempt
def exec_script(request):
    res = {}
    if request.method == 'POST':
        body_json = json.loads(request.body)
        clothing = body_json['clothing']
        img_data = body_json['image'] # base64 raw data (without prefix data:image/...)
        wd = os.getcwd() + '/keypoints/code'

        # Generate unique uuid
        img_id = uuid.uuid4()

        with open(wd + '/tmp'+str(img_id)+'.jpg', 'wb') as f:
            f.write(base64.b64decode(img_data)) # Valid only for jpg data
            f.close()

        # Run AI script
        res = process_image.delay('/tmp'+str(img_id)+'.jpg', clothing)

    return JsonResponse({'task_id': res.id})

def task_status(request, task_id):
    res = process_image.AsyncResult(task_id)
    print(res.result)
    return JsonResponse({'status': res.status, 'result': res.result})
