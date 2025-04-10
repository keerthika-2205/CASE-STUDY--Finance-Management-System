import mysql.connector
from util.db_property_util import DBPropertyUtil

class DBConnUtil:
    connection = None

    @staticmethod
    def get_connection():
        if DBConnUtil.connection is None:
            #conn_string = DBPropertyUtil.get_property_string("C:/Users/Admin/Desktop/FinanceManagementSystem/db.properties")
            DBConnUtil.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="NewPassword",
                database="finance_db",
                port=3306
            )
        return DBConnUtil.connection
