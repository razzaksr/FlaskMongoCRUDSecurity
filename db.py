from flask_mongoengine import MongoEngine,json
from werkzeug.security import generate_password_hash,check_password_hash

mydb=MongoEngine()

url="mongodb+srv://razak:mohamed@cluster0.ptmlylq.mongodb.net/vignesh?retryWrites=true&w=majority"

class User(mydb.Document):
    username = mydb.StringField(required=True, unique=True)
    password = mydb.StringField(required=True,max_length=255)
    email = mydb.StringField(required=True, unique=True)
    is_active = mydb.BooleanField(default=True)
    # Add other user-related fields as needed
    
    def set_password(self,password):
        self.password=generate_password_hash(password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.is_active

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

class Laptop(mydb.Document):
    model=mydb.StringField()
    serial=mydb.StringField()
    ram=mydb.IntField()
    ssd=mydb.IntField()
    stock=mydb.IntField()
    price=mydb.IntField()
    type=mydb.StringField()