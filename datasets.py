import pandas as pd
import os
import logging
from abc import ABC, abstractmethod
import time

from ds_utils import mount_count_table

class Datasets(ABC):
    def __init__(self, root_path=None):
        super().__init__()
        if root_path is None:
            self.dataset_root_path = "./datasets"
        else:
            self.dataset_root_path = root_path
        self.count = 0
        self.csv_path = None
        self.encoding = None
        self.prefilter_methods = []
        self.postfilter_methods = []
        self.table = []
        self.count_table = {}
        self.classes_count = 0

        logging.basicConfig(filename='example.log', level=logging.INFO)
    
    def read(self):
        try:
            self.csv = pd.read_csv(os.path.join(self.dataset_root_path, self.csv_path), 
                       encoding=self.encoding, nrows=None)
            self.update_count()
        except ValueError:
            logging.error("Path to the CSV file not defined")
            exit()
    
    def prefilter(self):
        for filter_method in self.prefilter_methods:
            filter_method()
        self.update_count()

    def postfilter(self):
        for filter_method in self.postfilter_methods:
            filter_method()
        self.update_count()

    def update_count(self):
        if self.table:
            self.count = len(self.table)
        else:
            self.count = len(self.csv)

    def mount_table(self):
        table = []
        for idx in self.csv.index:
            filename = self.find_filename(idx)
            finding = self.find_image_class(idx)
            target_path = self.solve_target_path(idx)
            url = self.find_img_url(idx)
            patientid = self.find_id(idx)
            table_row = {"path": target_path, "filename": filename, "class": finding, "url": url, "id": patientid}
            table.append(table_row)
        self.table = table

    def find_filename(self, idx):
        filename = ""
        return filename

    def find_image_class(self, idx):
        finding = ""
        return finding

    def find_id(self, idx):
        patientid = self.csv["patientid"][idx]
        return patientid

    def solve_target_path(self, idx):
        target_path = ""
        return target_path

    def mount_count_table(self):
        self.count_table = mount_count_table(self.table)
        self.classes_count = len(self.count_table)

    def find_img_url(self, idx):
        if "url" in self.csv:
            url_column = self.csv["url"]
        if "URL" in self.csv:
            url_column = self.csv["URL"]
        try:
            url = url_column[idx]
        except:
            url = None
        return url

    def update(self):
        self.mount_count_table()
        self.update_count()
            
        

class cohen (Datasets):
    def __init__(self, root_path):
        super().__init__(root_path)
        self.__name__ = "cohen"

        self.dataset_path = "covid-chestxray-dataset"
        self.csv_path = os.path.join(self.dataset_path, "metadata.csv")
        self.img_path = os.path.join(self.dataset_path, "images")
        
        self.prefilter_methods = [self.select_views]

    def select_views(self, views=None):
        if views is None:
            views = ["PA", "AP", "AP Supine", "AP semi erect", "AP erect"]
        ioi = self.csv.view.isin(views) #index of interest
        self.csv = self.csv[ioi]

    def find_filename(self, idx):
        filename = self.csv["filename"][idx]
        return filename
    
    def find_image_class(self, idx):
        finding = self.csv["finding"][idx]
        return finding

    def solve_target_path(self, idx):
        subpath = self.csv["folder"][idx]
        target_path = os.path.join(self.dataset_root_path, self.dataset_path, subpath)
        return target_path

class actualmed (Datasets):
    def __init__(self, root_path):
        super().__init__(root_path)
        self.__name__ = "actualmed"

        self.dataset_path = "Actualmed-COVID-chestxray-dataset"
        self.csv_path = os.path.join(self.dataset_path, "metadata.csv")
        self.img_path = os.path.join(self.dataset_path, "images")

    def find_filename(self, idx):
        filename = self.csv["imagename"][idx]
        return filename

    def find_image_class(self, idx):
        finding = self.csv["finding"][idx]
        return finding

    def solve_target_path(self, idx):
        target_path = os.path.join(self.dataset_root_path, self.img_path)
        return target_path

class fig1 (Datasets):
    def __init__(self, root_path):
        super().__init__(root_path)
        self.__name__ = "fig1"
        
        self.encoding = 'ISO-8859-1'
        self.dataset_path = "Figure1-COVID-chestxray-dataset"
        self.csv_path = os.path.join(self.dataset_path, "metadata.csv")
        self.img_path = os.path.join(self.dataset_path, "images")

    def find_filename(self, idx):
        filename_no_ext = self.csv["patientid"][idx]
        fileslist = os.listdir(os.path.join(self.dataset_root_path ,self.img_path))
        for f in fileslist:
            if filename_no_ext in f:
                return f

    def find_image_class(self, idx):
        finding = self.csv["finding"][idx]
        return finding

    def solve_target_path(self, idx):
        target_path = os.path.join(self.dataset_root_path, self.img_path)
        return target_path




