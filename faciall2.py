import boto3
import pprint

# Create a boto client that links to my aws bucket and  aws acc
client = boto3.client('rekognition',
                      aws_access_key_id="AKIATUBYJEPR5VOZWT67",
                      aws_secret_access_key="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",
                      region_name="us-east-1"
                      )

# user interaction of choice
Choice = input("What would you like to do?"
               "  1 : extract texts"
               "  2: detect labels"
               "  3: face comparison"
               "  4: face mood ")


# This function extracts texts in images
# It can be used to track number plates and other relevant texts in pictures.
def detect_texts():
    imageChoice = input("Do you want to access default images or set up your own(Y/N)")
    if imageChoice == "Y":
        print("Accessing saved images in AWS")
        response = client.detect_text(
            Image={
                'S3Object': {
                    'Bucket': 'faciallimages',
                    'Name': 'numberplate.jpg'
                }
            },
        )
        pprint.pprint(response)
    else:
        print("Upload a new image in the bucket in the aws account")


# measures and defines images, can be used to explain graphical images
# I used a building in this case
def detect_labels():
    response = client.detect_labels(
        Image={
            'S3Object': {
                'Bucket': 'faciallimages',
                'Name': 'sample.jfif'
            }
        },
        MaxLabels=5,
        MinConfidence=75
    )
    pprint.pprint(response)


# define similarities between faces
key_source = 'KIM DS160.jpg'
key_target = 'WIN_20211225_12_20_29_Pro.jpg'


def face_comparison(key_source, key_target):
    print("Using pre-defined images")
    response = client.compare_faces(
        SourceImage={
            "S3Object": {
                "Bucket": 'faciallimages',
                "Name": key_source,
            }
        },
        TargetImage={
            "S3Object": {
                "Bucket": 'faciallimages',
                "Name": key_target
            }
        },
        SimilarityThreshold=75,
    )
    return response['SourceImageFace'], response['FaceMatches']


source_face, matches = face_comparison(key_source, key_target)
print("Source Face ({Confidence}%)".format(**source_face))
for match in matches:
    print("Target Face ({Confidence}%)".format(**match['Face']))
    print("  Similarity : {}%".format(match['Similarity']))


# This function is expected to define the mood of the face
def face_mood():
    response = client.detect_faces(
        Image={
            'S3Object': {
                'Bucket': 'faciallimages',
                'Name': 'KIM DS160.jpg'
            }
        },
        Attributes=['ALL']
    )
    pprint.pprint(response['FaceDetails'])


# calling the functions depending on what you would like to execute
if Choice == "extract texts":
    detect_texts()

if Choice == "detect labels":
    detect_labels()

if Choice == "face comparison":
    face_comparison(key_source, key_target)

elif Choice == "face mood":
    face_mood()

else:
    print("Undefined choice, please rerun")
