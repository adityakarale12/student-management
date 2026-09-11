import os
from pathlib import Path

from dotenv import load_dotenv
from supabase import create_client
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL or SUPABASE_KEY is missing from .env")


supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Student(BaseModel):
    name: str
    course: str
    marks: int


@app.get("/")
def home():
    return {
        "message": "Student Management API is running"
    }


@app.post("/students")
def create_student(student: Student):

    data = {
        "name": student.name,
        "course": student.course,
        "marks": student.marks
    }

    response = (
        supabase
        .table("student-management")
        .insert(data)
        .execute()
    )

    return {
        "message": "Student created successfully",
        "data": response.data
    }


@app.get("/students")
def get_students():

    response = (
        supabase
        .table("student-management")
        .select("*")
        .execute()
    )

    return {
        "data": response.data
    }


@app.get("/students/{student_id}")
def get_student(student_id: int):

    response = (
        supabase
        .table("student-management")
        .select("*")
        .eq("id", student_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {
        "data": response.data[0]
    }


@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):

    data = {
        "name": student.name,
        "course": student.course,
        "marks": student.marks
    }

    response = (
        supabase
        .table("student-management")
        .update(data)
        .eq("id", student_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {
        "message": "Student updated successfully",
        "data": response.data
    }


@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    response = (
        supabase
        .table("student-management")
        .delete()
        .eq("id", student_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {
        "message": "Student deleted successfully",
        "data": response.data
    }