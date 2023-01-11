from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Member:
    db = "loginreg"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def save(cls, data):
        query = "INSERT INTO members ( first_name, last_name, email, password) VALUES (%(fname)s, %(lname)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_member_id(cls, data):
        query = "SELECT * FROM members WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        return cls(result[0])

    @classmethod
    def get_member_email(cls,data):
        query = "SELECT * FROM members WHERE email = %(email)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def validate_user(member):
        is_valid = True
        if len(member['fname']) <2:
            flash("First must be at least 2 characters.","Register")
            is_valid = False
        if len(member['lname']) <2:
            flash("Last must be at least 2 characters.","Register")
            is_valid = False
        if len(member['email']) <=0:
            flash("email is required.","Register")
            is_valid = False
        elif not EMAIL_REGEX.match(member['email']):
            flash("Invalid email address!","Register")
            is_valid = False
        if len(member['password']) <8:
            flash("Password must be at least 8 characters.","Register")
            is_valid = False
        if member['password'] != member['confirm']:
            flash("Password does not match","Register")
        return is_valid
