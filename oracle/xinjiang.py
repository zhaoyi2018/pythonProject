import cx_Oracle

dsn = cx_Oracle.makedsn(
    host="fs.dm.bionta.com",
    port="1521",
    service_name="ps"
)

connection = cx_Oracle.connect(
    user="sadan",
    password="123456",
    dsn=dsn
)

# ´´½¨Ò»¸öÓÎ±ê¶ÔÏó
cursor = connection.cursor()

# Ö´ÐÐSQL²éÑ¯
cursor.execute("SELECT * FROM your_table")

# »ñÈ¡²éÑ¯½á¹û
for row in cursor.fetchall():
    print(row)

# ¹Ø±ÕÓÎ±êºÍÁ¬½Ó
cursor.close()
connection.close()