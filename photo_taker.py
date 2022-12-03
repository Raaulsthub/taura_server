import cv2 as cv
import time
import boto3
import os


def main():

    cam_port = 0
    image_number = 0

    # aws client
    client = boto3.client('rekognition')

    some_one_entered = True

    # 1 photo per second loop
    while (some_one_entered):
        # capture photo
        cam = cv.VideoCapture(cam_port)    
        result, image = cam.read()
        # picture has been taken
        if result:
            print('Image taken and saved')
            image_name = 'image' + str(image_number) + '.png'
            cv.imwrite(str('./my_images/' + image_name), image)
            # aws analysis request
            time.sleep(1)
            for image in sorted(os.listdir('./my_images')):
                with open('my_images/' + image, 'rb') as image:
                    response = client.detect_faces(Image={'Bytes': image.read()}, Attributes=['ALL'])
            if(len(response) > 1):
                print('Person Detected')
                # salvar imagem + info no banco de dados
            else:
                print('No person detected...')
        # If captured image is corrupted, moving to else part
        else:
            print("ERROR! No image detected.")
        
        time.sleep(3)
        image_number += 1


if __name__ == "__main__":
    main()

