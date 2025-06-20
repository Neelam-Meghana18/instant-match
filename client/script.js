let currentStep = 0;
let answers = {};
let pollingInterval = null;

const questions = [
  { key: "name", text: "What's your name?", type: "text" },
  { key: "age", text: "What's your age?", type: "number" },
  {
    key: "issue", text: "What are you suffering from?", type: "select", options: [
      "stress", "anxiety", "loneliness", "depression", "sleep issues", "exam pressure", "overthinking", "relationship issues", "self-doubt", "anger issues"
    ]
  },
  {
    key: "language", text: "Preferred language?", type: "select", options: [
      "english", "telugu", "hindi", "tamil", "kannada", "malayalam", "marathi", "urdu", "punjabi", "gujarati"
    ]
  }
];

// Load first question
window.onload = renderQuestion;

function renderQuestion() {
  const input = document.getElementById("answerInput");
  const select = document.getElementById("answerSelect");
  const questionText = document.getElementById("question");

  const q = questions[currentStep];
  if (!q) return;

  questionText.innerText = q.text;

  if (q.type === "select") {
    input.style.display = "none";
    select.style.display = "inline";
    select.innerHTML = `<option value="">--Select--</option>` + q.options.map(opt =>
      `<option value="${opt}">${opt}</option>`
    ).join('');
  } else {
    select.style.display = "none";
    input.style.display = "inline";
    input.type = q.type;
    input.value = "";
  }
}

function nextQuestion() {
  const input = document.getElementById("answerInput");
  const select = document.getElementById("answerSelect");

  if (currentStep >= questions.length) return;

  const question = questions[currentStep];
  if (!question) return;

  let value = question.type === "select" ? select.value : input.value;
  if (!value) return alert("Please provide an answer.");

  if (question.key === "age") value = parseInt(value);
  answers[question.key] = value;

  currentStep++;

  if (currentStep >= questions.length) {
    document.getElementById("questionBox").style.display = "none";
    document.getElementById("matchResult").style.display = "block";
    document.getElementById("matchResult").innerHTML = `
      <p>Waiting for a match to arrive... ⏳</p>
      <p>Keep this tab open. You’ll be matched as soon as someone compatible arrives!</p>
    `;
    sendForMatch();
    return;
  }

  renderQuestion();
}

function sendForMatch() {
  fetch("http://localhost:5000/match", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(answers)
  })
    .then(res => res.json())
    .then(data => {
      if (data && data.error) {
        waitForMatch();
      } else {
        showMatch(data);
      }
    })
    .catch(err => {
      console.error(err);
      document.getElementById("matchResult").innerHTML = `<h3>Error connecting to backend!</h3>`;
    });
}

function waitForMatch() {
  if (pollingInterval) clearInterval(pollingInterval); // Avoid duplicate intervals

  pollingInterval = setInterval(() => {
    fetch(`http://localhost:5000/check-match?name=${answers.name}`)
      .then(res => res.json())
      .then(data => {
        if (data && !data.error) {
          clearInterval(pollingInterval);
          showMatch(data);
        }
      })
      .catch(() => {
        // silently ignore errors
      });
  }, 3000);
}

function showMatch(match) {
  const box = document.getElementById("questionBox");
  box.style.display = "none";

  const matchBox = document.getElementById("matchResult");
  matchBox.style.display = "block";

  // Save names for chat page
  localStorage.setItem("matchedName", match.name);
  localStorage.setItem("yourName", answers.name);

  matchBox.innerHTML = `
    <div style="
      background-color: #ffffffcc;
      padding: 30px;
      border-radius: 16px;
      box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
      max-width: 400px;
      margin: 0 auto;
      text-align: center;
    ">
      <h2 style="color: #333; margin-bottom: 10px;">🎉 You found a match!</h2>
      <p style="font-size: 1.1rem; color: #444;">
        <strong>${match.name}</strong> is here to chat with you 💬
      </p>
      <p style="font-size: 0.95rem; color: #666; margin-top: 10px;">
        Someone who understands you is just a message away.
      </p>
      <br/>
      <button onclick="window.location.href='chat.html'" style="
        background: #6c63ff;
        color: white;
        border: none;
        padding: 12px 20px;
        font-size: 1rem;
        border-radius: 8px;
        cursor: pointer;
        transition: background 0.3s ease;
      ">Chat Now</button>
    </div>
  `;
}
