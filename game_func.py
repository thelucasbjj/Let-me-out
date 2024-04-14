# coding: utf-8
from typing import Optional


def list_item_load(file_name: Optional[str] = None) -> list[list[str]]:
    ''' Контекстный менеджер загрузки файла списка предметов'''

    if not file_name:
        file_name = 'items.txt'

    with open(file_name, 'r', encoding='utf-8') as file_items:
        tmp_list = []
        for line in file_items.readlines():
            line = line.replace('\n', '')
            tmp_list.append((line.split(',')))
        return tmp_list
