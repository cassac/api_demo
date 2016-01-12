###Flask application demonstrating an API

Load app
`from app import *`
then create database
`db.create_all()`

Create a user:
```curl -i -H "Content-Type: application/json" -X POST -d '{"username":"<username>"}' http://localhost:5000/api/v1/users```


Get all users:
```curl -i -H "Content-Type: application/json" -X GET http://localhost:5000/api/v1/users```

Get a user
```curl -i -H "Content-Type: application/json" -X GET http://localhost:5000/api/v1/users/<username>```

Edit a user
```curl -i -H "Content-Type: application/json" -X POST -d '{"new_username":"<new_username>"}' http://localhost:5000/api/v1/users/<username>```

Delete a user
```curl -i -H "Content-Type: application/json" -X DELETE http://localhost:5000/api/v1/users/<username>```