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

    int deleteByPrimaryKey(idType idName);

    int insert(className record);

    int insertSelective(className record);

    List<className> selectByExample(classNameExample example);

    className selectByPrimaryKey(idType idName);

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
    "example_content": """\n  <sql id="Example_Where_Clause">
    <where>
      <foreach collection="oredCriteria" item="criteria" separator="or">
        <if test="criteria.valid">
          <trim prefix="(" prefixOverrides="and" suffix=")">
            <foreach collection="criteria.criteria" item="criterion">
              <choose>
                <when test="criterion.noValue">
                  and ${criterion.condition}
                </when>
                <when test="criterion.singleValue">
                  and ${criterion.condition} #{criterion.value}
                </when>
                <when test="criterion.betweenValue">
                  and ${criterion.condition} #{criterion.value} and #{criterion.secondValue}
                </when>
                <when test="criterion.listValue">
                  and ${criterion.condition}
                  <foreach close=")" collection="criterion.value" item="listItem" open="(" separator=",">
                    #{listItem}
                  </foreach>
                </when>
              </choose>
            </foreach>
          </trim>
        </if>
      </foreach>
    </where>
  </sql>
  <sql id="Update_By_Example_Where_Clause">
    <where>
      <foreach collection="example.oredCriteria" item="criteria" separator="or">
        <if test="criteria.valid">
          <trim prefix="(" prefixOverrides="and" suffix=")">
            <foreach collection="criteria.criteria" item="criterion">
              <choose>
                <when test="criterion.noValue">
                  and ${criterion.condition}
                </when>
                <when test="criterion.singleValue">
                  and ${criterion.condition} #{criterion.value}
                </when>
                <when test="criterion.betweenValue">
                  and ${criterion.condition} #{criterion.value} and #{criterion.secondValue}
                </when>
                <when test="criterion.listValue">
                  and ${criterion.condition}
                  <foreach close=")" collection="criterion.value" item="listItem" open="(" separator=",">
                    #{listItem}
                  </foreach>
                </when>
              </choose>
            </foreach>
          </trim>
        </if>
      </foreach>
    </where>
  </sql>""",
    "base_columns": """\n  <sql id="Base_Column_List">
    fields_list
  </sql>""",
    "common_sql": """\n  <select id="selectByExample" parameterType="io.dataease.plugins.common.base.domain.classNameExample" resultMap="BaseResultMap">
    select
    <if test="distinct">
      distinct
    </if>
    <include refid="Base_Column_List" />
    from class_name
    <if test="_parameter != null">
      <include refid="Example_Where_Clause" />
    </if>
    <if test="orderByClause != null">
      order by ${orderByClause}
    </if>
  </select>
  <select id="selectByPrimaryKey" parameterType="java.lang.idType" resultMap="BaseResultMap">
    select 
    <include refid="Base_Column_List" />
    from class_name
    where id_name = #{idName,jdbcType=idSqlType}
  </select>
  <delete id="deleteByPrimaryKey" parameterType="java.lang.idType">
    delete from class_name
    where id_name = #{idName,jdbcType=idSqlType}
  </delete>
  <delete id="deleteByExample" parameterType="io.dataease.plugins.common.base.domain.classNameExample">
    delete from class_name
    <if test="_parameter != null">
      <include refid="Example_Where_Clause" />
    </if>
  </delete>
  <select id="countByExample" parameterType="io.dataease.plugins.common.base.domain.classNameExample" resultType="java.lang.idType">
    select count(*) from class_name
    <if test="_parameter != null">
      <include refid="Example_Where_Clause" />
    </if>
  </select>""",
    "insert": """\n  <insert id="insert" parameterType="io.dataease.plugins.common.base.domain.className">
    insert into class_name (field_name_list)
    values (fieldSqlTyp_with_bracket_list)
  </insert>""",
    "insertSelective": """\n  <insert id="insertSelective" parameterType="io.dataease.plugins.common.base.domain.className">
    insert into class_name
    <trim prefix="(" suffix=")" suffixOverrides=",">
      if_value_list
    </trim>
    <trim prefix="values (" suffix=")" suffixOverrides=",">
      if_insert_value_list
    </trim>
  </insert>""",
    "updateByExampleSelective": """\n  <update id="updateByExampleSelective" parameterType="map">
    update class_name
    <set>
      if_set_value_list
    </set>
    <if test="_parameter != null">
      <include refid="Update_By_Example_Where_Clause" />
    </if>
  </update>""",
    "updateByExample": """\n  <update id="updateByExample" parameterType="map">
    update class_name
    set set_value_with_record_list
    <if test="_parameter != null">
      <include refid="Update_By_Example_Where_Clause" />
    </if>
  </update>""",
    "updateByPrimaryKeySelective": """\n  <update id="updateByPrimaryKeySelective" parameterType="io.dataease.plugins.common.base.domain.className">
    update class_name
    <set>
      if_set_value_except_first_list
    </set>
    where id_name = #{idName,jdbcType=idSqlType}
  </update>""",
    "updateByPrimaryKey": """\n  <update id="updateByPrimaryKey" parameterType="io.dataease.plugins.common.base.domain.AreaMappingGlobal">
    update area_mapping_global
    set set_value_expect_first_list
    where id_name = #{idName,jdbcType=idSqlType}
  </update>""",
    "last": """\n</mapper>"""
}

