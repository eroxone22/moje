#!/usr/bin/env python3
"""Merge iptv-org regional playlists into an existing customized M3U."""
from __future__ import annotations

import ftplib
import io
import os
import re
import sys
import unicodedata
from datetime import datetime, timezone
from urllib.request import Request, urlopen

SOURCES = [
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/cz.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/sk.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/sk_antik.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/hu.m3u",
]
REMOTE_FILE = os.getenv("FTP_REMOTE_FILE", "/ts-mta.g6.cz/web/moje_upravene_s_logami.m3u")


def fetch(url: str) -> str:
    req = Request(url, headers={"User-Agent": "iptv-playlist-sync/1.0"})
    with urlopen(req, timeout=45) as response:
        return response.read().decode("utf-8-sig")


def parse(text: str):
    lines = [line.rstrip("\r") for line in text.splitlines() if line.strip()]
    header = []
    records = []
    current = []
    for line in lines:
        if line.startswith("#EXTINF:"):
            if current:
                records.append(current)
            current = [line]
        elif current:
            current.append(line)
        else:
            header.append(line)
    if current:
        records.append(current)
    return header, records


def stream_index(record):
    for i, line in enumerate(record):
        if not line.startswith("#"):
            return i
    return None


def identity(record):
    if not record:
        return None
    extinf = record[0]
    match = re.search(r'\btvg-id="([^"]*)"', extinf, re.I)
    if match and match.group(1).strip():
        return "id:" + match.group(1).strip().casefold()
    name = extinf.rsplit(",", 1)[-1].strip()
    normalized = unicodedata.normalize("NFKD", name)
    normalized = "".join(c for c in normalized if not unicodedata.combining(c))
    normalized = re.sub(r"[^a-z0-9]+", "", normalized.casefold())
    return "name:" + normalized if normalized else None


def merge(existing_text: str, source_texts: list[str]) -> str:
    header, existing = parse(existing_text)
    if not header:
        header = ["#EXTM3U"]
    positions = {}
    for idx, record in enumerate(existing):
        key = identity(record)
        if key and key not in positions:
            positions[key] = idx

    added = []
    seen_source = set()
    for source_text in source_texts:
        _, source_records = parse(source_text)
        for source_record in source_records:
            key = identity(source_record)
            if key and key in seen_source:
                continue
            if key:
                seen_source.add(key)
            src_url_idx = stream_index(source_record)
            if src_url_idx is None:
                continue
            if key and key in positions:
                target = existing[positions[key]]
                target_url_idx = stream_index(target)
                if target_url_idx is not None:
                    target[target_url_idx] = source_record[src_url_idx]
            else:
                added.append(source_record)

    output = list(header)
    for record in existing:
        output.extend(record)
    for record in added:
        output.extend(record)
    return "\n".join(output) + "\n"


def ftp_connect():
    host = os.environ["FTP_HOST"]
    user = os.environ["FTP_USER"]
    password = os.environ["FTP_PASSWORD"]
    port = int(os.getenv("FTP_PORT", "21"))
    ftp = ftplib.FTP()
    ftp.connect(host, port, timeout=45)
    ftp.login(user, password)
    ftp.set_pasv(True)
    return ftp


def main():
    if not REMOTE_FILE.startswith("/"):
        raise ValueError("FTP_REMOTE_FILE must be an absolute server path")
    sources = [fetch(url) for url in SOURCES]
    ftp = ftp_connect()
    try:
        existing_buffer = io.BytesIO()
        try:
            ftp.retrbinary(f"RETR {REMOTE_FILE}", existing_buffer.write)
            existing_text = existing_buffer.getvalue().decode("utf-8-sig")
        except ftplib.error_perm as exc:
            if not str(exc).startswith("550"):
                raise
            raise RuntimeError(
                f"Existing playlist not found at {REMOTE_FILE}; refusing to create an empty replacement"
            ) from exc

        result = merge(existing_text, sources)
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        temp_file = REMOTE_FILE + ".uploading"
        backup_file = REMOTE_FILE + ".bak." + timestamp
        payload = result.encode("utf-8")
        ftp.storbinary(f"STOR {temp_file}", io.BytesIO(payload))
        ftp.rename(REMOTE_FILE, backup_file)
        try:
            ftp.rename(temp_file, REMOTE_FILE)
        except Exception:
            ftp.rename(backup_file, REMOTE_FILE)
            raise
        print(f"Updated {REMOTE_FILE}; backup: {backup_file}; bytes: {len(payload)}")
    finally:
        try:
            ftp.quit()
        except Exception:
            ftp.close()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
