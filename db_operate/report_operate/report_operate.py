from db_operate.shared_lib.get_config import *
from db_operate.shared_lib.mysql_helper import MysqlHelper
from db_operate.shared_lib.tools import *

CONFIG = get_config(file=os.path.join(os.path.dirname(__file__), 'config.json'))
logger = Logger(__name__)
import subprocess


def get_report_data_by_time_and_domain(db_helper, time, domain):
    query_sql = f"SELECT original_report_file FROM {CONFIG['report_table_name']} WHERE " \
                f"report_time='{time}' and " \
                f"field='{domain}'"
    res = db_helper.pd_read_sql(query_sql)
    if res is not None and not res.empty:
        return res['original_report_file'][0]
    else:
        return None


def to_doc(file_path, data):
    with open(file_path, 'wb') as doc_file:
        doc_file.write(data)


def to_pdf(from_doc_path, to_pdf_path):
    command = CONFIG["libreoffice"] + " --headless --convert-to pdf '" + from_doc_path + "' --outdir " + to_pdf_path

    result = subprocess.run(command, shell=True, check=True)

    if result.returncode == 0:
        print("Command executed successfully.")
    else:
        print(f"Command failed with return code: {result.returncode}")


def data_to_blob(dir_path, time, domain):
    doc_path = dir_path + "/" + domain + time + ".doc"
    pdf_path = dir_path + "/" + domain + time + ".pdf"
    with open(doc_path, 'rb') as file:
        doc_data = file.read()
    with open(pdf_path, 'rb') as file:
        pdf_data = file.read()
    return doc_data, pdf_data


def update_data_or_file_to_db(db_helper, doc_data, pdf_data, time, domain):
    update_sql = f"UPDATE {CONFIG['report_table_name']} " \
                 f"SET original_report_file = %s," \
                 f"publish_report_file = %s," \
                 f"publish_report_pdf = %s " \
                 f"WHERE report_time='{time}' and " \
                 f"field='{domain}'"
    if db_helper.operate(update_sql, (doc_data, doc_data, pdf_data)) > 0:
        logger.info("修改成功!")


if __name__ == '__main__':
    logger.info("周报操作")
    mysql_helper = MysqlHelper(section="mysql2")

    doc_path = "./data/" + CONFIG["report_field"] + CONFIG["report_time"] + ".doc"
    pdf_dir = "./data"
    # # 获取数据
    # data = get_report_data_by_time_and_domain(mysql_helper, CONFIG["report_time"], CONFIG["report_field"])
    # if data:
    #     to_doc(doc_path, data)

    # 读取数据
    to_pdf(doc_path, pdf_dir)
    doc_data, pdf_data = data_to_blob("./data", CONFIG["report_time"], CONFIG["report_field"])
    # 更新数据库数据
    for update_time in CONFIG["update_time_list"]:
        update_data_or_file_to_db(mysql_helper, doc_data, pdf_data, update_time, CONFIG["report_field"])

    mysql_helper.close()
