"""Provide client to insrument API."""
import logging
import logging.config
import requests

logger = logging.getLogger(__name__)

class Client():
  """Instruct API to move piece."""
  def __init__(self, url):
    self.url = url
  
  def get(self, square=None, piece=None):
    # validations ahoy
    url = '/'.join([self.url, 'move'])
    data = {'square[]': square, 'piece[]':piece}
    resp = requests.get('%s' % url, params=data)
    if resp.stats_code != 201:
      logger.warning(resp.txt)
    return resp.json()
