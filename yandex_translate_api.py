import requests
import json


class API(object):
    ERROR_TEXT = '😩' 

    def __init__(self, api_key, url='https://translate.yandex.net/api/', version='1.5'):
        self.api_key = api_key
        self._api_root = f'{url}v{version}/'

    def translate_text(self, text, to_lang='en') -> str:
        url = API._build_translate_text_url(self._api_root, self.api_key, text, to_lang)
        response = json.loads(requests.get(url).content)
        if response['code'] == 200:
            return response['text'][0]
        return API.ERROR_TEXT

    @staticmethod
    def _build_translate_text_url(api_root, api_key, text, to_lang) -> str:
        return f'{api_root}tr.json/translate?key={api_key}&text={text}&lang={to_lang}'