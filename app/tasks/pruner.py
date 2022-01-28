from datetime import date

class Pruner:
    def __init__(self):
      self.now = date()

    def prune(self):
      pass

    # delete releases older than x
    # delete entities and releases older than 1 day without interests