from config import db

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)#Always need an id
    first_name = db.Column(db.String(80), unique = False, nullable = False)#max len 80 for string
    last_name = db.Column(db.String(80), unique = False, nullable = False)#These are the column headings in sql i think
    email = db.Column(db.String(120), unique = True, nullable = False)

    def to_json(self):#Communicate API through json, is a python dict pretty much
        return {#Json convention is to use camelcase fields
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email
        }
    
