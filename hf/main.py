import argparse
import sys

from logger import LOG
from scan_directory import scan_directory
from get_applicant_info import get_applicants_info
from send_info import ApplicantUploader


parser = argparse.ArgumentParser()
parser.add_argument("-t", "--token", type=str, required=True,
                    help="Access token.")
parser.add_argument("-bd", "--base_dir", type=str, required=True,
                    help="Path to directory with resumes.")
parser.add_argument("--row", type=int,
                    help="The line with which to start parsing.")


# TODO уточнить имя файла - критерий, на который можно опираться?
# в Readme.md имя файла было подчеркнуто, так что используется как критерий.
# Хотел сначала вынести в отдельный конфиг, но вроде не нашел достаточного количества параметров
BASE_FILENAME = "Тестовая база.xlsx"


def main():
    args = parser.parse_args()

    try:
        uploader = ApplicantUploader(args.token)
    except AssertionError as e:
        LOG.error(f"Error durinng uploader initialization {type(e)}")
        sys.exit(1)

    if files := scan_directory(args.base_dir, BASE_FILENAME):
        for applicant in get_applicants_info(files, args.row):
            uploader.upload_applicant(applicant)


if __name__ == "__main__":
    main()
