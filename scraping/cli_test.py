import requests


def execute():
    print('コマンドが実行されました！')
    response = requests.get('https://www.google.com/')
    print(response.status_code)
