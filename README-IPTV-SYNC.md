# IPTV playlist synchronization

GitHub Actions runs every 6 hours and can also be started manually from the Actions tab.

It merges these iptv-org sources:
- cz.m3u
- sk.m3u
- sk_antik.m3u
- hu.m3u

The existing playlist is the base. Existing entries are never removed. When a source entry matches an existing entry by \`tvg-id\` (or normalized channel name if no ID exists), only its stream URL is refreshed; the existing metadata, logos, and VLC options remain unchanged. New source entries are appended.

Before replacing the playlist, the workflow renames the current file to a timestamped \`.bak.*\` backup on the server.

## Required GitHub Actions secrets

Add these in **Settings → Secrets and variables → Actions → New repository secret**:
- \`FTP_HOST\`: FTP server hostname or IP
- \`FTP_PORT\`: \`21\`
- \`FTP_USER\`: FTP username
- \`FTP_PASSWORD\`: FTP password

The remote file is \`/ts-mta.g6.cz/web/moje_upravene_s_logami.m3u\`.

**Security:** plain FTP does not encrypt credentials or playlist contents. Use FTPS if the hosting provider supports it; this workflow currently uses plain FTP.
