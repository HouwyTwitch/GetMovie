from requests import get
import re


def get_latest_chrome_useragent():
    url = 'https://www.whatismybrowser.com/guides/the-latest-user-agent/chrome'
    try:
        response = get(url)
        content = response.content.decode('utf-8-sig', errors='ignore')
        return content.split('<td>Chrome (Standard)</td>')[1].split('</span>')[0].split('<span class="code">')[1]
    except:
        return None

def sanitize_filename(filename):
    # Define a regex pattern for unsupported characters
    unsupported_chars = r'[\\/:*?"<>|]'
    
    # Replace unsupported characters with an underscore
    sanitized = re.sub(unsupported_chars, '_', filename)
    
    # Remove leading and trailing spaces and periods
    sanitized = sanitized.strip(' .')
    
    # If the filename is empty after sanitization, return a default name
    if not sanitized:
        return 'untitled'
    
    return sanitized