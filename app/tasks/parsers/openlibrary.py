import arrow
import requests

# https://openlibrary.org/dev/docs/api/authors
# Currently only 100 requests/IP are allowed for every 5 minutes.
class OpenLibrary:
    def get_author_releases(self, data):
        author = data["mainsnak"]["datavalue"]["value"]
        # Releases are ordered by last_modified
        result = requests.get(
            f"https://openlibrary.org/authors/${author}/works.json?limit=100"
        )
        return self.parse_releases(result.json())

    def parse_releases(self, json: dict):
        for entry in json["entries"]:
            result = self.parse_release(entry)
            yield result

    def parse_release(self, release: dict):
        return {
            "title": release["title"],
            "release_date": arrow.get(release["created"]["value"]),
            "data": {
                "last_modified": release["last_modified"]["value"],
                # Most greater than 1 are side projects or translations
                "authors": len(release["authors"]) - 1,
            },
        }
