import streamlit as st
import random
import os

# --- AUTHENTICATION CONFIGURATION ---
# Default teacher credentials
TEACHER_USER = "teacher"
TEACHER_PASS = "admin123"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# --- LOGIN PORTAL SCREEN ---
if not st.session_state.authenticated:
    st.set_page_config(page_title="Teacher Login - Student Portal", page_icon="🔐")
    st.title("🔐 Teacher Login Portal")
    st.markdown("Please enter your credentials to access and manage student records.")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_btn = st.form_submit_button("Login")
        
        if login_btn:
            if username == TEACHER_USER and password == TEACHER_PASS:
                st.session_state.authenticated = True
                st.success("Login successful! Loading dashboard...")
                st.rerun()
            else:
                st.error("Invalid username or password. (Hint: teacher / admin123)")
    st.stop()  # Stop execution here until authenticated


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
        # Format: id,name,age,python,ds,digital_logic,math
        subj_values = ",".join(str(v) for v in self.__subjects.values())
        return f"{self.__student_id},{self._name},{self._age},{subj_values}\n"


# --- SYLLABUS UNIT V: Text Files & Exception Handling ---
FILENAME = "students_v2.txt"

def load_records():
    students = []
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r") as file:
                for line in file:
                    parts = line.strip().split(",")
                    if len(parts) >= 7:
                        s_id, name, age = int(parts[0]), parts[1], int(parts[2])
                        subjects = {
                            "Python": float(parts[3]),
                            "Data Structures": float(parts[4]),
                            "Digital Logic": float(parts[5]),
                            "Mathematics": float(parts[6])
                        }
                        students.append(Student(s_id, name, age, subjects))
        except Exception as e:
            st.error(f"Error reading file: {e}")
    return students

def save_records(students):
    try:
        with open(FILENAME, "w") as file:
            for student in students:
                file.write(student.to_file_format())
    except IOError as e:
        st.error(f"Failed to write to file: {e}")


# --- INITIALIZE SESSION STATE ---
if "students" not in st.session_state:
    st.session_state.students = load_records()


# --- STREAMLIT DASHBOARD UI ---
st.title("🎓 Student Record Management System")
st.markdown("*B.Tech Computer Science Mini-Project | Teacher Dashboard*")
st.divider()

# Sidebar Navigation & Logout
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", [
    "➕ Add Student & Marks", 
    "📋 View All Records", 
    "🔍 Search by ID (Linear Search)", 
    "⭐ Filter High Achievers (Lambda)"
])

st.sidebar.divider()
if st.sidebar.button("🔒 Logout"):
    st.session_state.authenticated = False
    st.rerun()


# --- OPTION 1: ADD STUDENT ---
if menu == "➕ Add Student & Marks":
    st.subheader("Register New Student & Subject-wise Marks")
    
    if "suggested_id" not in st.session_state:
        st.session_state.suggested_id = random.randint(1001, 9999)

    with st.form("add_form"):
        s_id = st.number_input("Student ID", min_value=1, value=st.session_state.suggested_id)
        name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=17, max_value=100, value=20)
        
        st.markdown("### Enter Marks (Out of 100)")
        col1, col2 = st.columns(2)
        with col1:
            m_python = st.number_input("Python Programming", 0.0, 100.0, 80.0)
            m_ds = st.number_input("Data Structures", 0.0, 100.0, 75.0)
        with col2:
            m_dl = st.number_input("Digital Logic", 0.0, 100.0, 85.0)
            m_math = st.number_input("Mathematics", 0.0, 100.0, 90.0)
        
        submitted = st.form_submit_button("Save Student Record")
        if submitted:
            if name.strip() == "":
                st.warning("Please enter a valid student name.")
            else:
                subjects = {
                    "Python": m_python,
                    "Data Structures": m_ds,
                    "Digital Logic": m_dl,
                    "Mathematics": m_math
                }
                new_student = Student(int(s_id), name, int(age), subjects)
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
            subj = s.get_subjects()
            data.append({
                "ID": s.get_student_id(),
                "Name": s.get_name(),
                "Age": s.get_age(),
                "Python": subj["Python"],
                "Data Structures": subj["Data Structures"],
                "Digital Logic": subj["Digital Logic"],
                "Mathematics": subj["Mathematics"],
                "Total Marks": s.get_total_marks(),
                "Percentage (%)": f"{s.get_percentage()}%"
            })
        st.dataframe(data, use_container_width=True)


# --- OPTION 3: SEARCH STUDENT (UNIT III) ---
elif menu == "🔍 Search by ID (Linear Search)":
    st.subheader("Search Student Record via Linear Search Algorithm")
    
    target_id = st.number_input("Enter Student ID to Search", min_value=1, value=1001)
    
    if st.button("Search"):
        found_student = None
        # Linear Search Implementation (Unit III)
        for student in st.session_state.students:
            if student.get_student_id() == target_id:
                found_student = student
                break
        
        if found_student:
            st.success("Record Found!")
            subj = found_student.get_subjects()
            col1, col2, col3 = st.columns(3)
            col1.metric("Student Name", found_student.get_name())
            col2.metric("Total Marks", f"{found_student.get_total_marks()} / 400")
            col3.metric("Percentage", f"{found_student.get_percentage()}%")
            
            st.write("**Subject-wise Breakdown:**")
            st.json(subj)
        else:
            st.error("Student with this ID does not exist.")


# --- OPTION 4: FILTER HIGH ACHIEVERS (UNIT IV) ---
elif menu == "⭐ Filter High Achievers (Lambda)":
    st.subheader("Filter Top Students Based on Percentage")
    
    threshold = st.slider("Minimum Percentage Threshold (%)", 0.0, 100.0, 75.0)
    
    if st.button("Filter"):
        # Unit IV: Lambda Function and List Comprehension using percentage
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
