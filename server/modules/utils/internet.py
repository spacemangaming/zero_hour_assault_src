# URL functions written by nbm studios
import urllib.parse
import requests


def url_encode(url):
    return urllib.parse.quote(url)


def url_decode(url):
    return urllib.parse.unquote(url)


def url_get(url):
    try:
        raw_response = requests.get(url)
        return raw_response.text
    except:
        return "HTTP Request error!"


def url_post(url, params):
    try:
        raw_response = requests.post(url, params)
        return raw_response.text
    except:
        return ""
