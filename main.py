import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import urllib.request
import requests
import re
 
#cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN
 

url='http://add url here'
web_url = 'use web_url/patient'

cv2.namedWindow("live transmission", cv2.WINDOW_AUTOSIZE)
 
prev=""
pres=""


def fetch_and_print_patient_data(web_url):
    try:
        response = requests.get(web_url)
        if response.status_code == 200:
            patient_data = response.json()
            print("Patient ID:", patient_data['id'])
            print("Name:", patient_data['name'])
            print("Age:", patient_data['age'])
            print("Temperature:", patient_data['temperature'])
            print("Heart Rate:", patient_data['heart_rate'])
        else:
            print("Error:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)



while True:
    img_resp=urllib.request.urlopen(url+'cam-lo.jpg')
    imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
    frame=cv2.imdecode(imgnp,-1)
 
    decodedObjects = pyzbar.decode(frame)
    for obj in decodedObjects:
        pres=obj.data
        if prev == pres:
            pass
        else:
            print("Type:",obj.type)
            #print("Data: ",obj.data)
            qr_code_data = obj.data.decode("utf-8")
            print("QR Code Data:", qr_code_data)
            
            # Extract numbers from the QR code data using regular expression
            numbers = re.findall(r'\d+', qr_code_data)
            if numbers:
                
                number= int(numbers[0])  # Return the first number found
                full_url = f"{web_url}/{number}/json"
                print(full_url)
                fetch_and_print_patient_data(full_url)
            
            else:
                print("No number found in QR code data")
                
            
            prev=pres
        cv2.putText(frame, str(obj.data), (50, 50), font, 2,
                    (255, 0, 0), 3)
 
    cv2.imshow("live transmission", frame)
 
    key = cv2.waitKey(1)
    if key == 27:
        break
 
cv2.destroyAllWindows()
