class Storinator:
	__pending = {}
	def __init__(self, backend: str = None):
		"""Represents the storage extension backend"""
		self._backend = backend
		self.__pending = {}
		self.extension_error = AttributeError("Tried to use the base storinator class which has no methods for using datasources. Please use an extension class.")

	def _get_pending(self):
		return self.pending

	def _clear_pending(self, save: bool = True):
		if save:
			for item in self.__pending:
				self._close_datasource(item, save)
			self.__pending = {}
			return True
		else:
			self.__pending = {}
			return True			

	def _open_datasource(self, item, save):
		"""Placeholder internal method for opening a datasource"""
		raise self.extension_error

	def _close_datasource(self, item, save):
		"""Placeholder internal method for closing a datasource"""
		raise self.extension_error
	
	@property
	def pending(self):
		"""Returns the currently pending (open) datasources"""
		r = {}
		for item in self.__pending:
			r.update({
				item+"."+self.__pending[item]["type"]: {
					"type": self.__pending[item]["type"],
					"readonly": self.__pending[item]["readonly"],
					"uses_filewrapper": True if self.__pending[item]["fs"] is not None else False
				}
			})
		return r
	
	@property
	def save(self):
		"""Placeholder internal property for saving a datasource"""
		raise self.extension_error

	@property
	def backend(self):
		return self._backend

	def open(self, path: str,  readonly: bool = False):
		"""Open a new datasource"""
		self._open_datasource(path, readonly)
		return True
	
	def close(self, filename: str, save: bool = True):
		"""Closes a datasource"""
		self._close_datasource(filename, save)
	
	def close_all(self, save: bool = True):
		"""Close all currently pending (open) datasources"""
		self._clear_pending(save)

	def get_data(self, item):
		raise AttributeError(self.extension_error)

	def set_data(self, item, data):
		raise AttributeError(self.extension_error)

