import re


def remove_ineffective_text(prefix, lst):
    remove_list = ['\n', ' ']  # 首尾需要移除的东西
    for x in remove_list:
        list_cache = []
        for y in lst:
            split_list = y.split(x)
            for _ in split_list:
                if split_list[0] == '':
                    del split_list[0]
                if len(split_list) > 0:
                    if split_list[-1] == '':
                        del split_list[-1]
            for _ in split_list:
                if len(split_list) > 0:
                    if split_list[0][0] in prefix:
                        split_list[0] = re.sub(r'^' + split_list[0][0], '', split_list[0])
            list_cache.append(x.join(split_list))
        lst = list_cache
    duplicated_list = []  # 移除重复命令
    for x in lst:
        if x not in duplicated_list:
            duplicated_list.append(x)
    lst = duplicated_list
    return lst


def RemoveDuplicateSpace(text: str):
    strip_display_space = text.split(' ')
    display_list = []  # 清除指令中间多余的空格
    for x in strip_display_space:
        if x != '':
            display_list.append(x)
    text = ' '.join(display_list)
    return text
