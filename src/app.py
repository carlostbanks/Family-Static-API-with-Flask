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

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "family": members
    }
    if len(members) == 0:
        return "Error, no family members found", 400
    return jsonify(response_body), 200


@app.route('/members/<int:id>', methods=['GET'])
def get_specific_family_member(id):
    member = jackson_family.get_member(id)
    
    if member: 
        return jsonify(member), 200
    else:
        return jsonify({
            'status': 'failed',
            'message': 'User not found'
        }), 400

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_specific_family_member(id):
    member = jackson_family.get_member(id)

    if member: 
        jackson_family.delete_member(id)
        return jsonify({
            'status': 'success',
            'message': 'Family member successfully deleted :)'
        }), 200
    else:
        return jsonify({
            'status': 'failed',
            'message': 'User not found'
        }), 400

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
