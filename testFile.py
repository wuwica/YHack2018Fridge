
########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '95c6a3592b064fcba3f2cbe94750f973',
}

params = urllib.parse.urlencode({
    # Request parameters
    'visualFeatures': 'Description',
    'language': 'en',
})

try:
    conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
    conn.request("POST", "/vision/v2.0/analyze?%s" % params, "https://lh3.googleusercontent.com/LcMEqPsEgElBQDBfn5LZmxkplnEaB78nRgcLQTbb_wQqC7ahr1gr37-2ztY=w1200-h630-p", headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))