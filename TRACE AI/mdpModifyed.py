# import random
# import re
# from collections import defaultdict
# import numpy as np
# from typing import Dict, List, Tuple, Set
# import csv
# import os
# import time
# import pandas as pd
# import string
# import nltk
# from nltk.corpus import stopwords
# # Request and BeatifulSoup are used together for web scraping task.#



import re
import nltk
from nltk import word_tokenize
# Download the necessary NLTK datasets if not already downloaded
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)

# 4.1 The NLP algorithm shall normalize all text in its output by removing non-English characters and resolving encoding issues.
def remove_non_english_characters(text):
    # Ensure text is decoded correctly if it's in bytes
    try:
        text = text.decode('utf-8') if isinstance(text, bytes) else text
    except (UnicodeDecodeError, TypeError):
        text = text.decode('utf-8', errors='replace') if isinstance(text, bytes) else text
    
    # Filter characters that are ASCII (English letters, digits, or basic punctuation)
    return ''.join(char for char in text if char.isascii())

# 4.2. The NLP algorithm shall break up compound words (ex. sister-in-law -> sister, in, law).
def split_hyphens(text):
    return re.findall(r'\b\w+\b', text)

# 4.3 The NLP algorithm shall remove determiners (e.g., "the", "an", "a").
def remove_determiners(text):
    pass

# Main processing pipeline
if __name__ == "__main__":
    # Example input text
    text = "The sister-in-law bought an こんにちは apple."

    # Step 1: Normalize text by removing non-English characters
    cleaned_text = remove_non_english_characters(text)

    # Step 2: Split compound words (e.g., hyphenated words)
    split_text = ' '.join(split_hyphens(cleaned_text))

    # Step 3: Remove determiners
    # final_text = remove_determiners(split_text)

    # Print results
    print("Original Text:", text)
    print("Cleaned Text (Non-English Characters Removed):", cleaned_text)
    print("Text after Splitting Hyphens:", split_text)
    # print("Final Text (After Removing Determiners):", final_text)

    print(remove_determiners(split_text))
