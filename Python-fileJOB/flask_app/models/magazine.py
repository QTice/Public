from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.register import User



class Magazine:
    db_user = 'magazine'
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        


    @classmethod
    def get_all_page(cls):
        query = "SELECT * FROM magazines;"
        results = connectToMySQL('cls.db_user').query_db(query)
        lists = []
        for i in results:
            lists.append( cls(i))
        return lists

    @classmethod
    def save_page(cls, data):
        query = "INSERT INTO magazines (title,description,created_at,user_id) VALUES (%(title)s,%(description)s,Now(),%(user_id)s);" 
        result = connectToMySQL(cls.db_user).query_db(query,data)
        return result
    
    @classmethod
    def get_one(cls,data):
        query  = "SELECT * FROM magazines WHERE id = %(id)s;"
        result = connectToMySQL(cls.db_user).query_db(query,data)
        return cls(result[0])

    @classmethod
    def get_them(cls,data):
        query  = "SELECT * FROM magazines WHERE user_id = %(id)s;"
        result = connectToMySQL(cls.db_user).query_db(query,data)
        lists = []
        for i in result:
            lists.append( cls(i))
        return lists

    @classmethod
    def update(cls,data):
        print(data)
        query = "UPDATE magazines SET title=%(title)s,description=%(description)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_user).query_db(query,data)

    @classmethod
    def destroy_page(cls,data):
        query  = "DELETE FROM magazines WHERE id = %(id)s;"
        return connectToMySQL(cls.db_user).query_db(query,data)

    @classmethod
    def get_mine( cls , data ):
        query = "SELECT * FROM magazines JOIN users ON magazines.user_id = users.id WHERE user_id=%(id)s ;"
        results = connectToMySQL(cls.db_user).query_db( query , data )

        magazines = []
        
        for row_from_db in results:
            this_magazine = cls(row_from_db)

            data_user = {
                # **row_from_db,
                "id": row_from_db['users.id'],
                "first_name": row_from_db['first_name'],
                "last_name": row_from_db['last_name'],
                "email": row_from_db['email'],
                "password": row_from_db["password"],
                "created_at": row_from_db["users.created_at"],
                "updated_at": row_from_db["users.updated_at"]
            }
            this_user = User(data_user)
            this_magazine.page=this_user
            magazines.append(this_magazine)
        return magazines



    @classmethod
    def get_everybodys(cls):
        query= "SELECT * FROM magazines JOIN users ON magazines.user_id = users.id;"
        results = connectToMySQL(cls.db_user).query_db(query)

        magazines = []
        
        for row_from_db in results:
            this_magazine = cls(row_from_db)

            data_user = {
                **row_from_db,
                "id": row_from_db['users.id'],
                "created_at": row_from_db["users.created_at"],
                "updated_at": row_from_db["users.updated_at"]
            }
            this_user = User(data_user)
            this_magazine.page=this_user
            magazines.append(this_magazine)
        return magazines

    @classmethod
    def get_all_of_mine(cls):
        query= "SELECT * FROM magazines JOIN users ON magazines.user_id = users.id Where user_id=%(id)s;"
        results = connectToMySQL(cls.db_user).query_db(query)

        magazines = []
        
        for row_from_db in results:
            this_magazine = cls(row_from_db)

            data_user = {
                **row_from_db,
                "id": row_from_db['users.id'],
                "created_at": row_from_db["users.created_at"],
                "updated_at": row_from_db["users.updated_at"]
            }
            this_user = User(data_user)
            this_magazine.page=this_user
            magazines.append(this_magazine)
        return magazines

    # @classmethod
    # def get_everybodys(cls):
    #     query= "SELECT * FROM magazines JOIN users ON magazines.user_id = users.id;"
    #     results = connectToMySQL(cls.db_user).query_db(query)

    #     magazines = []
        
    #     for row_from_db in results:
    #         this_magazine = cls(row_from_db)

    #         data_user = {
    #             **row_from_db,
    #             "id": row_from_db['users.id'],
    #             "created_at": row_from_db["users.created_at"],
    #             "updated_at": row_from_db["users.updated_at"]
    #         }
    #         this_user = User(data_user)
    #         this_magazine.page=this_user
    #         magazines.append(this_magazine)
    #     return magazines


    @staticmethod
    def validate_page(page):
        is_valid_page = True
        if len(page['title']) < 2:
            is_valid_page = False
            flash("Title must be at least 2 characters.",'title')
        if len(page['description']) < 7:
            is_valid_page = False
            flash("Description must be at least 7 characters.",'description')
        return is_valid_page