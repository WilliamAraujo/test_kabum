import json


class ConfigHelper(object):
    def __init__(self, config_file):
        self.config_file = config_file

    def load_config(self):
        with open(self.config_file) as _configFile:
            try:
                return json.load(_configFile)

            except Exception as e:
                print('Config fail, exception: %s' % e)
                pass
