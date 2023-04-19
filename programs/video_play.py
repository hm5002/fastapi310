import cv2
import numpy as np

async def videoplay(file_path):
    
    video_path = file_path
   
    cap = cv2.VideoCapture(video_path)
    
    fps = round(cap.get(cv2.CAP_PROP_FPS))
   
    print(fps)
    w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(w,h)
   
    file_name = video_path

    while True:
        ret, frame = cap.read()
       
        if not ret:
            break
        
        #frame = cv2.resize(frame, (w,h))
       
        frame_array = np.array(frame)

        cv2.imshow("Result", frame_array)
        
        cv2.waitKey(100)

    cv2.destroyAllWindows()

    return (file_name)
