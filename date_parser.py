import re
from datetime import datetime

def convert_dates_in_text(text):
    def repl_ymd(m):
        yyyy, mm, dd = m.groups()
        return f"{yyyy}年{int(mm)}月{int(dd)}日"

    text = re.sub(r'\b(\d{4})-(\d{1,2})-(\d{1,2})\b', repl_ymd, text)

    def repl_mdy(m):
        mm, dd, yyyy = m.groups()
        return f"{yyyy}年{int(mm)}月{int(dd)}日"

    text = re.sub(r'\b(\d{1,2})/(\d{1,2})/(\d{4})\b', repl_mdy, text)

    return text

def extract_date_from_text(text):
    """
    Extracts date from text in various formats:
    1. YYYY-MM-DD
    2. MM/DD/YYYY
    3. YYYY年MM月DD日
    4. MM月DD日 (Assumes current year)
    
    Returns date as 'YYYY-MM-DD' string or None if not found.
    """
    if not text:
        return None
        
    # 1. YYYY年MM月DD日
    match = re.search(r"(\d{4})年(\d{1,2})月(\d{1,2})日", text)
    if match:
        y, m, d = match.groups()
        return f"{y}-{int(m):02d}-{int(d):02d}"

    # 2. MM月DD日 (Implicit Year)
    match = re.search(r"(\d{1,2})月(\d{1,2})日", text)
    if match:
        m, d = match.groups()
        current_year = datetime.now().year
        return f"{current_year}-{int(m):02d}-{int(d):02d}"

    # 3. MM/DD/YYYY
    match = re.search(r"(\d{1,2})/(\d{1,2})/(\d{4})", text)
    if match:
        m, d, y = match.groups()
        return f"{y}-{int(m):02d}-{int(d):02d}"

    # 4. YYYY-MM-DD
    match = re.search(r"(\d{4})-(\d{1,2})-(\d{1,2})", text)
    if match:
        y, m, d = match.groups()
        return f"{y}-{int(m):02d}-{int(d):02d}"

    return None
