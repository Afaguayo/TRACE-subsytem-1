# necessary imports

import random
import re
from collections import defaultdict
import numpy as np
from typing import Dict, List, Tuple, Set
import csv
import os
import time
# Request and BeatifulSoup are used together for web scraping task.#
# Request makes HTTP request to interact with the web servers (simplifies GET,POST)
import requests
# BeatifulSoup used for web scraping and parsing HTML ot XML documents
# ALlows you to navigate and extract data from the structure of a webpage
from bs4 import BeautifulSoup

# Natural Language Processing routine that cleans CSV text 
# Function: Takes a csv_path parameter "str"
# 𝗧𝗵𝗶𝘀 𝗙𝘂𝗻𝗰𝘁𝗶𝗼𝗻 𝗶𝘀 𝗮 𝗰𝗹𝗲𝗮𝗻𝗶𝗻𝗴 𝘁𝗮𝘀𝗸 𝗳𝗼𝗿 𝘁𝗲𝘅𝘁
def nlp_subroutine(csv_path: str):
    #​⁡ ⁡⁢⁣⁢​‌‍‌𝗪𝗶𝗹𝗹 𝗺𝗼𝗱𝗶𝗳𝘆 𝘀𝘁𝗼𝗽 𝘄𝗼𝗿𝗱𝘀​⁡
    # Words to clean/𝗥𝗲𝗺𝗼𝘃𝗲 from CSV file
    # 𝗪𝗲 𝗱𝗼 𝘁𝗵𝗶𝘀 𝗯𝗲𝗰𝗮𝘀𝘂𝗲 𝘁𝗵𝗲𝘆 𝗰𝗮𝗿𝗿𝘆 𝗹𝗶𝘁𝘁𝗹𝗲 𝗺𝗲𝗮𝗻𝗶𝗻𝗴𝗳𝘂𝗹 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝘁𝗶𝗼𝗻 𝗳𝗼𝗿 𝗡𝗟𝗣 𝘁𝗮𝘀𝗸
    stopwords = {"the", "and", "or"}
    # 𝗕𝗲𝗳𝗼𝗿𝗲 𝗮𝗻𝘆𝘁𝗵𝗶𝗻𝗴 𝗲𝗹𝘀𝗲 𝗰𝗵𝗲𝗰𝗸 𝗶𝗳 𝗙𝗜𝗟𝗘 𝗣𝗔𝗧𝗛 ⁡⁢⁣⁢𝗲𝘅𝗶𝘀𝘁⁡ 𝗲𝗹𝘀𝗲 𝗲𝗿𝗿𝗼𝗿
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    
    # 𝗖𝗿𝗲𝗮𝘁𝗲 𝗹𝗶𝘀𝘁 𝘁𝗼 𝘀𝘁𝗼𝗿𝗲 𝗰𝗹𝗲𝗮𝗻𝗲𝗱 𝘃𝗲𝗿𝘀𝗶𝗼𝗻𝘀 𝗼𝗳 𝘁𝗵𝗲 𝗿𝗼𝘄𝘀 𝗳𝗿𝗼𝗺 𝘁𝗵𝗲 𝗖𝗦𝗩 𝗳𝗶𝗹𝗲 𝗮𝗳𝘁𝗲𝗿 𝗽𝗿𝗼𝗰𝗲𝘀𝘀𝗶𝗻𝗴
    cleaned_rows = []

    # 𝗢𝗽𝗲𝗻 𝘁𝗵𝗲 𝗖𝗦𝗩 𝗳𝗶𝗹𝗲 𝗿𝗲𝗮𝗱-𝗼𝗻𝗹𝘆
    with open(csv_path, "r", encoding="utf-8") as infile:
        # 𝗥𝗲𝗮𝗱 𝘁𝗵𝗲 𝗖𝗦𝗩 𝗳𝗶𝗹𝗲.
        # 𝗣𝗮𝗿𝘀𝗲 𝘁𝗵𝗲 𝗥𝗼𝘄𝘀 𝗶𝗻𝘁𝗼 𝗱𝗶𝗰𝘁𝗶𝗼𝗻𝗮𝗿𝗶𝗲𝘀 𝘄𝗵𝗲𝗿𝗲 𝗞𝗘𝗬𝗦 = 𝗰𝗼𝗹𝘂𝗺𝗻 𝗵𝗲𝗮𝗱𝗲𝗿𝘀 𝗮𝗻𝗱 𝘃𝗮𝗹𝘂𝗲𝘀 𝗮𝗿𝗲 𝘁𝗵𝗲 𝗱𝗮𝘁𝗮 𝗶𝗻 𝗲𝗮𝗰𝗵 𝗿𝗼𝘄
        reader = csv.DictReader(infile)
        # .𝗳𝗶𝗹𝗱𝗲𝗻𝗮𝗺𝗲𝘀 𝗶𝘀 𝘁𝗵𝗲 𝗹𝗶𝘀𝘁 𝗼𝗳 𝗰𝗼𝗹𝘂𝗺𝗻 𝗵𝗲𝗮𝗱𝗲𝗿𝘀
        fieldnames = reader.fieldnames
        # 𝗖𝗵𝗲𝗰𝗸 𝗶𝗳 𝗡𝗢 𝗵𝗲𝗮𝗱𝗲𝗿𝘀 𝗼𝗿 𝗰𝗵𝗲𝗰𝗸𝘀 𝗶𝗳 𝘀𝗽𝗲𝗰𝗶𝗳𝗶𝗲𝗱 𝗻𝗮𝗺𝗲𝘀 𝗲𝘅𝗶𝗶𝘀𝘁 𝗶𝗻 𝗰𝘀𝘃 (𝗮𝗹𝗹 𝘁𝗵𝗿𝗲𝗲 𝗺𝘂𝘀𝘁 𝗯𝗲 𝗽𝗿𝗲𝘀𝗲𝗻𝘁)
        if not fieldnames or not {"id", "content", "url"}.issubset(fieldnames):
            raise ValueError("CSV must contain columns: id, content, url")
        # 𝗧𝗿𝗮𝘃𝗲𝗿𝘀𝗲 𝘁𝗵𝗲 𝗿𝗼𝘄𝘀
        for row in reader:
            # 𝗚𝗲𝘁 𝗰𝗼𝗻𝘁𝗲𝘅𝘁 𝗶𝗳 𝗲𝘅𝗶𝘀𝗶𝘁
            text = row["content"] if row["content"] else ""
            # 𝗙𝗶𝗻𝗱𝘀 𝗮𝗹𝗹 𝗼𝗰𝗰𝘂𝗿𝗲𝗻𝗰𝗲𝘀 𝗼𝗳 𝘁𝗵𝗲 𝗽𝗮𝘁𝘁𝗲𝗿𝗻𝘀 𝗶𝗻 𝘁𝗵𝗲 𝗴𝗶𝘃𝗲𝗻 𝘁𝗲𝘅𝘁 𝗮𝗻𝗱 𝗿𝗲𝘁𝘂𝗿𝗻𝗲𝘀 𝘁𝗵𝗲𝗻 𝗮𝘀 𝗮 𝗹𝗶𝘀𝘁
            # \𝘄 𝗺𝗮𝗰𝗵𝗲𝘀 𝗮𝗻𝘆 𝘄𝗼𝗿𝗱 𝗰𝗵𝗮𝗿𝗮𝗰𝘁𝗲𝗿 (𝗮-𝘇, 𝗔-𝗭), 𝗱𝗶𝗴𝗶𝘁 (𝟬-𝟵), 𝘂𝗻𝗱𝗲𝗿𝘀𝗰𝗼𝗿𝗲(_)
            # 𝗺𝗮𝘁𝗰𝗵𝗶𝗻𝗴 𝗶𝘀 𝗡𝗢𝗧 𝗰𝗮𝘀𝗲 𝘀𝗲𝗻𝘀𝗶𝘁𝗶𝘃𝗲
            words = re.findall(r"\w+", text, flags=re.IGNORECASE)
            # 𝗪𝗼𝗿𝗱𝘀 𝗻𝗼𝘁 𝘁𝗼 𝗶𝗻𝗰𝗹𝘂𝗱𝗲 𝘄𝗲 𝗳𝗶𝗹𝘁𝗲𝗿 𝗼𝘂𝘁 𝗯𝗮𝘀𝗲𝗱 𝗼𝗻 𝘀𝘁𝗼𝗽𝘄𝗼𝗿𝗱𝘀 𝗼𝗻𝗹𝘆 𝗮𝗱𝗱 𝗻𝗼𝗻- 𝘀𝘁𝗼𝗽𝘄𝗼𝗿𝗱𝘀
            filtered_words = [
                word for word in words
                if word.lower() not in stopwords
            ]
            # 𝗔 𝗰𝗹𝗲𝗮𝗻𝗲𝗱 𝘃𝗲𝗿𝘀𝗶𝗼𝗻 𝗼𝗳 𝘁𝗲𝘅𝘁 𝗰𝗼𝗻𝗰𝗮𝘁 𝘄𝗶𝘁𝗵 𝗳𝗶𝗹𝘁𝗲𝗿𝗲𝗱𝘄𝗼𝗿𝗱𝘀 
            cleaned_text = " ".join(filtered_words)
            # 𝗨𝗽𝗱𝗮𝘁𝗲 𝘁𝗵𝗲 𝗿𝗼𝘄 𝗶𝗻 𝗱𝗶𝗰 𝗺𝗮𝗽𝗽𝗶𝗻𝗴
            row["content"] = cleaned_text
            # 𝗔𝗽𝗽𝗲𝗻𝗱𝗲𝗱 𝘁𝗵𝗲 𝗿𝗼𝘄 𝘁𝗼 𝗰𝗹𝗲𝗮𝗻𝗲𝗱 𝗿𝗼𝘄𝘀
            cleaned_rows.append(row)


    # Overwrite original CSV with cleaned text
    with open(csv_path, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_rows)
    print(f"Cleaned CSV '{csv_path}' file has been generated.")

