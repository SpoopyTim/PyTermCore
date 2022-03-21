import json
import os
from src.core.storage.base import Storinator

class JsonStorinator(Storinator):
	def __init__(self):
		"""Represents a JSON storage backend"""
		super().__init__(backend = "json")
		self.__pending = self._Storinator__pending

	@property
	def save(self):
		"""Saves all currently pending (open) datasources"""
		for item in self.__pending:
			i = self.__pending[item]
			if i["type"] == "json":
				fs = i["fs"]
				json.dump(i["data"], fs)
				fs.close()

	def get_data(self, filename: str):
		"""Gets data from a currently pending (open) datasource"""
		if self.__pending.get(filename, None) is None:
			raise AttributeError(f"File: {filename} has not been opened")
			return False
		
		return self.__pending[filename]["data"]

	def set_data(self, filename: str, data):
		"""Overwrites the datasource's data"""
		if self.__pending.get(filename, None) is None:
			raise AttributeError(f"File: {filename} has not been opened")
			return False		
		self.__pending[filename]["data"] = data
		
		return True
	
	def _open_datasource(self, path: str, readonly: bool = False):
		path = os.path.abspath(path)
		fs = open(path, f"{'r' if readonly is True else 'w'}")
		self.__pending.update({
			os.path.basename(path).split(".")[0]: {
				'type': os.path.basename(path).split(".")[1],
				'fs': fs,
				'readonly': readonly
			}
		})

		return True

	def _close_datasource(self, filename: str, save: bool = True):
		if save:
			if self.__pending.get(filename, None) is None:
				raise AttributeError(f"File: {filename} has not been opened")
				return False
			i = self.__pending[filename.split(".")[0]]
			if self.__pending[filename]["readonly"]:
				fs = i["fs"]
				fs.close()
				return True
			fs = i["fs"]
			json.dump(i["data"], fs)
			fs.close()
			return True
		else:
			if self.__pending.get(filename, None) is None:
				raise AttributeError(f"File: {filename} has not been opened")
				return False
			i = self.__pending[filename.split(".")[0]]
			fs = i["fs"]
			fs.close()
			return True