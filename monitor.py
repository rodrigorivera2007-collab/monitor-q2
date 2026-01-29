import feedparser
import os
import time
import urllib.parse

# SOURCE CONFIGURATION
# Dictionary containing social media names and their respective Google Alerts RSS feed URLs
MY_ALERTS = {
    "Google News": "https://www.google.com/alerts/feeds/01887550311641805276/7716548066590087574",
    "Facebook": "https://www.google.com/alerts/feeds/01887550311641805276/135799460851061576",
    "Instagram": "https://www.google.com/alerts/feeds/01887550311641805276/3450936725565665775",
    "X (Twitter)": "https://www.google.com/alerts/feeds/01887550311641805276/6701889539388378885",
    "YouTube": "https://www.google.com/alerts/feeds/01887550311641805276/9628050986709898055",
    "LinkedIn": "https://www.google.com/alerts/feeds/01887550311641805276/5498586337459388710"
}

LOG_FILE = "registro_quetzal2.txt"

# URL cleaning function

def clean_google_link(raw_url):
    """
    Extracts the direct destination URL from a Google Alerts wrapper.
    """
    try:
        parsed_url = urllib.parse.urlparse(raw_url)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        
        if 'url' in query_params:
            return query_params['url'][0]
    except Exception:
        pass
    
    return raw_url

# MAIN PROCESSING FUNCTION
def update():
    """
    Fetches RSS feeds and appends new entries to the log file.
    """
    # Create log file with header if it doesn't exist
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write(f"QUETZAL-2 MONITORING LOG\n{'='*60}\n")

    # Load existing history to prevent duplicates
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        history = f.read()

    # Iterate through each alert source
    for source_name, rss_url in MY_ALERTS.items():
        feed = feedparser.parse(rss_url)
        
        if not feed.entries:
            continue

        # Append new entries to the log file
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            for entry in feed.entries:
                clean_link = clean_google_link(entry.link)
                
                # Save entry only if the link is not in history
                if clean_link not in history:
                    block = (
                        f"SOURCE:  {source_name}\n"
                        f"TITLE:   {entry.title}\n"
                        f"LINK:    {clean_link}\n"
                        f"DATE:    {entry.published}\n"
                        f"{'-' * 60}\n"
                    )
                    f.write(block)
                    history += clean_link

if __name__ == "__main__":
    update()
