from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///courses.db"

    db.init_app(app)

    Migrate(app, db)

    return app



from app import db

class Department(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))

    head_of_dept = db.Column(db.String(100))

    budget = db.Column(db.Float)

    courses = db.relationship("Course", back_populates="department")


class Course(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))

    code = db.Column(db.String(20), unique=True)

    credits = db.Column(db.Integer)

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("department.id")
    )

    department = db.relationship(
        "Department",
        back_populates="courses"
    )

    enrollments = db.relationship(
        "Enrollment",
        back_populates="course"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "credits": self.credits
        }


class Student(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(50))

    email = db.Column(db.String(100), unique=True)


class Enrollment(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("student.id")
    )

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("course.id")
    )

    student = db.relationship("Student")

    course = db.relationship(
        "Course",
        back_populates="enrollments"
    )




flask db init
flask db migrate -m "initial schema"
flask db upgrade



d = Department(
    name="Computer Science",
    head_of_dept="Dr Kumar",
    budget=500000
)
db.session.add(d)
db.session.commit()



@courses_bp.route("/", methods=["GET"])

def get_courses():

    courses = Course.query.all()

    return jsonify(
        [course.to_dict() for course in courses]
    )



@courses_bp.route("/", methods=["POST"])

def add_course():

    data = request.get_json()

    course = Course(
        name=data["name"],
        code=data["code"],
        credits=data["credits"]
    )

    db.session.add(course)

    db.session.commit()

    return jsonify(course.to_dict()),201




@courses_bp.route("/<int:id>")

def get_course(id):

    return jsonify(
        Course.query.get_or_404(id).to_dict()
    )


@courses_bp.route("/<int:id>",methods=["PUT"])

def update_course(id):

    course = Course.query.get_or_404(id)

    course.name = request.json["name"]

    db.session.commit()

    return jsonify(course.to_dict())


@courses_bp.route("/<int:id>",methods=["DELETE"])

def delete_course(id):

    course = Course.query.get_or_404(id)

    db.session.delete(course)

    db.session.commit()

    return "",204



@courses_bp.route("/<int:id>/students")

def course_students(id):

    students = Student.query.join(
        Enrollment
    ).filter(
        Enrollment.course_id==id
    ).all()

    return jsonify([
        s.first_name for s in students
    ])



//hands on 6

from fastapi import FastAPI

app = FastAPI(
    title="Course Management API",
    version="1.0"
)

@app.get("/")

async def root():

    return {
        "message":"API running"
    }



from pydantic import BaseModel
from typing import Optional

class CourseCreate(BaseModel):

    name:str

    code:str

    credits:int

    department_id:int


class CourseUpdate(BaseModel):

    name:Optional[str]=None

    code:Optional[str]=None

    credits:Optional[int]=None

    department_id:Optional[int]=None


class CourseResponse(BaseModel):

    id:int

    name:str

    code:str

    credits:int

    department_id:int


class DepartmentResponse(BaseModel):

    id:int

    name:str

    courses:list[CourseResponse]=[]



@app.post("/api/courses/")

async def create_course(
    course:CourseCreate
):

    return course


@app.post("/api/courses/")

async def create_course(
    course:CourseCreate
):

    return course



from typing import Optional

@app.get("/api/courses/")

async def get_courses(

skip:int=0,

limit:int=10,

department_id:Optional[int]=None

):

    return {

        "skip":skip,

        "limit":limit,

        "department":department_id

    }



from fastapi import Depends

async def get_db():

    db = Session()

    try:

        yield db

    finally:

        db.close()



@app.get("/courses")

async def courses(

db=Depends(get_db)

):

    return []




result = await db.execute(
select(Course)
)

courses = result.scalars().all()

await db.commit()