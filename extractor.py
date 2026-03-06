#!/usr/bin/env python3
import sys
import os
from datetime import datetime

from bs4 import BeautifulSoup


def parse_telegram_datetime(dt_str: str) -> str:
    """
    Parse Telegram HTML 'title' datetime (e.g. '06.03.2026 14:23:45')
    and return an ISO 8601 string.
    """
    patterns = [
        "%d.%m.%Y %H:%M:%S",
        "%d.%m.%Y %H:%M",
        "%d.%m.%y %H:%M:%S",
        "%d.%m.%y %H:%M",
    ]
    for pattern in patterns:
        try:
            dt = datetime.strptime(dt_str, pattern)
            return dt.isoformat()
        except ValueError:
            continue
    return dt_str


def extract_messages_from_html(html_path: str):
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    messages = []
    for msg_div in soup.find_all("div", class_="message"):
        from_name_div = msg_div.find("div", class_="from_name")
        if not from_name_div:
            user = "System"
        else:
            user = from_name_div.get_text(strip=True)

        date_div = msg_div.find("div", class_="pull_right date details")
        if date_div and date_div.has_attr("title"):
            raw_dt = date_div["title"]
            iso_dt = parse_telegram_datetime(raw_dt)
        else:
            iso_dt = ""

        text_div = msg_div.find("div", class_="text")
        if text_div:
            text = text_div.get_text("\n", strip=True)
        else:
            text = ""

        messages.append((user, iso_dt, text))

    return messages


def write_messages_to_txt(messages, out_path: str):
    with open(out_path, "w", encoding="utf-8") as f:
        for user, iso_dt, text in messages:
            f.write(f"{user}\n")
            f.write(f"{iso_dt}\n")
            f.write(f"{text}\n\n")


def collect_messages_from_path(path: str):
    """
    If path is a file, extract messages from that single HTML.
    If path is a directory, extract messages from all *.html files inside (non-recursive),
    and return a single combined list.
    """
    all_messages = []

    if os.path.isfile(path):
        return extract_messages_from_html(path)

    if os.path.isdir(path):
        # Process all .html files in alphabetical order for determinism
        for name in sorted(os.listdir(path)):
            if not name.lower().endswith(".html"):
                continue
            full_path = os.path.join(path, name)
            if not os.path.isfile(full_path):
                continue
            msgs = extract_messages_from_html(full_path)
            all_messages.extend(msgs)
        return all_messages

    print(f"Path not found: {path}")
    sys.exit(1)


def main():
    if len(sys.argv) != 3:
        print(
            "Usage: python extract_telegram_html.py <input.html_or_folder> <output.txt>"
        )
        sys.exit(1)

    input_path = sys.argv[1]
    output_txt = sys.argv[2]

    messages = collect_messages_from_path(input_path)
    write_messages_to_txt(messages, output_txt)
    print(f"Extracted {len(messages)} messages to {output_txt}")


if __name__ == "__main__":
    main()

