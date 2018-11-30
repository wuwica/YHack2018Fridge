########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64
import logging
import requests as requests

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


files = open('yogurt.png', 'rb').read()
resp=requests.post('http://westcentralus.api.cognitive.microsoft.com/vision/v2.0/recognizeText',params=params, data=files, headers=headers)
    

print(operation_id)
operation_id = resp.headers["Operation-Location"].split("textOperations/")[1]
print("------------>",operation_id)
####################################
# try:
#     getParams = urllib.parse.urlencode({
#             'operationId' : operation_id

#     })
#     conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
#     conn.request("GET", "/vision/v2.0/textOperations/{operation_id}?%s" % getParams, "{body}", getHeaders)
#     response = conn.getresponse()
#     data = response.read()
#     print (response.status)
#     print(data)
#     conn.close()
# except Exception as e:
#     print("[Errno {0}] {1}".format(e.errno, e.strerror))
