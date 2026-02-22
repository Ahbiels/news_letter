class SaveData():
    def __init__(self, data):
        self.data = data
        self.title = []

    def get_title(self):
        self.title = [
            title["title"] for title in self.data
        ]
        return self.title