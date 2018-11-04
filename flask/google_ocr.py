# OCR
from base64 import b64encode
import json
import requests

def make_image_data_list(image_filenames):
    img_requests = []
    for imgname in image_filenames:
        with open(imgname, 'rb') as f:
            ctxt = b64encode(f.read()).decode()
            # print(ctxt)
            img_requests.append({
                'image': {'content': ctxt},
                'features': [{
                    'type': 'TEXT_DETECTION',
                    'maxResults': 1
                }]
            })
    return img_requests


def make_image_data(image_filenames):
    imgdict = make_image_data_list(image_filenames)
    return json.dumps({"requests": imgdict}).encode()

def request_ocr(api_key, image_filenames):
    endpoint_url = 'https://vision.googleapis.com/v1/images:annotate'
    response = requests.post(endpoint_url,
                             data=make_image_data(image_filenames),
                             params={'key': api_key},
                             headers={'Content-Type': 'application/json'})
    return response
