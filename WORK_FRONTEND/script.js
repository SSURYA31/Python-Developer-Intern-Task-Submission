const BASE_URL = "http://127.0.0.1:8000";
let token = localStorage.getItem("token") || "";
let isLogin = true;

// Toggle login/register
function toggleMode() {
    isLogin = !isLogin;
    document.getElementById("formTitle").innerText = isLogin ? "Login" : "Register";
    document.getElementById("toggleText").innerText =
        isLogin ? "Don't have an account? Register" : "Already have an account? Login";
}

// Handle auth
async function handleAuth() {
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;

    let url = isLogin ? "/login" : "/register";

    let res = await fetch(`${BASE_URL}${url}`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ username, password })
    });

    let data = await res.json();

    if (isLogin && data.access_token) {
        localStorage.setItem("token", data.access_token);
        window.location.href = "dashboard.html";
    } else {
        alert(JSON.stringify(data));
    }
}

// Create task
async function createTask() {
    let body = {
        title: document.getElementById("title").value,
        description: document.getElementById("description").value,
        comment: document.getElementById("comment").value,
        time_period: document.getElementById("time").value
    };

    await fetch(`${BASE_URL}/tasks`, {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json"
        },
        body: JSON.stringify(body)
    });

    // clear fields
    document.getElementById("title").value = "";
    document.getElementById("description").value = "";
    document.getElementById("comment").value = "";
    document.getElementById("time").value = "";

    loadTasks();
}

// Load tasks
async function loadTasks() {
    let res = await fetch(`${BASE_URL}/tasks`, {
        headers: { "Authorization": "Bearer " + token }
    });

    let tasks = await res.json();

    let table = document.getElementById("taskTable");
    if (!table) return;

    table.innerHTML = "";

    tasks.forEach(t => {

        // 🟡 Pending / 🟢 Completed button
        let statusBtn = t.completed
            ? `<button class="completed-btn" onclick="alreadyDone()">Completed</button>`
            : `<button class="pending-btn" onclick="complete(${t.id})">Mark Complete</button>`;

        let row = `
        <tr>
            <td>${t.id}</td>
            <td>${t.title}</td>
            <td>${new Date().toLocaleDateString()}</td>

            <td>${statusBtn}</td>

            <td>
                <button class="view-btn" onclick="viewTask(${t.id})">View</button>
            </td>

            <td>
                <button class="delete-btn" onclick="removeTask(${t.id})">Delete</button>
            </td>
        </tr>
        `;

        table.innerHTML += row;
    });
}

// Complete
async function complete(id) {
    await fetch(`${BASE_URL}/tasks/${id}/complete`, {
        method: "PUT",
        headers: {"Authorization": "Bearer " + token}
    });
    loadTasks();
}

// Delete
async function removeTask(id) {
    await fetch(`${BASE_URL}/tasks/${id}`, {
        method: "DELETE",
        headers: {"Authorization": "Bearer " + token}
    });
    loadTasks();
}

// Auto load if dashboard
if (window.location.pathname.includes("dashboard.html")) {
    loadTasks();
}

function alreadyDone() {
    alert("Task is already completed ✅");
}

function viewTask(id) {
    window.location.href = `view.html?id=${id}`;
}

function getTaskId() {
    const params = new URLSearchParams(window.location.search);
    return params.get("id");
}

async function loadTaskDetails() {
    let id = getTaskId();

    let res = await fetch(`${BASE_URL}/tasks/${id}`, {
        headers: {"Authorization": "Bearer " + token}
    });

    let t = await res.json();

    document.getElementById("title").value = t.title;
    document.getElementById("description").value = t.description;
    document.getElementById("comment").value = t.comment;
    document.getElementById("time").value = t.time_period;
}

async function updateTask() {
    let id = getTaskId();

    let body = {
        title: title.value,
        description: description.value,
        comment: comment.value,
        time_period: time.value
    };

    await fetch(`${BASE_URL}/tasks/${id}`, {
        method: "PUT",
        headers: {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json"
        },
        body: JSON.stringify(body)
    });

    alert("Updated!");
}

if (window.location.pathname.includes("view.html")) {
    loadTaskDetails();
}