class rsna (Datasets):
    def __init__(self, root_path):
        super().__init__(root_path)
        self.__name__ = "rsna"

        self.dataset_path = "rsna-pneumonia-detection-challenge"
        self.csv_path = [os.path.join(self.dataset_path, "stage_2_detailed_class_info.csv"),
                         os.path.join(self.dataset_path, "stage_2_train_labels.csv")]
        self.img_path = os.path.join(self.dataset_path, "stage_2_train_images")

        self.prefilter_methods = [self.remove_unknown]

    def read(self):
        csv_list = []
        for csv_path in self.csv_path:
            df = pd.read_csv(os.path.join(self.dataset_root_path, csv_path),
                             encoding=self.encoding, nrows=None)

            csv_list.append(df)
        self.csv = pd.concat(csv_list, axis=1)
        duplic_columns_idx = self.csv.columns.duplicated()
        non_duplic_columns_idx = [not item for item in duplic_columns_idx]
        self.csv = self.csv.loc[:,non_duplic_columns_idx]
        self.count = len(self.csv)

    def find_filename(self, idx):
        filename_no_ext = self.csv["patientId"][idx]
        fileslist = os.listdir(os.path.join(self.dataset_root_path, self.img_path))
        for f in fileslist:
            if filename_no_ext in f:
                return f

    def find_image_class(self, idx):
        finding = self.csv["class"][idx]
        target = self.csv["Target"][idx]
        if finding == "Normal":
            return finding
        elif target == "1":
            return target

    def solve_target_path(self, idx):
        target_path = os.path.join(self.dataset_root_path, self.img_path)
        return target_path

    def remove_unknown(self):
        aux1_csv = self.csv[self.csv["class"] == "Normal"]
        aux2_csv = self.csv[self.csv["Target"] == 1]
        self.csv = pd.concat([aux1_csv, aux2_csv], ignore_index=True)

    def find_id(self, idx):
        patientid = self.csv["patientId"][idx]
        return patientid
        

class sirm (Datasets):
    def __init__(self, root_path):
        super().__init__(root_path)
        self.__name__ = "sirm"

        self.dataset_path = "COVID-19 Radiography Database"
        self.csv_path = [os.path.join(self.dataset_path, "COVID-19.metadata.xlsx")]
        self.img_path = [os.path.join(self.dataset_path, "COVID-19")]
        self.available_classes = ["COVID-19"]
        self.postfilter_methods = [self.discard_targets]

    def read(self):
        csv_list = []
        for csv_path in self.csv_path:
            df = pd.read_excel(os.path.join(self.dataset_root_path, csv_path))
            csv_list.append(df)
        self.csv = pd.concat(csv_list, ignore_index=True)
        self.count = len(self.csv)

    def find_filename(self, idx):
        filename_tag = self.csv["FILE NAME"][idx]
        if "COVID-19" in filename_tag:
            fileslist = os.listdir(os.path.join(self.dataset_root_path, self.img_path[0]))
        for f in fileslist:
            if filename_tag in f.replace(' ', ''): #remove espaco do nome do arquivo
                return f

    def find_image_class(self, idx):
        filename_tag = self.csv["FILE NAME"][idx]
        for finding in self.available_classes:
            if finding in filename_tag:
                return finding

    def solve_target_path(self, idx):
        filename_tag = self.csv["FILE NAME"][idx]
        for finding in self.available_classes:
            if finding in filename_tag:
    def discard_targets(self):
        rows_to_remove = []
        discard = ['100', '101', '102', '103', '104', '105',
                   '110', '111', '112', '113', '122', '123',
                   '124', '125', '126', '217']
        for row in self.table:
            for n in discard:
                if n in row["filename"]:
                    rows_to_remove.append(row)
        for row in rows_to_remove:
            self.table.remove(row)

    def find_id(self, idx):
        patientid = self.csv["FILE NAME"][idx]
        return patientid
    
if __name__ == "__main__":
    path = os.path.join(os.getcwd(), "datasets")
    sirm = sirm(path)
    
    sirm.read()
    sirm.mount_table()

    for item in sirm.table: print(item["filename"])
