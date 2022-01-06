#!/usr/bin/env python3
import asyncio
import argparse
import json
import logging
import sys
import os
from dotenv import load_dotenv

load_dotenv('.env') # other imports use env variables so this comes first
from en_passant import config
from en_passant.mover import Mover
from en_passant.api import run_passant_service
from en_passant.client import Client

FORMAT = '%(asctime)s %(levelname)s %(name)s - %(message)s'
LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'formatters': {
    'default': {
      'format': FORMAT,
    },
  },
  'handlers': {
    'console': {
      'class': 'logging.StreamHandler',
      'formatter': 'default',
    },
  },
  'loggers': {
    'en': {'level': 'DEBUG'},
  },
  'root': {
    'level': 'DEBUG',
    'handlers': ['console'],
  },
}
logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)

def main_client(argv=None):
  """Client for running API instance."""
  if argv is None:
    argv = sys.argv[1:]
  parser = argparse.ArgumentParser()
  parser.add_argument('--url', default='http://localhost:8080/en/api/v1/passant/', help='Base URL of target API.')
  parser.add_argument('--square', default='B4', help='The destination square of the pawn.')
  parser.add_argument('--piece', default=None, help='The en passanter (passantor?).')
  args = parser.parse_args(argv)
  if not move_validator(args.square, args.piece): # probably a good idea if this came with an actual function
    logger.info('You are not worthy of this move.')
    return 1
  logger.debug('Moving %s to %s' % (args.piece, args.square))
  client = Client(args.url)
  outputHandler(client.get(args.piece, args.square))

def main_cli(argv=None):
  """Direct CLI entry point."""
  if argv is None:
    argv = sys.argv[1:]
  parser = argparse.ArgumentParser()
  parser.add_argument('--square', default='B4', help='The destination square of the pawn.')
  parser.add_argument('--piece', default=None, help='The en passanter (passantor?).')
  args = parser.parse_args(argv)
  mover = Mover()
  # go ahead, make me validate
  return outputHandler(mover.move(args.piece, args.square))

def main_api(argv=None):
  """Start API, listen for requests."""
  if argv is None:
    argv = sys.argv[1:]
  parser = argparse.ArgumentParser()
  parser.add_argument('--host', default=None, help='The host to bind to.')
  parser.add_argument('--port', type=int, default=0, help='The port to bind to.')
  args = parser.parse_args(argv)
  return run_passant_service(host=args.host, port=args.port)

def outputHandler(capturedpiece, use_stdout=True):
  if use_stdout:
    print(capturedpiece)
    return 0
  with open('capture.out', 'w') as fhandle:
    fhandle.write(capturedpiece)
    return 0

if __name__ == '__main__':
  sys.exit(main_cli())
