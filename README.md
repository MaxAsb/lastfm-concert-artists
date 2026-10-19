# Last.fm Concert Artists

Öffentliche Künstlerliste für die Konzertsuche. Die Datei [`artists.json`](artists.json) enthält ausschließlich alphabetisch sortierte Künstlernamen, keine Hörhäufigkeiten, Einzeltitel oder Zugangsdaten.

## Tägliche Aktualisierung

Unter GitHub Settings > Secrets and variables > Actions die Secrets `LASTFM_API_KEY` (API-Key) und `LASTFM_USER` (Last.fm-Benutzername) erstellen. Dann in Actions den Workflow `Publish Last.fm artist names` manuell starten. Der Workflow läuft auch täglich.

Sollte GitHub das Zurückschreiben verweigern, unter Settings > Actions > General die Workflow permissions auf Read and write permissions einstellen.

Öffentlicher Abruf: https://raw.githubusercontent.com/MaxAsb/lastfm-concert-artists/main/artists.json
