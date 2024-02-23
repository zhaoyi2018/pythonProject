import json

from dataease.utils.utils import to_snake_name, to_capitalize_name

top_content = """package io.dataease.plugins.common.base.domain;

import java.util.ArrayList;
import java.util.List;

"""

class_first_content = """public class ReplaceClassExample {
    protected String orderByClause;

    protected boolean distinct;

    protected List<Criteria> oredCriteria;
    
    public ReplaceClassExample() {
        oredCriteria = new ArrayList<Criteria>();
    }

    public void setOrderByClause(String orderByClause) {
        this.orderByClause = orderByClause;
    }

    public String getOrderByClause() {
        return orderByClause;
    }

    public void setDistinct(boolean distinct) {
        this.distinct = distinct;
    }

    public boolean isDistinct() {
        return distinct;
    }

    public List<Criteria> getOredCriteria() {
        return oredCriteria;
    }

    public void or(Criteria criteria) {
        oredCriteria.add(criteria);
    }

    public Criteria or() {
        Criteria criteria = createCriteriaInternal();
        oredCriteria.add(criteria);
        return criteria;
    }

    public Criteria createCriteria() {
        Criteria criteria = createCriteriaInternal();
        if (oredCriteria.size() == 0) {
            oredCriteria.add(criteria);
        }
        return criteria;
    }

    protected Criteria createCriteriaInternal() {
        Criteria criteria = new Criteria();
        return criteria;
    }

    public void clear() {
        oredCriteria.clear();
        orderByClause = null;
        distinct = false;
    }

    protected abstract static class GeneratedCriteria {
        protected List<Criterion> criteria;

        protected GeneratedCriteria() {
            super();
            criteria = new ArrayList<Criterion>();
        }

        public boolean isValid() {
            return criteria.size() > 0;
        }

        public List<Criterion> getAllCriteria() {
            return criteria;
        }

        public List<Criterion> getCriteria() {
            return criteria;
        }

        protected void addCriterion(String condition) {
            if (condition == null) {
                throw new RuntimeException("Value for condition cannot be null");
            }
            criteria.add(new Criterion(condition));
        }

        protected void addCriterion(String condition, Object value, String property) {
            if (value == null) {
                throw new RuntimeException("Value for " + property + " cannot be null");
            }
            criteria.add(new Criterion(condition, value));
        }

        protected void addCriterion(String condition, Object value1, Object value2, String property) {
            if (value1 == null || value2 == null) {
                throw new RuntimeException("Between values for " + property + " cannot be null");
            }
            criteria.add(new Criterion(condition, value1, value2));
        }
"""

common_method_list = [
    """public Criteria andFieldNameIsNull() {
            addCriterion("field_name is null");
            return (Criteria) this;
        }""",
    """public Criteria andFieldNameIsNotNull() {
            addCriterion("field_name is not null");
            return (Criteria) this;
        }""",
    """public Criteria andFieldNameEqualTo(FieldType value) {
            addCriterion("field_name =", value, "fieldName");
            return (Criteria) this;
        }""",
    """public Criteria andFieldNameNotEqualTo(FieldType value) {
            addCriterion("field_name <>", value, "fieldName");
            return (Criteria) this;
        }""",
    """public Criteria andFieldNameGreaterThan(FieldType value) {
            addCriterion("field_name >", value, "fieldName");
            return (Criteria) this;
        }""",
    """public Criteria andFieldNameGreaterThanOrEqualTo(FieldType value) {
            addCriterion("field_name >=", value, "fieldName");
            return (Criteria) this;
        }""",
    """public Criteria andFieldNameLessThan(FieldType value) {
            addCriterion("field_name <", value, "fieldName");
            return (Criteria) this;
        }""",
    """public Criteria andFieldNameLessThanOrEqualTo(FieldType value) {
            addCriterion("field_name <=", value, "fieldName");
            return (Criteria) this;
        }""",
    """public Criteria andFieldNameIn(List<FieldType> values) {
            addCriterion("field_name in", values, "fieldName");
            return (Criteria) this;
        }""",
    """public Criteria andFieldNameNotIn(List<FieldType> values) {
            addCriterion("field_name not in", values, "fieldName");
            return (Criteria) this;
        }""",
    """public Criteria andFieldNameBetween(FieldType value1, FieldType value2) {
            addCriterion("field_name between", value1, value2, "fieldName");
            return (Criteria) this;
        }""",
    """public Criteria andFieldNameNotBetween(FieldType value1, FieldType value2) {
            addCriterion("field_name not between", value1, value2, "fieldName");
            return (Criteria) this;
        }"""
]

string_method_list = [
    """public Criteria andFieldNameLike(FieldType value) {
            addCriterion("field_name like", value, "fieldName");
            return (Criteria) this;
        }""",
    """public Criteria andFieldNameNotLike(FieldType value) {
            addCriterion("field_name not like", value, "fieldName");
            return (Criteria) this;
        }"""
]

method_content = """

        """

class_last_content = """
    }

    public static class Criteria extends GeneratedCriteria {

        protected Criteria() {
            super();
        }
    }

    public static class Criterion {
        private String condition;

        private Object value;

        private Object secondValue;

        private boolean noValue;

        private boolean singleValue;

        private boolean betweenValue;

        private boolean listValue;

        private String typeHandler;

        public String getCondition() {
            return condition;
        }

        public Object getValue() {
            return value;
        }

        public Object getSecondValue() {
            return secondValue;
        }

        public boolean isNoValue() {
            return noValue;
        }

        public boolean isSingleValue() {
            return singleValue;
        }

        public boolean isBetweenValue() {
            return betweenValue;
        }

        public boolean isListValue() {
            return listValue;
        }

        public String getTypeHandler() {
            return typeHandler;
        }

        protected Criterion(String condition) {
            super();
            this.condition = condition;
            this.typeHandler = null;
            this.noValue = true;
        }

        protected Criterion(String condition, Object value, String typeHandler) {
            super();
            this.condition = condition;
            this.value = value;
            this.typeHandler = typeHandler;
            if (value instanceof List<?>) {
                this.listValue = true;
            } else {
                this.singleValue = true;
            }
        }

        protected Criterion(String condition, Object value) {
            this(condition, value, null);
        }

        protected Criterion(String condition, Object value, Object secondValue, String typeHandler) {
            super();
            this.condition = condition;
            this.value = value;
            this.secondValue = secondValue;
            this.typeHandler = typeHandler;
            this.betweenValue = true;
        }

        protected Criterion(String condition, Object value, Object secondValue) {
            this(condition, value, secondValue, null);
        }
    }
}"""

with open('./config.json', 'r') as f:
    config_dict = json.load(f)


def gen_example_class(data):
    res = top_content
    res += class_first_content.replace("ReplaceClass", data["className"])
    for fieldName, fieldType in data["fields"].items():
        capi_name = to_capitalize_name(fieldName)
        snake_name = to_snake_name(fieldName)
        for method_string in common_method_list:
            res += method_content
            res += method_string.replace("fieldName", fieldName)\
                .replace("field_name", snake_name)\
                .replace("FieldName", capi_name)\
                .replace("FieldType", fieldType)
        if fieldType == "String":
            for method_string in string_method_list:
                res += method_content
                res += method_string.replace("fieldName", fieldName)\
                    .replace("field_name", snake_name)\
                    .replace("FieldName", capi_name)\
                    .replace("FieldType", fieldType)
    res += class_last_content
    return res


res = gen_example_class(config_dict)

with open("./data/example.class", "w") as f:
    f.write(res)