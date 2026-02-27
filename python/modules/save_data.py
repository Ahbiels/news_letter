class SaveData():
    def __init__(self, data):
        self.data = data
        self.title = self.get_title()

    def get_title(self):
        self.title = [
            title["title"] for title in self.data
        ]
        self.data
        return self.title