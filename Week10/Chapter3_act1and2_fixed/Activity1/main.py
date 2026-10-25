import pymongo
from pymongo import MongoClient
import sys

# Constants
MONGO_URI = "mongodb://root:kongbeng@localhost:27017/"
DB_NAME = "student_db"
COLLECTION_NAME = "students"

def connect_db():
    try:
        client = MongoClient(MONGO_URI)
        # Check connection
        client.admin.command('ping')
        print("Connected to MongoDB successfully!")
        return client[DB_NAME][COLLECTION_NAME]
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        sys.exit(1)

# --- Task 2: Create (Insert Data) ---

def create_student(collection):
    print("\n--- Add New Student ---")
    student_id = input("Enter Student ID (e.g., S001): ").strip()
    
    # --- Answer Start: Check validation and insert document ---
    if collection.find_one({"student_id": student_id}):
        print(f"Error: Student with ID {student_id} already exists!")
        return None
    
    name = input("Enter Name: ").strip()
    age = int(input("Enter Age: "))
    department = input("Enter Department: ").strip()
    gpa = float(input("Enter GPA: "))
    
    # Input courses as comma-separated list
    courses_input = input("Enter Courses (comma separated): ")
    courses = [c.strip() for c in courses_input.split(",") if c.strip()]

    student_doc = {
        "student_id": student_id,
        "name": name,
        "age": age,
        "department": department,
        "gpa": gpa,
        "courses": courses
    }
    
    try:
        result = collection.insert_one(student_doc)
        print(f"Student inserted successfully with _id: {result.inserted_id}")
        return result.inserted_id
    except Exception as e:
        print(f"Error inserting student: {e}")
        return None
    # --- Answer End ---

# --- Task 3: Read (Get by ID) ---

def get_student_by_id(collection):
    print("\n--- Get Student by ID ---")
    student_id = input("Enter Student ID: ").strip()
    
    # --- Answer Start: Find One document ---
    s = collection.find_one({"student_id": student_id})
    if s:
        print(f"Found: ID: {s['student_id']}, Name: {s['name']}, Dept: {s['department']}, GPA: {s['gpa']}, Courses: {s['courses']}")
    else:
        print("Student not found.")
    return s
    # --- Answer End ---

def get_all_students(collection):
    print("\n--- All Students ---")
    # --- Answer Start: Fetch all documents ---
    students = list(collection.find())
    if not students:
        print("No students found.")
    for s in students:
        print(f"ID: {s['student_id']}, Name: {s['name']}, Dept: {s['department']}, GPA: {s['gpa']}, Courses: {s['courses']}")
    return students
    # --- Answer End ---

def search_by_gpa(collection):
    print("\n--- Search by GPA ---")
    try:
        min_gpa = float(input("Enter minimum GPA: "))
        # --- Answer Start: Filter by GPA ---
        students = list(collection.find({"gpa": {"$gte": min_gpa}}))
        if not students:
            print(f"No students found with GPA >= {min_gpa}")
        for s in students:
            print(f"ID: {s['student_id']}, Name: {s['name']}, GPA: {s['gpa']}")
        return students
        # --- Answer End ---
    except ValueError:
        print("Invalid GPA input.")

# --- Task 4: Update ---

def update_student(collection):
    print("\n--- Update Student ---")
    student_id = input("Enter Student ID to update: ").strip()
    
    # --- Answer Start: Update document ($set or $push) ---
    if not collection.find_one({"student_id": student_id}):
        print("Student not found.")
        return
    
    print("1. Update GPA")
    print("2. Add Course")
    choice = input("Choose option: ")

    if choice == "1":
        new_gpa = float(input("Enter new GPA: "))
        collection.update_one({"student_id": student_id}, {"$set": {"gpa": new_gpa}})
        print("GPA updated successfully.")
    elif choice == "2":
        new_course = input("Enter new course name: ").strip()
        collection.update_one({"student_id": student_id}, {"$push": {"courses": new_course}})
        print("Course added successfully.")
    else:
        print("Invalid option.")
    # --- Answer End ---

# --- Task 5: Delete ---

def delete_student(collection):
    print("\n--- Delete Student ---")
    student_id = input("Enter Student ID to delete: ").strip()
    
    # --- Answer Start: Delete document ---
    result = collection.delete_one({"student_id": student_id})
    if result.deleted_count > 0:
        print("Student deleted successfully.")
    else:
        print("Student not found.")
    # --- Answer End ---

def clear_all_data(collection):
    print("\n--- Clear All Data ---")
    confirm = input("Are you sure you want to delete ALL students? (yes/no): ").strip().lower()
    if confirm == 'yes':
        result = collection.delete_many({})
        print(f"Deleted {result.deleted_count} students.")
    else:
        print("Operation cancelled.")

# --- Task 3: Read (Advanced Search) ---

def advanced_search(collection):
    print("\n--- Advanced Search ---")
    print("1. Find by Department AND Minimum GPA ($and)")
    print("2. Find by Department A OR Department B ($or)")
    choice = input("Choose option: ")
    
    # --- Answer Start: Advanced Logic with $and / $or ---
    if choice == '1':
        dept = input("Enter Department: ").strip()
        min_gpa = float(input("Enter minimum GPA: "))
        students = list(collection.find({"$and": [
            {"department": dept},
            {"gpa": {"$gte": min_gpa}}
        ]}))
        print(f"\nFound {len(students)} students in {dept} with GPA >= {min_gpa}:")
        for s in students:
            print(f"- {s['name']} (GPA: {s['gpa']})")
    elif choice == '2':
        dept1 = input("Enter Department 1: ").strip()
        dept2 = input("Enter Department 2: ").strip()
        students = list(collection.find({"$or": [
            {"department": dept1},
            {"department": dept2}
        ]}))
        print(f"\nFound {len(students)} students in {dept1} OR {dept2}:")
        for s in students:
            print(f"- {s['name']} (Dept: {s['department']})")
    else:
        print("Invalid option")
    # --- Answer End ---

def main():
    collection = connect_db()
    
    while True:
        print("\n=== Student Management System ===")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search by ID")
        print("4. Search by GPA")
        print("5. Update Student")
        print("6. Delete Student")
        print("7. Clear All Data")
        print("8. Advanced Search (AND/OR)")
        print("9. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            create_student(collection)
        elif choice == '2':
            get_all_students(collection)
        elif choice == '3':
            get_student_by_id(collection)
        elif choice == '4':
            search_by_gpa(collection)
        elif choice == '5':
            update_student(collection)
        elif choice == '6':
            delete_student(collection)
        elif choice == '7':
            clear_all_data(collection)
        elif choice == '8':
            advanced_search(collection)
        elif choice == '9':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()