"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")
jackson_family.add_member({    
                        "first_name":"John",
                        "age":33,
                        "Lucky Numbers": [7, 13, 22]
                        })
jackson_family.add_member({
                           "first_name": "Jane",
                            "age":35,
                           "Lucky Numbers": [10, 14, 3]})
jackson_family.add_member({
                            "first_name":"Jimmy" ,
                            "age":5 ,
                            "Lucky Numbers": [1]})

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():
    members = jackson_family.get_all_members()
    return jsonify(members), 200


@app.route('/member/<int:id>', methods=['GET'])
def get_member_for_id(id):
    member = jackson_family.get_member(id)
    if member is None:
        return jsonify({"msg": "No se encuentra información"}), 404
    return jsonify(member), 200


@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member_for_id(id):
    success = jackson_family.delete_member(id)
    if not success:
        return jsonify({"msg": "No se encuentra información"}), 404
    return jsonify({"done": True}), 200



@app.route("/member",methods=['POST'])
def new_member():
    body=request.get_json(silent=True)
    if body is None:
        return jsonify({"message":"debes enviar informacion en el body"})
    if "first_name" not in body:
        return jsonify({"message":"el campo first_name es obligatorio"})
    print(body)
    new_member_data = {
            "id": body.get("id",jackson_family._generateId()),
            "first_name": body["first_name"],
            "last_name": jackson_family.last_name,
            "age": body["age"],
            "lucky_numbers": body["lucky_numbers"]
        }
    return jsonify(jackson_family.add_member(new_member_data)),200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
