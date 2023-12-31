from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models import user_model


class Party:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.under = data["under"]
        self.descriptions = data["descriptions"]
        self.instructions = data["instructions"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]

    # ? ======= CREATE USER ==============
    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO parties (name, under, descriptions, instructions, user_id, created_at)
            VALUES (%(name)s, %(under)s, %(descriptions)s, %(instructions)s, %(user_id)s, %(created_at)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    #  ? ===================== UPDATE ==================
    @classmethod
    def update(cls, data):
        query = """
            UPDATE parties 
            SET name=%(name)s,
                under=%(under)s,
                descriptions=%(descriptions)s, 
                instructions=%(instructions)s, 
                created_at=%(created_at)s 
            WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    # ? =========== READ ALL ==================
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM parties;"
        results = connectToMySQL(DATABASE).query_db(query)
        parties = []
        for u in results:
            this_user = cls(u)
            parties.append(this_user)
        return parties

    # ? ========= READ ONE (GET BY ID)=============
    @classmethod
    def get_by_id(cls, data):
        query = """
            SELECT * FROM parties
            WHERE parties.id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        print(results)
        if len(results) < 1:
            return False
        return cls(results[0])

    # ? ========== parties VALIDATOR ============
    @staticmethod
    def parties_validate(data):
        is_valid = True

        if len(data["name"]) < 3:
            is_valid = False
            flash("Name At least 3 char Required")

        if len(data["descriptions"]) < 3:
            is_valid = False
            flash("Description At least 3 char Required")

        if len(data["instructions"]) < 3:
            is_valid = False
            flash("Instructions At least 3 char Required")

        if len(data["created_at"]) < 1:
            is_valid = False
            flash("Date Required")

        if "under" not in data:
            is_valid = False
            flash("Minute Required")

        return is_valid

    # ? =================== DELETE ======================
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM parties WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    # ? =================== JOIN ===========================
    @classmethod
    def get_all_user(cls):
        query = """
            SELECT * FROM parties 
            JOIN users 
            ON users.id = parties.user_id; 
        """
        results = connectToMySQL(DATABASE).query_db(query)
        all_parties = []
        if results:
            for row in results:
                this_party = cls(row)
                user_data = {
                    **row,
                    "id": row["users.id"],
                    "created_at": row["users.created_at"],
                    "updated_at": row["users.updated_at"],
                }
                this_user = user_model.User(user_data)
                this_party.writer = this_user
                all_parties.append(this_party)
        return all_parties

    @classmethod
    def get_one_user(cls, data):
        query = """
            SELECT * FROM parties 
            JOIN users 
            ON users.id = parties.user_id
            WHERE parties.id = %(id)s
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        this_party = cls(results[0])
        row = results[0]
        for row in results:
            user_data = {
                **row,
                "id": row["users.id"],
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"],
            }
            this_user = user_model.User(user_data)
            this_party.writer = this_user
        return this_party
