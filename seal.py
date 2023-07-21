#!/usr/bin/env python3
import os
from pathlib import Path as P
from random import choice
from time import sleep

import requests
from dotenv import load_dotenv
from pyperclip import copy

load_dotenv()

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")
PEXELS_BASE_URL = "https://api.pexels.com/v1/search"


def get_seal():
    if not PEXELS_API_KEY:
        raise ValueError("No PEXELS_API_KEY provided")
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": "seal", "per_page": 80}
    response = requests.get(PEXELS_BASE_URL, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    random_seal = choice(data["photos"])
    url_to_seal = random_seal["src"]["original"]
    author = random_seal["photographer"]
    return f"![seal]({url_to_seal})", author


def scrape_seal_urls():
    if not PEXELS_API_KEY:
        raise ValueError("No PEXELS_API_KEY provided")
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": "seal", "per_page": 80}
    response = requests.get(PEXELS_BASE_URL, headers=headers, params=params)
    if response.status_code == 429:
        print("Rate limit reached, sleeping 1 hour...")
        sleep(60 * 60)
        response = requests.get(PEXELS_BASE_URL, headers=headers, params=params)
    data = response.json()
    seal_urls = [seal["src"]["original"] for seal in data["photos"]]
    while next_page := data.get("next_page"):
        params["page"] = next_page
        response = requests.get(PEXELS_BASE_URL, headers=headers, params=params)
        if response.status_code == 429:
            print("Rate limit reached, sleeping 1 hour...")
            sleep(60 * 60)
            response = requests.get(PEXELS_BASE_URL, headers=headers, params=params)
        data = response.json()
        seal_urls.extend([seal["id"] for seal in data["photos"]])
    return seal_urls


def main():
    seal, author = get_seal()
    copy(seal)
    print("Copied seal to clipboard!")
    print(f"Seal by {author}")


if __name__ == "__main__":
    main()
