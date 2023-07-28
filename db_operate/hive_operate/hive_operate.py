from db_operate.shared_lib.get_config import *
from db_operate.shared_lib.hive_helper import HiveHelper
from db_operate.shared_lib.logger import Logger

CONFIG = get_config(file=os.path.join(os.path.dirname(__file__), 'config.json'))
logger = Logger(__name__)

if __name__ == '__main__':
    logger.info("城市对比-交通")
    hive_helper = HiveHelper()
    hive_helper.close()