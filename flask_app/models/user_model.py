from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models import party_model
from flask import flash
import re

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")


class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    # ?================ READ ALL ===================
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)
        print(results)
        users = []
        for row in results:
            this_user = cls(row)
            users.append(this_user)
        return users

    # ? ======= CREATE USER ==============
    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO users (first_name, last_name, email, password)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    # ? ========= READ ONE (GET BY ID)=============
    @classmethod
    def get_by_id(cls, data):
        query = """
            SELECT * FROM users
            WHERE users.id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    # ? ========= READ ONE (GET BY EMAIL)=============
    @classmethod
    def get_by_email(cls, data):
        query = """
            SELECT * FROM users
            WHERE users.email = %(email)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    # ? ========== USER VALIDATOR ============
    @staticmethod
    def validate(data):
        is_valid = True

        if len(data["first_name"]) < 2:
            is_valid = False
            flash("At least 2 char Required")

        if len(data["last_name"]) < 2:
            is_valid = False
            flash("At least 2 char Required")

        if len(data["email"]) < 1:
            is_valid = False
            flash("email Required")
        elif not EMAIL_REGEX.match(data["email"]):
            flash("Invalid email address!")
            is_valid = False
        else:
            data_for_email = {"email": data["email"]}
            potential_user = User.get_by_email(data_for_email)
            if potential_user:
                is_valid = False
                flash("email already taken!")

        if len(data["password"]) < 8:
            is_valid = False
            flash("password Required")
        elif not data["password"] == data["confirm_password"]:
            is_valid = False
            flash("passwords don't match!")

        return is_valid

    #  ? ===================== UPDATE ==================
    @classmethod
    def update(cls, data):
        query = """
            UPDATE users 
            SET first_name=%(first_name)s,
                last_name=%(last_name)s,
                email=%(email)s 
            WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    # ? =================== DELETE ======================
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
