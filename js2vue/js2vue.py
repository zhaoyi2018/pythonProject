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
        '"': '"',
        "'": "'"
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
        elif content[i] in ["}", ")", "]"] and char_queue[-2] == content[i] and char_queue[-1] in ["'", '"']:
            char_queue.pop()
            char_num -= 1
            char_queue.pop()
            char_num -= 1
        elif content[i] in ["}", ")", "]"] and content[i] in char_queue:
            temp = -1
            while content[i] != char_queue[temp]:
                temp -= 1
            char_num += temp
            char_queue = char_queue[:temp]
        if content[i] == "'":
            if char_queue[-1] == "'":
                char_queue.pop()
                char_num -= 1
            else:
                char_queue.append(char_dict.get(content[i]))
                char_num += 1
        if content[i] == '"':
            if char_queue[-1] == '"':
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


def get_attr_dict(attr_str, inner_elements):
    """

    :param attr_str: 字符串
    :param inner_elements: 一个列表，包含子元素
    :return:
    """
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
            attr_key = attr_str[1:end_index + 1].strip(" \"\'")
            attr_str = attr_str[end_index + 2:].strip(" ,:")
        else:
            attr_key = attr_str[:colon_index].strip(" \"\'")
            attr_str = attr_str[colon_index + 1:].strip(" ,:")
        attr_value_start_index = 0
        # 如果“:”后，非单引号或双引号
        if attr_str[:16] == "function($event)":
            attr_value_end_index = match_content_to_index(attr_str, 16)
        elif attr_str[:6] == "_vm._u":
            attr_value_end_index = match_content_to_index(attr_str, 6)
        elif attr_str[attr_value_start_index] not in ["'", "\"", "[", "{"]:
            pattern = "[-\\+\\*/0-9_\\.a-zA-Z$\\(\\)\\\\'\"\\[\\]{}=]*"
            attr_value_end_index = re.search(pattern, attr_str).end()
        else:
            attr_value_end_index = match_content_to_index(attr_str, attr_value_start_index)
        attr_value = attr_str[attr_value_start_index: attr_value_end_index + 1].strip(" ,")
        # 判断attr_key为attrs的attr_value进行二次处理
        if attr_key == "attrs":
            attr_dict.update(get_attr_dict(attr_value, inner_elements))
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
        elif attr_key == "scopedSlots":
            # 父级元素处理
            attr_dict["slot-scope"] = '"scope"'
            # 子级元素补充，记住我们只需要获取子集元素的字典就行
            # 1. 首先先剥壳
            stop_index = attr_value.find("return ")
            temp_inner_elements = to_husk(attr_value, stop_index+7)
            # 2. 开始循环处理
            while len(temp_inner_elements.strip(" ,")) > 0:
                if temp_inner_elements[:2] == "_c":
                    temp_end = match_content_to_index(temp_inner_elements, 2)
                    temp_inner_dict = split_inner_from_content(temp_inner_elements[:temp_end + 1])
                    inner_elements.append(temp_inner_dict)
                    if temp_end + 1 < len(temp_inner_elements):
                        temp_inner_elements = temp_inner_elements[temp_end + 1:].strip(" ,")
                    else:
                        break
                elif temp_inner_elements[0] == "(":
                    # 子级元素条件预备
                    end_condition_index = match_content_to_index(temp_inner_elements, 0)
                    condition = temp_inner_elements[1: end_condition_index]
                    # 子级元素, 切分三个部分
                    temp_inner_elements = temp_inner_elements[end_condition_index + 2:]
                    fisrt_content, second_content = match_content(temp_inner_elements)
                    second_content, temp_inner_elements = match_content(second_content)
                    # 子级元素内容生成后，存储的字典
                    fisrt_content = split_inner_from_content(fisrt_content)
                    fisrt_content['element_attr'] = "{v-if:" + "\"" + condition + "\"" + ", " + fisrt_content[
                                                                                                    'element_attr'][1:]
                    inner_elements.append(fisrt_content)
                    second_content = split_inner_from_content(second_content)
                    second_content['element_attr'] = "{v-else:'', " + second_content['element_attr'][1:]
                    inner_elements.append(second_content)
                elif temp_inner_elements[:11] == '_vm._v(" ")':
                    temp_inner_elements = temp_inner_elements[11:].strip(" ,")
                elif temp_inner_elements[0] == '[':
                    temp_inner_elements = temp_inner_elements[1: -1]
                else:
                    print("这是scopedSlots判断, 有问题:", temp_inner_elements)
                    break
        elif attr_key == "on" and attr_value[0] == "{":
            on_func_dict = get_attr_dict(attr_value, inner_elements)
            for key, value in on_func_dict.items():
                if value[:3] == "_vm":
                    attr_dict["@" + key] = "\"" + value[4:] + "\""
                elif key[0] == ":":
                    attr_dict["@" + key[1:]] = value
        elif attr_value != '' and attr_value[0] not in ['"', "'", "{", "[", "@"]:
            # 以_vm开头
            if attr_value.find("_vm.") >= 0:
                attr_dict[":" + attr_key] = "\"" + attr_value.replace("_vm.", "") + "\""
            # true和false
            else:
                attr_dict[":" + attr_key] = "\"" + attr_value + "\""
        elif attr_key == "model" and attr_value[0] == "{":
            attr_dict["v-model"] = "\"" + re.search("expression:\"([-a-zA-Z0-9_\\[\\]\\.]*)\"", attr_value).group(
                1) + "\""
        elif attr_key == "directives" and attr_value[0] == "[":
            temp_key = re.search("rawName:\"([-a-zA-Z0-9_]*)\"", attr_value).group(1)
            if "expression" not in attr_value:
                print("特殊情况:", attr_value)
                attr_dict[temp_key] = ""
            else:
                temp_value = re.search("expression:\"([-a-zA-Z0-9_\\[\\]$:'\\.!=&| ]*)\"", attr_value).group(1)
                attr_dict[temp_key] = "\"" + temp_value + "\""
        else:
            attr_dict[attr_key] = attr_value
        if attr_value_end_index + 2 < len(attr_str):
            attr_str = attr_str[attr_value_end_index + 2:]
        else:
            return attr_dict
    return attr_dict


