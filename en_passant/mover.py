import asyncio
import logging
import logging.config

logger = logging.getLogger(__name__)

class Mover:
  """Primary class to make the moves.
  Returns en passantee and its move history.
  """
  def __init__(self):
    self.error = Flase
  
  @property
  def error_message(self):
    return ', '.join(self._error_messages)
  
  def move(self, square, piece, *args, **kwargs):
    # validations aboard
    # this is as far as I take you
    """
    En Passant in its natural habitat
    """
    return capturedpiece
      
    
