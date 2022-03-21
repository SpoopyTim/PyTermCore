# PyTermCore
A bunch of useful modules for working with python

# Storinator
**Location: /src/core/storage/base.py**

**This module requires extensions**

## Usage
```py
# Import JsonStorinator to work on JSON Files
from src.core import JsonStorinator

# Initialize
storage = JsonStorinator()

# Open data.json for editing
storage.open("data.json")

# Output pending files and data about them
print(f"Pending Files: {storage.pending}")

# Set data inside of data.json (file extension is optional at this point)
storage.set_data("data", {"Hello": 1})

# Get data from data.json (file extension is optional at this point)
print(f"Data from file 'data.json': {storage.get_data('data')}")

# Save and close all pending files
storage.close_all(save=True)
```

## How to make Storinator Extensions
### Requirements:
  - Inherit Base Class: `Storinator`
  - Initialize using:
```py
def __init__(self):
    """Represents a <STORAGE_NAME> storage backend"""
    super().__init__(backend = "<STORAGE_NAME>")
    self.__pending = self._Storinator__pending
  ```
  - Have a `save` property
  - Have a `get_data` method
  - Have a `set_data` method
  - Have an `_open_datasource` method
  - Have a `_close_datasource` method

### Example Extension ([source](https://github.com/spoopytim/PyTermCore/blob/master/src/core/storage/extensions/json.py))
```py
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
        """Opens a new datasource"""
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
        """Closes the datasource"""
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
```
