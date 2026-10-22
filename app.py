import streamlit as st
import random
import os
import json

# ==========================================
# ADMIN CONFIGURATION (Change these as you like)
# ==========================================
ADMIN_USERNAME = "OwnerP"      # Change to your desired admin username
ADMIN_PASSWORD = "Pratik1106"   # Change to your desired admin password


# --- AUTHENTICATION & ROLE MANAGEMENT (UNIT V) ---
TEACHER_FILE = "teachers.txt"

def load_teachers():
    # Load default admin + any registered teachers
    teachers = {ADMIN_USERNAME: ADMIN_PASSWORD}
    if os.path.exists(TEACHER_FILE):
        try:
            with open(TEACHER_FILE, "r") as file:
                for line in file:
                    parts = line.strip().split(",")
                    if len(parts) == 2:
                        teachers[parts[0]] = parts[1]
        except Exception:
            pass
    else:
        save_teachers_to_file(teachers)
    return teachers

def save_teachers_to_file(teachers_dict):
    try:
        with open(TEACHER_FILE, "w") as file:
            for uname, pwd in teachers_dict.items():
                file.write(f"{uname},{pwd}\n")
    except IOError as e:
        st.error(f"Error saving teacher accounts: {e}")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "current_user" not in st.session_state:
    st.session_state.current_user = ""

# --- LOGIN & SIGN-UP PORTAL SCREEN ---
if not st.session_state.authenticated:
    st.set_page_config(page_title="Teacher Portal - Authentication", page_icon="🔐")
    st.title("🔐 Teacher Portal Authentication")
    st.markdown("Please log in or sign up for a new teacher account to manage student records.")
    
    auth_mode = st.radio("Select Option", ["Login", "Sign Up (Register)"], horizontal=True)
    teachers_db = load_teachers()
    
    if auth_mode == "Login":
        st.subheader("Teacher Login")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_btn = st.form_submit_button("Login")
            
            if login_btn:
                if username in teachers_db and teachers_db[username] == password:
                    st.session_state.authenticated = True
                    st.session_state.current_user = username
                    st.success("Login successful! Loading dashboard...")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
    else:
        st.subheader("Teacher Registration (Sign Up)")
        with st.form("signup_form"):
            new_user = st.text_input("Choose Username")
            new_pass = st.text_input("Choose Password", type="password")
            confirm_pass = st.text_input("Confirm Password", type="password")
            signup_btn = st.form_submit_button("Register Account")
            
            if signup_btn:
                if not new_user.strip() or not new_pass.strip():
                    st.warning("Please fill in all fields.")
                elif new_pass != confirm_pass:
                    st.error("Passwords do not match!")
                elif new_user in teachers_db or new_user == ADMIN_USERNAME:
                    st.error("Username already exists! Please choose another or log in.")
                else:
                    teachers_db[new_user.strip()] = new_pass.strip()
                    save_teachers_to_file(teachers_db)
                    st.success("Registration successful! You can now switch to 'Login' above.")
    st.stop()


# --- SYLLABUS UNIT IV: OOPs Concepts (Inheritance & Data Hiding) ---
class Person:
    def __init__(self, name, age):
        self._name = name      
        self._age = age        

class Student(Person):
    def __init__(self, student_id, name, age, subjects_dict):
        super().__init__(name, age)
        self.__student_id = student_id  
        self.__subjects = subjects_dict  # Dictionary of subject-wise marks

    def get_student_id(self):
        return self.__student_id

    def set_name(self, name):
        self._name = name

    def set_age(self, age):
        self._age = age

    def set_subjects(self, subjects_dict):
        self.__subjects = subjects_dict

    def get_name(self):
        return self._name

    def get_age(self):
        return self._age

    def get_subjects(self):
        return self.__subjects

    def get_total_marks(self):
        return sum(self.__subjects.values())

    def get_percentage(self):
        total_max = len(self.__subjects) * 100
        return round((self.get_total_marks() / total_max) * 100, 2) if total_max > 0 else 0.0

    def to_file_format(self):
        subj_json = json.dumps(self.__subjects)
        return f"{self.__student_id},{self._name},{self._age},{subj_json}\n"


# --- SYLLABUS UNIT V: Text Files & File Management ---
SUBJECT_FILE = "subjects.txt"
STUDENT_FILE = "students_v3.txt"

def load_subjects():
    default_subjects = ["Python Programming", "Data Structures", "Digital Logic", "Mathematics"]
    if os.path.exists(SUBJECT_FILE):
        try:
            with open(SUBJECT_FILE, "r") as file:
                subs = [line.strip() for line in file if line.strip()]
                return subs if subs else default_subjects
        except Exception:
            return default_subjects
    else:
        save_subjects(default_subjects)
        return default_subjects

def save_subjects(subjects_list):
    try:
        with open(SUBJECT_FILE, "w") as file:
            for sub in subjects_list:
                file.write(f"{sub}\n")
    except IOError as e:
        st.error(f"Error saving subjects: {e}")

