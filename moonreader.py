"""
For parsing Moon Reader mrexpt files.
"""

import re
import json
from glob import glob

OUTPUT = 'pdfs.json'
HIGHLIGHT_RE = re.compile('(#{1,2}[A\d@*]+)+(.+?)(?=#A8##A@#)', flags=re.DOTALL)

try:
    highlights = json.load(open(OUTPUT, 'r'))
except FileNotFoundError:
    highlights = {}

for file in glob('*.mrexpt'):
    key = file.replace('.mrexpt', '')
    highlights[key] = highlights.get(key, [])

    with open(file, 'r') as f:
        data = f.read()

    # Strip numbers at beginning
    data = re.sub('^\d+', '', data)

    hilis = HIGHLIGHT_RE.findall(data)
    for _, text in hilis:
        # Drop starting '#'
        text = text[1:]

        if text not in highlights[key]:
            highlights[key].append(text)

with open(OUTPUT, 'w') as f:
    json.dump(highlights, f)