import requests
import mimetypes
import os
import json
import sys

from typing import Iterable, Optional, Union, Dict, Any
from get_applicant_info import Applicant, normalize_salary
from logger import LOG


# TODO Дополнить таблицу соответствий отствутствующими статусами
# В инструкции к АПИ есть статусы с полем name на кириллице, но в ответе сервера их нет
# нужно уточнить этот момент. Как минимум дополнить соответсвия по оставшимся статусам.
STATUSES = {
    "Отправлено письмо": "contacted",
    "Интервью с HR": "HR Interview",
    "Выставлен оффер": "Offered",
    "Отказ": "Declined"
}


class ApplicantUploader():
    def __init__(self, token: str):
        self.token = token
        self.endpoint = "https://dev-100-api.huntflow.ru"
        self.base_headers = {"Authorization": f"Bearer {self.token}"}
        self.account_id = self._get_account_id()
        assert self.account_id
        self.vacancies_ids = self._get_vacancies()
        assert self.vacancies_ids
        self.vacancies_statuses = self._get_vacancies_statuses()
        assert self.vacancies_statuses

    def upload_file(self, fp: Optional[str]) -> Dict:
        """ Загрузить файл кандидата, если есть.

        :param fp: путь к файлу
        :type fp: str
        :return: распарсенные сервером данные
        :rtype: Dict
        """
        if fp is None:
            LOG.debug(f"The applicant has no resume-file.")
            return {}
        url = f"{self.endpoint}/account/{self.account_id}/upload"
        headers = {
            **self.base_headers,
            "X-File-Parse": "true"
        }
        fn = os.path.basename(fp)
        files = {"file": (fn, open(fp, "rb"), mimetypes.guess_type(fn)[0])}
        LOG.debug(f"Uploading resume")
        response = self._handle_request(
            requests.post(url=url, headers=headers, files=files)
        )
        file_id = response.get("id")
        LOG.debug(f"Success. File_id {file_id}")
        return response

    def upload_applicant(self, applicant_data: dict) -> Dict:
        """ Загрузить кандидата в базу.

        :param applicant_data: общие данные о кандидате
        :type applicant_data: dict
        :return: ответ сервера
        :rtype: dict
        """
        url = f"{self.endpoint}/account/{self.account_id}/applicants"
        LOG.debug(f"Start uploading applicant to db")
        response = self._handle_request(
            requests.post(url=url, headers=self.base_headers, json=applicant_data)
        )
        applicant_id = response.get("id")
        LOG.debug(f"Success. Applicant id {applicant_id}")
        return response

    def set_vacancy(self, applicant: Applicant, applicant_id: int) -> Dict:
        """ Установить кандидата на вакансию.

        :param applicant: информация о кандидате из .xlsx файла
        :type applicant: Applicant
        :param applicant_id: ид_кандидата в базе
        :type applicant_id: int
        :return: статус ответа
        :rtype: dict
        """
        url = f"{self.endpoint}/account/{self.account_id}/applicants/{applicant_id}/vacancy"
        if vacancy_id := self.vacancies_ids.get(applicant.vacancy):
            LOG.debug("Set vacancy to applicant.")
            body = {
                "vacancy": vacancy_id,
                "comment": applicant.comment,
            }
            if status := STATUSES.get(applicant.status):
                status_id = self.vacancies_statuses.get(status)
                body["status"] = status_id
            response = self._handle_request(
                requests.post(url=url, headers=self.base_headers, json=body)
            )
            applicant_vacancy_id = response.get("id")
            LOG.debug(f"Success. Applicant- vacancy id {applicant_vacancy_id}")
            return response

    def collect_parsed_data(self, data: dict) -> Dict:
        """ Собрать распознанные данные с загруженного файла.

        :param data: ответ сервера
        :type data: dict
        :return: словарь с данными для загрузки кандидата
        :rtype: Dict
        """
        LOG.debug(f"Collect data from resume.")

        def get_recursively(data: dict, keys: Iterable) -> Optional[Union[float, str]]:
            res = data
            for key in keys:
                if res and isinstance(res, dict):
                    res = res.get(key)
                if res and isinstance(res, list):
                    res = res[0]
            return res

        experience = get_recursively(data, ("fields", "experience"))
        position = None
        company = None
        if experience:
            position = experience.get("position")
            company = experience.get("company")

        external_data = {}
        if text := data.get("text"):
            external_data.setdefault("data", {"body": text})
        if file_id := data.get("id"):
            external_data.setdefault("files", [{"id": file_id}])

        result = {
            "last_name": get_recursively(data, ("fields", "name", "last")),
            "first_name": get_recursively(data, ("fields", "name", "first")),
            "middle_name": get_recursively(data, ("fields", "name", "middle")),
            "phone": get_recursively(data, ("fields", "phones")),
            "email": get_recursively(data, ("fields", "email")),
            "position": position,
            "company": company,
            # TODO уточнить приоритетность источников
            # на данный момент поле закоменнтировано из предположения, что информацию в excel занес рекрутер
            # после разговора с кандидатом
            # "money": normalize_salary(get_recursively(data, ("fields", "salary"))),

            "birthday_day": get_recursively(data, ("fields", "birthdate", "day")),
            "birthday_month": get_recursively(data, ("fields", "birthdate", "month")),
            "birthday_year": get_recursively(data, ("fields", "birthdate", "year")),
            "photo": get_recursively(data, ("photo", "id"))
        }
        result = {key: val for key, val in result.items() if val}
        if external_data:
            external_data["auth_type"] = "NATIVE"
            result.update({"externals": [external_data]})
        return result

    def _handle_request(self, response: requests.models.Response) -> Dict:
        """ Обработать ответ сервера.

        :param response: ответ сервера
        :type response: requests.models.Response
        :return: словарь с полученными данными или значение по умолчанию
        :rtype: dict
        """
        try:
            assert response.ok
            return response.json()
        except AssertionError:
            LOG.error(f"Error response status code")
            LOG.error(f"{response.status_code} - {response.text}")
            sys.exit(1)
        except json.JSONDecodeError:
            LOG.error(f"Not valid JSON")
            sys.exit(1)

    def _get_account_id(self):
        """ Получить идентификатор аккаунта. """
        url = f"{self.endpoint}/accounts"
        LOG.debug(f"Get account id")
        response = self._handle_request(
            requests.get(url=url, headers=self.base_headers)
        )
        if items := response.get("items"):
            return items[0].get("id")

    def _get_vacancies(self):
        """ Получить список идентификаторов вакансий """
        url = f"{self.endpoint}/account/{self.account_id}/vacancies"
        LOG.debug(f"Get vacancies")
        response = self._handle_request(
            requests.get(url=url, headers=self.base_headers)
        )
        if items := response.get("items"):
            return {el["position"]: el["id"] for el in items}
    
    def _get_vacancies_statuses(self):
        """ Получить список статусов вакансий """
        url = f"{self.endpoint}/account/{self.account_id}/vacancy/statuses"
        LOG.debug(f"Get vacancies statuses")
        response = self._handle_request(
            requests.get(url=url, headers=self.base_headers)
        )
        if items := response.get("items"):
            return {el["name"]: el["id"] for el in items}
