"""Combined wsgi, app module to hold API handlers."""
import logging
import logging.config
import traceback
import datetime
from distutils.utils import strtobool
try:
  from cheroot.wsgi import (
    Server as wsgiserver,
    PathInfoDispatcher)
 except ImportError:
  from cherrypy.wsgiserver import (
    CherryPyWSGIServer as wsgiserver,
    WSGIPathInfoDispatcher as PathInfoDispatcher)
import flask
from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api
from flasgger import Swagger
from flask_pymongo import pymongo
from pymongo import MongoClient

from en_passant import config
from en_passant.mover import Mover

logger = logging.getLogger(__name__)
logformat = '%(asctime)s: %(levelname)s: %(name)s: %(lineno)s - %(message)s'
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
console_fmt = logging.Formatter(logformat)
ch.setFormatter(console_fmt)
logger.addHandler(ch)

def resp_error(msg, status_code=501):
  resp = jsonify({'error':True, 'error_message':f'api internal error: {msg}'})
  resp.status_code = status_code
  return resp

def resp_missing(msg):
  resp = jsonify({'error':True, 'error_message':f'api client error: {msg}'})
  resp.status_code = 404
  return resp

def resp_success(capturedpiece):
  logger.debug(f'Captured: {capturedpiece}')
  resp = jsonify(capturedpiece)
  resp.status_code = 201
  return resp

class MoveApi(Resource):
  """Given a piece and square, return an en-passantee."""
  def post(self):
    """Given piece and square, perform move action, return captured piece.
    ---
    consumes:
      - application/json
    produces:
      - application/json
    tags:
      - move
    parameters:
      - in: body
        name: make-move
        description: The piece and square for the move.
        schema: 
          type: object
          required:
            - square
            - piece
          properties:
            square:
              type: array
              items:
                type: string
              description: Array of column, number. 
              
    
