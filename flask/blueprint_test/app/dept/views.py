# coding: utf-8

from app.dept import dept
from flask import jsonify
import json

dept_data = [
	{
		'name': 'Research',
		'id': 100
	},
	{
		'name': 'Market',
		'id': 101
	}
]

@dept.route('/<int:id>', methods=['GET'])
def get(id):
	for dept in dept_data:
		if int(dept['id']) == id:
			return jsonify(status='success', dept=dept)
	return jsonify(status='failed', msg='dept not found')
	
	
@dept.route('/depts', methods=['GET'])
def get_depts():
	data = {
		'status':'success',
		'depts':dept_data
	}
	return json.dumps(data, ensure_ascii=False, indent=1)
	
