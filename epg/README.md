# Combined XMLTV EPG: Czech and Hungarian sources

GitHub Actions runs the official `iptv-org/epg` grabber for five sites and writes their programme data into one XMLTV file.

## Sources

- Czech Republic: [mujtvprogram.cz](https://github.com/iptv-org/epg/tree/master/sites/mujtvprogram.cz)
- Czech Republic: [m.tv.sms.cz](https://github.com/iptv-org/epg/tree/master/sites/m.tv.sms.cz)
- Hungary: [mediaklikk.hu](https://github.com/iptv-org/epg/tree/master/sites/mediaklikk.hu)
- Hungary: [port.hu](https://github.com/iptv-org/epg/tree/master/sites/port.hu)
- Hungary: [tvmusor.hu](https://github.com/iptv-org/epg/tree/master/sites/tvmusor.hu)

## AquaPlay URL

`https://raw.githubusercontent.com/eroxone22/moje/main/epg/epg.xml`

Use this as the XMLTV/EPG URL in AquaPlay after the first successful workflow run.

The workflow collects two days of programme data and runs daily at 03:25 UTC. It can also be started manually in the [GitHub Actions tab](https://github.com/eroxone22/moje/actions).

Channel matching requires the playlist's `tvg-id` to match the XMLTV channel `id`. Similar channel names alone are not sufficient.

This repository provides programme guide data only, not TV streams.
