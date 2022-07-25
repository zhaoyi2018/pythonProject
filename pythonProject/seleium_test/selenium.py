# codiing=utf-8
import time
from pythonProject.seleium_test.selenium import webdriver
from pythonProject.seleium_test.selenium import ActionChains


dirver = webdriver.Firefox(executable_path=r'/data/home/zhaoyi/Downloads/geckodriver/geckodriver')
dirver.get("https://aqicn.org/city/china/fuzhou/xuefangzhan/cn")

names = ["pm2_5", "pm10", "o3", "no2", "so2", "co"]
air_quality = dirver.find_element_by_class_name("specie-selector").find_elements_by_tag_name("button")
dir_path = "../../docx/"
# 更换空气质量指标
for m in range(len(air_quality)):
    output_data = []
    ActionChains(dirver).move_to_element(air_quality[m]).perform()
    time.sleep(2)
    # 保证不擦边
    ActionChains(dirver).move_by_offset(0, -100).perform() # 上移
    time.sleep(2)
    # 获取年份的div块
    year_block_list = dirver.find_elements_by_class_name("year-block")
    for i in range(4, len(year_block_list)):
        # 鼠标移动到制定年份块处，使该年的数据展示出来
        ActionChains(dirver).move_to_element(year_block_list[i]).perform()
        time.sleep(2)
        # 移动鼠标远离其他年份模块
        ActionChains(dirver).move_by_offset(0, -120*(1 if i<=3 else -1)).perform() # 上下移
        time.sleep(2)
        ActionChains(dirver).move_by_offset(-200*(i%4), 0).perform() # 左移
        time.sleep(2)
        # 获取365天的div块
        calendar_year = dirver.find_element_by_class_name("calendar-year")
        # 找到全年日历
        every_day = calendar_year.find_element_by_tag_name("g").find_elements_by_tag_name("g")[7].find_elements_by_tag_name("rect")
        time.sleep(0.5)
        # 激活该天事件
        for j in range(len(every_day)):
            ActionChains(dirver).move_to_element(every_day[j]).perform()
            time.sleep(1)
            # 获取此时文本内容(有点问题，得提前控制下)
            try:
                text_data = dirver.find_element_by_class_name("yearly-aqi-tooltip").text
            except:
                print("无数值!")
            else:
                # 简单处理获取年份和数值
                date, value = text_data.split("\n")
                value = value.split(" ")[-1]
                print(names[m], date, value)
                output_data.append(",".join([names[m],date,value]))
        with open(dir_path+names[m]+".csv", "a") as f:
            f.writelines(output_data)