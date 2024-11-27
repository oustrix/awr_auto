from .awrde import Awrde


class App:
    def __init__(self):
        self.awrde: Awrde = Awrde()

    def run(self):
        self.awrde.start_processing()