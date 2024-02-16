# Importing all necessary libraries 
import cv2 
import os 

# Read the video from specified path 
cam = cv2.VideoCapture("four.mp4") 

try: 
	
	# creating a folder named data 
	if not os.path.exists('data_4'): 
		os.makedirs('data_4') 

# if not created then raise error 
except OSError: 
	print ('Error: Creating directory of data') 

# frame 
currentframe = 0

while(True): 
	
	# read every fifth frame
    for i in range(5):
        ret,frame = cam.read()
        # print("Frame queried.")

    if ret:
		# print("Frame retrieved.")
		# if video is still left continue creating images
        name = './data_4/frame' + str(currentframe) + '.jpg'
        print ('Creating...' + name)
		
        # Extracting size
        h, w, channels = frame.shape
        half = h//2
		
        # Crop image
        top = frame[:half, :]
		
        # Resize cropped image
        top = cv2.resize(top, (w, h))

		# writing the extracted images
        cv2.imwrite(name, top)

		# increasing counter so that it will
		# show how many frames are created
        currentframe += 1
    else:
	    break

# Release all space and windows once done 
cam.release() 
cv2.destroyAllWindows() 
