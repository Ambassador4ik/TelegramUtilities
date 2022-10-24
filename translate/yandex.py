from data import config
import requests
from datetime import datetime


class YandexTranslator:
    def __init__(self):
        self.data = '{"yandexPassportOauthToken":"' + config.yandex_token + '"}'
        response = requests.post('https://iam.api.cloud.yandex.net/iam/v1/tokens', headers={}, data=self.data).json()
        self.iamToken = response['iamToken']
        tokenexpires = response['expiresAt'][:-11]
        self.tokenExpiry = datetime.strptime(tokenexpires, "%Y-%m-%dT%H:%M:%S")

    def translate(self, text, lang):
        if self.tokenExpiry < datetime.now():
            response = requests.post('https://iam.api.cloud.yandex.net/iam/v1/tokens', headers={},
                                     data=self.data).json()
            self.iamToken = response['iamToken']
            tokenexpires = response['expiresAt'][:-11]
            self.tokenExpiry = datetime.strptime(tokenexpires, "%Y-%m-%dT%H:%M:%S")

        body = {
            "targetLanguageCode": lang,
            "texts": text,
            "folderId": config.yandex_folder_id,
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {0}".format(self.iamToken)
        }

        response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                                 json=body,
                                 headers=headers
                                 )

        return response.json()['translations'][0]['text']
