import pandas as pd
import os
import logging
from abc import ABC, abstractmethod
import time

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
        self.filter_methods = []
        self.table = []
        self.count_table = {}
        self.classes_count = 0

        logging.basicConfig(filename='example.log', level=logging.INFO)
    
    def read(self):
        try:
            self.csv = pd.read_csv(os.path.join(self.dataset_root_path, self.csv_path), 
                       encoding=self.encoding, nrows=None)
            self.count = len(self.csv)
        except ValueError:
            logging.error("Path to the CSV file not defined")
            exit()
    
    def filter(self):
        for filter_method in self.filter_methods:
            filter_method()

    def mount_table(self):
        table = []
        for idx in self.csv.index:
            filename = self.find_filename(idx)
            finding = self.find_image_class(idx)
            target_path = self.solve_target_path(idx)
            table_row = {"path": target_path, "filename": filename, "class": finding}
            table.append(table_row)
        self.table = table
        self.mount_count_table()
        self.classes_count = len(self.count_table)

    def find_filename(self, idx):
        filename = ""
        return filename

    def find_image_class(self, idx):
        finding = ""
        return finding

    def solve_target_path(self, idx):
        target_path = ""
        return target_path

    def mount_count_table(self):
        for row in self.table:
            if row["class"] not in self.count_table:
                self.count_table[row["class"]] = 1
            else:
                self.count_table[row["class"]] += 1

class cohen (Datasets):
    #TODO:
    # - mapping das classes

    def __init__(self, root_path):
        super().__init__(root_path)
        self.dataset_path = "covid-chestxray-dataset"
        self.csv_path = os.path.join(self.dataset_path, "metadata.csv")
        self.img_path = os.path.join(self.dataset_path, "images")
        
        self.filter_methods = [self.select_views]

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
    # TODO:
    # - mapping das classes

    def __init__(self, root_path):
        super().__init__(root_path)
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
    # TODO:
    # - mapping das classes

    def __init__(self, root_path):
        super().__init__(root_path)
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
    # TODO:
    # - mapping das classes

    def __init__(self, root_path):
        super().__init__(root_path)
        self.dataset_path = "rsna-pneumonia-detection-challenge"
        self.csv_path = [os.path.join(self.dataset_path, "stage_2_detailed_class_info.csv"),
                         os.path.join(self.dataset_path, "stage_2_train_labels.csv")]
        self.img_path = os.path.join(self.dataset_path, "stage_2_train_images")

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
        

class sirm (Datasets):
    # TODO:
    # - mapping das classes

    def __init__(self, root_path):
        super().__init__(root_path)
        self.dataset_path = "COVID-19 Radiography Database"
        self.csv_path = [os.path.join(self.dataset_path, "COVID-19.metadata.xlsx"),
                         os.path.join(self.dataset_path, "NORMAL.metadata.xlsx"),
                         os.path.join(self.dataset_path, "Viral Pneumonia.matadata.xlsx")]
        self.img_path = [os.path.join(self.dataset_path, "COVID-19"),
                         os.path.join(self.dataset_path, "NORMAL"),
                         os.path.join(self.dataset_path, "Viral Pneumonia")]
        self.available_classes = ["COVID-19", "NORMAL", "Viral Pneumonia"]

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
        elif "NORMAL" in filename_tag:
            fileslist = os.listdir(os.path.join(self.dataset_root_path, self.img_path[1]))
        elif "Viral Pneumonia" in filename_tag:
            fileslist = os.listdir(os.path.join(self.dataset_root_path, self.img_path[2]))
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
                idx = self.available_classes.index(finding)
                return os.path.join(self.dataset_root_path, self.img_path[idx])
    
if __name__ == "__main__":
    path = os.path.join(os.getcwd(), "datasets")
    sirm = sirm(path)
    
    sirm.read()
    sirm.mount_table()

    for item in sirm.table: print(item["filename"])

    # for item in cohen.count_table: print(f"{item}: {cohen.count_table[item]}")
    # print(len(cohen.count_table))
