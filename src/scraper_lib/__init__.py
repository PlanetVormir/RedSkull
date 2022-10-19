from datetime import timedelta
from urllib.parse import quote_plus
from http.client import responses as error_messages

import requests
import requests_cache

if __name__ == "__main__":
    from response_parsers import *
    from reverse_engineered import *
else:
    from .response_parsers import *
    from .reverse_engineered import *


class RedSkull:
    BASE_URL = "https://hdtoday.ru"
    HEADERS = {
        'sec-ch-ua': '"Not A;Brand";v="99", "Chromium";v="106", "Google Chrome";v="106"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/106.0.0.0 Safari/537.36',
    }
    SUPPORTED_SERVERS = [
        "filemoon"
    ]

    def __init__(self, headers=None):
        self.headers = headers or self.HEADERS
        self.session = requests_cache.CachedSession('requests_cache', expire_after=timedelta(minutes=30))
        self.session.headers.update(self.headers)
        self.__set_session_cookie()

    def __endpoint(self, path: str) -> str:
        # Returns a full URL by appending path to BASE_URL
        return self.BASE_URL.removesuffix("/") + "/" + path.removeprefix("/")

    def __get_endpoint(self, endpoint: str) -> requests.Response:
        with self.session.get(self.__endpoint(endpoint)) as response:
            if not response.ok:
                raise Exception(
                    f"HTTP Error {response.status_code}: {error_messages.get(response.status_code)}"
                )
        return response

    def __set_session_cookie(self):
        self.__get_endpoint("ajax/user/panel")

    @staticmethod
    def __vrf(query):
        return quote_plus(vrf_generator(query))

    def __media_id_info(self, media_id: str) -> str:
        media_code = media_id.split("-")[-1]
        vrf = self.__vrf(media_code)
        response = self.__get_endpoint(f"ajax/film/servers?id={quote_plus(media_code)}&vrf={vrf}")
        return response.json()["html"]

    def search(self, keyword: str, page_no: int = 1) -> dict:
        vrf = self.__vrf(keyword)
        response = self.__get_endpoint(f"search?vrf={vrf}&keyword={quote_plus(keyword)}&page={page_no}")
        html = response.content.decode()
        return Search(html).parse()

    def series(self, media_id: str) -> dict:
        html = self.__media_id_info(media_id)
        return Series(html, self.SUPPORTED_SERVERS).parse()

    def movie(self, media_id: str) -> dict:
        html = self.__media_id_info(media_id)
        return Movie(html, self.SUPPORTED_SERVERS).parse()

    def episode(self, episode_id: str) -> dict:
        response = self.__get_endpoint(f"ajax/episode/info?id={episode_id}")
        encrypted_url = response.json()["url"]
        iframe_url = encrypted_url_decoder(encrypted_url)
        return Episode(self.session, iframe_url).parse()

    def trending(self):
        response = self.__get_endpoint("home")
        html = response.content.decode()
        return Trending(html).parse()
