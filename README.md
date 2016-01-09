Flask application demonstrating an API

Create database
```from app import *```
```db.create_all()```

Create a user:
```curl -i -H "Content-Type: appliation/json" -X POST -d '{"username":"<username>"}' http://localhost:5000/api/v1/users```

Get all users:
```curl -i -H "Content-Type: appliation/json" -X GET http://localhost:5000/api/v1/users```

Get a user
```curl -i -H "Content-Type: application/json" -X GET http://localhost:5000/api/v1/users/<username>```

Edit a user
```curl -i -H "Content-Type: application/json" -X POST -d '{"new_username":"<new_username>"}' http://localhost:5000/api/v1/users/<username>```

Delete a user
```curl -i -H "Content-Type: appliation/json" -X DELETE http://localhost:5000/api/v1/users/<username>```
