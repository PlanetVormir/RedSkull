import dukpy
from urllib.parse import quote

__all__ = ["vrf_generator", "encrypted_url_decoder"]


def __encrypt(search_query, key="DZmuZuXqa9O0z3b7"):
    string = ""
    array = list(range(256))

    e = 0
    for u in range(256):
        e = (e + array[u] + ord(key[u % len(key)])) % 256
        i = array[u]
        array[u] = array[e]
        array[e] = i

    e, u = 0, 0
    for c in range(len(search_query)):
        u = (u + 1) % 256
        e = (e + array[u]) % 256
        i = array[u]
        array[u] = array[e]
        array[e] = i
        string += chr(ord(search_query[c]) ^ array[(array[u] + array[e]) % 256])
    return string


def __hash(n: str):
    u = ""
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

    for char in n:
        if ord(char) > 255:
            return

    for i in range(0, len(n), 3):
        array4 = [None, None, None, None]
        array4[0] = ord(n[i]) >> 2
        array4[1] = (3 & ord(n[i])) << 4
        if len(n) > i + 1:
            array4[1] |= ord(n[i + 1]) >> 4
            array4[2] = (15 & ord(n[i + 1])) << 2
        if len(n) > i + 2:
            array4[2] |= ord(n[i + 2]) >> 6
            array4[3] = 63 & ord(n[i + 2])

        for f in range(len(array4)):
            if array4[f] is None:
                u += "="
            else:
                t = array4[f]
                if 0 <= t and (t < 64):
                    u += characters[t]

    return u


def vrf_generator(query: str) -> str:
    return __hash(__encrypt(quote(query)))


def encrypted_url_decoder(encrypted_url):
    js_file_path = __file__.removesuffix("/__init__.py") + "/url_parser.js"
    with open(js_file_path) as js_file:
        javascript = js_file.read() + '\n' + f"main('{encrypted_url}')"
    return dukpy.evaljs(javascript)
