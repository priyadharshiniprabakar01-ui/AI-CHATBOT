import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


# ==================================================
# SETTINGS
# ==================================================

BASE_URL = "https://src.sastra.edu"

DB_FOLDER = "src_database"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


# ==================================================
# SRC IMPORTANT PEOPLE
# ==================================================

IMPORTANT_PEOPLE = """
SRC IMPORTANT PEOPLE AND ADMINISTRATION

Dean, Srinivasa Ramanujan Centre (SRC):
Dr. Santhi B

Dr. Santhi B is the Dean of Srinivasa Ramanujan Centre (SRC).
Her department is ICT.
Her educational qualifications include Ph.D. in Image Processing,
M.Tech in CSE, MCA, SLET, B.Ed and M.Sc. Mathematics.
Her areas of interest include Image Processing, Big Data Analytics,
Wireless Sensor Networks, Music Information Technology and Time Series Analysis.

Associate Dean — Infrastructure & Student Welfare:
Dr. Narasimhan D

Dr. Narasimhan D is the Associate Dean for Infrastructure
and Student Welfare at SRC.
His department is Mathematics.
His qualifications include M.Sc., M.Phil. and Ph.D.
His areas of interest include Bitopological Spaces, Graph Theory,
Deduplication and Data Analysis.

Associate Dean — Academics & Research:
Dr. Alli Rani A

Dr. Alli Rani A is the Associate Dean for Academics & Research at SRC.
Her department is Electronics and Communication Engineering.
Her qualifications include BE (ECE), ME (Communication System)
and Ph.D.
Her areas of interest include Signal Processing, Image Processing,
Wireless Sensor Networks and RF and Microwave Communication.

Associate NCC Officer:
Capt. T. Senthilnathan

Capt. T. Senthilnathan is the Associate NCC Officer at SRC.
He is an Assistant Professor in Mechanical Engineering.

SRC OFFICE CONTACT

Srinivasa Ramanujan Centre
Kumbakonam - 612001
Tamil Nadu, India

Office of Admissions:
0435-2426823

Official SRC Website:
https://src.sastra.edu/
"""


# ==================================================
# GET PAGE TEXT
# ==================================================

def get_page(url):

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

        for element in soup(
            ["script", "style", "nav", "footer"]
        ):
            element.decompose()

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        return text

    except Exception as e:

        print(
            f"❌ Could not read: {url}"
        )

        print(e)

        return ""


# ==================================================
# GET SRC LINKS
# ==================================================

def get_links(url):

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

            link = urljoin(
                url,
                a["href"]
            )

            parsed = urlparse(link)

            if parsed.netloc == "src.sastra.edu":

                link = link.split("#")[0]

                links.add(link)

        return list(links)

    except Exception as e:

        print("❌ Error getting links")

        print(e)

        return []


# ==================================================
# START
# ==================================================

print()
print("========================================")
print("🎓 SRC WEBSITE DATABASE BUILDER")
print("========================================")
print()


print("🔎 Finding SRC website pages...")

links = get_links(BASE_URL)

print(
    f"Found {len(links)} links."
)

print()


# Add homepage
if BASE_URL not in links:

    links.insert(
        0,
        BASE_URL
    )


# Limit
links = links[:50]


documents = []


# ==================================================
# DOWNLOAD WEBSITE PAGES
# ==================================================

for number, url in enumerate(
    links,
    start=1
):

    print(
        f"[{number}/{len(links)}] Reading:"
    )

    print(url)

    text = get_page(url)

    if not text:

        continue

    documents.append(
        Document(
            page_content=text,
            metadata={
                "source": url,
                "type": "official_src_website"
            }
        )
    )


print()
print(
    f"✅ Pages successfully loaded: {len(documents)}"
)


# ==================================================
# ADD IMPORTANT PEOPLE INFORMATION
# ==================================================

print()
print("👨‍🏫 Adding SRC administration information...")


documents.append(
    Document(
        page_content=IMPORTANT_PEOPLE,
        metadata={
            "source": "https://www.sastra.edu/staffprofiles/schools/src.php",
            "type": "official_src_administration"
        }
    )
)


print(
    "✅ SRC administration information added."
)


# ==================================================
# SPLIT TEXT
# ==================================================

print()
print("✂️ Splitting website content...")


splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150
)


chunks = splitter.split_documents(
    documents
)


print(
    f"Created {len(chunks)} searchable chunks."
)


# ==================================================
# CREATE EMBEDDINGS
# ==================================================

print()
print("🧠 Creating embeddings...")


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ==================================================
# DELETE OLD DATABASE
# ==================================================

print()
print("🗑️ Removing old database...")


if os.path.exists(DB_FOLDER):

    import shutil

    shutil.rmtree(
        DB_FOLDER
    )


# ==================================================
# CREATE CHROMA DATABASE
# ==================================================

print()
print("💾 Creating SRC searchable database...")


vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=DB_FOLDER,
    collection_name="src_website"
)


print()
print("========================================")
print("✅ SRC DATABASE CREATED SUCCESSFULLY!")
print("========================================")
print()

print(
    f"Database folder: {DB_FOLDER}"
)

print()

print(
    "The database now contains:"
)

print(
    "✅ SRC website information"
)

print(
    "✅ Faculty information"
)

print(
    "✅ Dean information"
)

print(
    "✅ Associate Dean information"
)

print(
    "✅ NCC information"
)

print(
    "✅ SRC contact information"
)

print()

