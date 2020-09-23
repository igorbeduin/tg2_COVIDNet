import pandas as pd
import logging
from abc import ABC, abstractmethod

class Datasets(ABC):
    def __init__(self):
        super().__init__()
        self.count = 0
        self.set_views()
        self.set_csv_path()
        logging.basicConfig(filename='example.log', level=logging.INFO)
    
    def read(self):
        try:
            self.csv = pd.read_csv(self.csv_path, nrows=None)
        except ValueError:
            logging.error("Path to the CSV file not defined")
            exit()
        if self.views:
            """ If a list of desired views is defined, makes restrict csv only to the csv views columns."""
            self.csv = self.csv[filter_views()]

    def filter_views(self):
        """ Returns the list of views in the csv file."""
        views_idx = self.views
        return self.csv.view.isin(self.views)

    # pure abstract methods
    def set_csv_path(self):
        """ This method should be replicated in every subclass of Dataset"""
        logging.warning("Running class with no path to csv file defined!")

    def set_views(self):
        """ This method should bet replicated in every class that has restricted views of radiography."""
        logging.info(f"Running class with no view restriction: CLASS = {self.__class__}")

class cohen (Datasets):
    def __init__(self):
        super().__init__()
        self.views = ["PA", "AP", "AP Supine", "AP semi erect", "AP erect"]

class actualmed (Datasets):
    def __init__(self):
        super().__init__()

class rsna (Datasets):
    def __init__(self):
        super().__init__()

class fig1 (Datasets):
    def __init__(self):
        super().__init__()

class sirm (Datasets):
    def __init__(self):
        super().__init__()

    
if __name__ == "__main__":
    cohen = cohen()
