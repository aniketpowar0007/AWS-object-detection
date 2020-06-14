import json
import boto3
from urllib.parse import unquote_plus
import cv2
import numpy as np

s3_client = boto3.client('s3')
dynamodb = boto3.client('dynamodb')
TABLE_NAME = 'tag-url' 
configThreshold = 0.5
nmsThreshold = 0.1

def lambda_handler(event, context):
    #1 get bucket name
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    #2 - Get the file/key name
    file_name = unquote_plus(event['Records'][0]['s3']['object']['key'])
    print("File {0} uploaded to {1} bucket".format(file_name, bucket_name))
    uploadedImage = s3_client.get_object(Bucket=bucket_name, Key=file_name)
    
    #Downloading weights file from s3 bucket
    weigth_bucket = 'serverless-object-detection'
    weigth_key = 'configuration-files/yolov3.weights'
    store_weigth_file = '/tmp/yolov3.weights'
    downloadFromBucket(weigth_bucket,weigth_key,store_weigth_file)
    
    #Downloading config file from s3 bucket
    cfg_key = 'configuration-files/yolov3.cfg'
    store_cfg_file = '/tmp/yolov3.cfg'
    downloadFromBucket(weigth_bucket,cfg_key,store_cfg_file)
    
    #Downloading labels from s3 bucket
    labels_key = 'configuration-files/coco.names'
    store_labels_file = '/tmp/coco.names'
    downloadFromBucket(weigth_bucket,labels_key,store_labels_file)
    
    strBucket = 'serverless-object-detection'
    strKey = file_name
    strWeightFile = '/tmp/uploaded_image.jpg'
    downloadFromBucket(strBucket,strKey,strWeightFile)
    
    # Storing the JSON object in the item variable
    data = {}
    data['url'] = {'S': 'https://layers-cloud.s3.amazonaws.com/'+strKey}
    data['tag'] = {'S':  str(get_prediction('/tmp/uploaded_image.jpg'))}
    print(data)
    
    # Strong the json object in the dynamo DB
    response = dynamodb.put_item(TableName=TABLE_NAME, Item=data)
    print(response)
   
    
def downloadFromBucket(Bucket_str,Key_str,File_str):
    s3 = boto3.client('s3')
    s3.download_file(Bucket_str, Key_str, File_str)
    
def get_prediction(image):
    
    image = cv2.imread(image)
    #image = cv2.resize(image, None, fx=0.4, fy=0.4)
    net = cv2.dnn.readNetFromDarknet('/tmp/yolov3.cfg', '/tmp/yolov3.weights')

    (H, W) = image.shape[:2]
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    layerOutputs = net.forward(ln)

    boxes = []
    confidences = []
    classIDs = []
    labels = open('/tmp/coco.names').read().strip().split("\n")
    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]
            if confidence > configThreshold:
                print(labels[classID])
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

    idxs = cv2.dnn.NMSBoxes(boxes, confidences, configThreshold,nmsThreshold)
    global objects
    objects = []
    np.random.seed(42)
    colors = np.random.randint(0, 255, size=(len(labels), 3), dtype="uint8")
    if len(idxs) > 0:
        for i in idxs.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            color = [int(c) for c in colors[classIDs[i]]]
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            tags = "{}".format(labels[classIDs[i]])
            objects.append(tags)
    return objects