jdbc_to_sql = {
    "Long": "BIGINT",
    "String": "VARCHAR",
    "Integer": "INTEGER"
}

def gen_mapper_class(data):
    idName = list(data["fields"].keys())[0]
    idType = data["fields"][idName]
    content = mapper_class\
        .replace("className", data["className"])\
        .replace("idType", idType)\
        .replace("idName", idName)
    with open("./data/{}Mapper.java".format(data["className"]), "w") as f:
        f.write(content)


def gen_mapper_xml(data):
    content = mapper_xml_dict["top"].replace("className", data["className"])
    field_dict = data["fields"]
    fieldName_list = [key for key in field_dict]
    snakeName_list = [to_snake_name(key) for key in fieldName_list]
    capiName_list = [to_capitalize_name(key) for key in fieldName_list]
    filedJdbcType_list = [key for key in field_dict.values()]
    fieldSqlTyp_list = [jdbc_to_sql[key] for key in filedJdbcType_list]

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

    # example
    content += mapper_xml_dict["example_content"]

    # base_columns
    content += mapper_xml_dict["base_columns"]\
        .replace("fields_list", ", ".join(['`{}`'.format(name) for name in snakeName_list]))

    # common_sql
    content += mapper_xml_dict["common_sql"]\
        .replace("className", data["className"])\
        .replace("class_name", to_snake_name(data["className"])) \
        .replace("id_name", snakeName_list[0]) \
        .replace("idName", fieldName_list[0]) \
        .replace("idType", filedJdbcType_list[0]) \
        .replace("idSqlType", fieldSqlTyp_list[0])

    # insert
    fieldSqlTyp_with_bracket_list = [
        "#{fieldName,jdbcType=fieldSqlType}"
        .replace("fieldName", fieldName_list[i])
        .replace("fieldSqlType", fieldSqlTyp_list[i])
        for i in range(len(fieldName_list))
    ]
    fieldSqlTyp_with_bracket_with_record_list = [
        "#{record.fieldName,jdbcType=fieldSqlType}"
        .replace("fieldName", fieldName_list[i])
        .replace("fieldSqlType", fieldSqlTyp_list[i])
        for i in range(len(fieldName_list))
    ]
    condition_list = [
        'test="fieldName != null"'
        .replace("fieldName", fieldName_list[i])
        for i in range(len(fieldName_list))
    ]
    condition_with_record_list = [
        'test="record.fieldName != null"'
        .replace("fieldName", fieldName_list[i])
        for i in range(len(fieldName_list))
    ]
    if_value_list = [
        """<if test="fieldName != null">
        field_name,
      </if>""".replace("fieldName", fieldName_list[i])
        .replace("field_name", snakeName_list[i])
        for i in range(len(fieldName_list))

    ]
    if_insert_value_list = [
        """<if condition>
        fieldSqlTyp_with_bracket,
      </if>"""
        .replace("condition", condition_list[i])
        .replace("fieldSqlTyp_with_bracket", fieldSqlTyp_with_bracket_list[i])
        for i in range(len(condition_list))
    ]

    content += mapper_xml_dict["insert"]\
        .replace("className", data["className"])\
        .replace("class_name", to_snake_name(data["className"])) \
        .replace("field_name_list", ", ".join(["`{}`".format(value) for value in snakeName_list])) \
        .replace("fieldSqlTyp_with_bracket_list", ", ".join(fieldSqlTyp_with_bracket_list))

    content += mapper_xml_dict["insertSelective"]\
        .replace("className", data["className"])\
        .replace("class_name", to_snake_name(data["className"])) \
        .replace("if_value_list", "\n      ".join(if_value_list)) \
        .replace("if_insert_value_list", "\n      ".join(if_insert_value_list))

    # update
    if_set_value_list = [
        """<if condition_with_record>
        field_name = fieldSqlTyp_with_bracket_with_record,
      </if>"""
        .replace("condition_with_record", condition_with_record_list[i])
        .replace("field_name", snakeName_list[i])
        .replace("fieldSqlTyp_with_bracket_with_record", fieldSqlTyp_with_bracket_with_record_list[i])
        for i in range(len(condition_with_record_list))
    ]
    content += mapper_xml_dict["updateByExampleSelective"]\
        .replace("class_name", to_snake_name(data["className"]))\
        .replace("if_set_value_list", "\n      ".join(if_set_value_list))

    set_value_with_record_list = [
        """field_name = #{record.fieldName,jdbcType=fieldSqlType}"""
        .replace("field_name", snakeName_list[i])
        .replace("fieldName", fieldName_list[i])
        .replace("fieldSqlType", fieldSqlTyp_list[i])
        for i in range(len(snakeName_list))
    ]
    content += mapper_xml_dict["updateByExample"]\
        .replace("class_name", to_snake_name(data["className"]))\
        .replace("set_value_with_record_list", ", ".join(set_value_with_record_list))

    if_set_value_except_first_list = [
        """<if condition>
        field_name = fieldSqlTyp_with_bracket,
      </if>"""
        .replace("condition", condition_list[i])
        .replace("field_name", snakeName_list[i])
        .replace("fieldSqlTyp_with_bracket", fieldSqlTyp_with_bracket_list[i])
        for i in range(1, len(condition_list))
    ]
    content += mapper_xml_dict["updateByPrimaryKeySelective"]\
        .replace("class_name", to_snake_name(data["className"])) \
        .replace("className", data["className"]) \
        .replace("idName", fieldName_list[0]) \
        .replace("idSqlType", fieldSqlTyp_list[0]) \
        .replace("id_name", snakeName_list[0]) \
        .replace("if_set_value_except_first_list", "\n      ".join(if_set_value_except_first_list))

    set_value_expect_first_list = [
        'field_name = fieldSqlTyp_with_bracket'
        .replace("field_name", snakeName_list[i])
        .replace("fieldSqlTyp_with_bracket", fieldSqlTyp_with_bracket_list[i])
        for i in range(1, len(snakeName_list))
    ]
    content += mapper_xml_dict["updateByPrimaryKey"]\
        .replace("class_name", to_snake_name(data["className"])) \
        .replace("className", data["className"]) \
        .replace("idName", fieldName_list[0]) \
        .replace("idSqlType", fieldSqlTyp_list[0]) \
        .replace("id_name", snakeName_list[0]) \
        .replace("set_value_expect_first_list", ", ".join(set_value_expect_first_list))

    # last
    content += mapper_xml_dict["last"]
    with open("./data/{}Mapper.xml".format(data["className"]), "w") as f:
        f.write(content)


for value in input_data["apiTable"]:
    gen_mapper_class(value)
    gen_mapper_xml(value)
