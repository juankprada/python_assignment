import logging


logging.basicConfig(format="[%(levelname)s]-%(asctime)s\t %(message)s ", datefmt="%d-%b-%y %H:%M:%S", level=logging.DEBUG)
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