# 𝗙𝘂𝗻𝗰𝘁𝗶𝗼𝗻: Load URLs from a CSV file with columns 'id' and 'website'.
# 𝗧𝗮𝗸𝗲𝘀 𝗖𝗦𝗩 𝗳𝗶𝗹𝗲 𝗽𝗮𝘁𝗵 𝗮𝗻𝗱 𝗿𝗲𝘁𝘂𝗿𝗻𝘀 𝗮 𝗹𝗶𝘀𝘁 𝗼𝗳 𝘁𝘆𝗽𝗲 𝘀𝘁𝗿𝗶𝗻𝗴 𝗶𝗻 𝘁𝗵𝗶𝘀 𝗰𝗮𝘀𝗲 𝗿𝗲𝘁𝘂𝗿𝗻𝘀 𝘁𝗵𝗲 𝗹𝗶𝘀𝘁 𝗼𝗳 𝗨𝗥𝗟𝘀
def load_urls_from_csv(csv_path: str) -> List[str]:
    # 𝗖𝗵𝗲𝗰𝗸 𝗶𝗳 𝗖𝗦𝗩 𝗳𝗶𝗹𝗲 𝗲𝘅𝗶𝘀𝘁 𝗲𝗹𝘀𝗲 𝗲𝗿𝗼𝗿
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    # 𝗧𝗿𝘆-𝗰𝗮𝘁𝗰𝗵 𝗯𝗹𝗼𝗰𝗸
    try:
        # 𝗦𝘁𝗼𝗿𝗲 𝗨𝗥𝗟𝘀
        urls = []
        # 𝗢𝗽𝗲𝗻 𝘁𝗵𝗲 𝗖𝗦𝗩 𝗳𝗶𝗹𝗲
        with open(csv_path, 'r', encoding='utf-8') as file:
            # 𝗥𝗲𝗮𝗱 𝗳𝗶𝗹𝗹𝗲 𝗶𝗻𝘁𝗼 𝗮 𝗱𝗶𝗰𝘁𝗶𝗼𝗻𝗮𝗿𝘆-𝗹𝗶𝗸𝗲 𝗳𝗼𝗿𝗺𝗮𝘁𝗲 𝘄𝗵𝗲𝗿𝗲 𝗲𝗮𝗰𝗵 𝗿𝗼𝘄 𝗶𝘀 𝗮 𝗱𝗶𝗰𝘁𝗶𝗼𝗻𝗮𝗿𝘆 𝗮𝗻𝗱 𝗞𝗘𝗬𝗦= 𝗰𝗼𝗹𝘂𝗺𝗻 𝗵𝗲𝗮𝗱𝗲𝗿𝘀
            reader = csv.DictReader(file)
            # 𝗖𝗵𝗲𝗰𝗸 𝗶𝗳 𝘀𝗽𝗰𝗶𝗳𝗶𝗲𝗱 𝗵𝗲𝗮𝗱𝗲𝗿 𝗻𝗼𝘁 𝗳𝗼𝘂𝗻𝗱
            if not {'id', 'website'}.issubset(set(reader.fieldnames or [])):
                raise ValueError("CSV must contain columns: id, website")
            # 𝗧𝗿𝗮𝘃𝗲𝗿𝘀𝗲 𝘁𝗵𝗲 𝗿𝗼𝘄𝘀
            for row in reader:
                # 𝗖𝗵𝗲𝗰𝗸 𝗶𝗳 𝘄𝗲𝗯𝘀𝗶𝘁𝗲 𝗵𝗮𝘀 𝗱𝗮𝘁𝗮
                if row['website']:
                    # 𝗦𝘁𝗿𝗶𝗽 𝗮𝗻𝘆 𝘄𝗵𝗶𝘁𝗲 𝘀𝗽𝗮𝗰𝗲 𝗮𝗻𝗱 𝗮𝗽𝗽𝗲𝗻𝗱 𝘁𝗵𝗲 𝗨𝗥𝗟
                    urls.append(row['website'].strip())
        # 𝗪𝗵𝗲𝗻 𝗱𝗼𝗻𝗲 𝘄𝗶𝘁𝗵 𝗮𝗹𝗹 𝗿𝗲𝘁𝘂𝗿𝗻 𝘁𝗵𝗲 𝗹𝗶𝘀 𝘁𝗼𝗳 𝗨𝗥𝗟𝘀
        return urls
    # 𝗘𝘅𝗰𝗲𝗽𝘁𝗶𝗼𝗻 𝗲𝗿𝗿𝗼𝗿
    except csv.Error as e:
        raise ValueError(f"Error reading CSV file: {e}")

# 𝗖𝗹𝗮𝘀𝘀: Web scraper functions and will pull something out of the URLs provided.
class WebScraper:
    # Initialize with list of URLs
    def __init__(self, urls):
        self.urls = urls

    # Scrape text content from web pages
    # 𝗜𝘁 𝘀𝗰𝗿𝗽𝗲𝘀 𝗳𝗿𝗼𝗺 𝗨𝗥𝗟𝘀, 𝘀𝗽𝗲𝗰𝗶𝗳𝗶𝗰𝗮𝗹𝗹𝘆 𝗲𝘅𝘁𝗿𝗮𝗰𝘁𝗶𝗻𝗴 𝗿𝗲𝗮𝗱𝗮𝗯𝗹𝗲 𝘁𝗲𝘅𝘁 𝗳𝗿𝗼𝗺 𝘀𝗽𝗲𝗰𝗶𝗳𝗶𝗲𝗰 𝗛𝗧𝗠𝗟
    def scrape_pages(self):
        # 𝗦𝘁𝗼𝗿𝗲 𝗿𝗲𝘀𝘂𝗹𝘁𝘀 𝗶𝗻 𝗹𝗶𝘀𝘁
        results = []
        # 𝗟𝗼𝗼𝗽 𝘁𝗵𝗿𝗼𝘂𝗴𝗵 𝗨𝗥𝗹𝘀
        for i, url in enumerate(self.urls, 1):
            # 𝗧𝗿𝘆-𝗰𝗮𝘁𝗰𝗵 𝗯𝗹𝗼𝗰𝗸
            try:
                # 𝗦𝗲𝗻𝗱 𝗛𝗧𝗧𝗣 𝗴𝗲𝘁 𝗿𝗲𝗾𝘂𝗲𝘀𝘁 𝘁𝗼 𝗨𝗥𝗟
                # 𝗠𝗮𝘆 𝗵𝗮𝗲 𝘁𝗼 𝗺𝗼𝗱𝗶𝗳𝘆 ⁡⁢⁣⁢𝘁𝗶𝗺𝗲𝗼𝘂𝘁⁡
                # 𝗦𝘁𝗼𝗿𝗲 𝗿𝗲𝘀𝗽𝗼𝗻𝘀𝗲
                response = requests.get(url, timeout=10)
                # 𝗥𝗮𝗶𝘀𝗲 𝗲𝘅𝗰𝗲𝗽𝘁𝗶𝗼𝗻 𝗶𝗳 𝘁𝗵𝗲 𝘀𝗲𝗿𝘃𝗲𝗿 𝗿𝗲𝘀𝗽𝗼𝗻𝗱𝘀 𝘄𝗶𝘁𝗵 𝗮𝗻 𝗛𝗧𝗧𝗣 𝗲𝗿𝗿𝗼𝗿
                response.raise_for_status()
                # 𝗣𝗮𝗿𝘀𝗲 𝘁𝗵𝗲 𝗛𝗧𝗠𝗟 𝗰𝗼𝗻𝘁𝗲𝗻𝘁 𝗼𝗳 𝘁𝗵𝗲 𝗿𝗲𝘀𝗽𝗼𝗻𝘀𝗲 
                soup = BeautifulSoup(response.text, 'html.parser')
                # Extract text from p, h1, h2, h3, and span tags
                # 𝗘𝘅𝘁𝗿𝗮𝗰𝘁 𝘃𝗶𝘀𝗶𝗯𝗹𝗲 𝘁𝗲𝘅𝘁 𝗳𝗿𝗼𝗺 𝗲𝗮𝗰𝗵 𝘁𝗮𝗴
                # 𝗝𝗼𝗶𝗻 𝘁𝗵𝗲 𝗲𝘅𝘁𝗿𝗮𝗰𝘁𝗲𝗱 𝘁𝗲𝘅𝘁 𝘄𝗶𝘁𝗵 𝘀𝗽𝗮𝗰𝗲𝘀 𝘁𝗼 𝗳𝗼𝗿𝗺 𝗮 𝘀𝗶𝗻𝗴𝗹𝗲 𝘁𝗲𝘅𝘁
                text = ' '.join([tag.get_text() for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'span'])])
                # 𝗥𝗲𝘀𝘂𝗹𝘁𝘀 𝗰𝗼𝗻𝘁𝗮𝗶𝗻 
                # 𝗶 = 𝗶𝗻𝗱𝗲𝘅 𝗼𝗳 𝘁𝗵𝗲 𝗨𝗥𝗹 𝗶𝗻 𝘁𝗵𝗲 𝗼𝗿𝗶𝗴𝗶𝗻𝗮𝗹 𝘁𝗲𝘅𝘁
                # 𝘁𝗲𝘅𝘁: 𝗘𝘅𝘁𝗿𝗮𝗰𝘁𝗲𝗱 𝗰𝗼𝗻𝘁𝗲𝗻𝘁
                # 𝘂𝗿𝗹: 𝗧𝗵𝗲 𝗨𝗥𝗟 𝗯𝗲𝗶𝗻𝗴 𝗽𝗿𝗼𝗰𝗲𝘀𝘀𝗲𝗱
                results.append((i, text, url))

                time.sleep(1)  # Be polite to servers, 𝗔𝘃𝗼𝗶𝗱 𝗼𝘃𝗲𝗿𝗹𝗼𝗮𝗱𝗶𝗻𝗴 𝘁𝗵𝗲 𝘀𝗲𝗿𝘃𝗲𝗿𝘀
            # 𝗘𝘅𝗰𝗲𝗽𝘁𝗶𝗼𝗻 𝗲𝗿𝗿𝗼𝗿
            except Exception as e:
                print(f"Error scraping {url}: {e}")
        # 𝗥𝗲𝘁𝘂𝗿𝗻 𝘁𝗵𝗲 𝗿𝗲𝘀𝘂𝗹𝘁𝘀 𝗰𝗼𝗹𝗹𝗲𝗰𝘁𝗲𝗱
        return results

    # 𝗙𝘂𝗻𝗰𝘁𝗶𝗼𝗻: Generate CSV file with scraped data
    # 𝗧𝗮𝗸𝗲𝘀 𝘁𝗵𝗲 𝗳𝗶𝗹𝗲𝗻𝗮𝗺𝗲 𝗮𝘀 𝗽𝗮𝗿𝗮𝗺𝗲𝘁𝗲𝗿
    def generate_csv(self, filename):
        # 𝗖𝗮𝗹𝗹 𝘁𝗵𝗲 𝘀𝗰𝗿𝗮𝗽𝗲_𝗽𝗮𝗴𝗲𝘀 𝗳𝘂𝗻𝗰𝘁𝗶𝗼𝗻
        data = self.scrape_pages()
        # 𝗢𝗽𝗲𝗻 𝗳𝗶𝗹𝗲𝗻𝗮𝗺𝗲, 𝘄𝗿𝗶𝘁𝗲 𝗼𝗻𝗹𝘆 𝗶𝗻𝘁𝗼 𝗮 𝗰𝘀𝘃 𝗳𝗶𝗹𝗲
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['id', 'content', 'url'])  # Header
            csv_writer.writerows(data)
        print(f"CSV file '{filename}' has been generated.")
        
