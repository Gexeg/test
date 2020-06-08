import openpyxl

from typing import Union, Dict
from dataclasses import dataclass

from logger import LOG
from scan_directory import Files


@dataclass
class Applicant:
    vacancy: str
    full_name: str
    salary: int
    comment: str
    status: str
    file_path: str = None


def get_fio(applicant: Applicant) -> Dict:
    """ Получить фамилию, имя и отчество из профиля кандидата.

    :param applicant: датакласс кандидата
    :type applicant: Applicant
    :return: фамилия, имя и отчество кандидата
    :rtype: Dict
    """
    labels = ("last_name", "first_name", "middle_name")
    row = applicant.full_name.strip().split()
    return {key: val for key, val in zip(labels, row)}


def normalize_salary(salary: Union[float, str]) -> float:
    """ Нормализовать запись о зарплате.

    :param salary: полученная из файла запись
    :type salary: Union[float, str]
    :return: нормализованная запись
    :rtype: float
    """
    numbers = set(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])

    salary = str(salary).replace(",", ".")
    salary = "".join(filter(lambda x: x in numbers, salary))
    salary = f"{salary} руб"

    return salary


def parse_xlsx(fp: str, from_row: int) -> Applicant:
    """ Получить данные кандидатов из базы.

    :param fp: путь до .xlsx файла
    :type fp: str
    :param from_row: строка с которой необходимо начать парсинг
    :type from_row: int
    :return: генератор, содержащий данные о кандидатах
    :rtype: Applicant
    :yield: информация о кандидате
    :rtype: Iterator[Applicant]
    """
    wb = openpyxl.load_workbook(fp)
    ws = wb.active
    rows = ws.iter_rows(values_only=True)

    # пропускаем заголовки
    next(rows)
    for ind, row in enumerate(rows, 2):
        if from_row and ind < from_row:
            continue
        applicant = Applicant(
            vacancy=row[0].strip(),
            full_name=row[1].strip(),
            salary=normalize_salary(row[2]),
            comment=row[3].strip(),
            status=row[4].strip()
        )
        LOG.debug(f"Get applicant info from .xlsx")
        LOG.debug(f"{applicant}")
        LOG.debug(f"Process {ind} row")
        yield applicant
    wb.close()


def get_applicants_info(files: Files, from_row: int = None) -> Applicant:
    """ Получить агрегированную инфомацию о кандидате.

    :param files: датакласс, содержащий пути к .xlsx базе и резюме кандидатов
    :type files: Files
    :param from_row: строка с которой необходимо начать парсинг
    :type from_row: int
    :return: генератор, содержащий агрегированные данные о кандидате
    :rtype: Applicant
    :yield: агрегированные данные о кандидате
    :rtype: Iterator[Applicant]
    """
    for applicant in parse_xlsx(files.base_fp, from_row):
        key = f"{applicant.vacancy}_{applicant.full_name}"
        applicant.file_path = files.files.get(key)
        if applicant.file_path:
            LOG.debug(f"Added resume {applicant.file_path}")
        yield applicant
