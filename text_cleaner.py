import re

def remove_space_before_god(text):
    """
    Removes half-width and full-width spaces before the character '神'.
    Args:
        text (str): Input text.
    Returns:
        str: Text with spaces removed before '神'.
    """
    text = re.sub(r'　(神)', r'\1', text)
    return text

def clean_text(text):
    """
    Master cleaning function.
    Currently only removes extra spaces before 'God' (神).
    """
    text = remove_space_before_god(text)
    return text

