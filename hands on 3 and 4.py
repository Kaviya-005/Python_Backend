pip install djangorestframework


INSTALLED_APPS = [
    ...
    "rest_framework",
]


from rest_framework import serializers
from .models import *

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = "__all__"


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Course
from .serializers import CourseSerializer

class CourseListView(APIView):

    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)



class CourseDetailView(APIView):

    def get(self, request, pk):
        course = Course.objects.get(pk=pk)
        return Response(CourseSerializer(course).data)

    def put(self, request, pk):
        course = Course.objects.get(pk=pk)
        serializer = CourseSerializer(course, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        Course.objects.get(pk=pk).delete()
        return Response(status=204)



from django.urls import path
from .views import *

urlpatterns = [
    path("courses/", CourseListView.as_view()),
    path("courses/<int:pk>/", CourseDetailView.as_view()),
]



from rest_framework import viewsets
from .models import Course
from .serializers import CourseSerializer

class CourseViewSet(viewsets.ModelViewSet):

    queryset = Course.objects.all()

    serializer_class = CourseSerializer



from rest_framework.decorators import action

class CourseViewSet(viewsets.ModelViewSet):

    queryset = Course.objects.all()

    serializer_class = CourseSerializer

    @action(detail=True, methods=["get"])

    def students(self, request, pk=None):

        course = self.get_object()

        students = Student.objects.filter(
            enrollment__course=course
        )

        serializer = StudentSerializer(
            students,
            many=True
        )

        return Response(serializer.data)



//hands on 4


from flask import Flask
from config import Config
from courses.routes import courses_bp

def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    app.register_blueprint(courses_bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run()



class Config:

    SECRET_KEY = "secret"

    DEBUG = True

    SQLALCHEMY_DATABASE_URI = "sqlite:///courses.db"



from flask import Blueprint

courses_bp = Blueprint(
    "courses",
    __name__,
    url_prefix="/api/courses"
)




from flask import request, jsonify

courses = []

@courses_bp.route("/", methods=["GET"])

def get_courses():

    return jsonify(courses)


@courses_bp.route("/", methods=["POST"])

def add_course():

    data = request.get_json()

    if not all(k in data for k in ("name","code","credits")):

        return jsonify({"error":"Missing fields"}),400

    courses.append(data)

    return jsonify(data),201



@courses_bp.route("/<int:id>", methods=["GET"])
def get_course(id):
    return jsonify({"id":id})

@courses_bp.route("/<int:id>", methods=["PUT"])
def update_course(id):
    return jsonify({"message":"Updated"})

@courses_bp.route("/<int:id>", methods=["DELETE"])
def delete_course(id):
    return jsonify({"message":"Deleted"})



from flask import jsonify

def make_response_json(data,status):

    return jsonify({

        "status":"success",

        "data":data

    }),status




@app.errorhandler(404)

def not_found(error):

    return jsonify({

        "error":"Not Found"

    }),404


@app.errorhandler(500)

def server_error(error):

    return jsonify({

        "error":"Internal Server Error"

    }),500


