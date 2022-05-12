import PySimpleGUI as sg
import boto3
import pathlib
import io
import os
from PIL import Image


# establishing connection to aws cloud
client = boto3.client("s3",
                      aws_access_key_id="AKIATUBYJEPR5VOZWT67",
                      aws_secret_access_key="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",
                      region_name="us-east-1"
                      )

BASE_DIR = pathlib.Path(__file__).parent.resolve()
Bucket_Name = "faciallimages"
sg.theme('Topanga')
sg.set_options(font='Courier 16')

file_types = [("JPEG (*.jpg)", "*.jpg"),
              ("All files (*.*)", "*.*")]


def load_image(file_name, window):
    if os.path.exists(file_name):
        image = Image.open(values['saved'])
        image.thumbnail((400, 400))
        bio = io.BytesIO()
        image.save(bio, format="PNG")
        window['Image'].update(bio.getvalue())


def upload_file(file_name, bucket, object_name=None, args=None):
    if object_name is None:
        object_name = file_name

    client.upload_file(file_name, bucket, object_name, ExtraArgs=args)
    sg.popup("File Uploaded")


def detect_texts(file_name):
    client = boto3.client("rekognition",
                          aws_access_key_id="AKIATUBYJEPR5VOZWT67",
                          aws_secret_access_key="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",
                          region_name="us-east-1"
                          )
    response = client.detect_text(
        Image={
            'S3Object': {
                'Bucket': f'{Bucket_Name}',
                'Name': f'{file_name}'
            }
        },
    )
    window2['Output'].update(response['TextDetections'])


def detect_labels(file_name):
    client = boto3.client("rekognition",
                          aws_access_key_id="AKIATUBYJEPR5VOZWT67",
                          aws_secret_access_key="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",
                          region_name="us-east-1"
                          )
    response = client.detect_labels(
        Image={
            'S3Object': {
                'Bucket': f'{Bucket_Name}',
                'Name': f'{file_name}'
            }
        },
        MaxLabels=5,
        MinConfidence=75
    )
    sg.PopupOK(response)


def face_comparison(file_name1, file_name2):
    client = boto3.client("rekognition",
                          aws_access_key_id="AKIATUBYJEPR5VOZWT67",
                          aws_secret_access_key="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",
                          region_name="us-east-1"
                          )
    response = client.compare_faces(
        SourceImage={
            'S3Object': {
                'Bucket': f'{Bucket_Name}',
                "Name": f'{file_name1}',
            }
        },
        TargetImage={
            'S3Object': {
                'Bucket': f'{Bucket_Name}',
                'Name': f'{file_name2}'
            }
        },
        SimilarityThreshold=75,
    )
    sg.PopupOK(response['FaceMatches'])


def face_mood(file_name):
    client = boto3.client("rekognition",
                          aws_access_key_id="AKIATUBYJEPR5VOZWT67",
                          aws_secret_access_key="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",
                          region_name="us-east-1"
                          )
    response = client.detect_faces(
        Image={
            'S3Object': {
                'Bucket': f'{Bucket_Name}',
                'Name': f'{file_name}'
            }
        },
        Attributes=['ALL'],
    )
    window5['Output'].update(response['FaceDetails'])


def layout1():
    layout1 = [
        [sg.T("HOME")],
        [sg.Button('EXTRACT TEXTS', key='extract')],
        [sg.Button('DETECT LABELS', key='labels')],
        [sg.Button('FACE COMPARISON', key='comparison')],
        [sg.Button('FACE MOOD', key='mood')],
        [sg.Button('Exit', key='-exit-')]
    ]
    return layout1


def layout2():
    layout2 = [
        [sg.T("Extract texts from images")],
        [sg.Input('Use Saved Images', key='saved'), sg.FileBrowse()],
        [sg.Button('Load Image', key='picture')],
        [sg.Image(key='Image')],
        [sg.Output(key='Output')],
        [sg.OK(key='ok'), sg.Button('Exit', key='-exit-')]
    ]
    return layout2


def layout3():
    layout3 = [
        [sg.T("Detect Labels from images")],
        [sg.Input('Use Saved Images', key='saved'), sg.FileBrowse()],
        [sg.Button('Load Image', key='picture')],
        [sg.Image(key='Image')],
        [sg.OK(key='ok'), sg.Button('Exit', key='-exit-')]
    ]
    return layout3


def layout4():
    layout4 = [
        [sg.T("Face Similarity")],
        [sg.Input('Use Saved Image1', key='saved1'), sg.FileBrowse()],
        [sg.Input('Use Saved Image2', key='saved2'), sg.FileBrowse()],
        [sg.Button('Load Image 1', key='picture1')], [sg.Button('Load Image 2', key='picture2')],
        [sg.Image(key='Image')],
        [sg.OK(key='ok'), sg.Button('Exit', key='-exit-')]
    ]
    return layout4


def layout5():
    layout5 = [
        [sg.T("Check Mood")],
        [sg.Input('Use Saved Images', key='saved'), sg.FileBrowse()],
        [sg.Button('Load Image', key='picture'), sg.Input()],
        [sg.Image(key='Image')],
        [sg.Output(key='Output')],
        [sg.OK(key='ok'), sg.Button('Exit', key='-exit-')]
    ]
    return layout5


window1 = sg.Window("HOME", layout1(), size=(500, 500))

while True:
    event, values = window1.read()
    if event == '-exit-':
        break
    if event == 'extract':
            window2 = sg.Window("Extract Texts..", layout2())
            event, values = window2.read()
            if event == '-exit-':
                window2.close()
            if event == 'picture':
                file_name = values['saved']
                window = window2
                load_image(file_name, window)
            if event == 'ok':
                file_name = values['saved']
                if file_name == '':
                    sg.popup_error("Missing File, Upload!")
                else:
                    try:
                         upload_file(file_name, Bucket_Name)
                         detect_texts(file_name)
                         window2['saved'].update('')
                    except:
                        sg.popup_error("Problem might have occured, check your code or aws s3")
    if event == 'labels':
            window3 = sg.Window("Detect Labels", layout3())
            event, values = window3.read()
            if event == '-exit-':
                window3.close()
            if event == 'picture':
                file_name = values['saved']
                window = window3
                load_image(file_name, window)
            if event == 'ok':
                file_name = values['saved']
                upload_file(file_name, Bucket_Name)
                detect_labels(file_name)
                window3['saved'].update('')
    if event == 'comparison':
            window4 = sg.Window("Face Comparison", layout4())
            event, values = window4.read()
            if event == '-exit-':
                window4.close()
            if event == 'picture1':
                file_name = values['saved1']
                window = window4
                load_image(file_name, window)
            if event == 'picture2':
                file_name = values['saved2']
                window = window4
                load_image(file_name, window)
            if event == 'ok':
                file_name1 = values['saved1']
                file_name2 = values['saved2']
                upload_file(file_name1, Bucket_Name)
                upload_file(file_name2, Bucket_Name)
                face_comparison(file_name1, file_name2)
                window4['saved1'].update('')
                window4['saved2'].update('')
    if event == 'mood':
            window5 = sg.Window("Check Mood", layout5())
            event, values = window5.read()
            if event == '-exit-':
                window5.close()
            if event == 'picture':
                file_name = values['saved']
                window = window5
                load_image(file_name, window)
            if event == 'ok':
                file_name = values['saved']
                upload_file(file_name, Bucket_Name)
                face_mood(file_name)
                window5['saved'].update('')

window1.close()
