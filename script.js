let gameState = {};

/**
 * Helper function to make POST requests and parse the JSON response.
 */
function postData(url, data = {}) {
  return fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  }).then(response => response.json());
}

/**
 * Initialize or reset the game by sending settings to the backend.
 */
function initGame() {
  const mode = document.getElementById("mode").value;
  const userPlayer = document.getElementById("player").value;
  const data = { mode, user_player: userPlayer };

  if (mode === "multi") {
    data.playerXName = document.getElementById("playerXNameInput")?.value || "Player X";
    data.playerOName = document.getElementById("playerONameInput")?.value || "Player O";
  } else {
    data.userName = document.getElementById("userNameInput")?.value || "Player";
  }

  postData("/start", data).then(result => {
    gameState = result;
    renderGame();
  });
}

/**
 * Render the game board, scoreboard, and message.
 */
function renderGame() {
  const boardDiv = document.getElementById("board");
  boardDiv.innerHTML = "";
  gameState.board.forEach((cell, index) => {
    const cellDiv = document.createElement("div");
    cellDiv.className = "cell";
    cellDiv.textContent = cell;
    cellDiv.addEventListener("click", () => makeMove(index));
    boardDiv.appendChild(cellDiv);
  });
  document.getElementById("message").innerHTML = gameState.message;
  document.getElementById("scoreboard").textContent = gameState.scoreboard;
  document.getElementById("nextBtn").disabled = gameState.game_active;
}

/**
 * Send a move to the backend.
 */
function makeMove(index) {
  postData("/move", { index }).then(result => {
    gameState = result;
    renderGame();
  });
}

/**
 * Advance to the next game (or reset the match if completed).
 */
function nextGame() {
  postData("/next").then(result => {
    gameState = result;
    renderGame();
  });
}

/**
 * Update the name input fields and control layout based on the selected mode.
 */
function updateNameInputs() {
  const mode = document.getElementById("mode").value;
  const controlPanel = document.getElementById("controlPanel");
  const modeGroup = document.getElementById("modeGroup");
  const nameInputsDiv = document.getElementById("nameInputs");
  const playerSelectionDiv = document.getElementById("playerSelectionDiv");

  if (mode === "multi") {
    controlPanel.classList.remove("single-player");
    nameInputsDiv.innerHTML = `
      <label for="playerXNameInput" style="font-weight:bold;">Player X Name</label>
      <input type="text" id="playerXNameInput" value="Player X" onchange="initGame()" />
      <label for="playerONameInput" style="font-weight:bold; margin-top:10px;">Player O Name</label>
      <input type="text" id="playerONameInput" value="Player O" onchange="initGame()" />
    `;
    playerSelectionDiv.style.display = "none";
  } else {
    controlPanel.classList.add("single-player");
    nameInputsDiv.innerHTML = `
      <label for="userNameInput" style="font-weight:bold;">Your Name</label>
      <input type="text" id="userNameInput" value="Player" onchange="initGame()" />
    `;
    playerSelectionDiv.style.display = "flex";
  }

  // Reorder elements: mode group, then name inputs, then symbol selector.
  controlPanel.innerHTML = "";
  controlPanel.appendChild(modeGroup);
  controlPanel.appendChild(nameInputsDiv);
  controlPanel.appendChild(playerSelectionDiv);
}

/**
 * Handlers for mode and symbol changes.
 */
function setMode() {
  updateNameInputs();
  initGame();
}

function setPlayer() {
  initGame();
}

/**
 * On initial load, set up the control panel and start the game.
 */
document.addEventListener("DOMContentLoaded", () => {
  updateNameInputs();
  initGame();
});
