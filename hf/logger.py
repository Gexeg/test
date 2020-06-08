from sys import stdout
from logging import DEBUG, FileHandler, Formatter, StreamHandler, getLogger


DEFAULT_LOG_FORMAT = "%(asctime)-23s | %(name)-23s | %(levelname)-8s | %(message)s"
fp = "/tmp/hf_api.log"

LOG = getLogger("hf_api")
LOG.setLevel(DEBUG)

formatter = Formatter("%(asctime)-23s | %(name)-23s | %(levelname)-8s | %(message)s")

stream_handler = StreamHandler(stream=stdout)
stream_handler.setFormatter(formatter)
stream_handler.setLevel(DEBUG)
LOG.addHandler(stream_handler)

file_handler = FileHandler(fp)
file_handler.setFormatter(formatter)
file_handler.setLevel(DEBUG)
LOG.addHandler(file_handler)
