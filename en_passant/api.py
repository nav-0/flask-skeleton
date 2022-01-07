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
            piece:
              type: array
              items:
                type: string
              description: Array of column, number.
    responses:
      201:
        description: An en passant capture. 
        schema: 
          id: en-capture
          properties:
            capturedpiece:
              type: object
              description: Captured piece with its move history.
    """
    return self.get(None)
  
  def get(self, square=None, piece=None):
    """Given a piece and a destination square, make an en passant capture and return captured piece. 
    ---
    produces:
      - application/json
    tags:
      - move
    parameters:
      - in: query
        name: square
        type: array
        items: 
          type: string
        required: true
        description: The destination square.
      - in: query
        name: piece
        type: array
        items: 
          type: string
        required: true
        description: En passanter (passantor?).
    responses:
      201:
        description: Capture piece en passant. 
        schema:
          id: en-capture
          properties:
            capturedpiece:
              type: object
              description: Captured peice with its move history.
    """
    req_body = request.get_json(force=True, silent=True)
    if not req_body:
      req_body = {}
    req_values = request.values
    square = req_body.get('square', req_values.get('square', square))
    piece = req_body.get('piece', req_values.get('piece', piece))
    # validations galore
    mover = Mover()
    try:
      capture = mover.move(square, piece)
    except BaseException as exc:
      logger.error('Mover had an issue.')
      return resp_error('Something went wrong %s' % str(exc))
    if not capture:
      return resp_error("Nothing captured.")
    return resp_success(capture)
  
  def run_passant_service(host=None, port=None):
    if not host:
      host = config.passant_host_bind
    if not port:
      port = config.passant_port_bind
    logger.info('Starting en passant service at $%s:%s', host, port)
    app = Flask(__name__)
    app.debug = config.passant_flask_debug
    if app.debug:
      logger.info('Server in debug mode.')
    api_version = '1.0'
    dispatch_path = '/en/api/v%s/passant/' % api_version
    dispatcher = PathInfoDispatcher({dispatch_path: app})
    server = wsgiserver((host, port), dispatcher)
    api = Api(app)
    app.config['SWAGGER'] = {
      'title': 'En Passant API',
      'basePath': dispatch_path,
      'version': api_version,
    }
    app.config['JSON_SORT_KEYS'] = False # retain resp key order
    swagger = Swagger(app)
    logger.info('Swagger available at %s' % '/'.join([x.rstrip('/') for x in [dispatch_path, 'apidocs']]))
    api.add_resource(
      MoveApi, 
      '/move',
      methods=['POST'],
      endpoint='moves')
    api.add_resource(
      MoveApi,
      '/move', # if params weren't arrays and say, strings, this would be /move/<param>
      methods=['GET'],
      endpoint='move')
    api.init_app(app)
    try:
      server.start()
    except KeyboardInterrupt:
      logger.info('Shutting down...')
      server.stop()
    # last opportunity to exit cleanly
    logger.info('Goodbye.')
    return 0
