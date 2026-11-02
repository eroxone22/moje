# Combined XMLTV EPG: mujtvprogram.cz + mediaklikk.hu

GitHub Actions downloads programme data from both upstream sites using the official iptv-org/epg grabber and merges it into one XMLTV file.

Output URL (after the first successful workflow run):

`https://raw.githubusercontent.com/eroxone22/moje/main/epg/epg.xml`

Sources:
- https://github.com/iptv-org/epg/tree/master/sites/mujtvprogram.cz
- https://github.com/iptv-org/epg/tree/master/sites/mediaklikk.hu

The workflow runs daily at 03:25 UTC and can also be started manually from the Actions tab. It collects a 2-day guide.

In AquaPlay, use the raw URL above as the XMLTV/EPG URL. Channel matching requires the playlist's tvg-id to match the XMLTV channel id.

This repository provides guide data only, not TV streams.
