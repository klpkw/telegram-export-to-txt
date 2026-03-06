## Telegram HTML to TXT Extractor

Convert exported Telegram chat history (in HTML format) into a simple, line‑oriented text file that is easy to read, diff, or feed into other tools.

Each message in the output contains:
- **Author line** – the sender name (or `System` for service messages)
- **Timestamp line** – message time in ISO 8601 format (when available)
- **Message text** – the message body (may span multiple lines)
- **Blank line** – separator between messages

### Requirements

- **Python 3.8+**
- Python package: **BeautifulSoup4**

Install the dependency with:

```bash
pip install beautifulsoup4
```

### Getting Telegram HTML export

1. In the Telegram desktop app, export chat history as **HTML**:
   - `Settings` → `Advanced` → `Export Telegram data`  
   - Choose **HTML** format.
2. You can point this tool either to:
   - a **single exported HTML file**, or
   - a **folder containing multiple HTML files** (non‑recursive; all `*.html` files in that folder are processed in alphabetical order).

### Usage

From the project directory:

```bash
python extractor.py <input.html_or_folder> <output.txt>
```

- **`<input.html_or_folder>`**: path to a single HTML export file *or* a directory with multiple Telegram HTML exports.
- **`<output.txt>`**: path to the text file that will be created.

Examples:

```bash
# Single exported HTML file
python extractor.py chat_export.html chat.txt

# Directory with multiple HTML exports
python extractor.py exports/ all_chats.txt
```

### Output format

For each message, the output text looks like:

```text
Alice
2026-03-06T14:23:45
Hey, are you there?

Bob
2026-03-06T14:24:10
Yes, what's up?
```

Notes:
- If a timestamp cannot be parsed, the original Telegram datetime string is written as‑is.
- System messages (e.g. "User joined the group") are labeled with user `System`.

### Limitations

- The extractor expects the standard Telegram desktop HTML export structure (e.g. `div.message`, `div.from_name`, `div.pull_right.date.details`, `div.text`).
- Attachments (photos, files, stickers, etc.) are not exported as binaries; only their textual description/captions are included if present in the HTML.

