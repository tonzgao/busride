from pywikibot.data import api
import pywikibot

site = pywikibot.Site("wikidata", "wikidata")

def list_entities(name: str) -> list:
  params = { 'action' :'wbsearchentities' , 'format' : 'json' , 'language' : 'en', 'type' : 'item', 'search': name}
  request = api.Request(site=site,**params)
  return request.submit()

def get_entity(id: str):
  # TODO: parse entity for relevant information
  request = api.Request(site=site,
                        action='wbgetentities',
                        format='json',
                        ids=id)    
  return request.submit()