from flask import Flask
from flask_restful import Resource, Api, abort, request

app = Flask(__name__)
api = Api(app)

users = []

def find_user(user_id):
    return next((u for u in users if u["id"] == user_id), None)

# --- Simple Home Page ---
@app.route("/")
def home():
    return "Hello World"

# --- Users Resources ---
class Users(Resource):
    def get(self):
        return {"users": users}

    def post(self):
        data = request.get_json()
        if not data or "id" not in data or "name" not in data:
            abort(400, message="User must have 'id' and 'name'")

        if find_user(data["id"]):
            abort(400, message=f"User with id {data['id']} already exists")

        users.append(data)
        return {"message": "User added", "user": data}, 201

class User(Resource):
    def get(self, user_id):
        user = find_user(user_id)
        if not user:
            abort(404, message="User not found")
        return user

    def put(self, user_id):
        user = find_user(user_id)
        if not user:
            abort(404, message="User not found")
        data = request.get_json()
        user.update(data)
        return {"message": "User updated", "user": user}

    def delete(self, user_id):
        user = find_user(user_id)
        if not user:
            abort(404, message="User not found")
        users.remove(user)
        return {"message": "User deleted"}

# --- API Routes ---
api.add_resource(Users, "/users")
api.add_resource(User, "/users/<int:user_id>")

print("New feature test")

if __name__ == "__main__":
    app.run(debug=True)
