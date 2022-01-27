import requests
import xml.etree.ElementTree as ET

header = "{http://musicbrainz.org/ns/mmd-2.0#}"

# Currently that rate is (on average) 1 request per second.
class MusicBrainz:
    def get_releases(self, data):
        artist = data["mainsnak"]["datavalue"]["value"]
        # TODO: set user agent https://musicbrainz.org/doc/MusicBrainz_API/Rate_Limiting#Provide_meaningful_User-Agent_strings
        result = requests.get(
            f"https://musicbrainz.org/ws/2/release-group?artist={artist}&type=album|ep&limit=100"
        )
        return self.parse_releases(result.text)

    def parse_releases(self, xml: str):
        root = ET.fromstring(xml)
        for release in root[0]:
            result = self.parse_release(release)
            yield result

    def parse_release(self, xml: ET.Element):
        title = xml.find(f"{header}title")
        date = xml.find(f"{header}first-release-date")
        type = xml.find(f"{header}primary-type")
        return {
            "release_date": date.text,
            "data": {"title": title.text, "type": type.text},
        }
