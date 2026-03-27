const API_BASE_URL = "http://127.0.0.1:8000";
// For production on Vercel, replace the line above with your Render backend URL.
// Example:
// const API_BASE_URL = "https://your-render-service.onrender.com";

const uploadBtn = document.getElementById("uploadBtn");
const urlBtn = document.getElementById("urlBtn");
const askBtn = document.getElementById("askBtn");
const healthBtn = document.getElementById("healthBtn");

const filesInput = document.getElementById("filesInput");
const urlInput = document.getElementById("urlInput");
const questionInput = document.getElementById("questionInput");

const uploadResult = document.getElementById("uploadResult");
const urlResult = document.getElementById("urlResult");
const healthBox = document.getElementById("healthBox");

const answerBox = document.getElementById("answerBox");
const answerText = document.getElementById("answerText");
const sourcesList = document.getElementById("sourcesList");

function renderError(target, message) {
  target.textContent = `Error: ${message}`;
}

function renderSuccess(target, payload) {
  target.textContent = JSON.stringify(payload, null, 2);
}

uploadBtn.addEventListener("click", async () => {
  const files = filesInput.files;
  if (!files || files.length === 0) {
    renderError(uploadResult, "Please choose at least one file.");
    return;
  }

  const formData = new FormData();
  for (const file of files) {
    formData.append("files", file);
  }

  uploadResult.textContent = "Uploading and indexing...";

  try {
    const response = await fetch(`${API_BASE_URL}/api/ingest/files`, {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Upload failed.");
    }

    renderSuccess(uploadResult, data);
  } catch (error) {
    renderError(uploadResult, error.message);
  }
});

urlBtn.addEventListener("click", async () => {
  const url = urlInput.value.trim();
  if (!url) {
    renderError(urlResult, "Please enter a URL.");
    return;
  }

  urlResult.textContent = "Indexing URL...";

  try {
    const response = await fetch(`${API_BASE_URL}/api/ingest/url`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url }),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "URL ingest failed.");
    }

    renderSuccess(urlResult, data);
  } catch (error) {
    renderError(urlResult, error.message);
  }
});

askBtn.addEventListener("click", async () => {
  const question = questionInput.value.trim();
  if (!question) {
    alert("Please enter a question.");
    return;
  }

  answerBox.classList.add("hidden");
  answerText.textContent = "";
  sourcesList.innerHTML = "";

  try {
    const response = await fetch(`${API_BASE_URL}/api/query`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question, top_k: 4 }),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Query failed.");
    }

    answerBox.classList.remove("hidden");
    answerText.textContent = data.answer;

    for (const source of data.sources) {
      const div = document.createElement("div");
      div.className = "source-item";
      div.innerHTML = `
        <strong>${source.source}</strong>
        <div><b>Score:</b> ${source.score}</div>
        <div><b>Chunk:</b> ${source.chunk_id}</div>
        <p>${source.text}</p>
      `;
      sourcesList.appendChild(div);
    }
  } catch (error) {
    alert(`Error: ${error.message}`);
  }
});

healthBtn.addEventListener("click", async () => {
  healthBox.textContent = "Checking backend health...";

  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    const data = await response.json();
    if (!response.ok) {
      throw new Error("Health check failed.");
    }
    renderSuccess(healthBox, data);
  } catch (error) {
    renderError(healthBox, error.message);
  }
});
