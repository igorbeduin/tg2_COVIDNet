import os
import shutil
import random

def mount_dataset(dst_path, table):
    if not os.path.isdir(dst_path):
        os.mkdir(dst_path)
    for row in table:
        target_path = os.path.join(dst_path, str(row["class"]))
        if not os.path.isdir(target_path):
            os.mkdir(target_path)
        file_path = os.path.join(row["path"], row["filename"])
        try:
            shutil.copy2(file_path, target_path)
        except:
            filename = row["filename"]
            print(f"Fail trying to copy file {filename}")

def filter_table(table, target_classes, remove_classes, mapping):
    rows_to_be_rmvd = []

    for row in table:
        if str(row["class"]) in remove_classes:
            rows_to_be_rmvd.append(row)
        elif str(row["class"]) not in target_classes:
            if str(row["class"]) in mapping:
                row["class"] = mapping[row["class"]]
            else:
                row["class"] = mapping["std"]     
    for row in rows_to_be_rmvd:
        table.remove(row)
    for row in table:
        if row["class"] not in count_table:
            count_table[row["class"]] = 1
        else:
            count_table[row["class"]] += 1
def split_table(table, split_ratio):
    random.shuffle(table)
    split_idx = int(split_ratio * len(table))
    train_table = table[split_idx:]
    test_table = table[:split_idx]
    return train_table, test_table

    return table, count_table

if __name__ == "__main__":
    pass
