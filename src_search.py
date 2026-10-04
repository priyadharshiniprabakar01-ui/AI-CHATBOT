import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import trafilatura
import re


BASE_URL = "https://src.sastra.edu"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def clean_text(text):
    """Clean extracted webpage text."""

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def get_page_text(url):
    """Download and extract readable text from a webpage."""

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=20
        )

        response.raise_for_status()

        text = trafilatura.extract(
            response.text
        )

        if text:

            return clean_text(text)

        # Fallback
        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        for element in soup(
            ["script", "style", "nav", "footer"]
        ):
            element.decompose()

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        return clean_text(text)

    except Exception as e:

        print(f"Error reading {url}: {e}")

        return ""


def get_links(url):
    """Get links belonging to the SRC website."""

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=20
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        links = set()

        for a in soup.find_all(
            "a",
            href=True
        ):

            href = a["href"].strip()

            if not href:
                continue

            full_url = urljoin(
                url,
                href
            )

            parsed = urlparse(full_url)

            # Only keep SRC website links
            if parsed.netloc == urlparse(BASE_URL).netloc:

                # Remove fragments
                full_url = full_url.split("#")[0]

                links.add(full_url)

        return list(links)

    except Exception as e:

        print(f"Error getting links: {e}")

        return []


def search_src_website(question):
    """
    Search SRC website pages and return
    the most relevant pages.
    """

    print("\n🔎 Searching SRC website...")

    # Get homepage
    homepage_text = get_page_text(
        BASE_URL
    )

    # Get links from homepage
    links = get_links(
        BASE_URL
    )

    print(
        f"Found {len(links)} SRC website links."
    )

    pages = []

    # Add homepage
    if homepage_text:

        pages.append({
            "url": BASE_URL,
            "text": homepage_text
        })

    # Read linked pages
    for index, link in enumerate(
        links[:30],
        start=1
    ):

        print(
            f"Reading page {index}/30: {link}"
        )

        text = get_page_text(
            link
        )

        if text:

            pages.append({
                "url": link,
                "text": text
            })

    # ----------------------------------------
    # SCORE PAGES
    # ----------------------------------------

    question_words = set(
        re.findall(
            r"\b[a-zA-Z]{3,}\b",
            question.lower()
        )
    )

    scored_pages = []

    for page in pages:

        text_lower = page["text"].lower()

        score = 0

        for word in question_words:

            if word in text_lower:

                score += 1

        scored_pages.append(
            (
                score,
                page
            )
        )

    # Highest score first
    scored_pages.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return scored_pages[:5]