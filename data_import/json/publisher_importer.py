import logging
import ijson
from jsonschema import validate
from databases.publisher_db import PublisherRepository
from models.publisher import Publisher
#
# # ��������� �����������
# logging.basicConfig(
#     filename='library.log',
#     level=logging.DEBUG,
#     format='%(asctime)s [%(levelname)s] [%(funcName)s:%(lineno)d] %(message)s'
# )


class JSONPublisherReader:

    def __init__(self, file, repo: PublisherRepository):
        self.repo = repo
        self.json_file = file
        logging.info("������������� jsonreader")

    def load_from_json(self):
        logging.info(f"�������� JSON: {self.json_file}")
        publishers = []
        try:
            with open(self.json_file, 'r') as file:
                parser = ijson.items(file, 'item')
                row_number = 1
                for publisher in parser:
                    required_fields = {
                        "��������",
                        "�����",
                        "�������",
                        "�����"
                    }

                    # �������� ������� ���� �����
                    missing_fields = required_fields - set(publisher.keys())
                    if missing_fields:
                        logging.warning(f"����������� ���� � ������ {row_number}: {missing_fields}")
                        raise ValueError("JSON �� �������� ����������� ���������")

                    logging.debug(f"������������ ������: {row_number}")
                    row_number += 1
                    try:
                        publisher = Publisher(
                            name=publisher['��������'],
                            address=publisher['�����'],
                            phone=publisher['�������'],
                            mail=publisher['�����']
                        )
                        self.repo.save(publisher)
                        publishers.append(publisher)

                    except (KeyError, ValueError) as e:
                        logging.warning(f"������ �������� ������: {row_number}. ������: {str(e)}")
                logging.info(f"��������� ����������� �� JSON: {len(publishers)}")
                return publishers

        except Exception as e:
            logging.error(f"������ ��� ������ JSON: {str(e)}", exc_info=True)
            return []
