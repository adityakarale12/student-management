const API = "https://student-management-x2dd.vercel.app/
    ";

let students = [];

async function fetchStudents() {
    try {
        const response = await fetch(API);

        if (!response.ok) {
            throw new Error("Failed to fetch students");
        }

        const result = await response.json();

        students = result.data || [];

        displayStudents(students);

    } catch (error) {
        document.getElementById("status").textContent =
            "Cannot connect to the FastAPI backend.";
    }
}

function displayStudents(data) {

    const table = document.getElementById("studentTable");

    table.innerHTML = "";

    if (data.length === 0) {
        table.innerHTML = `
            <tr>
                <td colspan="4" style="text-align:center;">
                    No students found
                </td>
            </tr>
        `;
        return;
    }

    data.forEach(student => {

        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${student.id}</td>
            <td>${student.name}</td>
            <td>${student.course}</td>
            <td>${student.marks}</td>
        `;

        table.appendChild(row);
    });
}

async function addStudent() {

    const name = document.getElementById("name").value.trim();
    const course = document.getElementById("course").value.trim();
    const marks = document.getElementById("marks").value;

    const status = document.getElementById("status");

    if (!name || !course || marks === "") {
        status.textContent = "Please fill all fields.";
        return;
    }

    try {

        const response = await fetch(API, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: name,
                course: course,
                marks: Number(marks)
            })
        });

        if (!response.ok) {
            throw new Error("Failed to add student");
        }

        status.textContent = `Thank you, ${name}! Student added successfully.`;

        document.getElementById("name").value = "";
        document.getElementById("course").value = "";
        document.getElementById("marks").value = "";

        await fetchStudents();

    } catch (error) {

        status.textContent =
            "Unable to add student. Check the backend.";
    }
}

function searchStudents() {

    const searchValue =
        document.getElementById("search").value.toLowerCase().trim();

    const filtered = students.filter(student =>
        student.name.toLowerCase().includes(searchValue) ||
        student.course.toLowerCase().includes(searchValue)
    );

    displayStudents(filtered);
}

async function deleteStudent() {

    const id = document.getElementById("deleteId").value;
    const status = document.getElementById("status");

    if (!id) {
        status.textContent = "Enter a student ID to delete.";
        return;
    }

    try {

        const response = await fetch(`${API}/${Number(id)}`, {
            method: "DELETE"
        });

        const result = await response.json();

        if (!response.ok) {
            status.textContent =
                result.detail || "Student not found.";
            return;
        }

        status.textContent =
            `Student ${id} deleted successfully.`;

        document.getElementById("deleteId").value = "";

        await fetchStudents();

    } catch (error) {

        status.textContent =
            "Unable to delete student. Check the backend.";
    }
}

fetchStudents();
