import re


def read_file_content(file_path):
    """
    读取文件，获取内容
    :param file_path:
    :return:
    """
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except IOError as e:
        print(f"Error reading file '{file_path}': {str(e)}")
        return None


def restyle_from_style(content):
    content = content.replace("\\n", "\n").replace("\n}", ";\n}").replace("{", "{\n\t")
    pattern = "\\[[-0-9a-zA-Z]+\\]"
    return re.sub(pattern, "", content)


file_content = read_file_content("/data/home/zhaoyi/Documents/PycharmProjects/pythonProject/js2vue/style.txt")
print("<style scoped lang=\"scss\">" + restyle_from_style(file_content) + "\n</style>")
