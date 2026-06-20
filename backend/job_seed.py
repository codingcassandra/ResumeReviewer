import requests
from bs4 import BeautifulSoup
import re


def clean_text(text: str) -> str:
    # remove extra whitespace
    text = re.sub(r'\s+', ' ', text)

    # remove weird unicode artifacts
    text = text.replace("\xa0", " ")

    return text.strip()


def extract_job_from_url(url: str):

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X)"
        }

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        # remove junk tags
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        # try to focus on job-like containers first
        main_content = soup.find("main")

        if main_content:
            text = main_content.get_text(separator=" ")
        else:
            text = soup.get_text(separator=" ")

        text = clean_text(text)

        # heuristics: trim to job-relevant portion
        keywords = ["responsibilities", "requirements", "qualifications", "what you'll do"]

        # try to find job section start
        lower_text = text.lower()
        start_index = 0

        for kw in keywords:
            idx = lower_text.find(kw)
            if idx != -1:
                start_index = min(idx, start_index) if start_index else idx

        text = text[start_index:] if start_index else text

        # limit size for LLM
        return text[:6000]

    except Exception as e:
        return None