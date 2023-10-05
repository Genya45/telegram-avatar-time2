from datetime import datetime
import numpy as np
import cv2

counter = 8
def getColor():
    global counter
    counter = counter + 1
    if counter > 5:
        counter = 0
        
    if counter == 0:
        return((255, 255, 255))
    if counter == 1:
        return((0, 255, 0))
    if counter == 2:
        return((0, 0, 255))
    if counter == 3:
        return((255, 255, 0))
    if counter == 4:
        return((255, 0, 255))
    if counter == 5:
        return((0, 255, 255))

def convert_time_to_string(dt):
    return dt.strftime("%H:%M")  # f"{dt.hour}:{dt.minute:02}"

def time_has_changed(prev_time):
    return convert_time_to_string(datetime.now()) != convert_time_to_string(prev_time)


def get_black_background():
    return np.zeros((500, 500))


def generate_time_image_bytes(dt):
    text = convert_time_to_string(dt)
    #image = get_black_background()
    #image = cv2.imread('/home/tg_time/telegram-avatar-time/utils/photo3.png')
    image = cv2.imread('photo.png')
    #print(image)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, text, (int(image.shape[0]*0.01), int(image.shape[1]*0.62)), font, 7, getColor(), 10, cv2.LINE_AA)
    _, bts = cv2.imencode('.jpg', image)
    return bts.tobytes()
