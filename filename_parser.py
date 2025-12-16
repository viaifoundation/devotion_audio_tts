from datetime import datetime, timedelta

# Full mapping: Chinese (Simplified + Traditional) → Standard English abbreviation
# Feel free to add more if you ever use rare books
CHINESE_TO_ENGLISH = {
    # Simplified Chinese (zh-cn)
    "创世记": "Genesis",   "创": "Genesis",
    "出埃及记": "Exodus",  "出": "Exodus",
    "利未记": "Leviticus", "利": "Leviticus",
    "民数记": "Numbers",   "民": "Numbers",
    "申命记": "Deuteronomy","申": "Deuteronomy",
    "约书亚记": "Joshua",  "书": "Joshua",
    "士师记": "Judges",    "士": "Judges",
    "路得记": "Ruth",      "得": "Ruth",
    "撒母耳记上": "1Samuel", "撒上": "1Samuel",
    "撒母耳记下": "2Samuel", "撒下": "2Samuel",
    "列王纪上": "1Kings",   "王上": "1Kings",
    "列王纪下": "2Kings",   "王下": "2Kings",
    "历代志上": "1Chronicles", "代上": "1Chron",
    "历代志下": "2Chronicles", "代下": "2Chron",
    "以斯拉记": "Ezra",    "拉": "Ezra",
    "尼希米记": "Nehemiah", "尼": "Nehemiah",
    "以斯帖记": "Esther",  "斯": "Esther",
    "约伯记": "Job",       "伯": "Job",
    "诗篇": "Psalm",       "诗": "Psalm",
    "箴言": "Proverbs",    "箴": "Proverbs",
    "传道书": "Ecclesiastes","传": "Ecclesiastes",
    "雅歌": "SongOfSolomon","歌": "SongOfSongs",
    "以赛亚书": "Isaiah",  "赛": "Isaiah",
    "耶利米书": "Jeremiah","耶": "Jeremiah",
    "耶利米哀歌": "Lamentations","哀": "Lamentations",
    "以西结书": "Ezekiel", "结": "Ezekiel",
    "但以理书": "Daniel",  "但": "Daniel",
    "何西阿书": "Hosea",   "何": "Hosea",
    "约珥书": "Joel",      "珥": "Joel",
    "阿摩司书": "Amos",    "摩": "Amos",
    "俄巴底亚书": "Obadiah","俄": "Obadiah",
    "约拿书": "Jonah",     "拿": "Jonah",
    "弥迦书": "Micah",     "弥": "Micah",
    "那鸿书": "Nahum",     "鸿": "Nahum",
    "哈巴谷书": "Habakkuk", "哈": "Habakkuk",
    "西番雅书": "Zephaniah","番": "Zephaniah",
    "哈该书": "Haggai",    "该": "Haggai",
    "撒迦利亚书": "Zechariah","亚": "Zechariah",
    "玛拉基书": "Malachi", "玛": "Malachi",

    "马太福音": "Matthew", "太": "Matthew",
    "马可福音": "Mark",   "可": "Mark",
    "路加福音": "Luke",   "路": "Luke",
    "约翰福音": "John",   "约": "John",
    "使徒行传": "Acts",   "徒": "Acts",
    "罗马书": "Romans",   "罗": "Romans",
    "哥林多前书": "1Corinthians", "林前": "1Cor",
    "哥林多后书": "2Corinthians", "林后": "2Cor",
    "加拉太书": "Galatians", "加": "Galatians",
    "以弗所书": "Ephesians", "弗": "Ephesians",
    "腓立比书": "Philippians","腓": "Philippians",
    "歌罗西书": "Colossians", "西": "Colossians",
    "帖撒罗尼迦前书": "1Thessalonians", "帖前": "1Thess",
    "帖撒罗尼迦后书": "2Thessalonians", "帖后": "2Thess",
    "提摩太前书": "1Timothy", "提前": "1Tim",
    "提摩太后书": "2Timothy", "提后": "2Tim",
    "提多书": "Titus",     "多": "Titus",
    "腓利门书": "Philemon", "门": "Philemon",
    "希伯来书": "Hebrews", "来": "Hebrews",
    "雅各书": "James",     "雅": "James",
    "彼得前书": "1Peter",  "彼前": "1Pet",
    "彼得后书": "2Peter",  "彼后": "2Pet",
    "约翰一书": "1John",   "约一": "1John",
    "约翰二书": "2John",   "约二": "2John",
    "约翰三书": "3John",   "约三": "3John",
    "犹大书": "Jude",      "犹": "Jude",
    "启示录": "Revelation","启": "Revelation",

    # Traditional Chinese (zh-tw) – most are the same, but a few differ
    "創世記": "Genesis", "出埃及記": "Exodus", "利未記": "Leviticus",
    "民數記": "Numbers", "申命記": "Deuteronomy",
    "約書亞記": "Joshua", "士師記": "Judges", "路得記": "Ruth",
    "撒母耳記上": "1Samuel", "撒母耳記下": "2Samuel",
    "列王紀上": "1Kings", "列王紀下": "2Kings",
    "歷代志上": "1Chronicles", "歷代志下": "2Chronicles",
    "以斯拉記": "Ezra", "尼希米記": "Nehemiah", "以斯帖記": "Esther",
    "約伯記": "Job", "詩篇": "Psalm", "箴言": "Proverbs",
    "傳道書": "Ecclesiastes", "雅歌": "SongOfSongs",
    "以賽亞書": "Isaiah", "耶利米書": "Jeremiah", "耶利米哀歌": "Lamentations",
    "以西結書": "Ezekiel", "但以理書": "Daniel",
    "馬太福音": "Matthew", "馬可福音": "Mark", "路加福音": "Luke",
    "約翰福音": "John", "使徒行傳": "Acts", "羅馬書": "Romans", 
}

