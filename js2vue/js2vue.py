import json
import re
import pprint


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


def match_content_to_index(content, start_index):
    """
    获取文本, 从start_index开始匹配
    :param content:
    :param start_index:
    :return:
    """
    if len(content) <= start_index:
        return -1
    char_queue = []
    char_dict = {
        "{": "}",
        "[": "]",
        "(": ")",
        "\'": "\'",
        "\"": "\""
    }
    char_queue.append(char_dict.get(content[start_index]))
    char_num = 1
    for i in range(start_index + 1, len(content)):
        if content[i] in ["{", "(", "["]:
            char_queue.append(char_dict.get(content[i]))
            char_num += 1
        if content[i] in ["}", ")", "]"] and char_queue[-1] == content[i]:
            char_queue.pop()
            char_num -= 1
        if content[i] == "\'":
            if char_queue[-1] == "\'":
                char_queue.pop()
                char_num -= 1
            else:
                char_queue.append(char_dict.get(content[i]))
                char_num += 1
        if content[i] == "\"":
            if char_queue[-1] == "\"":
                char_queue.pop()
                char_num -= 1
            else:
                char_queue.append(char_dict.get(content[i]))
                char_num += 1
        if char_num == 0:
            return i
    return -1


def split_elements_from_content(content):
    res = []
    # 先去除外壳
    content = content[1:-1]
    # 寻找第一个切分点
    while content.find("(") > 0:
        start_index = content.find("(")
        end_index = match_content_to_index(content, start_index)
        if content[start_index - 1] == 'c':
            res.append(content[start_index - 2:end_index + 1])
        else:
            res.append(content[start_index - 6:end_index + 1])
        content = content[end_index + 1:]
    return res


def split_inner_from_content(content):
    """
    拆分元素
    :param content:
    :return:
    """
    res = {}
    # 刨取外壳
    index = content.find("(")
    res["element_type"] = content[:index]
    content = content[index + 1:-1]
    if res["element_type"] == "_vm._v":
        res["element_value"] = content
        return res
    # 寻找元素类型
    index = content.find("'")
    if 0 <= index < 2:
        end_index = match_content_to_index(content, index)
        res["element_tag"] = content[index + 1:end_index]
        if end_index + 2 > len(content):
            return res
        else:
            content = content[end_index + 2:]
    # 寻找元素属性
    index = content.find("{")
    if 0 <= index < 2:
        end_index = match_content_to_index(content, index)
        res["element_attr"] = content[index:end_index + 1]
        if end_index + 2 > len(content):
            return res
        else:
            content = content[end_index + 2:]
    # 寻找子元素元素
    index = content.find("[")
    if 0 <= index < 2:
        end_index = match_content_to_index(content, index)
        res["element_inner_element"] = []
        for element in split_elements_from_content(content[index:end_index + 1]):
            res["element_inner_element"].append(split_inner_from_content(element))
        # res["element_inner_element"] = content[index:end_index+1]
        if end_index + 2 > len(content):
            return res
        else:
            content = content[end_index + 2:]
    # 寻找元素个数
    if len(content) == 1:
        res["element_nums"] = int(content)
    return res


def get_attr_dict(attr_str):
    if attr_str is None or attr_str.strip() == "":
        return ""
    attr_dict = {}
    attr_str = attr_str[1:-1]
    # 获取:下标
    while attr_str.find(":") > 0:
        colon_index = attr_str.find(":")
        # 先判断有无单引号或多引号
        if attr_str[0] in ["'", '"']:
            end_index = match_content_to_index(attr_str, 0)
            attr_key = attr_str[1:end_index+1].strip(" \"\'")
            attr_str = attr_str[end_index+2:].strip(" ,:")
        else:
            attr_key = attr_str[:colon_index].strip(" \"\'")
            attr_str = attr_str[colon_index + 1:].strip(" ,:")
        attr_value_start_index = 0
        # 如果“:”后，非单引号或双引号
        if attr_str[attr_value_start_index] not in ["'", "\"", "[", "{"]:
            pattern = "[-\\+\\*/0-9_\\.a-zA-Z$\\(\\)\\\\'\"\\[\\]{}=]*"
            attr_value_end_index = re.search(pattern, attr_str).end()
        else:
            attr_value_end_index = match_content_to_index(attr_str, attr_value_start_index)
        attr_value = attr_str[attr_value_start_index: attr_value_end_index + 1].strip(" ,")
        # 判断attr_key为attrs的attr_value进行二次处理
        if attr_key == "attrs":
            attr_dict.update(get_attr_dict(attr_value))
        elif attr_key == "staticStyle":
            temp_str = ""
            temp_dict = eval(attr_value)
            for key, value in temp_dict.items():
                if temp_str == "":
                    temp_str = key + ": " + value
                else:
                    temp_str = temp_str + "; " + key + ": " + value
            attr_dict["style"] = "\"" + temp_str + "\""
        elif attr_key == "staticClass":
            attr_dict["class"] = attr_value
        elif attr_key == "on":
            on_func_dict = get_attr_dict(attr_value)
            for key, value in on_func_dict.items():
                if value[:3] == "_vm":
                    attr_dict["@" + key] = "\"" + value[4:] + "\""
                elif key[0] == ":":
                    attr_dict["@" + key[1:]] = value
        elif attr_value[0] not in ['"', "'", "{", "[", "@"]:
            # 以_vm开头
            if attr_value.find("_vm.") >= 0:
                attr_dict[":" + attr_key] = "\"" + attr_value.replace("_vm.", "") + "\""
            # true和false
            else:
                attr_dict[":" + attr_key] = "\"" + attr_value + "\""
        elif attr_key == "model" and attr_value[0] == "{":
            attr_dict["v-model"] = re.search("expression:\"([-a-zA-Z0-9_\\[\\]]*)\"", attr_value).group(1)
        elif attr_key == "directives" and attr_value[0] == "[":
            temp_key = re.search("rawName:\"([-a-zA-Z0-9_]*)\"", attr_value).group(1)
            temp_value = re.search("expression:\"([-a-zA-Z0-9_\\[\\]:']*)\"", attr_value).group(1)
            attr_dict[temp_key] = "\"" + temp_value + "\""
        else:
            attr_dict[attr_key] = attr_value
        if attr_value_end_index + 2 < len(attr_str):
            attr_str = attr_str[attr_value_end_index + 2:]
        else:
            return attr_dict
    return attr_dict


def list_to_vue(data_list):
    vue_str = ""
    # 先区分类型
    while len(data_list) > 0:
        data_dict = data_list.pop(0)
        if data_dict["element_type"] == "_c":
            element_str = "<"
            # 获取元素类型
            element_str += data_dict["element_tag"]
            # 获取元素属性
            attr_dict = get_attr_dict(data_dict.get("element_attr"))
            for key, value in attr_dict.items():
                element_str = element_str + " " + key + "=" + value
            element_str += ">"
            print(element_str)
            # 迭代
            data_list.extend(data_dict.get("element_inner_element", []))
        else:
            # vue_str.append(data_dict["element_value"])
            # vue_str.append("\n")
            pass


file_content = read_file_content("/data/home/zhaoyi/Documents/PycharmProjects/pythonProject/js2vue/js.txt")
list_to_vue([split_inner_from_content(file_content)])
test = '{ref:"form",attrs:{"size":"mini","model":_vm.form,"label-width":"0px"}}'
