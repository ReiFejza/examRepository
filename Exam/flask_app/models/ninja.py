from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Ninja:

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.age = data['age']
        self.likes=data['likes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_who_liked=[]



    @classmethod
    def get_all(cls):
        query = "SELECT * FROM ninjas;"
        results = connectToMySQL('dojos_and_ninjas').query_db(query)
        ninjas = []
        for row in results:
            ninjas.append( cls(row))
        return ninjas

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM ninjas WHERE id = %(ninja_id)s;"
        results = connectToMySQL('dojos_and_ninjas').query_db(query,data)
        return cls( results[0] )

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO ninjas (first_name, last_name, age ) VALUES ( %(first_name)s, %(last_name)s, %(age)s );'
        return connectToMySQL('dojos_and_ninjas').query_db(query, data)
    
    @classmethod
    def update(cls, data):
        query = 'UPDATE ninjas SET likes = %(likes)s WHERE id=%(ninja_id)s;'
        return connectToMySQL('dojos_and_ninjas').query_db(query, data)

    @classmethod
    def addLike(cls, data):
        query = "INSERT INTO ninjas_was_like_from_users (ninjas_id,users_id) VALUES (%(ninja_id)s,%(user_id)s);"
        return connectToMySQL('dojos_and_ninjas').query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM ninjas WHERE id = %(id)s;"
        return connectToMySQL('dojos_and_ninjas').query_db(query,data)

    @classmethod
    def getUsersWhoLiked(cls, data):
        query = "SELECT * FROM ninjas_was_like_from_users LEFT JOIN ninjas ON ninjas_was_like_from_users.ninjas_id = ninjas.id LEFT JOIN users ON ninjas_was_like_from_users.users_id = users.id WHERE ninjas.id = %(ninja_id)s;"
        results = connectToMySQL('dojos_and_ninjas').query_db(query,data)
        myNinja = Ninja.get_one(data)
        for row in results:
            myNinja.users_who_liked.append(row['email'])
        myNinja.likes=len(myNinja.users_who_liked)
        print(myNinja.users_who_liked)
        return myNinja


    

    @staticmethod
    def validate_ninja(ninja):
        is_valid = True
        if len(ninja['first_name']) < 3:
            flash("Ninja's First name must be at least 3 characters","addNinja")
            is_valid= False
        if len(ninja['last_name']) < 3:
            flash("Last name must be at least 3 characters","addNinja")
            is_valid= False
        if len(ninja['age']) < 1:
            flash("Age is required","addNinja")
            is_valid= False
        return is_valid