import streamlit as st
import pandas as pd
import random

if "students" and "classes" not in st.session_state:
    st.session_state.students = []
    st.session_state.classes = []


# ------------------------------------------
# Create Student
# ------------------------------------------
def create_student(name, father_name, email, _class, password):

    if _class not in st.session_state.classes:
        return "Invalid Class"

    student = {
        "id": random.randint(100000, 999999),
        "name": name,
        "father_name": father_name,
        "email": email,
        "class": _class,
        "password": password,
    }
    st.session_state.students.append(student)
    return student


# ------------------------------------------
# List Student
# ------------------------------------------
def students_list():
    # Check if the students list exists and is not empty
    if "students" in st.session_state and st.session_state.students:

        # Flatten the data so the nested "class" dictionary looks clean in the table
        flattened_students = []
        for s in st.session_state.students:
            student_class = s.get("class", {})
            flattened_students.append(
                {
                    "ID": s.get("id"),
                    "Name": s.get("name"),
                    "Father's Name": s.get("father_name"),
                    "Email": s.get("email"),
                    "Class Name": student_class.get("name", "N/A"),
                    "Batch": student_class.get("batch", "N/A"),
                }
            )

        # Convert to a DataFrame
        df = pd.DataFrame(flattened_students)

        # Display as an interactive, clean data table
        st.subheader("👥 Registered Students")
        st.dataframe(df, use_container_width=True)

    else:
        st.warning("Sorry! No students found.")


# ------------------------------------------
# Update Student
# ------------------------------------------
def update_student(std_id, name, father_name, cls):
    if st.session_state.students:
        for std in st.session_state.students:
            if std.get("id") == std_id:
                std["name"] = name
                std["father_name"] = father_name
                std["class"] = cls

                st.success("Student successfully updated.")
                return
        else:
            st.warning("Invalid Student.")

    else:
        st.warning("student not found")


# ------------------------------------------
# Delete Student
# ------------------------------------------
def delete_student(dlt_std):
    if not st.session_state.students:
        st.warning("Sorry! No classes found to delete.")
        return

    for std in st.session_state.students:
        if std.get("id") == dlt_std.get("id"):
            st.session_state.students.remove(std)
            st.success("Student deleted successfully.")
            return
    st.error("Student already doesn't exist.")


# ------------------------------------------
# === Classes Function ===
# ------------------------------------------
# ------------------------------------------
# *** Create Class ***
# ------------------------------------------
def create_class(name, batch):
    cls = {
        "id": random.randint(100000, 999999),
        "name": name,
        "batch": batch,
    }
    st.session_state.classes.append(cls)
    return f"Successfully Added class {cls}"


# ------------------------------------------
# Find Class by id
# ------------------------------------------
def find_class_by_id(class_id):
    for cls in st.session_state.classes:
        if cls["id"] == class_id:
            return cls
    else:
        return f"Id: {class_id}. Class not found"


# ------------------------------------------
# List Classes
# ------------------------------------------
def classes_list():
    if "classes" in st.session_state and st.session_state.classes:

        flattened_classes = []
        for cls in st.session_state.classes:
            _class = {
                "ID": cls.get("id"),
                "Name": cls.get("name"),
                "Batch": cls.get("batch"),
            }
            flattened_classes.append(_class)

        cls_df = pd.DataFrame(flattened_classes)
        st.subheader("Registered Classes")
        st.dataframe(cls_df, use_container_width=True)

    else:
        st.warning("Sorry! Class not found")


# Update Class
def update_class(cls_id, name, batch):
    if not cls_id:
        st.warning("Invalid Class ID")
        return

    if not st.session_state.classes:
        st.warning("No Class")
        return

    for cls in st.session_state.classes:
        if cls.get("id") == cls_id:
            cls["name"] = name
            cls["batch"] = batch
            st.success(
                f"Class Update Successfully: Name - {cls.get('name')}, Batch - {cls.get('batch')}"
            )
            return
    else:
        st.warning("Invalid Class.")


# ------------------------------------------
# Delete Class
# ------------------------------------------
def delete_class(dlt_cls):
    if not st.session_state.classes:
        st.warning("Sorry! No classes found to delete.")
        return

    for cls in st.session_state.classes:
        if cls.get("id") == dlt_cls.get("id"):
            st.session_state.classes.remove(cls)
            st.success("Class deleted successfully.")
            return
    st.error("Class already doesn't exist.")


# ------------------------------------------
# === Streamlit UI ===
# ------------------------------------------
st.title("Student Management System")
# ------------------------------------------
# *** Students section ***
# ------------------------------------------
menu = st.sidebar.selectbox(
    label="Student Menu",
    options=["Create Student", "Students List", "Update Student", "Delete Student"],
)

