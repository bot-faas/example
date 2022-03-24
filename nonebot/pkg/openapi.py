import json
import requests
import os
import qqbot

token = qqbot.Token(os.environ.get("APP_ID"), os.environ.get("APP_TOKEN"))
sandbox = os.environ.get("SANDBOX_BOT") == "true"


def OpenAPI():
    return token, sandbox


def PicUpload(name, file):
    url = os.environ.get("HOME_URL")+"/api/v1/open/guild/pic"

    payload = {}
    files = [
        ('pic', (name, file, 'image/png'))
    ]
    sandbox = 0
    if os.environ.get("SANDBOX_BOT") == "true":
        sandbox = 1
    headers = {
        'X-AppId': os.environ.get("APP_ID"),
        'X-Sandbox': str(sandbox),
        'X-AppToken': os.environ.get("APP_TOKEN")
    }

    response = requests.request(
        "POST", url, headers=headers, data=payload, files=files)

    return json.loads(response.text)
