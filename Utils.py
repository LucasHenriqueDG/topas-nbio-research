import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

def get_header(path: str) -> list:
    columns = []

    with open(path) as file:
        index = 0
        lines = file.readlines()

        for line in range(len(lines)):
            if lines[line].__contains__("as follow"):
                index = line + 1
                break
        for column in range(index, len(lines) - 1):
            content = lines[column].split(":")[-1].strip()
            if content != "":
                columns.append(content)
        return columns

def get_phsp(path: str, header: list) -> pd.DataFrame:
    return pd.read_csv(path, names=header, sep=r"\s+")

def get_dataframe(filename: str, dirpath: str) -> pd.DataFrame:
    """
        Return the dataframe for the analysis
        :param filename: name of the file (without extension)
        :param dirpath: path to the directory where the file is located
        :return:
    """

    header = get_header(f"{dirpath}/{filename}.header")
    return get_phsp(f"{dirpath}/{filename}.phsp", header)

def create_seed_dir(folder_name: str, tgt_dir: str = "outputs/topas") -> int:

    """
    Method used to create the directory for the new simulation
    :param tgt_dir: Partial path to the folder (final path will be tgt_dir/folder_name)
    :param folder_name: Name of the folder
    :return:
    """

    os.makedirs(tgt_dir+"/"+folder_name, exist_ok=True)
    files = os.listdir(folder_name)

    index = len(files) + 1
    if index == 0:
        new_dir = f"{folder_name}/seed1"
    else:
        new_dir = f"{folder_name}/seed{index}"

    os.makedirs(new_dir, exist_ok=True)
    return index

def move_files(folder_name, src_dir: str, filter_list: list[str], tgt_dir: str = "topas/outputs"):

    """
    Method used to move the files generated at the end of the simulation
    :param folder_name: Name of the folder created
    :param src_dir: path to the directory where the files are located.
    :param filter_list: Files that are not going to be moved during the process (place the name of the input file here, alongside with the
    supportFiles folder).
    :param tgt_dir: Partial path name where the files are going to be moved (final path will be tgt_dir/folder_name)
    :return:
    """

    index = create_seed_dir(f"{tgt_dir}/{folder_name}")

    check_list = os.listdir(src_dir)
    for file in check_list:
        if not file in filter_list:
            os.rename(f"{src_dir}/{file}", f"{tgt_dir}/{folder_name}/seed{index}/{file}")
