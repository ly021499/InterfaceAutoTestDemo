#!/usr/bin/python 
# @Time  : 2021/9/17 17:35
# @Desc  : 工具函数
from config import Config
import jsonpath
import os


def get_target_value(obj, key):
    """
    获取JSON数据中的指定key的value值
    :param obj: dict, 字典对象
    :param key: str, 键名
    :return:
    """
    if not isinstance(obj, dict):
        return "TypeError: unexpected types, Only Supporte Dictionary"

    # 当值不唯一时，通过.分割字符串，取对应索引的值
    if "." in str(key):
        value, index = str(key).split('.')
    else:
        value = key
        index = 0
    expr = '$..{}'.format(str(value))

    field_value = jsonpath.jsonpath(obj=obj, expr=expr)[int(index)]

    return field_value


def copy_environment():
    """
    每次运行复制一份environment
    :return:
    """
    raw_file_path = os.path.join(Config.REPORT_DIR, 'environment.properties')
    new_file_path = os.path.join(Config.REPORT_DIR, 'summary/environment.properties')

    with open(raw_file_path, 'rb+') as f:
        data = f.read()
    with open(new_file_path, 'wb+') as f2:
        f2.write(data)


def open_allure():
    """
    运行完后，自动打开 allure 报告
    :return:
    """
    copy_environment()

    output_dir = os.path.join(Config.REPORT_DIR, 'output')
    summary_dir = os.path.join(Config.REPORT_DIR, 'summary')

    generate_allure_cmd = "allure generate {} -o {} --clean".format(output_dir, summary_dir)
    os.system(generate_allure_cmd)

    # 当前环境下如果为开发环境，则自动打开 allure 报告
    if 'win' in Config.SYSTEM:
        open_allure_cmd = "allure open {}".format(summary_dir)
        os.system(open_allure_cmd)