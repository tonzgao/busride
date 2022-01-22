import requests
import xml.etree.ElementTree as ET


# Currently that rate is (on average) 1 request per second.
class MusicBrainz:
    def get_releases(self, artist: str):
        # TODO: set user agent https://musicbrainz.org/doc/MusicBrainz_API/Rate_Limiting#Provide_meaningful_User-Agent_strings
        result = requests.get(
            f"https://musicbrainz.org/ws/2/artist/{artist}?inc=releases"
        )
        return self.parse_releases(result.text)

    def parse_releases(self, xml: dict):
        return xml
