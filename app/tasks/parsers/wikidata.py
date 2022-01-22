from .musicbrainz import MusicBrainz
from .openlibrary import OpenLibrary
from .tmdb import TMDB

parsers = {"P434": MusicBrainz, "P648": OpenLibrary, "P4985": TMDB}
