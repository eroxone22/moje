# Combined XMLTV EPG: Slovakia, Czechia and Hungary

GitHub Actions runs the official `iptv-org/epg` grabber for these four sources and combines their programme data into one XMLTV file.

## Sources

- Czechia: [mujtvprogram.cz](https://github.com/iptv-org/epg/tree/master/sites/mujtvprogram.cz)
- Slovakia: [webtv.sk](https://github.com/iptv-org/epg/tree/master/sites/webtv.sk)
- Hungary: [port.hu](https://github.com/iptv-org/epg/blob/master/sites/port.hu/port.hu.channels.xml)
- Slovakia: [horizon.tv](https://github.com/iptv-org/epg/tree/master/sites/horizon.tv)

## AquaPlay URL

`https://raw.githubusercontent.com/eroxone22/moje/main/epg/epg.xml`

Use this as the XMLTV/EPG URL in AquaPlay after the latest workflow run completes successfully.

The workflow collects two days of programme data and runs daily at 03:25 UTC. It can also be started manually in the [GitHub Actions tab](https://github.com/eroxone22/moje/actions).

Channel matching requires the playlist's `tvg-id` to match the XMLTV channel `id`. Similar channel names alone are not sufficient.

This repository provides programme guide data only, not TV streams.
