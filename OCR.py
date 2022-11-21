from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
import json
from array import array
import os
#from PIL import Image
import sys
import time
import locale

arabic_to_english = {'١': '1', '٢': '2', '٣': '3', '٤': '4', '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9', '٠': '0'}
english_to_arabic = {'1': '١', '2': '٢', '3': '٣', '4': '٤', '5': '٥', '6': '٦', '7': '٧', '8': '٨', '9': '٩', '0': '٠'}

def InvoiceToJSON(data):
    to_json = {"invoice_number": data[6],
                "date": data[9][:2]+'/'+data[9][3:5]+'/'+data[9][6:]}
    return to_json

def ocr(image_url):
    lines=[]
    '''
    Authenticate
    Authenticates your credentials and creates a client.
    '''
    subscription_key = "fc0cde20c343425ca8fb03deb813f5d2"
    endpoint = "https://eg-id-ocr.cognitiveservices.azure.com/"

    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
    '''
    END - Authenticate
    '''

    '''
    OCR: Read File using the Read API, extract text - remote
    This example will extract text in an image, then print results, line by line.
    This API call can also extract handwriting style text (not shown).
    '''
    print("===== Read File - remote =====")
    # Get an image with text
    read_image_url = image_url

    # Call API with URL and raw response (allows you to get the operation location)
    read_response = computervision_client.read(read_image_url,  raw=True)

    # Get the operation location (URL with an ID at the end) from the response
    read_operation_location = read_response.headers["Operation-Location"]

    # Grab the ID from the URL
    operation_id = read_operation_location.split("/")[-1]
    # Call the "GET" API and wait for it to retrieve the results
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
        time.sleep(1)

    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                lines.append(line.text)
                #print(line.text)
                #print(line.bounding_box)
    print()
    # create json

    '''
    END - Read File - remote
    '''
    return InvoiceToJSON(lines)
#https://i.pinimg.com/originals/0d/38/ff/0d38ff362c926d069986bc892ddb2351.jpg
#image_url = "https://i.ibb.co/kGzHGRP/index.jpg"
#image_url = "https://i.pinimg.com/564x/d5/a1/03/d5a10397f6ffb38b4f74df057215ac34.jpg"
#result = ocr(image_url)
#print(result)
