const list = document.getElementById("list");
const input = document.getElementById("todo");

async function loadTodos() {
  const res = await fetch("/todos");
  if (!res.ok) {
    list.innerHTML = "<li>Could not load todos</li>";
    return;
  }
  list.innerHTML = "";
  for (const todo of await res.json()) {
    const li = document.createElement("li");
    li.textContent = todo;
    list.appendChild(li);
  }
}

document.getElementById("form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const res = await fetch("/todos", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ todo: input.value }),
  });
  if (!res.ok) {
    const data = await res.json().catch(() => null);
    alert(data?.error ?? `Failed to create todo (HTTP ${res.status})`);
    return;
  }
  input.value = "";
  loadTodos();
});

loadTodos();
