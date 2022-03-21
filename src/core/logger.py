from datetime import datetime
import pytz

class Loginator:
	def __init__(self, debug: bool = False, timezone: str = "Europe/London"):
		"""Used for logging actions"""
		self.debug = debug
		utc_now = pytz.utc.localize(datetime.utcnow())
		self.timezone = utc_now.astimezone(pytz.timezone(timezone))
		self.format = None
		self.set_format(format="{TIME} | [{LEVEL}] - {MESSAGE}")

	def set_format(self, format: str):
		"""Sets the format for logging. Available default variables are {TIME}, {LEVEL}, {MESSAGE}. Other variables can be added but must be passed as exact kwargs to the log function you are using (i.e. display_message, log, error or info)"""
		self.format = format

	def _get_time(self, time_format: str = "%H:%M:%S @ %d/%m/%Y"):
		return self.timezone.strftime(time_format)
	
	def display_message(self, level: str, message: str, **kwargs):
		"""Display a message using  the global format"""
		print(self.format.format(TIME=self._get_time(), LEVEL=level, MESSAGE=message, **kwargs))

	def log(self, message: str, **kwargs):
		self.display_message(level="LOG", message=message, **kwargs)

	def error(self, message: str, **kwargs):
		self.display_message(level="ERROR", message=message, **kwargs)

	def info(self, message: str, **kwargs):
		self.display_message(level="INFO", message=message, **kwargs)