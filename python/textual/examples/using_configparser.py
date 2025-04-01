```py
import configparser
from pathlib import Path

class MyTextualApp(App)
    
    def __init__(self):
        super().__init__()

        config_path = Path(__file__).resolve().parent / "config.ini"
        if not config_path.exists():
            raise FileNotFoundError("config.ini file not found.")

        self.config = configparser.ConfigParser()  # Available globally as self.app.config
        self.config.read(config_path)

        ##~ Config settings ~##
        self.my_string_foo  = self.config.get("MAIN", "my_string_foo")
        self.my_boolean_foo = self.config.getboolean("MAIN", "my_boolean_foo")
        self.my_integer_foo = self.config.getint("MAIN", "my_integer_foo")
        self.my_float_foo   = self.config.getfloat("MAIN", "my_float_foo")
```