def load_records():
    students = []
    if os.path.exists(STUDENT_FILE):
        try:
            with open(STUDENT_FILE, "r") as file:
                for line in file:
                    parts = line.strip().split(",", 3)
                    if len(parts) == 4:
                        s_id, name, age, subj_json = int(parts[0]), parts[1], int(parts[2]), parts[3]
                        subjects = json.loads(subj_json)
                        students.append(Student(s_id, name, age, subjects))
        except Exception as e:
            st.error(f"Error reading records file: {e}")
    return students

def save_records(students):
    try:
        with open(STUDENT_FILE, "w") as file:
            for student in students:
                file.write(student.to_file_format())
    except IOError as e:
        st.error(f"Failed to write to file: {e}")


# --- INITIALIZE SESSION STATE ---
if "subjects" not in st.session_state:
    st.session_state.subjects = load_subjects()
if "students" not in st.session_state:
    st.session_state.students = load_records()


# --- STREAMLIT DASHBOARD UI ---
is_admin = (st.session_state.current_user == ADMIN_USERNAME)

st.title("🎓 Student Record Management System")
role_label = "Administrator (Admin)" if is_admin else f"Teacher ({st.session_state.current_user})"
st.markdown(f"*Logged in as: **{role_label}** | B.Tech Computer Science Mini-Project*")
st.divider()

# Build dynamic sidebar navigation based on role
nav_options = [
    "➕ Add Student & Marks", 
    "📋 View All Records", 
    "✏️ Edit Student Record",
    "📚 Manage Subjects",
    "🔍 Search by ID (Linear Search)", 
    "⭐ Filter High Achievers (Lambda)"
]

# Insert 'Manage Teachers' option exclusively for the Admin
if is_admin:
    nav_options.insert(4, "👥 Manage Teachers")

st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", nav_options)

st.sidebar.divider()
if st.sidebar.button("🔒 Logout"):
    st.session_state.authenticated = False
    st.session_state.current_user = ""
    st.rerun()


# --- OPTION 1: ADD STUDENT ---
if menu == "➕ Add Student & Marks":
    st.subheader("Register New Student & Subject Marks")
    
    if "suggested_id" not in st.session_state:
        st.session_state.suggested_id = random.randint(1001, 9999)

    current_subjects = st.session_state.subjects
    if not current_subjects:
        st.warning("Please add subjects first in the 'Manage Subjects' menu!")
    else:
        with st.form("add_form"):
            s_id = st.number_input("Student ID", min_value=1, value=st.session_state.suggested_id)
            name = st.text_input("Full Name")
            age = st.number_input("Age", min_value=17, max_value=100, value=20)
            
            st.markdown(f"### Enter Marks (Out of 100) for {len(current_subjects)} Subjects")
            subject_marks = {}
            
            cols = st.columns(2)
            for idx, sub in enumerate(current_subjects):
                with cols[idx % 2]:
                    subject_marks[sub] = st.number_input(f"{sub}", 0.0, 100.0, 75.0, key=f"add_{sub}")
            
            submitted = st.form_submit_button("Save Student Record")
            if submitted:
                if name.strip() == "":
                    st.warning("Please enter a valid student name.")
                else:
                    new_student = Student(int(s_id), name, int(age), subject_marks)
                    st.session_state.students.append(new_student)
                    save_records(st.session_state.students)
                    st.success(f"Successfully added record for {name}!")
                    st.session_state.suggested_id = random.randint(1001, 9999)


# --- OPTION 2: VIEW RECORDS ---
elif menu == "📋 View All Records":
    st.subheader("All Student Records & Performance Summary")
    
    if not st.session_state.students:
        st.info("No student records found yet. Add some students first!")
    else:
        data = []
        for s in st.session_state.students:
            record = {
                "ID": s.get_student_id(),
                "Name": s.get_name(),
                "Age": s.get_age()
            }
            for sub, mark in s.get_subjects().items():
                record[sub] = mark
            record["Total Marks"] = s.get_total_marks()
            record["Percentage (%)"] = f"{s.get_percentage()}%"
            data.append(record)
            
        st.dataframe(data, use_container_width=True)


# --- OPTION 3: EDIT STUDENT RECORD ---
elif menu == "✏️ Edit Student Record":
    st.subheader("Edit Existing Student Details & Marks")
    
    if not st.session_state.students:
        st.info("No records available to edit.")
    else:
        student_ids = [s.get_student_id() for s in st.session_state.students]
        selected_id = st.selectbox("Select Student ID to Edit", student_ids)
        
        target_student = next((s for s in st.session_state.students if s.get_student_id() == selected_id), None)
        
        if target_student:
            with st.form("edit_form"):
                new_name = st.text_input("Full Name", value=target_student.get_name())
                new_age = st.number_input("Age", min_value=17, max_value=100, value=target_student.get_age())
                
                st.markdown("### Update Subject Marks")
                current_subs = target_student.get_subjects()
                updated_marks = {}
                
                for sub in st.session_state.subjects:
                    default_val = current_subs.get(sub, 50.0)
                    updated_marks[sub] = st.number_input(f"{sub}", 0.0, 100.0, float(default_val), key=f"edit_{sub}")
                
                update_btn = st.form_submit_button("Update Record")
                if update_btn:
                    target_student.set_name(new_name)
                    target_student.set_age(int(new_age))
                    target_student.set_subjects(updated_marks)
                    save_records(st.session_state.students)
                    st.success(f"Successfully updated record for ID {selected_id}!")


