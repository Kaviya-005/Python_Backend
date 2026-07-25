class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(100), unique=True)

    hashed_password = db.Column(db.String(255))

    is_active = db.Column(db.Boolean, default=True)



from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(password, hashed_password):
    return pwd_context.verify(
        password,
        hashed_password
    )


@app.post("/api/v1/auth/register")

async def register(user:UserCreate):

    hashed = get_password_hash(user.password)

    return {
        "email":user.email,
        "hashed_password":hashed
    }



from jose import jwt

SECRET_KEY = "secret"

ALGORITHM = "HS256"

@app.post("/api/v1/auth/login")

async def login():

    token = jwt.encode(
        {"sub":"student@gmail.com"},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {

        "access_token":token,

        "token_type":"bearer"

    }



from fastapi import Depends

def get_current_user():

    return "Authenticated User"


@app.post("/api/v1/courses/")

async def add_course(

current_user=Depends(get_current_user)

):

    return {

        "message":"Authorized"

    }



from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(

CORSMiddleware,

allow_origins=[
"http://localhost:3000"
],

allow_methods=["*"],

allow_headers=["*"]

)


//hands on 10



from flask import Flask

app = Flask(__name__)

@app.route("/api/courses/<int:id>")

def get_course(id):

    return {

        "id":id,

        "name":"Python"

    }

app.run(port=5001)




from flask import Flask

app = Flask(__name__)

@app.route("/api/students/<int:id>")

def get_student(id):

    return {

        "id":id,

        "name":"John"

    }

app.run(port=5002)




import requests

@app.route("/api/students/<int:id>/enroll")

def enroll(id):

    response = requests.get(

    "http://localhost:5001/api/courses/1"

    )

    return response.json()




import requests

try:

    requests.get(
        "http://localhost:5001/api/courses/1"
    )

except requests.ConnectionError:

    return {

        "error":"Course Service Unavailable"

    },503



from flask import Flask
import requests

app = Flask(__name__)

@app.route("/api/courses/<path:path>")

def gateway_courses(path):

    return requests.get(

    f"http://localhost:5001/api/courses/{path}"

    ).text


@app.route("/api/students/<path:path>")

def gateway_students(path):

    return requests.get(

    f"http://localhost:5002/api/students/{path}"

    ).text

app.run(port=5000)