import requests
from bs4 import BeautifulSoup

class API(object):
    def __init__(self, url='http://superemojitranslator.com/emoji-translate'):
        self._api_url = url

    def translate_to_emojies(self, text) -> str:
        response = requests.post('http://superemojitranslator.com/emoji-translate',
                                 data={'phrase-to-translate': text})
        parsed_html = BeautifulSoup(response.text, features='html5lib')
        translated_text = parsed_html.body.find(
            'textarea', attrs={'name': 'translated-phrase'}).text
        return translated_text
