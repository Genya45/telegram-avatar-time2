from datetime import datetime
import numpy as np
import cv2
import requests
import os
from random import randint

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

def getNewPhoto():
    r = requests.get('https://thispersondoesnotexist.com/')

    if r.status_code == 200:
        # Получаем содержимое изображения
        image_content = r.content

        # Преобразовываем бинарные данные в объект изображения
        nparr = np.frombuffer(image_content, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Изменяем размер изображения
        desired_size = (640, 640)
        resized_image = cv2.resize(image, desired_size)
        
        return resized_image

        # Сохраняем изображение в формате PNG
        #cv2.imwrite('photoFace.png', resized_image)
        #print("Изображение сохранено успешно!")
    else:
        print("Ошибка при получении изображения:", r.status_code)

def getAnimePhoto():
    #r = requests.get('https://api.waifu.pics/sfw/waifu')
    r = requests.get('https://api.waifu.pics/nsfw/waifu')
    r = requests.get(r.json()['url'])

    if r.status_code == 200:
        # Получаем содержимое изображения
        image_content = r.content

        # Преобразовываем бинарные данные в объект изображения
        nparr = np.frombuffer(image_content, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        
        return image    



def generate_time_image_bytes(dt):
    text = convert_time_to_string(dt)
    #image = get_black_background()
    #image = cv2.imread('/home/tg_time/telegram-avatar-time/utils/photo3.png')
    
    
    #image = cv2.imread('photo.png')
    #image = getAnimePhoto()
    
    #image = getNewPhoto()
    
    
    
    image_folder = './img'
    img_list = os.listdir(image_folder)
    image_name = img_list[randint(0, len(img_list) - 1)]
    img_path = os.path.join(image_folder, image_name).encode('utf-8')
    image = cv2.imread(img_path.decode('utf-8'))
    
    #print(image)
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    
    #cv2.putText(image, text, (int(image.shape[0]*0.01), int(image.shape[1]*0.62)), font, 7, getColor(), 10, cv2.LINE_AA)
    
    
    _, bts = cv2.imencode('.jpg', image)
    return bts.tobytes()
