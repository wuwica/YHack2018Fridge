########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64
import logging

# These two lines enable debugging at httplib level (requests->urllib3->http.client)
# You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.
try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
http_client.HTTPConnection.debuglevel = 1

# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


operation_id = ""

headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': '95c6a3592b064fcba3f2cbe94750f973',
}

getHeaders = {
    # Request headers
    'Ocp-Apim-Subscription-Key': '95c6a3592b064fcba3f2cbe94750f973',
}

params = urllib.parse.urlencode({
    # Request parameters
    'mode': 'Printed',
})



try:
    conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
    files = {'files': open('granolabar.jpg', 'rb')}
    with open("granolabar.jpg", "rb") as imageFile:
        f = imageFile.read()
        b = bytearray(f)
        #print (b[0])
    #conn.request("POST", "/vision/v2.0/recognizeText?%s" % params, '{"url":"https://lh3.googleusercontent.com/LcMEqPsEgElBQDBfn5LZmxkplnEaB78nRgcLQTbb_wQqC7ahr1gr37-2ztY=w1200-h630-p"}', headers)
    conn.request("POST", "/vision/v2.0/recognizeText?%s" % params, b, headers)

    response = conn.getresponse()
    data = response.read()
    print(operation_id)
    operation_id = response.headers["Operation-Location"].split("textOperations/")[1]
    print("------------>",operation_id)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

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
