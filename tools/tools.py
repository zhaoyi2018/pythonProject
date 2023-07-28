import pandas


def get_first_num_index(data):
    if data is None or data == '':
        return -1
    for index, char_value in enumerate(data):
        if char_value.isnumeric():
            return index
    return -1


def func1(data, split_dot):
    if data is None or split_dot is None or data == '' or split_dot == '':
        return data
    res = [item.strip() for item in data.split(split_dot)]
    name = list()
    value = list()
    for item in res:
        index = get_first_num_index(item)
        if index < 0:
            continue
        else:
            name.append(item[:index].strip())
            value.append(item[index:].strip())
    return [name, value]


def func2(data, start_dot, medium_dot, end_dot):
    lng = []
    lat = []
    res = [item.strip() for item in data.split("\n")]
    for item in res:
        start_index = item.index(start_dot)
        end_index = item.index(end_dot)
        value = item[start_index + 1: end_index].split(medium_dot)
        lng.append(value[0].strip())
        lat.append(value[1].strip())
    return [lng, lat]


def python_split_to_java(content):
    return "".join([value if index == 0 else value.capitalize() for index, value in enumerate(content.split("_"))])


def sankey_simple(dataframe, key_dict, flag, inner=True):
    # link队列
    df = dataframe[dataframe[flag].isin(key_dict)]
    df['weight'] = df['weight'].astype(int)
    print(str(df.to_json(orient='records', force_ascii=False)).replace("\"source\"", "source").replace("\"target\"",
                                                                                                       "target").replace(
        "\"weight\"", "weight").replace('weight', 'value'))

    # name队列
    update_key_dict = set(df['source' if 'target' == flag else 'target'])
    if inner:
        key_dict = key_dict.union(update_key_dict)
    else:
        key_dict = update_key_dict
    names = pandas.DataFrame(data=list(key_dict), columns=['name'])
    print(str(names.to_json(orient='records', force_ascii=False)).replace("\"name\"", "name"))

    # 迭代
    print("\n次级:")
    sankey_simple(dataframe, update_key_dict, flag, False)


def a_union_of_multiple_sets_interacting(*args):
    if len(args) == 0:
        return set()
    res = set()
    for i in range(len(args)):
        for j in range(i + 1, len(args)):
            res = res.union(args[i].intersection(args[j]))
    return res


# data1 = "核桃12.5万吨；毛茶4.14万吨；粮17.69万吨；烟叶1万吨；甘蔗17.69万吨；生猪71.29万头；水产品1.67万吨"
# split_dot = "；"
# print(func1(data1, split_dot))

# data2 = """应急管理局@99.920544,24.600043；
# 凤山公园应急避难点@99.911927,24.59775；
# 茶花公园应急避难点@99.928717,24.590439；
# 源通公园应急避难点@99.94092,24.586345；"""
# start_dot = "@"
# medium_dot = ","
# end_dot = "；"
# print(func2(data2, start_dot, medium_dot, end_dot))

print(python_split_to_java("rlt_public_safety_case_similarity_spatial_distribution"))

#
# print(a_union_of_multiple_sets_interacting({1, 2, 3}, {2, 4}, {4, 1}, {3, 6}))
