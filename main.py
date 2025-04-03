
from typing import Optional
from fastapi import FastAPI, File, Path, UploadFile, HTTPException
from pydantic import BaseModel
from fastapi.responses import FileResponse
from typing import Literal
import os


app = FastAPI()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True) 



@app.post("/upload/")
async def upload_file(file: UploadFile = File()):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as f:
        while chunk := await file.read(1024 * 1024):  
            f.write(chunk)

    return {"filename": file.filename, "location": file_path}

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(file_path):
        return {"error": "File not found"}

    return FileResponse(file_path, media_type="application/pdf", filename=filename)

students = {
    1:{"name":"shruthi",
        "age":"17",
        "year":"12"
       }
}

class Student(BaseModel):
      name: str
      age : int
      year : str


class update_student(BaseModel):
      name: Optional[str]=None
      age: Optional[int]=None
      year: Optional[str]=None      

@app.get("/")
def index():
    return {"name": "First Data"}

@app.get("/get-student/{student_id}")
def get_student(student_id: int = Path(..., description="The ID of the student you want to view")):
        return students[student_id]

@app.get("/student-by-name/{student_id}")        
def get_student(*,student_id: int ,name: str):
      for student_id in students:
           if students[student_id]["name"] == name:
                return students[student_id]
      return{"data":"not found"}

@app.post("/create-student/{student_id}", response_model=Student)
async def create_student(student_id: int , student: Student):
      if student_id in students:
            return{"error": "student exist"}
      
      students[student_id]=student
      return students[student_id]
            

@app.put("/update-student/{student_id}")
def update_student(student_id: int , student: update_student):
      if student_id not in students:
            return {"error":"invalid"}
      

      if student.name != None:
            students[student_id].name = student.name

      if student.age != None:
            students[student_id].age = student.age

      if student.year != None:
            students[student_id].year = student.year

            return students[student_id]           
      
@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
      if Student not in students:
            raise HTTPException (status_code=404, detail="student not found") 
      

      del students[student_id]
      return{"message":"student deleted successfully"}
      

student={
     "poo":{"name":"poo"},
     "foo":{"name":"foo", "age":"12"},
     "soo":{"name":"soo", "age": None, "year": "9 years"},
}


@app.get("/student/{student_id}", response_model_exclude_unset=True)
async def read_student(student_id: Literal["poo", "foo", "soo"]):
         return student[student_id]

@app.get("/student/{student_id}/name", response_model_include={"name", "age"})
async def read_student_name(student_id: Literal["poo", "foo", "soo"]):
         return student[student_id]

@app.get("/student/{student_id}/public", response_model_exclude={"year"})
async def read_student(student_id: Literal["poo", "foo", "soo"]):
         return student[student_id]
