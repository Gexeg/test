import os
import unicodedata
from typing import Optional, Dict
from dataclasses import dataclass

from logger import LOG


@dataclass
class Files:
    base_fp: str
    files: Dict[str, str]


def get_info(directory) -> Dict[str, str]:
    """ Получить файлы-резюме, находящиеся в директории и сохранить их в словаре.

    Ключ формируется из названия директории(должность) и имени файла(ФИО) без расширения

    :param directory: директория с файлами
    :type directory: file-object
    :return: словарь, содержащий путь до файлов-резюме.
    :rtype: Dict[str, str]
    """
    result = {}
    for file in os.scandir(directory):
        applicant_name = file.name.split(".")[0]
        key = f"{directory.name}_{applicant_name}"
        key = unicodedata.normalize("NFC", key)
        result[key] = file.path
    return result


def scan_directory(path: str, base_name: str) -> Optional[Files]:
    """ Получить пути до файлов-резюме и до главного файла-базы.

    :param path: путь до директории с данными
    :type path: str
    :param path: имя файла, содержащего базу
    :type path: str
    :return: датакласс с данными
    :rtype: Optional[Files]
    """
    dirs = {}
    base_fp = None
    for element in os.scandir(path):
        if element.is_file() and element.name == base_name:
            base_fp = element.path
        if os.path.isdir(element.path):
            dirs.update(get_info(element))
    if base_fp:
        files = Files(base_fp, dirs)
        LOG.debug(f"Get basefile and resume")
        LOG.debug(f"{files}")
        return files
    LOG.warning(f"Cannot find basefile")
