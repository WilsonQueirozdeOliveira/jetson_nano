# import the opencv library
import cv2
  
  
# define a video capture object
# 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3280, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method=0 ! video/x-raw, width=320, height=240, format=BGRx ! videoconvert ! video/x-raw,format=BGR ! appsink'
vid = cv2.VideoCapture(
    'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=1920, height=1080, format=NV12, framerate=29/1 ! nvvidconv flip-method=0 ! video/x-raw, width=960, height=540, format=BGRx ! videoconvert ! video/x-raw,format=BGR ! appsink'
    , cv2.CAP_GSTREAMER)
  
while(True):
      
    # Capture the video frame
    # by frame
    ret, frame = vid.read()
  
    # Display the resulting frame
    cv2.imshow('frame', frame)
      
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()