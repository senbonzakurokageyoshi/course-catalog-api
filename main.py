from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from data import find_course, get_all_courses
from models import Course, Enrollment, EnrollmentIn

app = FastAPI(title="Course Catalog API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Course Catalog API is running"}


def pagination(page: int = 1, page_size: int = 20):
    return {"offset": (page - 1) * page_size, "limit": page_size}


@app.get("/courses", response_model=list[Course])
def list_courses(
    is_elective: bool | None = None,
    sort: str = "popular",
    p: dict = Depends(pagination),
):
    courses = get_all_courses()
    if is_elective is not None:
        courses = [c for c in courses if c.is_elective == is_elective]
    if sort == "popular":
        courses.sort(key=lambda c: c.likes, reverse=True)
    else:
        courses.sort(key=lambda c: c.title)
    return courses[p["offset"] : p["offset"] + p["limit"]]


@app.get("/courses/{course_id}", response_model=Course)
def get_course(course_id: str):
    course = find_course(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@app.post("/courses/{course_id}/like", response_model=Course)
def like_course(course_id: str):
    course = find_course(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    course.likes += 1
    return course


ENROLLMENTS: list[Enrollment] = []


@app.post("/enrollments", response_model=Enrollment, status_code=201)
def create_enrollment(data: EnrollmentIn):
    if not find_course(data.course_id):
        raise HTTPException(status_code=404, detail="Course not found")
    enrollment = Enrollment(
        id=len(ENROLLMENTS) + 1,
        course_id=data.course_id,
        student_name=data.student_name,
    )
    ENROLLMENTS.append(enrollment)
    return enrollment


@app.get("/enrollments", response_model=list[Enrollment])
def list_enrollments():
    return ENROLLMENTS
