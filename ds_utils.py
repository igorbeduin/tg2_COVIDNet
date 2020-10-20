import os
import random
import shutil

import cv2
from pydicom import dcmread


def mount_dataset(dst_path, table):
    if not os.path.isdir(dst_path):
        os.mkdir(dst_path)
    for row in table:
        target_path = os.path.join(dst_path, str(row["class"]))
        if not os.path.isdir(target_path):
            os.mkdir(target_path)
        file_path = os.path.join(row["path"], row["filename"])
        if ".dcm" not in row["filename"]:
            try:
                shutil.copy2(file_path, target_path)
            except:
                filename = row["filename"]
                print(f"Fail trying to copy file {filename}")
        else:
            image = dcmread(file_path)
            pixel_array_numpy = image.pixel_array
            new_filename = row["filename"].replace(".dcm", ".png")
            try:
                # cv2.imshow("window", pixel_array_numpy)
                # cv2.waitKey()
                cv2.imwrite(os.path.join(target_path, new_filename), pixel_array_numpy)
            except:
                filename = row["filename"]
                print(f"Fail trying to write DCM file {filename}")

def filter_table(table, mapping, remove_classes=None, general_case="subst"):
    new_table = []
    new_table = table.copy()
    rows_to_remove = []
    for row in new_table:
        if str(row["class"]) in mapping:
            row["class"] = mapping[str(row["class"])]
        elif remove_classes is None:
            if general_case == "subst":
                row["class"] = mapping["std_subst"]
            elif general_case == "remove":
                rows_to_remove.append(row)
        else:
            if str(row["class"]) in remove_classes:
                rows_to_remove.append(row)
            else:
                row["class"] = mapping["std_subst"]
    for row in rows_to_remove:
        new_table.remove(row)
    return new_table

def mount_count_table(table):
    count_table = {}
    for row in table:
        if row["class"] not in count_table:
            count_table[row["class"]] = 1
        else:
            count_table[row["class"]] += 1
    return count_table

def split_table(table, split_ratio):
    new_table = []
    new_table = table.copy()
    random.shuffle(new_table)
    split_idx = int(split_ratio * len(new_table))
    train_table = new_table[split_idx:]
    test_table = new_table[:split_idx]
    return train_table, test_table

def table_info(table, count_table=None):
    if count_table is None:
        count_table = mount_count_table(table)
    print(f"Total de imagens: {len(table)}")
    print(f"Contagem de cada classe por dataset: {count_table}")

if __name__ == "__main__":
    pass
