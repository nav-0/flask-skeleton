import os
from distutils.util import strtobool

passant_host_bind = os.environ.get('PASSANT_HOST_BIND', '0.0.0.0')
passant_port_bind = int(os.environ.get('PASSANT_PORT_BIND', 8080))
passant_flask_debug = bool(strtobool(str(os.environ.get('PASSANT_FLASK_DEBUG', False))))

# other things you want me to have
