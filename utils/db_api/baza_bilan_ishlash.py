import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE myfiles_teacher (
            id int NOT NULL,
            Name varchar(255) NOT NULL,
            email varchar(255)
            language varchar(3),
            PRIMARY KEY(id)
            );
"""
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())


    def add_user(self, id: int, name: str, email: str = None, language: str = 'uz'):
        #SQL_EXAMPLE = "INSERT INTO myfiles_teacher(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO myfiles_teacher(id, Name, email, language) VALUES(?, ?, ?, ?)
        """
        self.execute(sql, parameters=(id, name, email, language), commit=True)


    def select_all_users(self):
        sql = """
        SELECT * FROM myfiles_teacher
        """
        return self.execute(sql, fetchall=True)

    def select_users(self, **kwargs):
        #SQL_EXAMPLE = "SELECT * FROM myfiles_menu where id= 1 and Name= 'John'"
        sql = "SELECT * FROM myfiles_type WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def filter_product(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM my_files_menu where id = 1 AND Name = 'John'"
        sql = "SELECT * FROM Myfiles_producte WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM myfiles_teacher", fetchone=True)

    def update_user_email(self, email, id):
        #SQL_EXAMPLE = "UPDATE myfiles_menu SET email=mail@gmail.com WHERE  id=12345"

        sql = f"""
        UPDATE myfiles_menu SET email=? WHERE id=?
        """
        return self.execute(sql,parameters=(email,id), commit=True)

    def delete_users(self):
        self.execute("DELETE FROM myfiles_teacher WHERE TRUE", commit=True)

    def anketa(self):
        pass

    #********************************************************************************
    def user_qoshish(self, ism: str, tg_id: int, fam: str = None, username: str=None):
        #SQL_EXAMPLE = "INSERT INTO myfiles_teacher(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO users(ism, fam, username,tg_id) VALUES(?, ?, ?, ?)
        """
        self.execute(sql, parameters=(ism, fam, username,tg_id), commit=True)


    def select_all_foydalanuvchilar(self):  # *o'rniga tg_id  qilsek faqat shuni tg_id beradi
        sql = """
        SELECT * FROM users               
        """
        return self.execute(sql, fetchall=True)

    def select_foydalanuvchilar(self, **kwargs):
        #SQL_EXAMPLE = "SELECT FROM myfiles_teacher where id= 1 and Name= 'John'"
        sql = "SELECT FROM users WHERE id = 6 and ism= 'Senku'"
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def sanash_foydalanuvchilar(self):
        return self.execute("SELECT COUNT(*) FROM users", fetchone=True)

    #&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& baza orqali buttun

    def select_all_menu(self):
        sql = """
        SELECT * FROM menu
        """
        return self.execute(sql, fetchall=True)

    # qiyin usula qilingan
    # def select_all_mahsulotlar(self):
    #     sql = """
    #     SELECT * FROM mahsulotlar WHERE turi = 'taom'
    #     """
    #     return self.execute(sql, fetchall=True)
    #
    # def select_all_ichimliklar(self):
    #     sql = """
    #     SELECT * FROM mahsulotlar WHERE turi = 'ichimlik'
    #     """
    #     return self.execute(sql, fetchall=True)
    #
    # def select_all_salatlar(self):
    #     sql = """
    #     SELECT * FROM mahsulotlar WHERE turi = 'salat'
    #     """
    #     return self.execute(sql, fetchall=True)
    #
    # def select_all_fast_food(self):
    #     sql = """
    #     SELECT * FROM  mahsulotlar WHERE turi = 'fast_food'
    #     """
    #     return self.execute(sql, fetchall=True)
    #
    # def select_all_shirinliklar(self):
    #     sql = """
    #     SELECT * FROM  mahsulotlar WHERE turi = 'shirinlik'
    #     """
    #     return self.execute(sql, fetchall=True)
    #
    # def select_all_milliy_taomlar(self):
    #     sql = """
    #     SELECT * FROM  mahsulotlar WHERE turi = 'milliy_taom'
    #     """
    #     return self.execute(sql, fetchall=True)

    #)))))))))))))))))))))))))))))))))))))))))))))))

    def select_mahsulot(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM myfiles_teacher where id= 1 and Name= 'John'"
        sql = "SELECT nomi FROM mahsulotlar WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchall=True)

    def select_mahsulot_only(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM myfiles_teacher where id= 1 and Name= 'John'"
        sql = "SELECT * FROM mahsulotlar WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def select_all_mahsulotlar(self):
        sql = """
        SELECT nomi FROM mahsulotlar
        """
        return self.execute(sql, fetchall=True)

    def add_mahsulot_to_korzinka(self, nomi: str, narxi: int, rasm: str,  soni: int,  tg_id: int, ism: str):
        #SQL_EXAMPLE = "INSERT INTO myfiles_teacher(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO korzinka (nomi, narxi, rasm, soni, tg_id, ism) VALUES(?, ?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(nomi, narxi, rasm, soni, tg_id, ism), commit=True)


    def count_mahsulot(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM myfiles_teacher where id= 1 and Name= 'John'"
        sql = "SELECT soni FROM korzinka WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def update_user_korzinka(self, soni, tg_id,nomi):
        #SQL_EXAMPLE = "UPDATE myfiles_menu SET email=mail@gmail.com WHERE  id=12345"

        sql = f"""
        UPDATE korzinka SET soni=? WHERE tg_id=? and nomi=? 
        """
        return self.execute(sql,parameters=(soni,tg_id,nomi), commit=True)


    def select_mahsulotlar_from_korzinka(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM myfiles_teacher where id= 1 and Name= 'John'"
        sql = "SELECT * FROM korzinka WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchall=True)


    def select_mahsulot_from_korzinka_only(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM myfiles_teacher where id= 1 and Name= 'John'"
        sql = "SELECT * FROM korzinka WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)


    def delet_mahsulot_from_korzinka(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM myfiles_teacher where id= 1 and Name= 'John'"
        sql = "DELETE FROM korzinka WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, commit=True)


def logger(statement):
    print(f"""
    --------------------------------------------------------
    Executing:
    {statement}
    --------------------------------------------------------

""")