def translate_chinese_book(book_name: str) -> str:
    """Return English book name if input is Chinese, otherwise return original."""
    return CHINESE_TO_ENGLISH.get(book_name.strip(), book_name)

def generate_filename(verse: str, date: str = None) -> str:
    if date is None:
        date_obj = datetime.today()
    else:
        date_obj = datetime.strptime(date, "%Y-%m-%d")

    # Split verse into book + chapter:verse
    # Accepts many formats: 約翰福音 3:16, John 3:16, 约3:16, 詩篇23:1 etc.
    parts = verse.replace("：", ":").split()
    chapter_verse = parts[-1]                     # last part is always chapter:verse
    book_parts = parts[:-1]

    # Re-join book name in case it has multiple words (e.g. 撒母耳記上)
    full_book = "".join(book_parts)
    english_book = translate_chinese_book(full_book)

    # Final reference: Psalm-23-1 or 1Cor-3-16 etc.
    reference = f"{english_book}-{chapter_verse.replace(':', '-')}"

    date_str = date_obj.strftime("%Y-%m-%d")
    return f"VOTD_{reference}_{date_str}.mp3"

import re

# Books with only one chapter (where "Book Num" often means "Book Verse")
SINGLE_CHAPTER_BOOKS = {
    "俄巴底亚书", "俄", "Obadiah",
    "腓利门书", "门", "Philemon",
    "约翰二书", "约二", "2John",
    "约翰三书", "约三", "3John",
    "犹大书", "犹", "Jude"
}

def extract_verse_from_text(text: str) -> str:
    """
    Extracts the first valid Chinese Bible verse reference from text.
    Strictly matches known book names defined in CHINESE_TO_ENGLISH mapping.
    
    Supports:
    1. Standard: Book Chapter:Verse(-Range)? (e.g., 罗马书 10:14-17)
    2. Single-Chapter: Book Verse(-Range)? (e.g., 犹大书 24-25 -> 犹大书 1:24-25)
    """
    # Sort keys by length descending
    book_names = sorted(CHINESE_TO_ENGLISH.keys(), key=len, reverse=True)
    book_pattern = "|".join(map(re.escape, book_names))
    
    # Pattern 1: Standard (Book Chap:Verse...)
    # Matches: 罗马书 10:14, 罗马书 10:14-17
    # Dash pattern: hyphen, en dash, em dash, double em dash
    dash_re = r"(?:-|—|——|–)"
    
    # regex_std matches: (Book) (Chapter) : (Verse[-Verse])
    # Note: We use dash_re for the range part
    regex_std = rf"({book_pattern})\s*(\d+)[:：](\d+(?:{dash_re}\d+)?)"
    match_std = re.search(regex_std, text)
    
    if match_std:
        raw = match_std.group(0)
        # Normalize all dash types to standard hyphen
        raw = re.sub(dash_re, '-', raw)
        return raw.replace('：', ':')

    # Pattern 2: Single Chapter Books (Book Verse...)
    # Only match if the book is in SINGLE_CHAPTER_BOOKS logic
    # Filter book_names to only single chapter ones
    single_books = [b for b in book_names if b in SINGLE_CHAPTER_BOOKS]
    if single_books:
        single_pattern = "|".join(map(re.escape, single_books))
        regex_single = rf"({single_pattern})\s*(\d+(?:{dash_re}\d+)?)"
        match_single = re.search(regex_single, text)
        
        if match_single:
            book = match_single.group(1)
            verse_part = match_single.group(2)
            # Normalize dashes in verse part
            verse_part = re.sub(dash_re, '-', verse_part)
            # Normalize to Book 1:Verse format so other tools parse it correctly
            return f"{book} 1:{verse_part}"

    return None



# ———————————————————————
# Demo
# ———————————————————————
if __name__ == "__main__":
    test_verses = [
        "John 3:16",
        "約翰福音 3:16",      # Simplified
        "約翰福音 3：16",     # Full-width colon
        "約3:16",            # Common short form
        "詩篇 23:1",
        "馬太福音5:16",
        "啟示錄 22:21",       # Revelation
        "撒母耳記上 16:7",    # 1 Samuel
    ]

    for v in test_verses:
        print(f"{v:20} → {generate_filename(v)}")
