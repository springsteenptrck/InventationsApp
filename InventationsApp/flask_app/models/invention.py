from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

db = "inventations"

class Invention:
    db = "inventations"
    def __init__(self, data=None):
        if data is not None:
            self.id = data['id']
            self.name = data['name']
            self.description = data['description']
            self.patent_approved = data['patent_approved']
            self.inventor_id = data['inventor_id']
            self.first_name = data['first_name']
            self.last_name = data['last_name']


    @classmethod
    def read_all_inventions(cls):
        query = "SELECT * FROM inventions LEFT JOIN users ON users.id = inventions.inventor_id;"
        results = connectToMySQL(db).query_db(query)
        all_inventions = []

        for row in results:
            invention = cls(row) 
            all_inventions.append(invention)

        return all_inventions

    @classmethod
    def create_invention(cls,data):
        query = "INSERT INTO inventions(name, description, patent_approved, inventor_id) VALUES (%(name)s, %(description)s, %(patent_approved)s, %(inventor_id)s);"
        results = connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_one_with_user(cls,data):
        query = "SELECT * FROM inventions LEFT JOIN users on users.id = inventions.inventor_id WHERE inventions.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        row = results[0]
        one_invention = cls(row)
        user_data = {
            "id": row['users.id'],
            "first_name": row['first_name'],
            "last_name": row['last_name'],
            "email": row['email'],
            "password": row['password'],
            "created_at": row['users.created_at'],
            "updated_at": row['users.updated_at'],
        }

        one_invention.inventor = user.User(user_data)

        return one_invention

    @classmethod
    def update(cls,data):
        query = """
        UPDATE inventions
        SET name=%(name)s, description=%(description)s, patent_approved=%(patent_approved)s 
        WHERE id = %(id)s;"""

        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def delete_invention(cls, data):
        query = "DELETE FROM inventions WHERE id = %(id)s;"
        connectToMySQL(db).query_db(query, data)
    
    @staticmethod
    def valid(invention):
        is_valid = True 
        if len(invention['name']) < 3:
            flash("*Name must be at least 3 characters")
            is_valid = False
        if len(invention['description']) < 1:
            flash("*A description must be submitted")
            is_valid = False
        print(is_valid)
        return is_valid

