import os

file_list1 = set(os.listdir("./data/tmp1"))
file_list2 = set(os.listdir("./data/tmp2"))

need_files = file_list1 - file_list2

pass

