from fastapi import FastAPI, HTTPException, status

@app.get("/api/courses/{id}", response_model=CourseResponse)

async def get_course(id:int):
    return {"id":id,"name":"Python","code":"CS101","credits":4}


@app.post(
    "/api/courses/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED
)

async def create_course(course:CourseCreate):

    return {
        "id":1,
        **course.dict()
    }



@app.put("/api/courses/{id}")

async def update_course(id:int, course:CourseUpdate):

    if id != 1:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return {"message":"Updated"}


@app.delete(
"/api/courses/{id}",
status_code=status.HTTP_204_NO_CONTENT
)

async def delete_course(id:int):

    return




from fastapi import HTTPException

raise HTTPException(
    status_code=404,
    detail="Course not found"
)




@app.get("/api/courses/{id}/students")

async def get_students(id:int):

    return [
        {"id":1,"name":"John"},
        {"id":2,"name":"Alice"}
    ]



from fastapi import BackgroundTasks

def send_confirmation_email(email:str):

    print(f"Sending confirmation to {email}")


@app.post("/api/enrollments/")

async def enroll(

background_tasks:BackgroundTasks

):

    background_tasks.add_task(
        send_confirmation_email,
        "student@gmail.com"
    )

    return {
        "message":"Enrollment Successful"
    }



app = FastAPI(

title="Course Management API",

description="Course API using FastAPI",

version="1.0",

contact={
"name":"Admin",
"email":"admin@gmail.com"
}

)



//hands on 8


@app.patch("/api/v1/courses/{id}")

async def patch_course(

id:int,

course:CourseUpdate

):

    return {
        "message":"Partially Updated"
    }



from fastapi import Response

@app.post("/api/v1/courses/")

async def create_course(

response:Response,

course:CourseCreate

):

    response.headers["Location"]="/api/v1/courses/1"

    return {
        "id":1
    }




@app.get("/api/v1/courses/")

async def get_courses(

page:int=1,

page_size:int=2

):

    return {

        "count":10,

        "next":"/api/v1/courses/?page=2",

        "previous":None,

        "results":[]

    }




@app.get("/api/v1/courses/")

async def search_courses(

search:str=""

):

    return {

        "search":search

    }



from fastapi import HTTPException

raise HTTPException(

status_code=404,

detail={

"error":{

"code":"NOT_FOUND",

"message":"Course not found",

"field":None

}

}

)