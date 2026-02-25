import os 

class Log:
    def __init__(self):
        self._info = []

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @property
    def info(self):
        self.clear_terminal()
        info_pipeline = " >> ".join(self._info)
        print("="*len(info_pipeline))
        print(info_pipeline)
        print("="*len(info_pipeline))

        
    @info.setter
    def info(self, info):
        self._info.append(info)
        self.info


