import json
from dataease.utils.utils import to_snake_name, to_capitalize_name


with open("./config.json", "r") as f:
    input_data = json.load(f)

mapper_class = """package io.dataease.plugins.common.base.mapper;

import io.dataease.plugins.common.base.domain.className;
import io.dataease.plugins.common.base.domain.classNameExample;
import java.util.List;
import org.apache.ibatis.annotations.Param;

public interface classNameMapper {
    long countByExample(classNameExample example);

    int deleteByExample(classNameExample example);

    int deleteByPrimaryKey(Long id);

    int insert(className record);

    int insertSelective(className record);

    List<className> selectByExample(classNameExample example);

    className selectByPrimaryKey(Long id);

    int updateByExampleSelective(@Param("record") className record, @Param("example") classNameExample example);

    int updateByExample(@Param("record") className record, @Param("example") classNameExample example);

    int updateByPrimaryKeySelective(className record);

    int updateByPrimaryKey(className record);
}"""

mapper_xml_dict = {
    "top": """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="io.dataease.plugins.common.base.mapper.classNameMapper">""",
    "result_content": [
        """\n  <resultMap id="BaseResultMap" type="io.dataease.plugins.common.base.domain.className">""",
        """\n    <id column="id_name" jdbcType="idSqlType" property="idName" />""",
        """\n    <result column="field_name" jdbcType="fieldSqlType" property="fieldName" />""",
        """\n  </resultMap>"""
    ],
    "jdbc_to_sql": {
        "Long": "BIGINT",
        "String": "VARCHAR",
        "Integer": "INTEGER"
    },
    "last": """\n</mapper>"""
}


def gen_mapper_class(data):
    content = mapper_class.replace("className", data["className"])
    with open("./data/{}Mapper.class".format(data["className"]), "w") as f:
        f.write(content)


def gen_mapper_xml(data):
    content = mapper_xml_dict["top"].replace("className", data["className"])
    field_dict = data["fields"]
    fieldName_list = [key for key in field_dict]
    snakeName_list = [to_snake_name(key) for key in fieldName_list]
    capiName_list = [to_capitalize_name(key) for key in fieldName_list]
    filedJdbcType_list = [key for key in field_dict.values()]
    fieldSqlTyp_list = [mapper_xml_dict["jdbc_to_sql"][key] for key in filedJdbcType_list]

    # result
    for index, value in enumerate(mapper_xml_dict["result_content"]):
        if index == 0:
            content += value.replace("className", data["className"])
        elif index == 1:
            content += value.replace("id_name", snakeName_list[0])\
                .replace("idSqlType", fieldSqlTyp_list[0])\
                .replace("idName", fieldName_list[0])
        elif index == 2:
            i = 1
            while i < len(fieldName_list):
                content += value.replace("field_name", snakeName_list[i])\
                    .replace("fieldSqlType", fieldSqlTyp_list[i])\
                    .replace("fieldName", fieldName_list[i])
                i += 1
        else:
            content += value

    # last
    content += mapper_xml_dict["last"]
    with open("./data/{}Mapper.xml".format(data["className"]), "w") as f:
        f.write(content)


gen_mapper_xml(input_data)