# 𝗙𝘂𝗻𝗰𝘁𝗶𝗼𝗻: Load web text from a CSV file
# 𝗧𝗮𝗸𝗲𝗱 𝗖𝗦𝗩 𝗽𝗮𝘁𝗵 𝗮𝘀 𝗽𝗮𝗿𝗮𝗺𝗲𝘁𝗲𝗿 𝗮𝗻𝗱 𝗿𝗲𝘁𝘂𝗿𝗻𝘀 𝗮 𝘀𝘁𝗿𝗶𝗻𝗴
def load_web_text(csv_path: str) -> str:
    # 𝗖𝗵𝗲𝗰𝗸 𝗶𝗳 𝗖𝗦𝗩 𝗽𝗮𝘁𝗵 𝗲𝘅𝗶𝘀𝘁 𝗲𝗹𝘀𝗲 𝗲𝗿𝗿𝗼𝗿
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    # 𝗧𝗿𝘆-𝗰𝗮𝘁𝗰𝗵 𝗯𝗹𝗼𝗰𝗸
    try:
        # 𝗢𝗽𝗲𝗻 𝗖𝗦𝗩 𝗽𝗮𝘁𝗵, 𝗿𝗲𝗮𝗱-𝗼𝗻𝗹𝘆
        with open(csv_path, 'r', encoding='utf-8') as file:
            # 𝗣𝗮𝗿𝘀𝗲 𝘁𝗵𝗲 𝗥𝗼𝘄𝘀 𝗶𝗻𝘁𝗼 𝗱𝗶𝗰𝘁𝗶𝗼𝗻𝗮𝗿𝗶𝗲𝘀 𝘄𝗵𝗲𝗿𝗲 𝗞𝗘𝗬𝗦 = 𝗰𝗼𝗹𝘂𝗺𝗻 𝗵𝗲𝗮𝗱𝗲𝗿𝘀 𝗮𝗻𝗱 𝘃𝗮𝗹𝘂𝗲𝘀 𝗮𝗿𝗲 𝘁𝗵𝗲 𝗱𝗮𝘁𝗮 𝗶𝗻 𝗲𝗮𝗰𝗵 𝗿𝗼𝘄
            reader = csv.DictReader(file)
            # 𝗖𝗵𝗲𝗰𝗸 𝗶𝗳 𝘀𝗽𝗲𝗰𝗶𝗳𝗶𝗲𝗱 𝗵𝗲𝗮𝗱𝗲𝗿𝘀 𝗶𝗻 𝗻𝗼𝘁 𝗳𝗼𝘂𝗻𝗱 
            if not {'id', 'content', 'url'}.issubset(set(reader.fieldnames or [])):
                raise ValueError("CSV must contain columns: id, content, url")
            # 𝗦𝘁𝗼𝗿𝗲 𝗰𝗼𝗻𝘁𝗲𝗻𝘁𝘀 𝗳𝗼𝘂𝗻𝗱 𝗶𝗻 𝗹𝗶𝘀𝘁
            contents = []
            # 𝗧𝗿𝗮𝘃𝗲𝗿𝘀𝗲 𝘁𝗵𝗲 𝗿𝗼𝘄𝘀
            for row in reader:
                # 𝗖𝗵𝗲𝗰𝗸 𝗶𝗳 𝗿𝗼𝘄 𝗵𝗮𝘀 𝗰𝗼𝗻𝘁𝗲𝗻𝘁𝘀, 𝗶𝗳 𝘀𝗼 𝗹𝗼𝘄𝗲𝗿() 𝗰𝗼𝗻𝘁𝗲𝗻𝘁𝘀 𝗮𝗻𝗱 𝗮𝗱𝗱 𝗶𝘁 𝘁𝗼 𝗰𝗼𝗻𝘁𝗲𝗻𝘁𝘀 𝗹𝗶𝘀𝘁
                if row['content']:
                    contents.append(row['content'].lower())
        # 𝗥𝗲𝘁𝘂𝗿𝗻 𝗮𝗹𝗹 𝗲𝘅𝘁𝗿𝗮𝗰𝘁𝗲𝗱 𝗰𝗼𝗻𝘁𝗲𝗻𝘁𝘀 𝘁𝗼 𝗮 𝘀𝗶𝗻𝗴𝗹𝗲 𝗿𝗲𝘀𝘂𝗹𝘁𝗶𝗻𝗴 𝘀𝘁𝗿𝗶𝗻𝗴
        return " ".join(contents)
    # 𝗘𝘅𝗰𝗲𝗽𝘁𝗶𝗼𝗻 𝗲𝗿𝗿𝗼𝗿
    except csv.Error as e:
        raise ValueError(f"Error reading CSV file: {e}")

# 𝗙𝘂𝗻𝗰𝘁𝗶𝗼𝗻: Load wordlist from a file
# 𝗧𝗮𝗸𝗲𝘀 𝘁𝗵𝗲 𝘄𝗼𝗿𝗱𝗹𝗶𝘀𝘁 𝗳𝗶𝗹𝗲
# 𝗥𝗲𝘁𝘂𝗿𝗻𝘀 𝗮 𝗹𝗶𝘀𝘁 𝗼𝗳 𝘀𝘁𝗿𝗶𝗻𝗴𝘀
def load_wordlist(file_path: str) -> List[str]:
    # 𝗖𝗵𝗲𝗰𝗸 𝗶𝗳 𝗳𝗶𝗹𝗲 𝗽𝗮𝘁𝗵 𝗲𝘅𝗶𝘀𝗶𝘁 𝗲𝗹𝘀𝗲 𝗲𝗿𝗿𝗼𝗿
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Wordlist file not found: {file_path}")
    # 𝗧𝗿𝘆-𝗰𝗮𝘁𝗰𝗵 𝗯𝗹𝗼𝗰𝗸
    try:
        # 𝗢𝗽𝗲𝗻 𝗳𝗶𝗹𝗲, 𝗿𝗲𝗮𝗱-𝗼𝗻𝗹𝘆
        with open(file_path, 'r', encoding='utf-8') as file:
            # 𝗹𝗼𝘄𝗲𝗿𝘀 𝗮𝗻𝗱 𝘀𝘁𝗿𝗶𝗽𝘀 𝘁𝗲𝘅𝘁 𝗼𝗳 𝘄𝗵𝗶𝘁𝗲 𝘀𝗽𝗮𝗰𝗲 𝗮𝗻𝗱 𝘀𝘁𝗼𝗿𝗲 𝗶𝗻 𝘄𝗼𝗿𝗱 𝗹𝗶𝘀𝘁
            words = [line.strip().lower() for line in file if line.strip()]
        # 𝗥𝗲𝘁𝘂𝗿𝗻 𝘁𝗵𝗲 𝘄𝗼𝗿𝗱 𝗹𝗶𝘀𝘁
        # 𝗘𝗫: 𝘀𝟭="𝗵𝗲𝗹𝗹𝗼", 𝘀𝟮="𝗛𝗶", 𝘀𝟯="𝗥𝗮𝘂𝗹" 𝗰𝗼𝗻𝘃𝗲𝗿𝘁𝘀 𝘁𝗼 ["𝗵𝗲𝗹𝗹𝗼","𝗛𝗶","𝗥𝗮𝘂𝗹"]
        return words
    # 𝗘𝘅𝗰𝗲𝗽𝘁𝗶𝗼𝗻 𝗲𝗿𝗿𝗼𝗿
    except Exception as e:
        raise ValueError(f"Error reading wordlist file: {e}")

