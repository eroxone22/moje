# SK + CZ + HU XMLTV EPG

This folder contains an automatically refreshed combined XMLTV guide for Slovakia, Czechia and Hungary.

## Source feeds

- Slovakia: Rytec `rytecSK_Basic.xz` (with Rytec mirrors)
- Czechia: IPTV-EPG.org `epg-cz.xml`
- Hungary: IPTV-EPG.org `epg-hu.xml`
- Extra Czech/Slovak shared and sports/movie listings: Rytec feeds where available

The workflow refreshes the combined file daily. The generated guide is published at:

`https://raw.githubusercontent.com/eroxone22/moje/main/epg/epg.xml`

## AquaPlay

Paste that URL into AquaPlay's EPG/XMLTV URL field. Channel matching still depends on the `tvg-id` values in your M3U playlist matching the XMLTV `channel id` values.

Sources are third-party public XMLTV feeds. Their coverage and availability can change. This repository only combines guide data; it does not provide TV streams.
