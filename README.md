# Django-Customer-Manager
Simple shopping app.

Set the cred.txt file(read below) and just run 
```
docker-compose up
```
and go to http://127.0.0.1:8000/


### Customer demo
![Customer demo](https://i.ibb.co/zb0R6Dm/customer-demo-gif.gif)

---

### Admin demo
![Admin demo](https://i.ibb.co/BsVQFfw/Admin-Demo-1.gif)

---
#### Credential file
Some credentials are loaded from a file called **cred.txt**.
Create a text file: /app/ContactManager/cred.txt
The content of the file should be filled like this but with your credentials and values:
```
{	
"RES_PASS_EMAIL":"A",
"RES_PASS_PASSWORD":"B",
"IBB_API_KEY":"C",
"SUPERUSER_NAME": "D",
"SUPERUSER_EMAIL": "E",
"SUPERUSER_PASS": "F"
}
```
* A -> The email django uses to send a reset password link for customer when he/she requests a password reset
* B -> Password of the eamil you entered in A
* C -> API key that you can get from [imgbb](https://imgbb.com) to upload images
* D -> Default superuser **name** to create(if does not already exist) when server starts
* E -> Default superuser **email** to create(if does not already exist) when server starts
* F -> Default superuser **password** to create(if does not already exist) when server starts 
