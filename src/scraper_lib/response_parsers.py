import re
from json import loads as parse_json
from bs4 import BeautifulSoup, element
from urllib.parse import urlparse, parse_qs
from http.client import responses as error_messages

import dukpy

__all__ = ["Search", "Series", "Movie", "Episode"]


class Search:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, "html.parser")

    def parse(self) -> dict:
        return {
            "max_page_no": self.__parse_max_page_no(),
            "results": self.__parse_results()
        }

    def __parse_max_page_no(self) -> int:
        navigation_anchor_tags = self.soup.select("div.content > div.pagenav > ul.pagination > li > a")
        for i, anchor_tag in enumerate(navigation_anchor_tags):
            is_arrow_key_anchor = bytes(anchor_tag.text, "utf8") == b"\xc2\xbb"
            is_last_page_anchor = is_arrow_key_anchor or ((i + 1) == len(navigation_anchor_tags))
            if not is_last_page_anchor:
                continue
            navigation_url = urlparse(anchor_tag["href"])
            page_no = parse_qs(navigation_url.query)["page"][0]
            return int(page_no)

    def __parse_results(self) -> list:
        results = []
        for item in self.soup.select("div.filmlist > div.item"):
            results.append(self.__parse_result(item))
        return results

    @staticmethod
    def __parse_result(item: element.Tag) -> dict:
        return {
            "title": elems[0]["title"] if (elems := item.select("a.poster")) else None,
            "poster": elems[0]["src"] if (elems := item.select("a.poster > img")) else None,
            "quality": elems[0].text.strip() if (elems := item.select("div.icons > div.quality")) else None,
            "rating": elems[0].text.strip() if (elems := item.select("span.imdb")) else None,
            "type": elems[0].text.strip() if (elems := item.select("div.meta > i.type")) else None,
            "media_id": elems[0]["href"] if (elems := item.select("a.poster")) else None,
        }


class Series:
    def __init__(self, html, supported_servers):
        self.soup = BeautifulSoup(html, "html.parser")
        self.supported_servers = supported_servers
        self.servers = self.__parse_servers()

    def parse(self):
        return {
            "servers": self.servers,
            "episodes": self.__parse_series()
        }

    def __parse_servers(self) -> dict:
        servers = {}

        for item in self.soup.select("div#servers > div.server"):
            server_name = elems[0].text.strip().lower() if (elems := item.select("div")) else None
            is_valid_server = (server_name is not None) and (server_name in self.supported_servers)

            if is_valid_server:
                server_id = item["data-id"].strip()
                servers[server_name] = server_id

        return servers

    def __parse_series(self) -> dict:
        series = {}

        for item in self.soup.select("div#episodes > div.episodes"):
            season = int(item["data-season"])
            series[season] = self.__parse_episodes(item)

        return series

    def __parse_episodes(self, item: element.Tag) -> dict:
        episodes = {}

        for episode in item.select("div.range > div.episode > a"):
            episode_number = episode["data-kname"].removesuffix("-end").split("-")[-1]
            episode_number = int(episode_number) if episode_number != "full" else 1
            episodes[episode_number] = self.__parse_episode(episode)

        return episodes

    def __parse_episode(self, item: element.Tag) -> dict:
        return {
            "name": item.select("span.name")[0].text,
            "date": item["title"].split(" - ")[-1],
            "sources": self.__parse_episode_sources(parse_json(item["data-ep"]))
        }

    def __parse_episode_sources(self, data: dict) -> dict:
        supported_server_ids = self.servers.values()
        sources = {
            server_id: episode_id for server_id, episode_id in data.items() if server_id in supported_server_ids
        }

        return sources


class Movie:
    def __init__(self, html, supported_servers):
        self.__series_data = Series(html, supported_servers).parse()

    def parse(self):
        server_map = {
            server_id: server_name for server_name, server_id in self.__series_data["servers"].items()
        }
        sources = self.__series_data["episodes"][1][1]["sources"]
        sources = {
            server_map[server_id]: episode_id for server_id, episode_id in sources.items()
        }
        return sources


class Episode:
    def __init__(self, session, iframe_url):
        self.session = session
        self.iframe_url = iframe_url

    def parse(self):
        return {
            "url": self.__get_m3u8_url()
        }

    def __get_m3u8_url(self):
        if "filemoon" in self.iframe_url:
            return self.__filemoon_parser()
        return ""

    def __filemoon_parser(self):
        # fetch HTML contents from URL
        with self.session.get(self.iframe_url) as response:
            if not response.ok:
                raise Exception(
                    f"HTTP Error {response.status_code}: {error_messages.get(response.status_code)}"
                )

        # Find the script with player information
        soup = BeautifulSoup(response.content.decode(), "html.parser")
        script = None
        for script_tag in soup.select("script"):
            if script_tag.text.startswith("eval"):
                script = script_tag.text.removeprefix("eval")

        if script is None:
            raise Exception("Unable to find player information script from FileMoon Server")

        # Find m3u8 URL inside script
        script = dukpy.evaljs(script)
        url = re.search(
            r'file\s*:\s*"((http|ftp|https)://([\w_-]+(?:\.[\w_-]+)+)([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-]))"',
            script
        ).group(1)

        if "m3u8" in url:
            return url

        raise Exception("Unable to find m3u8 URL from FileMoon Server")
