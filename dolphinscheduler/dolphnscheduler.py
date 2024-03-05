from tools import file_util
from db_operate.shared_lib.get_config import *
from db_operate.shared_lib.logger import Logger

CONFIG = get_config(file=os.path.join(os.path.dirname(__file__), 'config.json'))
logger = Logger(__name__)


def gene_script(dir_path, file_name):
    """
    生成脚本
    :return:
    """
    if file_name.endswith("py"):
        return "source ${project_path}/venv/bin/activate\n" \
                   "cd ${project_path}" + dir_path + "\n" \
                                                     "python3 " + file_name + "\n" + "deactivate"
    else:
        return "cd ${project_path}" + dir_path + "\n" \
                                                "Rscript " + file_name + " ${project_path}" + dir_path


abs_path = "/data/home/zhaoyi/Documents/Idea_project/leader-warehouse-dongxiang-backend-schedule-modules-src-main" \
           "-dongxiang_analyse/backend-schedule-modules/src/main/dongxiang_analyse"
for key, value in CONFIG['oozie'].items():
    if file_util.exist_file(abs_path + value, file_type='file'):
        item_list = value.split("/")
        print(key)
        print(gene_script("/".join(item_list[:-1]), item_list[-1]))
        print()
    else:
        print("File path is Error->", key)