def to_husk(string, stop_index):
    """
    剥壳
    :param string: 输入字符串
    :param stop_index: 最终停止位置
    :return:
    """
    if stop_index < 0 or (string[stop_index] not in ['"', "'", "[", "(", "{", "]", ")", "}"] and string[stop_index:stop_index+2] != "_c"):
        print("输入参数有问题：", string, string[stop_index - 1], stop_index)
        return string
    start = 0
    end = len(string)
    while start < stop_index:
        if string[start] not in ['"', "'", "[", "(", "{"]:
            start += 1
        else:
            temp_end = match_content_to_index(string, start)
            if temp_end >= stop_index:
                end = temp_end
                start += 1
            else:
                start = temp_end + 1
    return string[start: end]


def match_content(string):
    """
    返回第一个匹配内容，和剩余内容
    :param string:
    :return:
    """
    if len(string) <= 0:
        return -1
    start = 0
    while start < len(string):
        if string[start] not in ['"', "'", "[", "(", "{"]:
            start += 1
        else:
            end_index = match_content_to_index(string, start)
            return string[:end_index + 1].strip(" ,[]"), string[end_index + 1:].strip(" ,:[]")


def dict_to_vue(data_dict, nums=0):
    element_str = ""
    # 先区分类型
    if data_dict["element_type"] == "_c":
        one_element_str = "<"
        # 获取元素类型
        one_element_str += data_dict["element_tag"]
        # 获取元素属性
        if "element_inner_element" not in data_dict:
            data_dict["element_inner_element"] = []
        attr_dict = get_attr_dict(data_dict.get("element_attr"), data_dict.get("element_inner_element"))
        # 字典字符串化
        if type(attr_dict) == dict:
            for key, value in attr_dict.items():
                one_element_str = one_element_str + " " + key + "=" + value
        one_element_str += ">"
        # 迭代
        for inner_dict in data_dict.get("element_inner_element", []):
            inner_content = dict_to_vue(inner_dict, nums + 1)
            if inner_content != "":
                one_element_str += "\n" + ("\t" * (nums + 1)) + inner_content + "\n" + ("\t" * nums)
        one_element_str += "</" + data_dict["element_tag"] + ">"
        # one_element_str *= data_dict.get("element_nums", 1)
        element_str = one_element_str
    elif data_dict["element_type"] == "_vm._v":
        if data_dict["element_value"].find("_vm._s") >= 0:
            element_str += "{{ "
            content = data_dict["element_value"].strip()[7:-1]
            if content.find("_vm.") >= 0:
                element_str += content.replace("_vm.", "")
            else:
                element_str += content.strip()
            element_str += " }}"
        else:
            element_str += data_dict["element_value"].strip(" \"[]")
    else:
        print("未处理元素：", data_dict)
    return element_str


