

def is_user_authorized_to_visit_page(req_user, authorized_id):
	if req_user.groups.all()[0].name == 'admin':
		return True
	else:
		return str(req_user.customer.id) == str(authorized_id)
