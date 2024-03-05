import math

import pandas as pd

from db_operate.shared_lib.get_config import *
from db_operate.shared_lib.tools import *

CONFIG = get_config(file=os.path.join(os.path.dirname(__file__), 'config.json'))
logger = Logger(__name__)


if __name__ == '__main__':
    logger.info("hive数据库操作")
    hive_helper = HiveHelper(section="hive-fengqing_leaderwarehouse")

    # 读取excel文件
    tables = ["face_clustering_result", "large_enterprises_taxes_jc_test", "ozrlt_city_management_parts_devices_run_state_num_statistics",
                                              "ozrlt_population_association_analysis_elderly_facility_community", "ozrlt_population_preschool_struct_orgname_kg_children_num",
                                              "ozrlt_transportation_cross_road_count_this_month", "ozrlt_transportation_cross_road_count_today",
                                              "ozrlt_transportation_overall_analysis_abnormal_statistic", "ozrlt_transportation_overall_analysis_network",
                                              "r_familyinfo_jc_v2", "rlt2_population_association_analysis_difficult_student", "rlt2_population_association_analysis_elderly_facility_community",
                                              "rlt2_population_preschool_struct_orgname_kg_children_num", "rlt2_public_safe_letter_department_summary", "rlt2_public_safe_letter_increase_rank",
                                              "rlt_business_environment_large_enterprises_space_distribution_table", "rlt_ccb_carbon_rank_guide", "rlt_city_management_petition_analysis",
                                              "rlt_citymanagement_grid_event_big_type", "rlt_citymanagement_traffic_traffic_heat_change", "rlt_health_city_not_completed_this_month",
                                              "rlt_health_city_today_event_num_gps", "rlt_police_crimer_age_v2", "rlt_population_association_analysis_difficult_student",
                                              "rlt_population_association_analysis_elderly_facility_community", "rlt_population_association_analysis_school_child__dist", "rlt_population_brain_report",
                                              "rlt_population_preschool_struct_orgname_kg_children_num", "rlt_temp_low_income_spatial_distribution", "rlt_today_area_accept_event_num"
                                              ]

    # backup_hive_db_to_sql(hive_helper, "./data/fengqing-leaderhouse-v3.sql", tables)
    execute_sql_file(hive_helper, "./data/fengqing-leaderhouse.sql")
    hive_helper.close()

