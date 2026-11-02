#!/usr/bin/env python3
"""Combine public XMLTV feeds into one XMLTV file."""

from __future__ import annotations

import gzip
import lzma
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

OUT = Path(__file__).with_name("epg.xml")
USER_AGENT = "Mozilla/5.0 (compatible; SK-CZ-HU-EPG-Merger/1.0)"

# Required country feeds first; optional Rytec additions improve coverage.
SOURCES = [
    ("Slovakia / Rytec", [
        "https://www.xmltvepg.nl/rytecSK_Basic.xz",
        "https://rytecepg.wanwizard.eu/rytecSK_Basic.xz",
        "https://epg.vuplus-community.net/rytecSK_Basic.xz",
    ], True),
    ("Czechia / IPTV-EPG", [
        "https://iptv-epg.org/files/epg-cz.xml",
    ], True),
    ("Hungary / IPTV-EPG", [
        "https://iptv-epg.org/files/epg-hu.xml",
    ], True),
    ("Czechia+Slovakia / Rytec common", [
        "https://www.xmltvepg.nl/rytecCZ_SK_Common.xz",
        "https://rytecepg.wanwizard.eu/rytecCZ_SK_Common.xz",
        "https://epg.vuplus-community.net/rytecCZ_SK_Common.xz",
    ], False),
    ("Czechia+Slovakia / Rytec sport-movies", [
        "https://www.xmltvepg.nl/rytecCZ_SK_SportMovies.xz",
        "https://rytecepg.wanwizard.eu/rytecCZ_SK_SportMovies.xz",
        "https://epg.vuplus-community.net/rytecCZ_SK_SportMovies.xz",
    ], False),
]

def download_xml(url: str) -> ET.Element:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=120) as response:
        data = response.read()
    if data.startswith(b"\xfd7zXZ\x00"):
        data = lzma.decompress(data)
    elif data.startswith(b"\x1f\x8b"):
        data = gzip.decompress(data)
    root = ET.fromstring(data)
    if root.tag != "tv":
        raise ValueError(f"Unexpected XMLTV root element: {root.tag}")
    return root

def main() -> None:
    merged = ET.Element("tv", {
        "generator-info-name": "SK-CZ-HU EPG merger",
        "generator-info-url": "https://github.com/eroxone22/moje",
    })
    channel_ids: set[str] = set()
    programme_keys: set[tuple[str, str, str]] = set()
    loaded_required = 0
    loaded_optional = 0

    for label, urls, required in SOURCES:
        root = None
        last_error = None
        for url in urls:
            try:
                root = download_xml(url)
                print(f"OK {label}: {url}")
                break
            except Exception as exc:
                last_error = exc
                print(f"FAILED {url}: {exc}", file=sys.stderr)
        if root is None:
            if required:
                raise RuntimeError(f"Required source unavailable: {label}: {last_error}")
            print(f"Skipping optional source: {label}", file=sys.stderr)
            continue

        if required:
            loaded_required += 1
        else:
            loaded_optional += 1

        for channel in root.findall("channel"):
            channel_id = channel.get("id")
            if channel_id and channel_id not in channel_ids:
                merged.append(channel)
                channel_ids.add(channel_id)

        for programme in root.findall("programme"):
            key = (
                programme.get("channel", ""),
                programme.get("start", ""),
                programme.get("stop", ""),
            )
            if key not in programme_keys:
                merged.append(programme)
                programme_keys.add(key)

    if loaded_required != 3:
        raise RuntimeError("Not all three required country feeds were loaded.")
    programmes = [node for node in merged if node.tag == "programme"]
    channels = [node for node in merged if node.tag == "channel"]
    for node in list(merged):
        merged.remove(node)
    merged.extend(channels)
    programmes.sort(key=lambda p: (p.get("start", ""), p.get("channel", "")))
    merged.extend(programmes)

    ET.indent(merged, space="  ")
    OUT.write_bytes(ET.tostring(merged, encoding="utf-8", xml_declaration=True))
    print(f"Wrote {OUT}: {len(channels)} channels, {len(programmes)} programmes; optional feeds loaded: {loaded_optional}")

if __name__ == "__main__":
    main()