# Class: 𝗠anaging the Markov Decision Process (𝗠𝗗𝗣) for generating credentials. 𝗠𝗗𝗣 𝗶𝘀 𝗮 𝗿𝗲𝗶𝗻𝗳𝗼𝗿𝗰𝗲𝗺𝗲𝗻𝘁 𝗹𝗲𝗮𝗿𝗻𝗶𝗻𝗴 (𝗥𝗟)
# 𝗖𝗿𝗲𝗱𝗲𝗻𝘁𝗶𝗮𝗹𝘀 𝗮𝗿𝗲 𝘁𝗵𝗲 𝘂𝘀𝗲𝗿𝗻𝗮𝗺𝗲𝘀 𝗮𝗻𝗱 𝗽𝗮𝘀𝘀𝘄𝗼𝗿𝗱𝘀
class CredentialMDP:
    # 𝗖𝗼𝗻𝘀𝘁𝗿𝘂𝗰𝘁𝗼𝗿
    # 𝗼𝗿𝗱𝗲𝗿 - 𝗱𝗲𝗽𝘁𝗵, 𝗵𝗼𝘄 𝗳𝗮𝗿 𝘁𝗼 𝗹𝗼𝗼𝗸 𝗮𝗵𝗲𝗮𝗱
    # 𝗴𝗮𝗺𝗺𝗮 - 𝗗𝗲𝗮𝗹𝘀 𝘄𝗶𝘁𝗵 𝗳𝘂𝘁𝘂𝗿𝗲 𝗿𝗲𝘄𝗮𝗿𝗱𝘀 𝗰𝗼𝗻𝘀𝗶𝗱𝗲𝗿𝗮𝘁𝗶𝗼𝗻 ⁡⁢⁣⁢(𝗻𝗲𝗲𝗱 𝘁𝗼 𝗳𝗶𝗻𝗱 𝗼𝗽𝘁𝗶𝗺𝗮𝗹 𝘃𝗮𝗹𝘂𝗲)⁡
    def __init__(self, order: int = 2, gamma: float = 0.9):
        # 𝗼𝗿𝗱𝗲𝗿: 𝗱𝗲𝗽𝘁𝗵 - 𝗵𝗼𝘄 𝗳𝗮𝗿 𝘁𝗼 𝗹𝗼𝗼𝗸 𝗮𝗵𝗲𝗮𝗱
        self.order = order
        # 𝗖𝗼𝗻𝘁𝗿𝗼𝗹𝘀 𝗵𝗼𝘄 𝗺𝘂𝗰𝗵 𝗳𝘂𝘁𝘂𝗿𝗲 𝗿𝗲𝘄𝗮𝗿𝗱𝘀 𝗮𝗿𝗲 𝘃𝗹𝗮𝘂𝗲𝗱 𝗰𝗼𝗺𝗽𝗮𝗿𝗲𝗱 𝘁𝗼 𝗶𝗺𝗺𝗲𝗱𝗶𝗮𝘁𝗲𝗱 𝗿𝗲𝘄𝗮𝗿𝗱𝘀
        # 𝗗𝗶𝘀𝗰𝗼𝘂𝗻𝘁𝗲𝗱 𝗳𝗮𝗰𝘁𝗼𝗿: 𝘃𝗮𝗹𝘂𝗲 𝗰𝗹𝗼𝘀𝗲𝗿 𝘁𝗼 𝟭 𝗺𝗲𝗮𝗻𝘀 𝘁𝗵𝗲 𝗮𝗴𝗲𝗻𝘁 𝘃𝗮𝗹𝘂𝗲𝘀 𝗳𝘂𝘁𝘂𝗿𝗲 𝗿𝗲𝘄𝗮𝗿𝗱𝘀 𝗮𝗹𝗺𝗼𝘀𝘁 𝗮𝘀 𝗺𝘂𝗰𝗵 𝗮𝘀 𝗶𝗺𝗺𝗲𝗱𝗶𝗮𝘁𝗲 𝗿𝗲𝘄𝗮𝗿𝗱𝘀, 𝘄𝗵𝗶𝗹𝗲 𝘃𝗮𝗹𝘂𝗲𝘀 𝗰𝗹𝗼𝘀𝗲𝗿 𝘁𝗼 𝘇𝗲𝗿𝗼 𝗺𝗲𝗮𝗻𝘀 𝘁𝗵𝗲 𝗮𝗴𝗲𝗻𝘁 𝗳𝗼𝗰𝘂𝘀𝗲𝘀 𝗺𝗼𝗿𝗲 𝗼𝗻 𝗶𝗺𝗺𝗲𝗱𝗶𝗮𝘁𝗲 𝗿𝗲𝘄𝗮𝗿𝗱𝘀.
        self.gamma = gamma
        # 𝗦𝘁𝗼𝗿𝗲𝘀 𝗤-𝘃𝗮𝗹𝘂𝗲𝘀 𝗳𝗼𝗿 𝘀𝘁𝗮𝘁𝗲-𝗮𝗰𝘁𝗶𝗼𝗻 𝗽𝗮𝗶𝗿𝘀
        self.q_values: Dict[str, Dict[Tuple[str, str], float]] = defaultdict(lambda: defaultdict(float))
        # 𝗦𝗼𝘁𝗿𝗲𝘀 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝘁𝗶𝗼𝗻 𝗮𝗯𝗼𝘂𝘁 𝗽𝗼𝘀𝘀𝗶𝗯𝗹𝗲 𝘀𝘁𝗮𝘁𝗲 𝘁𝗿𝗮𝗻𝘀𝗶𝘁𝗶𝗼𝗻𝘀
        self.state_transitions: Dict[str, Dict[str, Set[str]]] = defaultdict(lambda: defaultdict(set))
        # 𝗞𝗲𝗲𝗽𝘀 𝘁𝗿𝗮𝗰𝗸 𝗼𝗳 𝘂𝘀𝗲𝗿𝗻𝗮𝗺𝗲𝘀 𝘁𝗵𝗮𝘁 𝗵𝗮𝘃𝗲 𝗮𝗹𝗿𝗲𝗮𝗱𝘆 𝗯𝗲𝗲𝗻 𝘂𝘀𝗲𝗱, 𝗔𝘃𝗼𝗶𝗱 𝗿𝗲𝗽𝗲𝗮𝘁𝗶𝗻𝗴
        self.used_usernames: Set[str] = set()
        # 𝗧𝗵𝗲 𝗲𝘅𝗽𝗹𝗼𝗿𝗮𝘁𝗶𝗼𝗻 𝗿𝗮𝘁𝗲, 𝗱𝗲𝘁𝗲𝗿𝗺𝗶𝗻𝗲𝘀 𝘁𝗵𝗲 𝗽𝗿𝗼𝗯𝗮𝗯𝗶𝗹𝗶𝘁𝘆 𝗼𝗳 𝘁𝗵𝗲 𝗮𝗴𝗲𝗻𝘁  𝗲𝘅𝗽𝗹𝗼𝗿𝗶𝗻𝗴 𝗿𝗮𝗻𝗱𝗼𝗺 𝗮𝗰𝘁𝗶𝗼𝗻𝘀 𝗿𝗮𝘁𝗵𝗲𝗿 𝘁𝗵𝗮𝗻 𝗲𝘅𝗽𝗹𝗼𝗶𝘁𝗶𝗻𝗴 𝘁𝗵𝗲 𝗯𝗲𝘀𝘁 𝗸𝗻𝗼𝘄𝗻 𝗮𝗰𝘁𝗶𝗼𝗻𝘀 .𝟭= 𝟭𝟬% 𝗼𝗳 𝗿𝗮𝗻𝗱𝗼𝗺 𝗲𝘅𝗽𝗹𝗼𝗿𝗮𝘁𝗶𝗼𝗻, 𝟵𝟬% 𝗼𝗳 𝘀𝗽𝗹𝗼𝗶𝘁𝗶𝗻𝗴 𝘁𝗵𝗲 𝗯𝗲𝘀𝘁-𝗸𝗻𝗼𝘄𝗻 𝗮𝗰𝘁𝗶𝗼𝗻.
        self.epsilon = 0.1
        # 𝗛𝗼𝘄 𝗾𝘂𝗶𝗰𝗸𝗹𝘆 𝘁𝗵𝗲 𝗮𝗴𝗲𝗻𝘁 𝘂𝗽𝗮𝗱𝘁𝗲𝘀 𝘁𝗵𝗲 𝗤-𝘃𝗮𝗹𝘂𝗲𝘀 𝗮𝗳𝘁𝗲𝗿 𝗿𝗲𝗰𝗶𝗲𝘃𝗶𝗻𝗴 𝗻𝗲𝘄 𝗿𝗲𝘄𝗮𝗿𝗱𝘀
        self.learning_rate = 0.1
        # 𝗧𝗵𝗲 𝗶𝗻𝘁𝗶𝘁𝗮𝗹 𝘀𝘁𝗮𝘁𝗲𝘀 𝘁𝗵𝗲 𝗮𝗴𝗲𝗻𝘁 𝗰𝗮𝗻 𝘀𝘁𝗮𝗿𝘁 𝗳𝗿𝗼𝗺
        self.initial_states: List[str] = []

    # 𝗙𝘂𝗻𝗰𝘁𝗶𝗼𝗻: Calculate the strength of a password
    # 𝗧𝗮𝗸𝗲 𝗽𝗮𝘀𝘀𝘄𝗼𝗿𝗱 𝗮𝗻𝗱 𝗮𝘀𝘀𝗶𝗴𝗻 𝘀𝗰𝗼𝗿𝗲 𝘁𝗼 𝗶𝘁 𝗮𝗻𝗱 𝗿𝗲𝘁𝘂𝗿𝗻 𝗶𝘁. 𝗧𝗵𝗲 𝗿𝗲𝘄𝗮𝗿𝗱𝘀 𝗳𝗼𝗿 𝗴𝗲𝗻𝗲𝗿𝗮𝘁𝗶𝗴𝗻 𝗴𝗼𝗼𝗱 𝗽𝗮𝘀𝘀𝘄𝗼𝗿𝗱𝘀
    def calculate_password_strength(self, password: str) -> float:
        score = 0.0
        if len(password) >= 12:
            score += 0.3
        if re.search(r'[A-Z]', password):
            score += 0.2
        if re.search(r'[0-9]', password):
            score += 0.2
        if re.search(r'[!@#$%^&*]', password):
            score += 0.2
        if len(set(password)) >= 8:
            score += 0.1
        return score

    # 𝗙𝘂𝗻𝗰𝘁𝗶𝗼𝗻: Calculate the quality of a username
    # 𝗧𝗮𝗸𝗲 𝘂𝘀𝗲𝗿𝗻𝗮𝗺𝗲 𝗮𝗻𝗱 𝗮𝘀𝘀𝗶𝗴𝗻 𝘀𝗰𝗼𝗿𝗲 𝘁𝗼 𝗶𝘁, 𝗮𝗹𝘀𝗼 𝗮 𝗿𝗲𝘄𝗮𝗿𝗱 𝗳𝗼𝗿 𝗴𝗲𝗻𝗲𝗿𝗮𝘁𝗶𝗴𝗻 𝗴𝗼𝗼𝗱 𝘂𝘀𝗲𝗿𝗻𝗮𝗺𝗲𝘀
    def calculate_username_quality(self, username: str) -> float:
        score = 0.0
        if len(username) >= 6:
            score += 0.3
        if username not in self.used_usernames:
            score += 0.4
        if re.match(r'^[a-z]', username):
            score += 0.2
        if not re.search(r'\s', username):
            score += 0.1
        return score

    # 𝗙𝘂𝗻𝗰𝘁𝗶𝗼𝗻: Get the reward for a state-action pair
    # 𝗖𝗮𝗹𝗰𝘂𝗹𝗮𝘁𝗲 𝗿𝗲𝘄𝗮𝗿𝗱𝘀 𝗳𝗼𝗿 𝗮 𝗴𝗶𝘃𝗲𝗻 𝘀𝘁𝗮𝘁𝗲-𝗮𝗰𝘁𝗶𝗼𝗻 𝗽𝗮𝗶𝗿 𝗯𝗮𝘀𝗲𝗱 𝗼𝗻 𝘁𝗵𝗲 𝗰𝘂𝗿𝗿𝗲𝗻𝘁 𝘀𝘁𝗮𝘁𝗲, 𝗮𝗰𝘁𝗶𝗼𝗻 𝘁𝗮𝗸𝗲𝗻, 𝗻𝗲𝘅𝘁 𝗮𝗰𝘁𝗶𝗼𝗻
    # 𝗥𝗲𝘁𝘂𝗿𝗻 𝗿𝗲𝘄𝗮𝗿𝗱 𝗰𝗹𝗮𝗰𝘂𝗹𝗮𝘁𝗲𝗱
    def get_reward(self, state: str, action: str, next_char: str) -> float:
        # 𝗖𝗵𝗲𝗰𝗸 𝘀𝘁𝗮𝘁𝗲 𝗶𝘀 𝘂𝘀𝗲𝗿𝗻𝗮𝗺𝗲
        if 'username' in state:
            # 𝗦𝗸𝗶𝗽 "𝘂𝘀𝗲𝗿𝗻𝗮𝗺𝗲" 𝗻𝗮𝗺𝗲
            current = state[9:] + next_char
            # 𝗥𝗲𝘁𝘂𝗿𝗻 𝘂𝘀𝗲𝗿𝗻𝗮𝗺𝗲 𝗰𝗮𝗹𝗰𝘂𝗹𝗮𝘁𝗲𝗱 𝗿𝗲𝘄𝗮𝗿𝗱 
            return self.calculate_username_quality(current) / len(current)
        else:
            # 𝗦𝘁𝗮𝘁𝗲 𝗶𝘀 𝗽𝗮𝘀𝘀𝘄𝗼𝗿𝗱, 𝘁𝗵𝗲𝗻 𝘀𝗸𝗶𝗽 𝗽𝗮𝘀𝘀𝘄𝗼𝗿𝗱 𝗻𝗮𝗺𝗲
            current = state[9:] + next_char
            # 𝗥𝗲𝘁𝘂𝗿𝗻 𝗽𝗮𝘀𝘀𝘄𝗼𝗿𝗱 𝗰𝗮𝗹𝗰𝘂𝗹𝗮𝘁𝗲𝗱 𝗿𝘄𝗮𝗿𝗱
            return self.calculate_password_strength(current) / len(current)

    # 𝗙𝘂𝗻𝗰𝘁𝗶𝗼𝗻: Get possible actions for a state
    # 𝗥𝗲𝘁𝘂𝗿𝗻 𝗹𝗶𝘀𝘁 𝗼𝗳 𝘀𝘁𝗿𝗶𝗻𝗴 - 𝗽𝗼𝘀𝘀𝗶𝗯𝗹𝗲 𝗮𝗰𝘁𝗶𝗼𝗻𝘀
    def get_possible_actions(self, state: str) -> List[str]:
        return list(self.state_transitions[state].keys())

    # 𝗙𝘂𝗻𝗰𝘁𝗶𝗼𝗻: Choose an action based on epsilon-greedy strategy
    # 𝗖𝘂𝗿𝗿𝗲𝗻𝘁 𝘀𝘁𝗮𝘁𝗲 𝗼𝗳 𝘀𝘆𝘀𝘁𝗲𝗺, 𝗿𝗲𝗽𝗿𝗲𝘀𝗲𝗻𝘁𝗶𝗻𝗴 𝗽𝗮𝗿𝘁𝗶𝗮𝗹𝗹𝘆 𝗯𝘂𝗶𝗹𝘁 𝘂𝘀𝗲𝗿𝗻𝗮𝗺𝗲𝘀 𝗼𝗿 𝗽𝗮𝘀𝘀𝘄𝗿𝗼𝗱𝘀
    def choose_action(self, state: str) -> Tuple[str, str]:
        # 𝗴𝗲𝘁 𝗹𝗶𝘀𝘁 𝗼𝗳 𝗽𝗼𝘀𝘀𝗶𝗯𝗹𝗲 𝗮𝗰𝘁𝗶𝗼𝗻𝘀 𝘁𝗼 𝘁𝗮𝗸𝗲
        possible_actions = self.get_possible_actions(state)
        # 𝗜𝗳 𝗻𝗼 𝗺𝗼𝗿𝗲 𝗮𝗰𝘁𝗶𝗼𝗻𝘀 𝗿𝗲𝘁𝘂𝗿𝗻 𝗲𝗺𝗽𝘁𝘆 𝘀𝘁𝗿𝗶𝗻𝗴 𝘂𝘀𝗲𝗿𝗻𝗮𝗺𝗲 𝗮𝗻𝗱 𝗽𝗮𝘀𝘀𝘄𝗼𝗿𝗱
        if not possible_actions:
            return "", ""
        # 𝗜𝗳 𝗿𝗮𝗻𝗱𝗼𝗺𝗹𝘆 𝗴𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 𝘃𝗮𝗹𝘂𝗲 𝗶𝘀 𝗹𝗲𝘀𝘀 𝘁𝗵𝗮𝗻 𝘁𝗵𝗲 𝗲𝘅𝗽𝗹𝗼𝗿𝗮𝘁𝗶𝗼𝗻 𝗿𝗮𝘁𝗲 𝗲𝗽𝘀𝗶𝗹𝗼𝗻, 𝘁𝗲𝗵 𝗮𝗴𝗲𝗻𝘁 𝘄𝗶𝗹𝗹 𝗲𝘅𝗽𝗹𝗼𝗿𝗲 𝗯𝘆 𝗰𝗵𝗼𝗼𝘀𝗶𝗻𝗴 𝗮 𝗿𝗮𝗻𝗱𝗼𝗺 𝗮𝘁𝗶𝗼𝗻
        if random.random() < self.epsilon:
            # 𝗚𝗲𝘁 𝗿𝗮𝗻𝗱𝗼𝗺 𝗮𝗰𝘁𝗶𝗼𝗻
            action = random.choice(possible_actions)
            # 𝗕𝗮𝘀𝗲𝗱 𝗼𝗻 𝘁𝗵𝗮𝘁 𝗮𝗰𝘁𝗶𝗼𝗻 𝗴𝗲𝘁 𝗻𝗲𝘅𝘁 𝘀𝘁𝗮𝘁𝗲 (𝗻𝗲𝘅𝘁 𝗰𝗵𝗮𝗿)
            next_char = random.choice(list(self.state_transitions[state][action]))
        else:
            # Choose best 𝗸𝗻𝗼𝘄𝗻 action based on Q-values
            # 𝗦𝘁𝗼𝗿𝗲 𝗺𝗮𝘅𝗶𝗺𝘂𝗺 𝗤-𝘃𝗮𝗹𝘂𝗲𝘀 𝗳𝗼𝗿 𝗲𝗮𝗰𝗵 𝗽𝗼𝘀𝘀𝗶𝗯𝗹𝗲 𝗮𝗰𝘁𝗶𝗼𝗻𝘀
            action_values = {}
            # 𝘁𝗿𝗮𝘃𝗲𝗿𝘀𝗲 𝗽𝗼𝘀𝘀𝗶𝗯𝗹𝗲 𝗮𝗰𝘁𝗶𝗼𝗻𝘀
            for act in possible_actions:
                # 𝗰𝗵𝗲𝗰𝗸 𝗶𝗳 𝗻𝗲𝘅𝘁 𝘁𝗿𝗮𝗻𝘁𝗶𝗼𝗻 𝘁𝗼 𝘁𝗵𝗮𝘁 𝗮𝗰𝘁𝗶𝗼𝗻 𝗮𝗻𝗱 𝗰𝗮𝗹𝗰𝘂𝗹𝗮𝘁𝗲 𝘁𝗵𝗲 𝗤-𝘃𝗮𝗹𝘂𝗲𝘀 𝗳𝗼𝗿 𝘁𝗵𝗼𝘀𝗲 𝗮𝗰𝘁𝗶𝗼𝗻𝘀
                if self.state_transitions[state][act]:
                    # 𝗴𝗲𝘁 𝗺𝗮𝘅𝗶𝗺𝘂𝗺 𝗤-𝘃𝗮𝗹𝘂𝗲 𝗼𝗳 𝘁𝗵𝗲 𝗰𝘂𝗿𝗿𝗲𝗻𝘁 𝗮𝗰𝘁𝗶𝗼𝗻 𝗯𝘆 𝗰𝗵𝗲𝗰𝗸𝗶𝗻𝗴 𝗮𝗹𝗹 𝗽𝗼𝘀𝘀𝗶𝗯𝗹𝗸𝗲 𝗻𝗲𝘅𝘁 𝗰𝗵𝗮𝗿𝗮𝗰𝘁𝗲𝗿𝘀
                    value = max([self.q_values[state][(act, nxt_ch)] for nxt_ch in self.state_transitions[state][act]])
                    # 𝗦𝘁𝗼𝗿𝗲 𝘃𝗮𝗹𝘂𝗲
                    action_values[act] = value

            # 𝗖𝗵𝗲𝗰𝗸 𝗶𝗳 𝘄𝗲𝗿𝗲 𝗮𝗰𝘁𝗶𝗼𝗻 𝘃𝗮𝗹𝘂𝗲
            if action_values:
                #  𝗚𝗲𝘁 𝗯𝗲𝘀𝘁 𝗮𝗰𝘁𝗶𝗼𝗻 𝗯𝗮𝘀𝗲𝗱 𝗼𝗻 𝗵𝗶𝗴𝗵𝗲𝘀𝘁 𝗤-𝘃𝗮𝗹𝘂𝗲𝘀
                action = max(action_values.items(), key=lambda x: x[1])[0]
                # 𝗻𝗲𝘅𝘁 𝗻𝗲𝘅𝘁 𝗰𝗵𝗮𝗿𝗮𝗰𝘁𝗲𝗿 𝘀𝘁𝗮𝘁𝗲
                next_char = random.choice(list(self.state_transitions[state][action]))
            else:
                # 𝗜𝗳 𝗻𝗼 𝗮𝗰𝘁𝗶𝗼𝗻𝘀 𝘃𝗮𝗹𝘂𝗲𝘀, 𝘁𝗵𝗲𝗻 𝗴𝗲𝘁 𝗿𝗮𝗻𝗱𝗼𝗺 𝗮𝗰𝘁𝗶𝗼𝗻
                action = random.choice(possible_actions)
                # 𝗙𝗿𝗼𝗺 𝘁𝗵𝗮𝘁 𝗿𝗮𝗻𝗱𝗼𝗺 𝗮𝗰𝘁𝗶𝗼𝗻 𝗴𝗲𝘁 𝘁𝗵𝗲 𝗻𝗲𝘅𝘁 𝗰𝗵𝗮𝗿𝗮𝗰𝘁𝗲𝗿 𝘀𝘁𝗮𝘁𝗲
                next_char = random.choice(list(self.state_transitions[state][action]))
        # 𝗥𝗲𝘁𝘂𝗿𝗻 𝘁𝗵𝗲 𝗮𝗰𝘁𝗶𝗼𝗻 𝗮𝗻𝗱 𝗻𝗲𝘅𝘁 𝗰𝗵𝗮𝗿𝗮𝗰𝘁𝗲𝗿 𝘀𝘁𝗮𝘁𝗲
        return action, next_char

    # 𝗙𝘂𝗻𝗰𝘁𝗶𝗼𝗻: Update Q-value based on the Bellman equation (⁡⁢⁣⁢𝘄𝗲 𝗱𝗼 𝗻𝗼𝘁 𝗻𝗲𝗲𝗱 𝘁𝗼 𝗰𝗵𝗮𝗻𝗴𝗲⁡)
    def update_q_value(self, state: str, action: str, next_char: str, next_state: str, reward: float):
        next_action_values = []
        for next_action in self.get_possible_actions(next_state):
            for next_next_char in self.state_transitions[next_state][next_action]:
                next_action_values.append(self.q_values[next_state][(next_action, next_next_char)])

        max_next_q = max(next_action_values, default=0)
        current_q = self.q_values[state][(action, next_char)]
        new_q = current_q + self.learning_rate * (reward + self.gamma * max_next_q - current_q)
        self.q_values[state][(action, next_char)] = new_q

