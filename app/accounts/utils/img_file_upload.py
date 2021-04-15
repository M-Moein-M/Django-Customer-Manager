from pathlib import Path
import json
import requests
import base64


class ImgFieldUploader:
	def __init__(self, request_files, model_field_name, instance):
		self.request_files = request_files
		self.model_field_name = model_field_name
		self.instance = instance
		self.pic_url = None

	def save_pic(self):
		if self.is_field_available_in_request_files():
			self.upload_pic_to_host()
			self.save_new_url_to_instance()
		else:
			return

	def is_field_available_in_request_files(self):
		files = dict(self.request_files)
		return bool(files.get(self.model_field_name))

	def upload_pic_to_host(self):
		pic = self.get_pic_from_files()
		encoded_pic = base64.b64encode(pic)
		self.upload_encoded_pic_to_host(encoded_pic)

	def get_pic_from_files(self):
		files = dict(self.request_files)
		return files.get(self.model_field_name)[0].read()

	def upload_encoded_pic_to_host(self, pic):
		data = {'image': pic}
		url = ibb_api_url
		res = requests.post(url, data)
		res_data = json.loads(res.text)
		self.pic_url = res_data['data']['url']

	def save_new_url_to_instance(self):
		setattr(self.instance, self.model_field_name, self.pic_url)
		self.instance.save(update_fields=[self.model_field_name])


def get_ibb_api_key():
	with open(Path(__file__).parent.parent.parent / 'ContactManager' / 'cred.txt', 'r') as f:
		cred_dict = json.loads(f.read())
		return cred_dict['IBB_API_KEY']


ibb_api_key = get_ibb_api_key()
ibb_api_url = f"https://api.imgbb.com/1/upload?key={ibb_api_key}"