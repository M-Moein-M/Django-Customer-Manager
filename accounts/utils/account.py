import base64
from pathlib import Path
import requests
import json


def handle_profilepic_post(req_files):
	files = dict(req_files)
	if files.get('profile_pic') is not None:
		upload_profilepic_to_host(base64.b64encode(files.get('profile_pic')[0].read()))
	else:
		return


def upload_profilepic_to_host(pic):
	data = {'image': pic}
	url = ibb_api_url
	res = requests.post(url, data)
	res_data = json.loads(res.text)
	print(res_data['data']['url'])


def get_ibb_api_key():
	with open(Path(__file__).parent.parent.parent / 'ContactManager' / 'cred.txt', 'r') as f:
		cred_dict = json.loads(f.read())
		return cred_dict['IBB_API_KEY']


ibb_api_key = get_ibb_api_key()
ibb_api_url = f"https://api.imgbb.com/1/upload?key={ibb_api_key}"
