from pyngrok import ngrok
import logging
import socket
# Setup a logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)

# Then call the pyngrok method throwing the error, for example
tunnel = ngrok.connect(7867, "tcp").public_url

print("ip: ", socket.gethostbyname(tunnel.strip("tcp://").split(":")[0]))