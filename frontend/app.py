import requests
import gradio as gr

API = "http://localhost:8000/students"  # change to your deployed FastAPI URL


def fetch_students(search=""):
    res = requests.get(API).json()
    data = res.get("data", [])
    if search:
        s = search.lower()
        data = [d for d in data if s in d["name"].lower() or s in d["course"].lower()]
    rows = [[d["id"], d["name"], d["course"], d["marks"]] for d in data]
    return rows


def add_student(name, course, marks):
    if not name or not course or marks is None:
        return "Fill all fields", fetch_students()
    requests.post(API, json={"name": name, "course": course, "marks": int(marks)})
    return f"Thank you, {name}! Student added.", fetch_students()


def delete_student(student_id):
    if not student_id:
        return "Enter an ID to delete", fetch_students()
    requests.delete(f"{API}/{int(student_id)}")
    return f"Deleted student {student_id}", fetch_students()


with gr.Blocks(title="Student Manager") as demo:
    gr.Markdown("## 🎓 Student Manager")

    with gr.Row():
        name = gr.Textbox(label="Name")
        course = gr.Textbox(label="Course")
        marks = gr.Number(label="Marks")
    add_btn = gr.Button("Add Student", variant="primary")

    search = gr.Textbox(label="🔍 Search by name or course")

    table = gr.Dataframe(headers=["ID", "Name", "Course", "Marks"], value=fetch_students())

    with gr.Row():
        del_id = gr.Number(label="Student ID to delete")
        del_btn = gr.Button("Delete", variant="stop")

    status = gr.Textbox(label="Status", interactive=False)

    add_btn.click(add_student, [name, course, marks], [status, table])
    search.change(fetch_students, [search], table)
    del_btn.click(delete_student, [del_id], [status, table])

demo.launch()