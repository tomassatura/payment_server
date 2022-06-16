from src.server import PaymentServer
from xml.etree import ElementTree
from src.get_base_dir_path import GetBaseDirPath
from src.records_keeping import Records

Records().clear_records()
Records().clear_balance()
Records().clear_results()

base_path = GetBaseDirPath().__call__()

for index in range(1, 21):
    path2payment = "{}/resources/payments/payment_{}.xml".format(base_path, index)
    tree = ElementTree.parse(path2payment)
    root = tree.getroot()
    input_string = ElementTree.tostring(root, encoding='utf8').decode('utf8')
    transaction = PaymentServer(input_string)
    transaction.handle()
    transaction.output_string.write("tests/results/result_payment_{}.xml".format(index))