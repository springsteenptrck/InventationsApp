from flask import flash
from flask_app.models import invention
from flask_bcrypt import Bcrypt
from flask_app.config.mysqlconnection import connectToMySQL
import re


db = "inventations"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User: 
    db = "inventations"
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.inventions = []

    @classmethod
    def create_user(cls,data): 
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        user_id = connectToMySQL(db).query_db(query, data)
        return user_id

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(db).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def get_by_id(cls, user_id):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        data = {
            'id': user_id
        }
        result = connectToMySQL(db).query_db(query, data)
    
        if not result:
            return None
    
        return cls(result[0])

    @staticmethod
    def valid(user):
        is_valid = True 
        if len(user['first_name']) < 2:
            flash("*First Name must be at least 1 characters", category='registration_form_error')
            is_valid = False
        if len(user['last_name']) < 3:
            flash("*Last Name must be at least 3 characters", category='registration_form_error')
            is_valid = False

        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query, {'email': user['email']})
        
        if len(results) > 0:
            flash('Email already exists.', 'register_err')
            is_valid = False
        if len(user['email']) < 5:
            flash("*Email must be at least 3 characters", category='registration_form_error')
            is_valid = False
        if len(user['password']) < 8:
            flash("*Password must be at least 8 characters", category='registration_form_error')
            is_valid = False
        elif user['password'] != user['confirm_password']:
            flash("*Passwords do not match", category='registration_form_error')
            is_valid = False
        return is_valid

    @classmethod
    def get_user_with_inventions(cls, data):
        query = """
        SELECT * FROM users LEFT JOIN invention ON users.id = invention.inventor_id WHERE users.id = %(id)s
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        
        user = cls(results[0])

        for row in results:
            invention_data = {
                'id': row['id'],
                'name': row['name'],
                'description': row['description'],
                'patent_approved': row['patent_approved'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
                'inventor_id': row['inventor_id'],
            }

            user.inventions.append(invention.Invention(invention_data))

        return user 