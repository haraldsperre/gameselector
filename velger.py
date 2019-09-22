import simplejson as json
import requests
import xml.etree.ElementTree as ET
from random import shuffle


def finn_spill_liste(sted):
  with open('steder.json', encoding='utf-8') as sted_file:
    steder = json.load(sted_file)
  sted = steder[sted]
  url = 'https://www.boardgamegeek.com/xmlapi2/collection'
  status_code = 0

  while status_code != 200:
    querystring = {
      'username': sted,
      'excludesubtype': 'boardgameexpansion'
    }
    response = requests.get(url, params=querystring)
    status_code = response.status_code

  return list(ET.fromstring(response.text))

def finn_spill(sted, antall_spillere, spilletid):
  url = 'https://www.boardgamegeek.com/xmlapi2/thing'
  spill = finn_spill_liste(sted)
  spill_liste = list(spill)
  shuffle(spill_liste)

  for valg in spill_liste:
    querystring = {
      'id': valg.attrib['objectid']
    }
    response = requests.get(url, params=querystring)
    info = ET.fromstring(response.text).getchildren()[0].getchildren()
    spill = {}
    for element in info:
      if element.tag == 'image':
        spill['image'] = element.text
      elif element.tag == 'name' and element.attrib['type'] == 'primary':
        spill['navn'] = element.attrib['value']
      elif element.tag == 'minplayers':
        spill['minplayers'] = int(element.attrib['value'])
        if spill['minplayers'] > antall_spillere:
          break
      elif element.tag == 'maxplayers':
        spill['maxplayers'] = int(element.attrib['value'])
        if spill['maxplayers'] < antall_spillere:
          break
      elif element.tag == 'minplaytime':
        spill['mintid'] = int(element.attrib['value'])
        if spill['mintid'] > spilletid:
          break
      elif element.tag == 'maxplaytime':
        spill['maxtid'] = int(element.attrib['value'])
      if 'maxtid' in spill and 'mintid' in spill:
        if (spill['maxtid'] + spill['mintid'])/2 > spilletid:
          break
    else:
      return spill
  return {}
