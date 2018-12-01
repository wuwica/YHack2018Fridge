import requests
url = 'https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/analyze?visualFeatures=Categories&language=en'
files = {'media': open('test.jpg', 'rb')}
requests.post(url, files=files)