
import boto3 
def detect_labels_local_file(photo):


    client = boto3.client('rekognition')
   
    with open(photo, 'rb') as image:
        response = client.detect_labels(Image={'Bytes': image.read()})
   
    result = []
   
    for lable in response["Labels"]:
        name = lable["Name"]
        confidence = lable["Confidence"]
        result.append(f"{name}:{confidence:.2f}%")
    
    
    r= "<br/>".join(map(str, result))
    return r




import boto3

def compare_faces(sourceFile, targetFile):

    
    client = boto3.client('rekognition')

    imageSource = open(sourceFile, 'rb')
    imageTarget = open(targetFile, 'rb')

    response = client.compare_faces(SimilarityThreshold=0,
                                    SourceImage={'Bytes': imageSource.read()},
                                    TargetImage={'Bytes': imageTarget.read()})

    for faceMatch in response['FaceMatches']:
        # position = faceMatch['Face']['BoundingBox']
        similarity = faceMatch['Similarity']
    imageSource.close()
    imageTarget.close()
    return f"동일 인물일 확률은 {similarity:.2f}%입니다."
