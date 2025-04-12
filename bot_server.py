from flask import Flask, request
import requests
import os

BOT_TOKEN = '7628414959:AAET9VmwCMNLjeH06GU_VsaEfArwDuKPY5M'
DOWNLOAD_URL = f'https://api.telegram.org/file/bot{BOT_TOKEN}/'
API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/'

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()

    if 'message' in data and 'photo' in data['message']:
        chat_id = data['message']['chat']['id']
        photo = data['message']['photo'][-1]
        file_id = photo['file_id']

        file_info = requests.get(API_URL + f'getFile?file_id={file_id}').json()
        file_path = file_info['result']['file_path']

        file_url = DOWNLOAD_URL + file_path
        img_data = requests.get(file_url).content
        file_name = f'dog_{file_id}.jpg'
        with open(file_name, 'wb') as f:
            f.write(img_data)

        # Phản hồi
        requests.post(API_URL + 'sendMessage', json={
            'chat_id': chat_id,
            'text': f'Đã lưu ảnh: {file_name}'
        })

    return 'ok'

if __name__ == '__main__':
    app.run(port=5000)