# --- OPTION 4: MANAGE SUBJECTS ---
elif menu == "📚 Manage Subjects":
    st.subheader("Add or Remove Subjects")
    
    st.write("Current Subjects in Syllabus:")
    for sub in st.session_state.subjects:
        st.markdown(f"- **{sub}**")
        
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Add New Subject")
        new_sub = st.text_input("Subject Name")
        if st.button("Add Subject"):
            if new_sub.strip() == "":
                st.warning("Subject name cannot be empty.")
            elif new_sub in st.session_state.subjects:
                st.error("Subject already exists!")
            else:
                st.session_state.subjects.append(new_sub.strip())
                save_subjects(st.session_state.subjects)
                st.success(f"Added subject: {new_sub}")
                st.rerun()
                
    with col2:
        st.markdown("### Remove Subject")
        sub_to_remove = st.selectbox("Select Subject to Remove", st.session_state.subjects)
        if st.button("Remove Subject"):
            if len(st.session_state.subjects) <= 1:
                st.error("You must keep at least one subject!")
            else:
                st.session_state.subjects.remove(sub_to_remove)
                save_subjects(st.session_state.subjects)
                for s in st.session_state.students:
                    subs = s.get_subjects()
                    if sub_to_remove in subs:
                        del subs[sub_to_remove]
                        s.set_subjects(subs)
                save_records(st.session_state.students)
                st.success(f"Removed subject: {sub_to_remove}")
                st.rerun()


# --- OPTION 5: MANAGE TEACHERS (ADMIN ONLY) ---
elif menu == "👥 Manage Teachers":
    if not is_admin:
        st.error("Access Denied: Only the Administrator can manage teachers.")
    else:
        st.subheader("Admin Panel: Manage Teacher Accounts")
        
        teachers_db = load_teachers()
        st.write(f"Total Registered Accounts: **{len(teachers_db)}**")
        
        for uname in teachers_db.keys():
            st.markdown(f"- **{uname}**")
            
        st.divider()
        st.markdown("### Delete Teacher Account")
        deletable_teachers = [u for u in teachers_db.keys() if u != ADMIN_USERNAME]
        
        if not deletable_teachers:
            st.info("No removable teacher accounts found (Admin account cannot be deleted).")
        else:
            teacher_to_delete = st.selectbox("Select Teacher Username to Delete", deletable_teachers)
            if st.button("Delete Selected Account"):
                del teachers_db[teacher_to_delete]
                save_teachers_to_file(teachers_db)
                st.success(f"Successfully deleted teacher account: {teacher_to_delete}")
                st.rerun()


# --- OPTION 6: SEARCH STUDENT (UNIT III) ---
elif menu == "🔍 Search by ID (Linear Search)":
    st.subheader("Search Student Record via Linear Search Algorithm")
    
    target_id = st.number_input("Enter Student ID to Search", min_value=1, value=1001)
    
    if st.button("Search"):
        found_student = None
        for student in st.session_state.students:
            if student.get_student_id() == target_id:
                found_student = student
                break
        
        if found_student:
            st.success("Record Found!")
            col1, col2, col3 = st.columns(3)
            col1.metric("Student Name", found_student.get_name())
            col2.metric("Total Marks", f"{found_student.get_total_marks()} / {len(found_student.get_subjects()) * 100}")
            col3.metric("Percentage", f"{found_student.get_percentage()}%")
            
            st.write("**Subject-wise Breakdown:**")
            st.json(found_student.get_subjects())
        else:
            st.error("Student with this ID does not exist.")


# --- OPTION 7: FILTER HIGH ACHIEVERS (UNIT IV) ---
elif menu == "⭐ Filter High Achievers (Lambda)":
    st.subheader("Filter Top Students Based on Percentage")
    
    threshold = st.slider("Minimum Percentage Threshold (%)", 0.0, 100.0, 75.0)
    
    if st.button("Filter"):
        is_high_achiever = lambda s: s.get_percentage() >= threshold
        filtered = [s for s in st.session_state.students if is_high_achiever(s)]
        
        if filtered:
            st.write(f"Found **{len(filtered)}** students scoring $\ge$ {threshold}%:")
            filtered_data = []
            for s in filtered:
                filtered_data.append({
                    "ID": s.get_student_id(),
                    "Name": s.get_name(),
                    "Total Marks": s.get_total_marks(),
                    "Percentage (%)": f"{s.get_percentage()}%"
                })
            st.table(filtered_data)
        else:
            st.warning("No students meet this criteria.")
