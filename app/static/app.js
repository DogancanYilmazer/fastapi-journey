const pollList = document.getElementById("poll-list");
const activePoll = document.getElementById("active-poll");
const createForm = document.getElementById("create-form");
const optionsContainer = document.getElementById("options-container");
const addOptionBtn = document.getElementById("add-option-btn");

let currentPollId = null;
let socket = null;

function addOptionInput() {
  const optionDiv = document.createElement("div");
  optionDiv.className = "option-input-group";
  optionDiv.innerHTML = `
    <input type="text" class="option-input" placeholder="Option" />
    <button type="button" class="remove-option-btn">Remove</button>
  `;
  optionsContainer.appendChild(optionDiv);
  
  optionDiv.querySelector(".remove-option-btn").addEventListener("click", (e) => {
    e.preventDefault();
    optionDiv.remove();
  });
}

addOptionBtn.addEventListener("click", (e) => {
  e.preventDefault();
  addOptionInput();
});

async function api(path, options = {}) {
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) throw new Error(await res.text());
  if (res.status === 204) return null;
  return res.json();
}

async function loadPolls() {
  const polls = await api("/polls");
  pollList.innerHTML = polls.length ? "" : "No polls yet.";

  polls.forEach((poll) => {
    const item = document.createElement("div");
    item.className = "poll-item";
    item.innerHTML = `
      <span>${poll.question}</span>
      <div>
        <button class="secondary" data-open="${poll.id}">Open</button>
        <button class="danger" data-delete="${poll.id}">Delete</button>
      </div>
    `;
    pollList.appendChild(item);
  });
}

function connectWebSocket(pollId) {
  if (socket) socket.close();
  const protocol = location.protocol === "https:" ? "wss" : "ws";
  socket = new WebSocket(`${protocol}://${location.host}/ws/polls/${pollId}`);

  socket.onopen = () => {
    console.log("WebSocket connected:", pollId);
  };

  socket.onmessage = (event) => {
    const message = JSON.parse(event.data);
    if (message.type === "connected" || message.type === "poll_updated") {
      renderPoll(message.poll);
    }
    if (message.type === "poll_deleted") {
      activePoll.innerHTML = "This poll was deleted.";
      currentPollId = null;
      socket.close();
      loadPolls();
    }
  };

  socket.onerror = (error) => {
    console.error("WebSocket error:", error);
    activePoll.innerHTML = "Error connecting to poll.";
  };

  socket.onclose = () => {
    if (currentPollId === pollId) {
      const status = document.createElement("p");
      status.className = "status";
      status.textContent = "WebSocket connection closed.";
      activePoll.appendChild(status);
    }
  };
}

function renderPoll(poll) {
  currentPollId = poll.id;
  activePoll.innerHTML = `<h3>${poll.question}</h3>`;

  poll.options.forEach((option) => {
    const row = document.createElement("div");
    row.className = "option-row";
    row.innerHTML = `
      <div>
        <div class="option-name">${option}</div>
        <div class="vote-count">Votes: ${poll.votes[option]}</div>
      </div>
      <button data-vote="${option}">Vote</button>
    `;
    activePoll.appendChild(row);
  });
}

createForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const question = document.getElementById("question").value;
  const options = Array.from(document.querySelectorAll(".option-input"))
    .map((input) => input.value.trim())
    .filter((val) => val);

  if (options.length < 2) {
    alert("Please add at least 2 options");
    return;
  }

  const poll = await api("/polls", {
    method: "POST",
    body: JSON.stringify({ question, options }),
  });

  createForm.reset();
  optionsContainer.innerHTML = "";
  // Add initial option fields for next poll
  addOptionInput();
  addOptionInput();
  
  await loadPolls();
  connectWebSocket(poll.id);
});

// Add first two empty options on page load
addOptionInput();
addOptionInput();

pollList.addEventListener("click", async (event) => {
  const openId = event.target.dataset.open;
  const deleteId = event.target.dataset.delete;

  if (openId) connectWebSocket(openId);

  if (deleteId) {
    await api(`/polls/${deleteId}`, { method: "DELETE" });
    if (currentPollId === deleteId) {
      activePoll.innerHTML = "Poll deleted.";
      currentPollId = null;
    }
    await loadPolls();
  }
});

activePoll.addEventListener("click", async (event) => {
  const option = event.target.dataset.vote;
  if (!option || !currentPollId) return;

  if (socket && socket.readyState === WebSocket.OPEN) {
    socket.send(JSON.stringify({ type: "vote", option }));
  } else {
    const poll = await api(`/polls/${currentPollId}/vote`, {
      method: "POST",
      body: JSON.stringify({ option }),
    });
    renderPoll(poll);
  }
});

loadPolls();
