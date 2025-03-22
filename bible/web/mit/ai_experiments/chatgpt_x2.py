#!/usr/bin/env python3

from bs4 import BeautifulSoup
import json
import re

html_content = """
<HTML>
<HEAD>
<TITLE>Bible Gateway Psalm 23 :: NIV</TITLE>
<link href="ss.css" tppabs="http://www.ugcs.caltech.edu/~werdna/nnh/bibles/niv/ss.css" rel="stylesheet" type="text/css">
</HEAD>
<BODY BGCOLOR="#ffffcc">
</DL><B>Psalm 23</B><DL COMPACT>
<DT>1 <DD>Psalm 23  A psalm of David.
<DT>1 <DD>The LORD is my shepherd, I shall not be in want.
<DT>2 <DD>He makes me lie down in green pastures, he leads me beside quiet waters,
<DT>3 <DD>he restores my soul. He guides me in paths of righteousness for his name's sake.
<DT>4 <DD>Even though I walk through the valley of the shadow of death, <sup>[<a href="#footnote_252747245_1">1</a>]</sup> I will fear no evil, for you are with me; your rod and your staff, they comfort me.
<DT>5 <DD>You prepare a table before me in the presence of my enemies. You anoint my head with oil; my cup overflows.
<DT>6 <DD>Surely goodness and love will follow me all the days of my life, and I will dwell in the house of the LORD forever.
</DL>
<OL>
    <LI><A NAME="footnote_252747245_1">[4] Or <I>through the darkest valley</I></A></LI>
</OL>
</BODY>
</HTML>
"""

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Extract Psalm title
title = soup.find('b').get_text(strip=True) if soup.find('b') else "Unknown Title"

# Extract verses while recording footnote locations
verses = {}
footnote_references = {}

for dt, dd in zip(soup.find_all('dt'), soup.find_all('dd')):
    verse_number = dt.get_text(strip=True)
    verse_text = dd.get_text(strip=True)

    # Find footnotes inside the verse
    footnote_links = dd.find_all('a', href=True)
    
    if footnote_links:
        footnote_references[verse_number] = []
        for link in footnote_links:
            footnote_id = link['href'].strip("#")  # Extract footnote reference
            placeholder = f"[{footnote_id}]"  # Create a placeholder
            verse_text = re.sub(r"\[\d+\]", placeholder, verse_text)  # Replace reference with placeholder
            footnote_references[verse_number].append(footnote_id)

    verses[verse_number] = verse_text

# Extract footnotes
footnotes = {}
for li in soup.find_all('li'):
    footnote_id = li.find('a')['name'] if li.find('a') else None
    footnote_text = li.get_text(strip=True)
    if footnote_id:
        footnotes[footnote_id] = footnote_text

# Structure the data into JSON format
psalm_data = {
    "title": title,
    "verses": verses,
    "footnotes": footnotes,
    "footnote_references": footnote_references  # Maps verse numbers to footnotes they contain
}

# Convert to JSON
psalm_json = json.dumps(psalm_data, indent=4)

# Output JSON
print(psalm_json)
