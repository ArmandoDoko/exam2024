from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Painting:
    db_name = 'exam2024'
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.price = data['price']
        self.quantity = data['quantity']
        self.user_id= data['user_id']
        self.created_at = data['created_at']
        self.updated_at= data['updated_at']

    @classmethod
    def create(cls,data):
        query = 'INSERT INTO paintings (title, description, price, quantity, user_id) VALUES ( %(title)s, %(description)s, %(price)s, %(quantity)s, %(user_id)s);'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def getAllPaintings(cls):
        query = 'SELECT * FROM paintings;'
        results = connectToMySQL(cls.db_name).query_db(query)
        paintings= []
        if results:
            for painting in results:
                paintings.append(painting)
        return paintings


    @classmethod
    def get_logged_paintings(cls,data):
        query = "SELECT * FROM paintings where user_id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        paintings=[]
        if results:
            for painting in results:
                paintings.append(painting)
        return paintings
            

    @classmethod
    def get_painting_by_id(cls,data):
        query = "SELECT * FROM paintings left join users on paintings.user_id = users.id WHERE paintings.id = %(painting_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    @classmethod
    def delete_Painting(cls,data):
        query = 'DELETE FROM paintings WHERE id=%(painting_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def update_painting(cls,data):
        query = 'UPDATE paintings set title = %(title)s, description = %(description)s, price = %(price)s, quantity = %(quantity)s WHERE id = %(id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def delete_users_paintings(cls,data):
        query = 'DELETE FROM paintings Where paintings.user_id=%(user_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
    

    @classmethod
    def addPainted(cls, data):
        try:
            query = 'INSERT INTO painted (user_id, painting_id) VALUES (%(id)s, %(painting_id)s);'
            return connectToMySQL(cls.db_name).query_db(query, data)
        except Exception as e:
            print(f"An error occurred in addPainted: {e}")
            raise e  
    
    @classmethod
    def removePainted(cls,data):
        query= 'DELETE FROM painted where painting_id = %(painting_id)s and user_id = %(id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_painters(cls,data):
        query = 'SELECT user_id from painters where painted.painting_id = %(painting_id)s;'
        results =connectToMySQL(cls.db_name).query_db(query, data)
        painters=[]
        if results:
            for person in results:
                painters.append(person['user_id'])
        return painters
    
    @classmethod
    def get_painters_info(cls,data):
        query = 'SELECT * FROM painted left join users on painted.user_id = user_id where painted.painting_id=%(painting_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        painters =[]
        if results:
            for person in results:
                painters.append(person)
        return painters
    
    @classmethod
    def delete_all_painted(cls,data):
        query = 'DELETE FROM painted Where painting_id =%(painting_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @staticmethod
    def validate_painting(data):
        is_valid = True
        if len(data['title'])<2:
            flash('Title should be at least 2 characters!','title')
            is_valid=False
        if len(data['description'])<2:
            flash('Description should be at least 10 characters long!', 'description')
            is_valid=False
        if len(data['price'])<0:
            is_valid=False
            flash('Price should be greater than 0!', 'price')
            is_valid=False
        return is_valid