import argparse
import requests
from urllib.parse import urlparse
import os
import traceback
from requests.exceptions import HTTPError
from dotenv import load_dotenv


def shorten_link(long_url, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "long_url": long_url
    }
    url = "https://api-ssl.bitly.com/v4/shorten"
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    short_url = response.json()["link"]
    return short_url


def get_clicks_count(bitlink, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    url_components = urlparse(bitlink)
    domain = url_components.netloc
    bitlink_id = url_components.path.lstrip('/')
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{domain}/{bitlink_id}/clicks/summary"
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    clicks_count = response.json()['total_clicks']
    return clicks_count


def is_bitlink(short_url, token):
    headers = {
        "Authorization": "Bearer {}".format(token)
    }
    url_components = urlparse(short_url)
    domain = url_components.netloc
    bitlink_id = os.path.basename(url_components.path)
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{domain}/{bitlink_id}"
    response = requests.get(url, headers=headers)
    return response.ok


def main():
    parser = argparse.ArgumentParser(description='Сокращение ссылок с помощью Bitly')
    parser.add_argument('url', help='Ссылка для сокращения или битлинк для получения количества кликов')
    args = parser.parse_args()
    
    load_dotenv()
    token = os.getenv('BITLY_TOKEN')
    user_url = args.url
    
    if is_bitlink(user_url, token):
        try:
            clicks_count = get_clicks_count(user_url, token)
            print("Количество кликов : ", clicks_count)
        except requests.exceptions.RequestException as e:
            print("Не удалось получить количество кликов:")
            traceback.print_exc()
    else:
        try:
            shortened_link = shorten_link(user_url, token)
            print("Битли ", shortened_link)
        except requests.exceptions.RequestException as e:
            print("Не удалось сократить ссылку:")
            traceback.print_exc()


if __name__ == "__main__":
    main()