# Class:  𝗚enerating credentials using Markov Decision Process
class CredentialGeneratorMDP:
    # 𝗖𝗼𝗻𝘀𝘁𝗿𝘂𝗰𝘁𝗼𝗿
    # 𝗧𝗮𝗸𝗲𝘀 𝗶𝗻 𝗖𝗦𝗩 𝗽𝗮𝘁𝗵 𝗰𝗼𝗻𝘁𝗮𝗶𝗻𝗲𝘀 𝘄𝗲𝗯 𝗱𝗮𝘁𝗮, 𝘄𝗼𝗿𝗱𝗹𝗶𝘀𝘁 𝗽𝗮𝘁𝗵 𝗳𝗼𝗿 𝘂𝘀𝗲𝗿𝗻𝗮𝗺𝗲𝘀 𝗮𝗻𝗱 𝗽𝗮𝘀𝘀𝘄𝗼𝗿𝗱𝘀
    def __init__(self, csv_path: str, wordlist_path: str):
        # 𝗧𝗿𝘆-𝗰𝗮𝘁𝗰𝗵 𝗯𝗹𝗼𝗰𝗸
        try:
            # 𝗖𝗮𝗹𝗹 𝗳𝘂𝗻𝗰𝘁𝗶𝗼𝗻 𝗲𝘅𝘁𝗿𝗮𝗰𝘁𝗶𝗻𝗴 𝘂𝘀𝗲𝗳𝘂𝗹𝗹 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝘁𝗶𝗼𝗻 𝘁𝗼 𝗴𝘂𝗶𝗱 𝘁𝗵𝗲 𝗰𝗿𝗲𝗱𝗲𝗻𝘁𝗶𝗮𝗹 𝗴𝗲𝗻𝗲𝗿𝗮𝘁𝗶𝗼𝗻 𝗽𝗿𝗼𝗰𝗲𝘀𝘀
            self.web_text = load_web_text(csv_path)
            # 𝗖𝗮𝗹𝗹 𝗳𝘂𝗻𝗰𝘁𝗶𝗼𝗻 𝘁𝗼 𝗴𝗲𝘁 𝗰𝗹𝗲𝗮𝗻𝗲𝗱 𝘄𝗼𝗿𝗱𝗹𝗶𝘀𝘁
            self.wordlists = load_wordlist(wordlist_path)
        # 𝗘𝘅𝗰𝗲𝗽𝘁𝗶𝗼𝗻 𝗲𝗿𝗿𝗼𝗿
        except (FileNotFoundError, ValueError) as e:
            print(f"Error loading input files: {e}")
            self.web_text = csv_path
            self.wordlists = wordlist_path
        # 𝗚𝗲𝘁 𝘂𝘀𝗲𝗿𝗻𝗮𝗺𝗲
        self.username_mdp = CredentialMDP(order=2)
        self.password_mdp = CredentialMDP(order=3)
        # 𝗚𝗲𝘁 𝘁𝗵𝗲 𝗽𝗮𝘀𝘀𝘄𝗼𝗿𝗱
        # 𝘂𝘀𝗲𝗿𝗻𝗮𝗺𝗲 𝗮𝗻𝗱 𝗽𝗮𝘀𝘀𝘄𝗼𝗿𝗱 𝗹𝗲𝗻𝗴𝘁𝗵 𝗰𝗼𝗻𝘀𝘁𝗿𝗶𝗻𝘁𝘀
        self.min_username_length = 5
        self.min_password_length = 10

    # 𝗙𝘂𝗻𝗰𝘁𝗶𝗼𝗻: Preprocess text data
    # 𝗧𝗮𝗸𝗲 𝘁𝗲𝘅𝘁 𝗮𝘀 𝗽𝗮𝗿𝗮𝗺𝗲𝘁𝗲𝗿 𝗮𝗻𝗱 𝗿𝗲𝘁𝘂𝗿𝗻𝘀 𝗮 𝗹𝗶𝘀𝘁 𝗼𝗳 𝘀𝘁𝗿𝗶𝗻𝗴𝘀
    def preprocess_text(self, text: str) -> List[str]:
        # 𝗦𝘁𝗼𝗿𝗲 𝗰𝗹𝗲𝗮𝗻𝗲𝗱 𝘄𝗼𝗿𝗱𝘀
        words = re.findall(r'\w+', text.lower())
        # 𝗥𝗲𝘁𝘂𝗿𝗻 𝗼𝗻𝗹𝘆 𝘁𝗵𝗲 𝘄𝗼𝗿𝗱𝘀 𝘁𝗵𝗮𝘁 𝗺𝗲𝗲𝘁 𝗺𝗶𝗻𝗶𝗺𝘂𝗺 𝗰𝗼𝗻𝘀𝘁𝗿𝗮𝗶𝗻𝘁𝘀
        return [word for word in words if len(word) >= 4]

    # 𝗙𝘂𝗻𝗰𝘁𝗶𝗼𝗻: Build state transitions for username and password generation
    def build_state_transitions(self):
        # 𝗖𝗼𝗺𝗯𝗶𝗻𝗲𝘀 𝘁𝗵𝗲 𝗽𝗿𝗲𝗽𝗼𝗰𝗲𝘀𝘀𝗲𝗱 𝘁𝗲𝘅𝘁 𝗳𝗿𝗼𝗺 𝘄𝗲𝗯_𝘁𝗲𝘅𝘁 𝗮𝗻𝗱 𝘁𝗵𝗲 𝘄𝗿𝗼𝗱𝗹𝗶𝘀𝘁
        username_data = set(self.preprocess_text(self.web_text) + self.wordlists)
        # 𝗙𝗶𝗹𝘁𝗲𝗿𝘀 𝘁𝗵𝗲 𝘂𝗻𝘀𝗲𝗿𝗻𝗮𝗺𝗲_𝗱𝗮𝘁𝗮 𝘁𝗼 𝗼𝗻𝗹𝘆 𝗶𝗻𝗰𝗹𝘂𝗱𝗲 𝘄𝗼𝗿𝗱𝘀 𝘄𝗶𝘁𝗵 𝗮𝘁 𝗹𝗲𝗮𝘀𝘁 𝟴 𝗰𝗵𝗮𝗿𝗮𝗰𝘁𝗲𝗿𝘀 𝘁𝗼 𝗯𝗲 𝘂𝘀𝗲𝗱 𝗳𝗼𝗿 𝗽𝗮𝘀𝘀𝘄𝗼𝗿𝗱 𝗴𝗲𝗻𝗲𝗿𝗮𝘁𝗶𝗼𝗻
        password_data = set(word for word in username_data if len(word) >= 8)

        # 𝗧𝗿𝗮𝘃𝗲𝗿𝘀𝗲 𝘂𝘀𝗲𝗿𝗻𝗮𝗺𝗲𝘀
        for word in username_data:
            # 𝗧𝗿𝗮𝘃𝗲𝗿𝘀 𝗲𝗮𝗰𝗵 𝗰𝗵𝗮𝗿𝗮𝗰𝘁𝗲𝗿 𝗶𝗻 𝘁𝗵𝗲 𝗽𝗮𝘀𝘀𝘄𝗼𝗿𝗱
            for i in range(len(word) - self.username_mdp.order):
                state = f"username_{word[i:i+self.username_mdp.order]}"
                action = word[i+self.username_mdp.order]
                next_char = word[i+self.username_mdp.order]
                self.username_mdp.state_transitions[state][action].add(next_char)
                if i == 0:
                    self.username_mdp.initial_states.append(state)
        # 𝗧𝗿𝗮𝘃𝗲𝗿𝘀𝗲 𝗽𝗮𝘀𝘀𝘄𝗼𝗿𝗱𝘀
        for word in password_data:
            # 𝗧𝗿𝗮𝘃𝗲𝗿𝘀𝗲 𝘁𝗵𝗲 𝗰𝗵𝗮𝗿𝗮𝗰𝘁𝗲𝗿𝘀 𝗶𝗻 𝘁𝗵𝗲 𝗽𝗮𝘀𝘀𝘄𝗼𝗿𝗱
            for i in range(len(word) - self.password_mdp.order):
                state = f"password_{word[i:i+self.password_mdp.order]}"
                action = word[i+self.password_mdp.order]
                next_char = word[i+self.password_mdp.order]
                self.password_mdp.state_transitions[state][action].add(next_char)
                if i == 0:
                    self.password_mdp.initial_states.append(state)

    # 𝗙𝘂𝗻𝗰𝘁𝗶𝗼𝗻: Generate a username and password pair
    def generate_credential(self) -> Tuple[str, str]:
        # Generate username
        if not self.username_mdp.initial_states:
            state = f"username_{random.choice(self.wordlists)[:2]}"
        else:
            # 𝗘𝗹𝘀𝗲 𝘂𝘀𝗲 𝗿𝗮𝗻𝗱𝗼𝗺
            state = random.choice(self.username_mdp.initial_states)
        # 𝗜𝗴𝗻𝗼𝗿𝗲 𝗳𝗶𝗿𝘀𝘁 𝗻 𝗰𝗵𝗮𝗿𝗮𝗰𝘁𝗲𝗿𝘀
        username = state[9:]
        # 𝗪𝗵𝗶𝗹𝗲 𝘂𝘀𝗲𝗿𝗻𝗺𝗮𝗲 𝗹𝗲𝘀𝘀 𝘁𝗵𝗮𝗻 𝗺𝗶𝗻 𝘂𝘀𝗲𝗿𝗻𝗮𝗺𝗲 𝗹𝗲𝗻𝗴𝘁𝗵
        while len(username) < self.min_username_length:
            # 𝗚𝗲𝘁 𝗮𝗰𝘁𝗶𝗼𝗻 𝗮𝗻𝗱 𝗻𝗲𝘅𝘁 𝗰𝗵𝗮𝗿𝗮𝗰𝘁𝗲𝗿
            action, next_char = self.username_mdp.choose_action(state)
            # 𝗜𝗳 𝗻𝗼𝘁𝗵𝗶𝗻𝗴 𝗳𝗼𝘂𝗻𝗱 𝗲𝘅𝗶𝘁
            if not action or not next_char:
                break
            # 𝗔𝗱𝗱 𝗰𝗵𝗮𝗿𝗮𝗰𝘁𝗲𝗿 𝘁𝗼 𝘁𝗵𝗲 𝘂𝘀𝗲𝗿𝗻𝗮𝗺𝗲
            username += next_char
            # 𝗚𝗲𝘁 𝗻𝗲𝘅𝘁 𝘀𝘁𝗮𝘁𝗲
            next_state = f"username_{username[-self.username_mdp.order:]}"
            # 𝗚𝗲𝘁 𝗿𝗲𝘄𝗮𝗿𝗱
            reward = self.username_mdp.get_reward(state, action, next_char)
            self.username_mdp.update_q_value(state, action, next_char, next_state, reward)
            # 𝗨𝗽𝗱𝗮𝘁𝗲 𝘁𝗵𝗲 𝗰𝘂𝗿𝗿𝗲𝗻𝘁 𝘀𝘁𝗮𝘁𝗲
            state = next_state
        # 𝘂𝘀𝗲𝗿𝗻𝗺𝗮𝗲 𝗿𝗲𝗮𝗰𝗵 𝗺𝗶𝗻𝗶𝗺𝘂𝗺 𝗹𝗲𝗻𝗴𝘁𝗵 𝗮𝗱𝗱 𝗿𝗮𝗻𝗱𝗼𝗺 𝗻𝘂𝗺𝗯𝗲𝗿 𝗮𝘁 𝘁𝗵𝗲 𝗲𝗻𝗱
        username = f"{username}{random.randint(1, 999)}"
        self.username_mdp.used_usernames.add(username)

        # Generate password
        if not self.password_mdp.initial_states:
            state = f"password_{random.choice(self.wordlists)[:3]}"
        else:
            # 𝗘𝗹𝘀𝗲 𝘂𝘀𝗲 𝗿𝗮𝗻𝗱𝗼𝗺
            state = random.choice(self.password_mdp.initial_states)
        # 𝗶𝗴𝗻𝗼𝗿𝗲 𝗳𝗶𝗿𝘀𝘁 𝗻 𝗰𝗵𝗮𝗿𝗮𝗰𝘁𝗲𝗿 
        password = state[9:]
        # 𝗪𝗵𝗶𝗹𝗲 𝗽𝗮𝘀𝘀𝘄𝗼𝗿𝗱 𝗹𝗲𝘀𝘀 𝘁𝗵𝗮𝗻 𝗺𝗶𝗻𝗶𝗺 𝗽𝗮𝘀𝘀𝗼𝘄𝗿𝗱 𝗹𝗲𝗻𝗴𝘁𝗵
        while len(password) < self.min_password_length:
            # 𝗚𝗲𝘁 𝗮𝗰𝘁𝗶𝗼𝗻 𝗮𝗻𝗱 𝗻𝗲𝘅𝘁 𝗰𝗵𝗮𝗿𝗮𝗰𝘁𝗲𝗿 𝘁𝗼 𝗮𝗱𝗱 𝘁𝗼 𝗽𝗮𝘀𝘀𝘄𝗼𝗿𝗱
            action, next_char = self.password_mdp.choose_action(state)
            # 𝗜𝗳 𝗻𝗼𝘁𝗵𝗶𝗻𝗴 𝗲𝘅𝗶𝘁
            if not action or not next_char:
                break
            # 𝗔𝗱𝗱 𝗰𝗵𝗮𝗿𝗮𝗰𝘁𝗲𝗿 𝘁𝗼 𝗽𝗮𝘀𝘀𝘄𝗼𝗿𝗱
            password += next_char
            # 𝗴𝗲𝘁 𝗻𝗲𝘅𝘁 𝘀𝘁𝗮𝘁𝗲
            next_state = f"password_{password[-self.password_mdp.order:]}"
            # 𝗚𝗲𝘁 𝘁𝗵𝗲 𝗿𝗲𝘄𝗮𝗿𝗱 𝗴𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱
            reward = self.password_mdp.get_reward(state, action, next_char)
            self.password_mdp.update_q_value(state, action, next_char, next_state, reward)
            # 𝗨𝗽𝗱𝗮𝘁𝗲 𝘁𝗵𝗲 𝗰𝘂𝗿𝗿𝗲𝗻𝘁 𝘀𝘁𝗮𝘁𝗲
            state = next_state
        # 𝗘𝗻𝗵𝗮𝗻𝗰𝗲 𝗽𝗮𝘀𝘀𝘄𝗼𝗿𝗱
        password = self.enhance_password(password)
        # 𝗥𝗲𝘁𝘂𝗿𝗻 𝘁𝗵𝗲 𝘂𝘀𝗲𝗿𝗻𝗮𝗺𝗲 𝗮𝗻𝗱 𝗽𝗮𝘀𝘀𝘄𝗼𝗿𝗱
        return username, password

    # 𝗙𝘂𝗻𝗰𝘁𝗶𝗼𝗻: Enhance the generated password
    # 𝗧𝗮𝗸𝗲𝘀 𝗽𝗮𝘀𝘀𝘄𝗼𝗿𝗱 𝗮𝘀 𝗽𝗮𝗿𝗮𝗺𝗲𝘁𝗲𝗿 𝗮𝗻𝗱 𝗿𝗲𝘁𝘂𝗿𝗻𝘀 𝗮 𝘀𝘁𝗿𝗶𝗻𝗴
    def enhance_password(self, password: str) -> str:
        # 𝗘𝗻𝗵𝗮𝗻𝗰𝗲 𝗽𝗮𝘀𝘀𝘄𝗼𝗿𝗱 𝗮𝗻𝗱 𝗿𝗲𝘁𝘂𝗿𝗻 𝗲𝗻𝗵𝗮𝗻𝗰𝗲𝗱 𝗽𝗮𝘀𝘀𝘄𝗼𝗿𝗱𝘀
        enhanced = password.capitalize()
        enhanced = f"{enhanced}{random.choice('!@#$%^&*')}{random.randint(0, 9)}"
        return enhanced

    # 𝗙𝘂𝗻𝗰𝘁𝗶𝗼𝗻: Generate multiple credentials
    # 𝗖𝗼𝘂𝗻𝘁 𝗴𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝘀 𝘀𝗽𝗲𝗰𝗶𝗳𝗶𝗲𝗱 𝗻𝘂𝗺𝗯𝗲𝗿 𝗼𝗳 𝘂𝘀𝗲𝗿𝗻𝗮𝗺𝗲𝘀 𝗮𝗻𝗱 𝗽𝗮𝘀𝘀𝘄𝗼𝗿𝗱𝘀 ⁡⁢⁣⁢(𝗺𝗮𝘆 𝗻𝗲𝗲𝗱 𝗯𝗲 𝗰𝗵𝗮𝗻𝗴𝗲𝗱)⁡
    # 𝗥𝗲𝘁𝘂𝗿𝗻𝘀 𝗮 𝗹𝗶𝘀𝘁 𝗼𝗳 𝘁𝘂𝗽𝗹𝗲𝘀 𝗼𝗳 𝘁𝘆𝗽𝗲 𝘀𝘁𝗿𝗶𝗻𝗴, 𝘀𝘁𝗿𝗶𝗻𝗴 𝗶𝗻𝗱𝗶𝗰𝗮𝘁𝗶𝗻𝗴 𝘂𝘀𝗲𝗿𝗻𝗮𝗺𝗲 𝗮𝗻𝗱 𝗽𝗮𝘀𝘀𝘄𝗼𝗿𝗱 𝗽𝗮𝗶𝗿𝘀
    def generate_credentials(self, count: int = 10) -> List[Tuple[str, str]]:
        # 𝗕𝘂𝗶𝗹𝗱 𝘀𝘁𝗮𝗲-𝘁𝗿𝗮𝗻𝘀𝗶𝘁𝗶𝗼𝗻𝘀
        self.build_state_transitions()
        # 𝗦𝘁𝗼𝗿𝗶𝗻𝗴 𝗰𝗿𝗲𝗱𝗲𝗻𝘁𝗶𝗮𝗹𝘀
        credentials = []
        # 𝗚𝗼 𝘁𝗶𝗹𝗹 𝗻 𝗿𝗲𝗮𝗰𝗵𝗲𝗱
        for _ in range(count):
            # 𝗚𝗲𝘁 𝘂𝘀𝗲𝗿𝗻𝗮𝗺𝗲 𝗮𝗻𝗱 𝗽𝗮𝘀𝘀𝘄𝗼𝗿𝗱 𝗽𝗮𝗶𝗿𝘀
            username, password = self.generate_credential()
            # 𝗔𝗱𝗱 𝗰𝗿𝗲𝗱𝗲𝗻𝘁𝗶𝗮𝗹𝘀 𝘁𝗼 𝗹𝗶𝘀𝘁 𝗰𝗿𝗲𝗱𝗲𝗻𝘁𝗶𝗮𝗹𝘀
            credentials.append((username, password))
        # 𝗥𝗲𝘁𝘂𝗿𝗻 𝘁𝗵𝗲 𝗰𝗿𝗲𝗱𝗲𝗻𝘁𝗶𝗮𝗹𝘀 𝗴𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 (𝘂𝘀𝗲𝗿𝗻𝗮𝗺𝗲, 𝗽𝗮𝘀𝘀𝘄𝗼𝗿𝗱)
        return credentials

