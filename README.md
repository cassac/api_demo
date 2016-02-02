###Flask application demonstrating an API

Load app
`from app import *`
then create database
`db.create_all()`

Create a user:
```curl -i -H "Content-Type: application/json" -X POST -d '{"username":"<username>"}' http://localhost:5000/api/v1/users```

Get all users:
```curl -i -H "Content-Type: application/json" -X GET http://localhost:5000/api/v1/users```

Get a user:
```curl -u <username>:<password> -i -H "Content-Type: application/json" -X GET http://localhost:5000/api/v1/users/<username>```

Edit a user:
```curl -u <username>:<password> -i -H "Content-Type: application/json" -X POST -d '{"new_username":"<new_username>"}' http://localhost:5000/api/v1/users/<username>```

Delete a user:
```curl -u <username>:<password> -i -H "Content-Type: application/json" -X DELETE http://localhost:5000/api/v1/users/<username>```

Get all messages:
```curl -u <username>:<password> -i -H "Content-Type: application/json" -X GET http://localhost:5000/api/v1/messages```

Create a message:
```curl -u <username>:<password> -i -H Content-Type: application/json" -X POST -d '{"recipients":"<username>,<username>", "sender":"<username>", "text":"this is a message"}' http://localhost:5000/api/v1/messages```