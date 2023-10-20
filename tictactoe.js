const selectBox = document.querySelector(".select-box"),
  selectBtnX = selectBox.querySelector(".options .playerX"),
  selectBtnO = selectBox.querySelector(".options .playerO"),
  playBoard = document.querySelector(".play-board"),
  players = document.querySelector(".players"),
  allBox = document.querySelectorAll("section span"),
  resultBox = document.querySelector(".result-box"),
  reviewBox = document.querySelector(".review-box"),
  wonText = resultBox.querySelector(".won-text"),
  replayBtn = resultBox.querySelector(".btn"),
  replayBtn2 = reviewBox.querySelector(".btn");

let counter = 1;

cases = {
  1: [0, 0],
  2: [0, 1],
  3: [0, 2],
  4: [1, 0],
  5: [1, 1],
  6: [1, 2],
  7: [2, 0],
  8: [2, 1],
  9: [2, 2],
  10: [3, 3],
};

let fontsarray = [
  "Caveat",
  "Indie Flower",
  "Gloria Hallelujah",
  "Shadows Into Light",
];

let playerXIcon = "X";
let playerOIcon = "O";
let playerSign = "X";

window.onload = () => {
  for (let i = 0; i < allBox.length; i++) {
    allBox[i].setAttribute("onclick", `call_button_click(${i + 1},this)`);
  }
};

selectBtnX.onclick = () => {
  selectBox.classList.add("hide");
  playBoard.classList.add("show");
};

selectBtnO.onclick = () => {
  selectBox.classList.add("hide");
  playBoard.classList.add("show");
  players.setAttribute("class", "players active player");
  playerSign = "O";
};

function call_button_click(val, element) {
  row = cases[val][0];
  column = cases[val][1];
  const key = getKeyByValue(cases, [row, column]);
  changeStyle(`box${key}`);
  clickedBox(element);
  const inputData = { row: row, column: column };
  fetch("/send_data", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ data: inputData }),
  })
    .then((response) => response.json())
    .then((data) => {
      row = data["row"];
      column = data["column"];
      text = data["text"];
      box = data["box"];
      const key = getKeyByValue(cases, [row, column]);
      setTimeout(() => {
        bot(key);
      }, 250);
      if (text !== "") {
        setTimeout(() => {
          gameEnded(text, box);
        }, 250);
      }
    })
    .catch((error) => {
      console.error("Error sending/receiving data:", error);
    });
}

function clickedBox(element) {
  const box = element.getAttribute("class");
  const lastChar = box.charAt(box.length - 1);
  [row, column] = cases[lastChar]; // Get the row and column of the player
  addText(counter + "- You -> row: " + row + " column: " + column, "p"); // Game review
  if (players.classList.contains("player")) {
    playerSign = "O";
    element.innerHTML = `<i class="${playerOIcon}">O</i>`;
    players.classList.remove("active");
  } else {
    element.innerHTML = `<i class="${playerXIcon}">X</i>`;
    players.classList.add("active");
  }
  element.style.pointerEvents = "none";
  playBoard.style.pointerEvents = "none";
  counter++;
}

function bot(key) {
  if (key <= 9) {
    addText(counter + "- AI -> row: " + row + " column: " + column, "p"); //Game Review
    playerSign = "O";
    changeStyle(`box${key}`);
    if (players.classList.contains("player")) {
      playerSign = "X";
      allBox[key - 1].innerHTML = `<i class="${playerXIcon}">X</i>`;
      players.classList.add("active");
    } else {
      allBox[key - 1].innerHTML = `<i class="${playerOIcon}">O</i>`;
      players.classList.remove("active");
    }
    allBox[key - 1].style.pointerEvents = "none";
    playBoard.style.pointerEvents = "auto";
    playerSign = "X";
    counter++;
  }
}

function getKeyByValue(obj, targetValue) {
  for (const key in obj) {
    if (obj.hasOwnProperty(key) && Array.isArray(obj[key])) {
      const array = obj[key];
      if (arraysAreEqual(array, targetValue)) {
        return key;
      }
    }
  }
  return null;
}

function arraysAreEqual(arr1, arr2) {
  if (arr1.length !== arr2.length) {
    return false;
  }
  for (let i = 0; i < arr1.length; i++) {
    if (arr1[i] !== arr2[i]) {
      return false;
    }
  }
  return true;
}

function gameEnded(text, box) {
  b0 = box[0];
  b1 = box[1];
  b2 = box[2];
  const key0 = getKeyByValue(cases, [b0[0], b0[1]]);
  const key1 = getKeyByValue(cases, [b1[0], b1[1]]);
  const key2 = getKeyByValue(cases, [b2[0], b2[1]]);
  if (text === "AI won the game!") {
    endingCermony(key0, key1, key2, text);
  } else if (text === "You won the game!") {
    endingCermony(key0, key1, key2, text);
  } else {
    setTimeout(() => {
      resultBox.classList.add("show");
      playBoard.classList.remove("show");
    }, 700);
    wonText.textContent = "Match has been drawn!";
    addText("Match has been drawn!");
  }
}

function resetGame() {
  fetch("/reset_game", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ reset: true }),
  }).catch((error) => {
    console.error("Error sending/receiving data:", error);
  });
}

function changeStyle(aclass) {
  var thefont = fontsarray[Math.floor(Math.random() * fontsarray.length)];
  document.getElementsByClassName(aclass)[0].style.fontFamily = thefont;
}

function setBackgroundStyles(className) {
  const element = document.getElementsByClassName(className)[0];
  element.style.background = "#5c5cb1";
  element.style.color = "#fff";
}

function endingCermony(key0, key1, key2, text) {
  // Change Background color for winner and showing the result
  setTimeout(() => {
    setBackgroundStyles(`box${key0}`);
  }, 100);
  setTimeout(() => {
    setBackgroundStyles(`box${key1}`);
  }, 400);
  setTimeout(() => {
    setBackgroundStyles(`box${key2}`);
  }, 700);
  setTimeout(() => {
    resultBox.classList.add("show");
    playBoard.classList.remove("show");
  }, 1000);
  wonText.innerHTML = text;
  addText(text); // Game Review
}

function showReview() {
  resultBox.classList.remove("show");
  reviewBox.classList.add("show");
}

function addText(text, type = "h3") {
  const context = document.createElement(type);
  context.textContent = text;
  const targetElement = document.querySelector(".review-box");
  targetElement.appendChild(context);
}

replayBtn.onclick = () => {
  window.location.reload();
  resetGame();
};

replayBtn2.onclick = () => {
  addText("Game is Reseting", "p");
  window.location.reload();
  resetGame();
};
