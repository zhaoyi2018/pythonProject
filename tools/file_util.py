import os


def exist_file(file_path, file_type):
    """
    判断是否存在某个文件
    :param file_path: 文件路径
    :param file_type: 文件类型(文件夹, 文件)
    :return:
    """
    if not os.path.exists(file_path):
        return False
    if file_type == "dir" and os.path.isdir(file_path):
        return True
    elif file_type == "file" and os.path.isfile(file_path):
        return True
    return False
