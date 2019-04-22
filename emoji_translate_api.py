import requests
from bs4 import BeautifulSoup


class API(object):
    def __init__(self, url='http://superemojitranslator.com/emoji-translate'):
        self._api_url = url

    def translate_to_emojies(self, text) -> str:
        data = {'phrase-to-translate': text}
        response = requests.post(self._api_url, data)
        parsed_html = BeautifulSoup(response.text, features='html5lib')
        translated_text = parsed_html.body.find(
            'textarea', attrs={'name': 'translated-phrase'}).text
        return translated_text