file_content = read_file_content("/data/home/zhaoyi/Documents/PycharmProjects/pythonProject/js2vue/js.txt")
# 处理换行
file_content = file_content.replace("\n", "").replace("\t", " ").replace("\\n", "")
# 数据处理前, 先将三元表达式(? :), v-for循环(vm._l)替换为可处理文本
# 1.先处理三元表达式
while file_content.find(")?") > 0:
    index1 = file_content.find(")?") + 1
    index0 = file_content[:index1].rfind("(")
    # ?后面有两种情况，第一种_c(...), 第二种[...]
    if file_content[index1 + 1:index1 + 3] == "_c":
        index2 = match_content_to_index(file_content, index1 + 3) + 1
    elif file_content[index1 + 1] == "[":
        index2 = match_content_to_index(file_content, index1 + 1) + 1
    else:
        print("?后面有:", index1, file_content[index1 + 1], file_content[index1 - 3:index1 + 3])
        break
    print("下标：", index0, index1, index2)
    print("头部条件：", file_content[index0: index1 + 1])
    print("冒号查看：", file_content[index2-1: index2 + 10])
    second_content = match_content(file_content[index2+1:])[0]
    print("第一个匹配内容:", second_content, len(second_content), file_content[index2+1+len(second_content):index2+1+len(second_content)+5])
    file_content = file_content[:index2] + "," + file_content[index2 + 1:]
    file_content = file_content[:index0] + file_content[index1 + 1:]
# 2.处理v-for
while file_content.find("_vm._l") > 0:
    index0 = file_content.find("_vm._l")
    index1 = file_content[index0:].find("return ") + 7
    index4 = match_content_to_index(file_content, index0 + 6)
    index3 = match_content_to_index(file_content, index1 + index0 + 2)
    print(index0, index1, index3, index4)
    print("头部:", file_content[index0: index1 + index0])
    print("尾部:", file_content[index3: index4+2])
    print("全部:", file_content[index0: index4+2])
    key = re.search("_vm\\._l\\(\\(([_a-zA-Z.\\[\\]]+?)\\)", file_content[index0: index1 + index0]).group(1).replace("_vm.", "")
    value = re.search("function([()a-z A-Z,]*?)\\{", file_content[index0: index1 + index0]).group(1)
    print("Key:", key, " Value:", value, "_c('for', {value:'" + value + " in " + key + "'}, [")
    file_content = file_content[:index3 + 1] + "])" + file_content[index4 + 1:]
    file_content = file_content[:index0] + "_c('for', {value:'" + value + " in " + key + "'}, [" + \
                   file_content[index1 + index0:]

print(dict_to_vue(split_inner_from_content(file_content)))
# print(to_husk(file_content, len("([{key:\"default\",fn:function(scope){return [")))
