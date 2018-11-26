# coding: utf-8
from flask import jsonify
from app.user import user
import json

user_data = [
	{
		'id': 200,
		'name': 'Allen',
		'age': 23
	},
	{
		'id': 201,
		'name': 'Bob',
		'age': 24
	}
]

@user.route('/<int:id>', methods=['GET'])
def get(id):
	for user in user_data:
		if user['id'] == id:
			return jsonify(status='success', user=user)
			
@user.route('/users', methods=['GET'])
def users():
	data = {
		'status': 'success',
		'users': user_data
	}
	return json.dumps(data, ensure_ascii=False, indent=1)
	