# 𝗙𝘂𝗻𝗰𝘁𝗶𝗼𝗻: Main function to run the credential generation process
def main():
    # File paths
    # 𝗡𝗲𝗲𝗱 𝘁𝗼 𝗯𝗲 𝗰𝗵𝗮𝗻𝗴𝗱𝗲𝗱 𝗹𝗮𝘁𝗲𝗿 𝗼𝗻⁡
    site_list_csv_path = "site_list.csv"
    csv_path = "web_text.csv"
    wordlist_path = "wordlist.txt"

    # Load URLs from the CSV file
    urls = load_urls_from_csv(site_list_csv_path)

    scraper = WebScraper(urls)
    scraper.generate_csv(csv_path)

    # Use NLP routine to clean CSV file
    nlp_subroutine(csv_path)
    # 𝗧𝗿𝘆-𝗰𝗮𝘁𝗰𝗵 𝗯𝗹𝗼𝗰𝗸
    try:
        # 𝗖𝗿𝗲𝗮𝘁𝗲 𝗰𝗿𝗲𝗱𝗲𝗻𝘁𝗶𝗮𝗹𝘀 𝗼𝗯𝗷𝗲𝗰𝘁
        generator = CredentialGeneratorMDP(csv_path, wordlist_path)
        # 𝗴𝗲𝘁 𝗰𝗿𝗲𝗱𝗲𝗻𝘁𝗶𝗮𝗹𝘀
        credentials = generator.generate_credentials(15)
        print("\nGenerated Credentials:")
        for username, password in credentials:
            print(f"Username: {username}, Password: {password}")
    # 𝗘𝘅𝗰𝗲𝗽𝘁𝗶𝗼𝗻𝘀 𝗲𝗿𝗿𝗼𝗿
    except Exception as e:
        print(f"Error generating credentials: {e}")

if __name__ == "__main__":
    main()
