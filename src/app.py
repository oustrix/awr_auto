from .awrde import Awrde
from .cst_studio import CST


class App:
    def __init__(self):
        self.awrde: Awrde = Awrde()
        # self.cst: CST = CST()

    def run(self):
        self.awrde.start_processing()
        # self.cst.start_processing()
