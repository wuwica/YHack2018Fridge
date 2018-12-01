########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64
import logging
import requests as requests

img_name = 'yogurt.png'
operation_id = ""

headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': '95c6a3592b064fcba3f2cbe94750f973',
}

params = urllib.parse.urlencode({
    # Request parameters
    'mode': 'Printed',
})


files = open(img_name, 'rb').read()
resp=requests.post('http://westcentralus.api.cognitive.microsoft.com/vision/v2.0/recognizeText',params=params, data=files, headers=headers)
    
print (resp.status_code)
if resp.status_code == 202:
    print("status: request processed")
else:
    print("status:", resp.status_code)

print(operation_id)
operation_id = resp.headers["Operation-Location"].split("textOperations/")[1]
print("------------>",operation_id)
