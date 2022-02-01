import logging
from logging.handlers import RotatingFileHandler

class Logs:
	def __init__(self, active, max_bytes=10*1024*1024) -> None:
		self.active = active
		self.logfile_name = "logs.txt"
		self.file_max_size = max_bytes
		RFhandler = RotatingFileHandler(
			filename=self.logfile_name,
			mode="a",
			maxBytes=self.file_max_size,
			backupCount=3)

		logging.basicConfig(
			level=logging.DEBUG,
			format="%(asctime)s:%(name)s:%(levelname)s:%(message)s",
			datefmt="%Y-%m-%dT%H:%M:%S",
			handlers=[RFhandler]
		)
		pass

	def debug(self, msg):
		if self.active:
			logging.debug(msg)
	
	def setLevel(self, logger_name, level):
		logger = logging.getLogger(logger_name)
		if level == "WARNING":
			logger.setLevel(logging.WARNING)