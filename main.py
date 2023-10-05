import time
from telethon import TelegramClient
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
from telethon.tl.functions.account import UpdateUsernameRequest
import random
import requests

from telethon.tl.functions.account import UpdateProfileRequest
from config import api_hash, api_id
from utils import time_has_changed, generate_time_image_bytes
from datetime import datetime, timedelta
import argparse
import pytz

from get_name_and_photo import get_img_and_name


def valid_tz(s):
    try:
        return pytz.timezone(s)
    except:
        msg = "Not a valid tz: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


parser = argparse.ArgumentParser()
parser.add_argument("--api_id", required=False, help="user api ID", type=str, default=api_id)
parser.add_argument("--api_hash", required=False, help="user api Hash", type=str, default=api_hash)
parser.add_argument("--tz", required=False,  help="user api Hash", type=valid_tz, default=valid_tz('Europe/Kiev'))

args = parser.parse_args()

client = TelegramClient("carpediem", args.api_id, args.api_hash)
client.start()


async def main():
    prev_update_time = datetime.now() - timedelta(minutes=1)
    timerCount = 0
    aboutTimer = datetime.now()

    while True:
        if datetime.now().day - aboutTimer.day >= 1 or  datetime.now().day < aboutTimer.day:
        #if datetime.now().second - aboutTimer.second >= 5 or  datetime.now().second < aboutTimer.second:
            array = 0
            with open("citats.txt", encoding='utf-8') as file:
                array = [row.strip() for row in file]
                
                
            aboutTimer = datetime.now()
            timerCount = timerCount + 1
            #print('hello' + str(datetime.now().second))
            citata = 'Цитата дня: «'+ array[random.randint(0, len(array)-1)] + '»'
            print(citata)
            #await client(UpdateProfileRequest(first_name='Іван Франко (Каменяр) ' + str(timerCount)))
            await client(UpdateProfileRequest(about=citata))
            #await client(UpdateUsernameRequest('Test' + str(datetime.now().second)))

        if time_has_changed(prev_update_time):
            '''
            r = requests.get('https://randomuser.me/api/?nat=ua&randomapi')
            first_name = r.json()['results'][0]['name']['first']
            last_name = r.json()['results'][0]['name']['last']            
            minuteValue = datetime.now().minute
            myName = first_name + ' ' + last_name + ' ' + str((datetime.now().hour + 3) % 24) + ':' + (str(minuteValue) if minuteValue > 10 else ('0' + str(minuteValue)))
            
            #await client(UpdateUsernameRequest(myName))
            await client(UpdateProfileRequest(first_name=myName))            
            bts = generate_time_image_bytes(datetime.now(args.tz).replace(tzinfo=None))
            '''
            bts, myName = get_img_and_name()
            await client(UpdateProfileRequest(first_name=myName))            
            await client(UpdateProfileRequest(about=myName))
            
            
            await client(DeletePhotosRequest(await client.get_profile_photos('me')))
            file = await client.upload_file(bts)
            await client(UploadProfilePhotoRequest(file=file))
            prev_update_time = datetime.now()
            time.sleep(1)
            #print('or')
        time.sleep(1)
        #print('help' + str(datetime.now().second))
        #await client(UpdateProfileRequest(about='Test ' + str(datetime.now().second)))
            

if __name__ == '__main__':
    import asyncio
    asyncio.get_event_loop().run_until_complete(main())
