# Django-Customer-Manager
Simple shopping app.


### Customer demo
![Customer demo](https://i.ibb.co/zb0R6Dm/customer-demo-gif.gif)

---

### Admin demo
![Admin demo](https://i.ibb.co/BsVQFfw/Admin-Demo-1.gif)

---
#### Credential file
Some credentials are loaded from a file called **cred.txt**. This file is something like this:
```
{	
"RES_PASS_EMAIL":"A",
"RES_PASS_PASSWORD":"B",
"DB_PORT":"C",
"LOCAL_DB_PASS": "D",
"IBB_API_KEY":"E"
}
```
* A -> The email django uses to send a reset password link for customer when he/she requests a password reset
* B -> Password of the eamil you entered in A
* C -> Your databse port(I used postgresql-pgAdmin so it was "5432")
* D -> Your database password
* E -> API key that you can get from [imgbb](https://imgbb.com) to upload images
