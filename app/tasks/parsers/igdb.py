import requests
import arrow

from app.models.orm.api import Api
from app.models.pydantic.api import ApiEnum

from ...libs.logger import logger
from ...libs.redis import get_redis


# TODO https://api-docs.igdb.com/#account-creation
class IGDB:
    def __init__(self):
      self.redis = None
      self.cache = None

    async def get_key(self):
      if not self.redis: 
        self.redis = await get_redis()
      api = await Api.get_key(ApiEnum.igdb)
      id = api.data['id']
      token = await self.redis.execute('GET', f'igdb-{id}')
      if not token:
        return await self.init_key(api)
      return id, token.decode('utf-8')

    async def init_key(self, api):
      id = api.data['id']
      response = requests.post(f"https://id.twitch.tv/oauth2/token?client_id={id}&client_secret={api.data['secret']}&grant_type=client_credentials").json()
      token = response['access_token']
      self.redis.execute('SET', f'igdb-{id}', token, 'EX', response['expires_in'])
      return id, token

    def _get_recent_releases(self, id, token):
        cutoff = int(arrow.utcnow().shift(weeks=-1).float_timestamp) # TODO: pass from release_checker
        # TODO: getting cloudflare blocked despite valid credentials?
        result = requests.get(
            f"https://api.igdb.com/v4/release_dates", 
            data=f'fields *; where date > {cutoff}; sort date asc;',            
            headers={
              'Client-ID': id,
              'Authorization': f"Bearer {token}",
            }
        )
        print('here', result)
        return self.parse_releases(result.json())

    def parse_releases(self, json: dict):
        logger.debug(json)
        # TODO

    async def get_recent_releases(self):
      id, token = await self.get_key()
      self.cache = self._get_recent_releases(id, token)

    async def get_releases(self, data):
      if not self.cache:
        await self.get_recent_releases()

      company = data["mainsnak"]["datavalue"]["value"]
      # TODO: find in cache

