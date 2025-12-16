import re
from filename_parser import CHINESE_TO_ENGLISH, SINGLE_CHAPTER_BOOKS

def convert_bible_reference(text):
    """
    Parse text and convert Bible references to a TTS-friendly format.
    strictly matches Chinese Bible book names.
    
    Rules:
    1. Standard (Colon): "約翰福音 3:16" -> "約翰福音3章16節"
    2. Single-Chapter (No Colon): "猶大書 5" -> "猶大書5節"
       (Only for books in SINGLE_CHAPTER_BOOKS)
    
    Handles:
    - Variable spacing around book names.
    - Full-width/Half-width colons (: ：).
    - Ranges with various dashes (-, —, –, ——) -> "至".
    - Commas -> "，".
    """
    
    # 1. Prepare Regex Patterns
    # Sort by length to match "约翰一书" before "约翰"
    all_books = sorted(CHINESE_TO_ENGLISH.keys(), key=len, reverse=True)
    
    # Filter for single chapter books (intersection of known Chinese books and Single list)
    # SINGLE_CHAPTER_BOOKS contains both Chinese and English, so this filter works for the Chinese keys.
    single_books = [b for b in all_books if b in SINGLE_CHAPTER_BOOKS]

    all_books_pattern = "|".join(map(re.escape, all_books))
    single_books_pattern = "|".join(map(re.escape, single_books))
    
    dash_pattern = r"[-—–]+" # Match one or more dash-like chars including em-dash
    
    # Helper to format the numbers part (verses)
    def format_verse_numbers(v_str):
        # Replace dashes with '至'
        v_str = re.sub(dash_pattern, '至', v_str)
        # Replace commas with Chinese comma
        v_str = v_str.replace(',', '，')
        return v_str

    # ---------------------------------------------------------
    # Pattern A: Standard Reference with Colon (Book Chap:Verse)
    # matches: Book Name + Spaces + Chapter + Colon + Verse(s)
    # ---------------------------------------------------------
    # Group 1: Book Name
    # Group 2: Chapter
    # Group 3: Verses (digits, dashes, commas)
    pattern_std = rf"({all_books_pattern})\s*(\d+)\s*[:：]\s*([\d{dash_pattern},]+)"
    
    def replace_std(match):
        book = match.group(1)
        chapter = match.group(2)
        verses = match.group(3)
        return f"{book}{chapter}章{format_verse_numbers(verses)}節"

    text = re.sub(pattern_std, replace_std, text)

    # ---------------------------------------------------------
    # Pattern B: Single Chapter Books (Book Verse) - NO COLON
    # matches: SingleBook Name + Spaces + Verse(s)
    # Lookahead (negative) ensures we don't match if a colon follows (though Pattern A should have caught it)
    # ---------------------------------------------------------
    # Group 1: Book Name
    # Group 2: Verses
    pattern_single = rf"({single_books_pattern})\s*([\d{dash_pattern},]+)(?![0-9:：])"
    
    def replace_single(match):
        book = match.group(1)
        verses = match.group(2)
        return f"{book}{format_verse_numbers(verses)}節"

    text = re.sub(pattern_single, replace_single, text)
    
    return text