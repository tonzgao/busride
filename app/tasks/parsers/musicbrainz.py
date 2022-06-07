import xml.etree.ElementTree as ET

import arrow
import requests

from ...libs.logger import logger

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
        logger.debug(xml)
        root = ET.fromstring(xml)
        for release in root[0]:
            try:
                result = self.parse_release(release)
                if result:
                    yield result
            except Exception as e:
                logger.warn(f"Failed to parse release", exc_info=e)

    def parse_release(self, xml: ET.Element):
        title = xml.find(f"{header}title")
        date = xml.find(f"{header}first-release-date")
        type = xml.find(f"{header}primary-type")
        if not date.text:
            return
        return {
            "release_date": arrow.get(date.text),
            "title": title.text,
            "data": {"type": type.text},
        }