# Create Student
if menu == "Create Student":
    st.header("Create Student")
    name = st.text_input(label="Enter your name - e.g. babo Rao")
    father_name = st.text_input(label="Enter your father name - e.g. shakeel")
    email = st.text_input(label="Enter you email - e.g. babo@gmail.com")
    selected_class = st.selectbox(
        "Select Class",
        options=st.session_state.classes,
        format_func=lambda x: f"{x.get('name')} ({x.get('batch')})" if x else "",
    )
    password = st.text_input(label="Enter your password - e.g. 10th")

    # save student
    if st.button("Create Student"):
        if name and father_name and email and selected_class and password is not None:
            std = create_student(name, father_name, email, selected_class, password)
            st.success("🎉 Student Created Successfully!")
            st.write(f"{std}")
        else:
            st.error("Please fill you fields")

# List all students
elif menu == "Students List":
    st.header("Show All Students")
    students_list()

# Update Student
elif menu == "Update Student":
    if not st.session_state.students:
        st.warning("No students available to update.")
    elif not st.session_state.classes:
        st.warning("No class available to update.")

    else:
        # 1. Select the student to update
        selected_student = st.selectbox(
            "Select Student to Update",
            options=st.session_state.students,
            format_func=lambda x: f"{x.get('name')} (ID: {x.get('id')})" if x else "",
            key="update_student_selectbox",  # Fixed key name to match 'update' intent
        )

        # 2. Text fields for names
        name = st.text_input(
            label="Update Student Name", value=selected_student.get("name", "")
        )
        father_name = st.text_input(
            label="Update Student Father Name",
            value=selected_student.get("father_name", ""),
        )

        # 3. CALCULATE DEFAULT CLASS INDEX
        student_current_class = selected_student.get("class", {})

        # Find where the student's class matches an item in the master classes list
        default_index = 0
        for idx, cls in enumerate(st.session_state.classes):
            if cls.get("id") == student_current_class.get("id"):
                default_index = idx
                break

        # 4. Display the class selectbox with the pre-selected default index
        selected_class = st.selectbox(
            "Select Class",
            options=st.session_state.classes,
            index=default_index,  # <-- This sets the default!
            format_func=lambda x: f"{x.get('name')} ({x.get('batch')})" if x else "",
            key="select_class_for_student_selectbox",
        )

    if st.button('Update Confirm'):
        update_student(selected_student.get('id'), name, father_name, selected_class)


#  delete student
elif menu == "Delete Student":
    selected_student = st.selectbox(
        "Select Class",
        options=st.session_state.students,
        key="delete_student_selectbox",
    )

    if st.button("Delete Class"):
        if selected_student is None:
            st.warning("Class Not Selected")
        else:
            delete_student(selected_student)


st.divider()

# ------------------------------------------
# *** Classese Part ***
# ------------------------------------------
menu = st.sidebar.selectbox(
    label="Class Menu",
    options=["Create Class", "Classes List", "Update Class", "Delete Class"],
)

# Create Class
if menu == "Create Class":
    st.header("Create Class")
    name = st.text_input(label="Enter Class Name - e.g. 10th")
    batch = st.text_input(label="Enter Batch Name - e.g. 2026")

    if st.button("Create Class"):
        if name and batch is not None:
            cls = create_class(name, batch)
            st.success("🎉 Class Created Successfully!")
            st.write(f"**Class Name:** `{name}`, **Class Batch:** `{batch}`")
        else:
            st.error("Please fill you fields")

# List all classes
elif menu == "Classes List":
    st.header("Show All classes")
    classes_list()

# Update Class
elif menu == "Update Class":
    if not st.session_state.classes:
        st.warning("No classes available to update.")
    else:
        # format_func makes the dropdown display just the class name (e.g., "10th (2026)")
        selected_class = st.selectbox(
            "Select Class",
            options=st.session_state.classes,
            format_func=lambda x: (
                f"ID: {x.get('id')} - {x.get('name')} ({x.get('batch')})" if x else ""
            ),
            key="update_class_selectbox",
        )

        # Use 'value' to set the default text in the inputs
        name = st.text_input(
            label="Update class Name:", value=selected_class.get("name", "")
        )
        batch = st.text_input(
            label="Update class Batch:", value=selected_class.get("batch", "")
        )

        if st.button("Update Class"):
            update_class(selected_class.get("id"), name, batch)


#  delete class
elif menu == "Delete Class":
    if not st.session_state.classes:
        st.warning("No classes available to update.")

    selected_class = st.selectbox(
        "Select Class",
        options=st.session_state.classes,
        format_func=lambda x: (
            f"ID: {x.get('id')} - {x.get('name')} ({x.get('batch')})" if x else ""
        ),
        key="delete_class_selectbox",
    )

    if st.button("Delete Class"):
        if selected_class is None:
            st.warning("Class Not Selected")
        else:
            delete_class(selected_class)
