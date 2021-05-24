import cv2
import os
import io
import PySimpleGUI as gui
from PIL import Image

# face recogition func
def faceRecog(inpImg):

    cv2_directory = os.path.dirname(cv2.__file__)

    faceCascade = cv2.CascadeClassifier(cv2_directory + '\data\haarcascade_frontalface_alt.xml')

    grayImg = cv2.cvtColor(inpImg, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(grayImg)

    for (column, row, width, height) in faces:
        cv2.rectangle(inpImg, (column,row), (column+width, row+height), (0,0,255), 3)

def cameraFaceRecog():
    print("Loading camera")
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Error opening camera")
    else:
        print("Camera opened")
        while True:
            ret, frame = camera.read()
            faceRecog(frame)
            if ret:
                cv2.imshow('LiveCam', frame)
            else:
                print("Frame read error")
            # q button to quit
            if cv2.waitKey(1) == ord('q'):
                break

    camera.release()
    cv2.destroyAllWindows()

def faceRecogByFilename(fileName):
    inpImg = cv2.imread(fileName)
    faceRecog(inpImg)
    return inpImg

def simpleImageFaceRecogeExample():
    cv2.imshow("Result", faceRecogByFilename('input_img.jpg'))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def loadImagesAndDetectFaces():
    windowImages = gui.Window(
        "Select images",
        [
            [
                gui.Column(
                    [
                        [gui.Button("CLOSE")],
                        [
                            gui.Text("Image Folder"),
                            gui.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
                            gui.FolderBrowse(),
                        ],
                        [
                            gui.Listbox(
                                values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
                            )
                        ],
                    ]
                ),
                gui.VSeperator(),
                gui.Column(
                    [
                        [gui.Text("Choose an image from list on left:")],
                        [gui.Text(size=(40, 1), key="-TOUT-")],
                        [gui.Image(key="-IMAGE-")],
                    ]
                ),
            ]
        ]
    )

    # Create an event loop
    while True:
        event, values = windowImages.read()
        # End program if user closes window or
        # presses the OK button
        # Folder name was filled in, make a list of files in the folder
        if event == "-FOLDER-":
            folder = values["-FOLDER-"]
            try:
                # Get list of files in folder
                file_list = os.listdir(folder)
            except:
                file_list = []

            fnames = [
                f
                for f in file_list
                if os.path.isfile(os.path.join(folder, f))
                and f.lower().endswith((".png"))
            ]
            windowImages["-FILE LIST-"].update(fnames)
        elif event == "-FILE LIST-":  # A file was chosen from the listbox
            try:
                nameOfFile = os.path.join(
                    values["-FOLDER-"], values["-FILE LIST-"][0]
                )
                windowImages["-TOUT-"].update(nameOfFile)
                imageWithFaces = faceRecogByFilename(nameOfFile)
                im_resize = cv2.resize(imageWithFaces, (500, 500))
                is_success, im_buf_arr = cv2.imencode(".png", im_resize)

                if is_success:
                    io_buf = io.BytesIO(im_buf_arr)
                    byte_im = io_buf.getvalue()
                    windowImages["-TOUT-"].update(nameOfFile + ' face detected')
                    windowImages["-IMAGE-"].update(data=byte_im)
            except:
                pass
        elif event == "CLOSE" or event == gui.WIN_CLOSED:
            break
        elif event == "YOUR IMAGES FACE DETECT":
            loadImagesAndDetectFaces()
        elif event == "EXAMPLE":
            simpleImageFaceRecogeExample()
        elif event == "CAMERA":
            cameraFaceRecog()

    windowImages.close()

#main code
window = gui.Window(
    "Face Recognition by Sebastian Pytel",
    [
        [gui.Text("Face Recognition by Sebastian Pytel")],
        [gui.Button("YOUR IMAGES FACE DETECT")],
        [gui.Button("EXAMPLE")],
        [gui.Button("CAMERA")],
        [gui.Button("CLOSE")],
    ]
)

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "CLOSE" or event == gui.WIN_CLOSED:
        break
    elif event == "YOUR IMAGES FACE DETECT":
        loadImagesAndDetectFaces()
    elif event == "EXAMPLE":
        simpleImageFaceRecogeExample()
    elif event == "CAMERA":
        cameraFaceRecog()

window.close()

