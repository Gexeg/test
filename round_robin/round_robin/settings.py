import json

class Settings:
    def __init__(self):
        self.settings = {}
        self.__set_start_settings()

    def __set_start_settings(self):
        with open('start_settings.json') as settings_file:
            data = json.load(settings_file)
            self.settings = data

    def get_available_settings(self):
        return self.settings.keys()
