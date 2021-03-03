import base64
from pathlib import Path
import requests
import json


def is_user_authorized_to_visit_page(req_user, authorized_id):
	if req_user.groups.all()[0].name == 'admin':
		return True
	else:
		return str(req_user.customer.id) == str(authorized_id)


def handle_profilepic_post(req_files, customer):
	files = dict(req_files)
	if files.get('profile_pic') is not None:
		upload_profilepic_to_host(base64.b64encode(files.get('profile_pic')[0].read()), customer)
	else:
		return


def save_new_profilepic(new_url, customer):
	customer.profile_pic = new_url
	customer.save(update_fields=['profile_pic'])


def upload_profilepic_to_host(pic, customer):
	data = {'image': pic}
	url = ibb_api_url
	res = requests.post(url, data)
	res_data = json.loads(res.text)
	save_new_profilepic(res_data['data']['url'], customer)


def get_ibb_api_key():
	with open(Path(__file__).parent.parent.parent / 'ContactManager' / 'cred.txt', 'r') as f:
		cred_dict = json.loads(f.read())
		return cred_dict['IBB_API_KEY']


ibb_api_key = get_ibb_api_key()
ibb_api_url = f"https://api.imgbb.com/1/upload?key={ibb_api_key}"
