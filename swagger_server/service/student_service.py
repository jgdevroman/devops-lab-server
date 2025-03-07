import os
from pymongo import MongoClient
from bson.objectid import ObjectId

# MongoDB connection
client = MongoClient(os.getenv('MONGO_URI', 'mongodb://localhost:27017/'))
db = client['student_db']
students = db['students']


def add(student=None):
    if students.find_one({"first_name": student.first_name, "last_name": student.last_name}):
        return 'already exists', 409

    result = students.insert_one(student.to_dict())
    student.student_id = str(result.inserted_id)
    return student.student_id


def get_by_id(student_id=None):
    student = students.find_one({"_id": ObjectId(student_id)})
    if not student:
        logging.debug(f"Student with ID {student_id} not found")
        return 'not found', 404
    student['student_id'] = student_id
    print(student)
    return student


def delete(student_id=None):
    result = students.delete_one({"_id": ObjectId(student_id)})
    if result.deleted_count == 0:
        return 'not found', 404
    return student_id