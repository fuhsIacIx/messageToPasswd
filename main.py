# -*- coding: utf-8 -*-
# @Time    : 2024/8/20 20:35
# @Author  : sakuya
# @File    : main.py
# @Software: PyCharm

from pypinyin import pinyin, Style
import os

multiplier = 24
divisor = 9
passwd_number = 10

def convert_to_pinyin(target_text):
    grade_one_code=""
    for char in target_text:
        if '\u4e00' <= char <= '\u9fff':
            grade_one_code_list = pinyin(char, style=Style.NORMAL)
            if isinstance(grade_one_code_list[0], list):
                grade_one_code += grade_one_code_list[0][0]
            else:
                grade_one_code += grade_one_code_list[0]
        else:
            grade_one_code += char
    return grade_one_code

def convert_to_ascii(grade_one_code):
    grade_two_code = ""
    for char in grade_one_code:
        ascii_value = ord(char)
        grade_two_code += f"{ascii_value}"
    return grade_two_code

def is_safe(ascii_code_original, original_number):
    ascii_code = ascii_code_original
    index = len(original_number)
    if index >= 93:
        index = 31
    while ascii_code < 33:
        ascii_code += index

    while ascii_code > 126:
        ascii_code -= index

    return ascii_code


def convert_to_password(original_number):
    global divisor
    global multiplier
    global passwd_number
    target_number = int(original_number)
    y_index = int(passwd_number * 0.6)
    is_over_change = True
    final_passwd = ""
    if target_number % 10 != 0:
        y_index = target_number % 10
    change_number = int(target_number * multiplier / divisor)
    str_number = str(change_number)
    while is_over_change:
        if len(str_number) <= passwd_number * 2:
            for i in range(y_index):
                str_number += original_number[i]
        elif len(str_number) >= passwd_number * 3:
            str_number = str_number[(passwd_number - y_index):]
        else:
            y_index = len(str_number) - (passwd_number * 2)
            is_over_change = False

    x_number = str_number[:-(y_index * 3)]
    y_number = str_number[-(y_index * 3):]
    x_number_list = [x_number[i:i+2] for i in range(0, len(x_number), 2)]
    y_number_list = [y_number[i:i+3] for i in range(0, len(y_number), 3)]

    for li in x_number_list:
        ascii_code = int(li)
        ascii_code = is_safe(ascii_code, original_number)
        final_passwd += chr(ascii_code)

    for li in y_number_list:
        ascii_code_y = int(li)
        ascii_code_y = is_safe(ascii_code_y, original_number)
        final_passwd += chr(ascii_code_y)

    return final_passwd





if __name__ == '__main__':
    original_string = input("请输入账户或者软件名\n")
    code = (convert_to_ascii(convert_to_pinyin(original_string)))
    print("由上述信息生成的密码为；" + convert_to_password(code))
    os.system("pause")


