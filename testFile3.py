
import http.client, urllib.request, urllib.parse, urllib.error, base64, time
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

from testFile2 import operation_id
print("operation________id", operation_id)

caloriesCount = -1

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': '95c6a3592b064fcba3f2cbe94750f973',
}

#operation_id = "b3083a77-f454-4220-a716-b5061caafb1a"
params = urllib.parse.urlencode({
    'operationId' : operation_id
})


try:
    conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
    time.sleep(5)
    conn.request("GET", "/vision/v2.0/textOperations/{operationId}?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    print(data)

    dataStr = data.decode("utf-8")
    print(type(data.decode("utf-8")))
    print (dataStr.find("Calories"))
    print(dataStr[dataStr.find("Calories"):dataStr.find("Calories") + 14])
    caloriesData = dataStr[dataStr.find("Calories"):dataStr.find("Calories") + 14]
    print(caloriesData)
    caloriesData = caloriesData.split(',')
    for dataStr in caloriesData[:]:
        arr = [int(s) for s in dataStr.split() if s.isdigit()]
        if len(arr) != 0:
            caloriesCount = arr[0]

    if caloriesCount == -1:
        caloriesCount = 200
        #caloriesCount = 6*itemWeight

    print(caloriesCount)

    #print([int(s) for s in caloriesData.split() if s.isdigit()])
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

####################################