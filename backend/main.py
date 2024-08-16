from flask import request, jsonify
from config import app, db
from models import Contact


@app.route("/contacts", methods=["GET"])
def get_contacts():
    contacts = Contact.query.all()#Uses flask orm to get all contacts that exist in db
    json_contacts = list(map(lambda x: x.to_json(), contacts))
    return jsonify({"contacts": json_contacts})


@app.route("/create_contact", methods=["POST"])
def create_contact():
    first_name = request.json.get("firstName")#request is the input
    last_name = request.json.get("lastName")
    email = request.json.get("email")
    
    if not first_name or not last_name or not email:
        return jsonify({"message": "You must include a first name, last name, and email"}), 400

    new_contact = Contact(first_name = first_name, last_name = last_name, email = email)#Different init method for db
    try:
        db.session.add(new_contact)
        db.session.commit()#Commit staged build into database permanently
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    return jsonify({"message": "User created!"}), 201


@app.route("/update_contact/<int:user_id>", methods=["PATCH"])#<> for specific variable pass
def update_contact(user_id):#matches path parameter specificed in <>
    contact = Contact.query.get(user_id)#Essnetially given this object, we can modify our sql db directly as a python object
    if not contact:
        return jsonify({"message": "User not found"}), 404
    data = request.json#this is parsing the request input given
    contact.first_name = data.get("firstName", contact.first_name)#Replaces the contact in db with data object["firstName"], if it doesn't exist resorts to second parameter
    contact.last_name = data.get("lastName", contact.last_name)
    contact.email = data.get("email", contact.email)

    db.session.commit()

    return jsonify({"message": "User updated."}), 200


@app.route("/delete_contact/<int:user_id>", methods=["DELETE"])
def delete_contact(user_id):
    contact = Contact.query.get(user_id)#Essnetially given this object, we can modify our sql db directly as a python object
    if not contact:
        return jsonify({"message": "User not found"}), 404
    db.session.delete(contact)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()#get the context of application

    app.run(debug=True)
