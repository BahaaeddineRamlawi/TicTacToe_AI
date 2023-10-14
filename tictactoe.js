const selectBox = document.querySelector(".select-box"),
  selectBtnX = selectBox.querySelector(".options .playerX"),
  selectBtnO = selectBox.querySelector(".options .playerO"),
  playBoard = document.querySelector(".play-board"),
  players = document.querySelector(".players"),
  allBox = document.querySelectorAll("section span"),
  resultBox = document.querySelector(".result-box"),
  wonText = resultBox.querySelector(".won-text"),
  replayBtn = resultBox.querySelector("button");

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
};
let fontsarray = [
  "Caveat",
  "Indie Flower",
  "Gloria Hallelujah",
  "Shadows Into Light",
];

window.onload = () => {
  for (let i = 0; i < allBox.length; i++) {
    allBox[i].setAttribute("onclick", `call_button_click(${i + 1},this)`);
  }
  resetGame();
};

selectBtnX.onclick = () => {
  selectBox.classList.add("hide");
  playBoard.classList.add("show");
};

selectBtnO.onclick = () => {
  selectBox.classList.add("hide");
  playBoard.classList.add("show");
  players.setAttribute("class", "players active player");
};

let playerXIcon = "X";
let playerOIcon = "O";
let playerSign = "X";

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
      let randomTimeDelay = (Math.random() * 100 + 200).toFixed();
      setTimeout(() => {
        bot(row, column);
      }, randomTimeDelay);
      if (text !== "") {
        setTimeout(() => {
          gameEnded(text);
        }, randomTimeDelay);
      }
    })
    .catch((error) => {
      console.error("Error sending/receiving data:", error);
    });
}

function clickedBox(element) {
  if (players.classList.contains("player")) {
    playerSign = "O";
    element.innerHTML = `<i class="${playerOIcon}">O</i>`;
    players.classList.remove("active");
    element.setAttribute("id", playerSign);
  } else {
    element.innerHTML = `<i class="${playerXIcon}">X</i>`;
    players.classList.add("active");
    element.setAttribute("id", playerSign);
  }
  element.style.pointerEvents = "none";
  playBoard.style.pointerEvents = "none";
}

function bot(row, column) {
  const key = getKeyByValue(cases, [row, column]) - 1;
  playerSign = "O";
  if (key >= 0 && key < 9) {
    changeStyle(`box${key + 1}`);
    if (players.classList.contains("player")) {
      playerSign = "X";
      allBox[key].innerHTML = `<i class="${playerXIcon}">X</i>`;
      allBox[key].setAttribute("id", playerSign);
      players.classList.add("active");
    } else {
      allBox[key].innerHTML = `<i class="${playerOIcon}">O</i>`;
      players.classList.remove("active");
      allBox[key].setAttribute("id", playerSign);
    }
    allBox[key].style.pointerEvents = "none";
    playBoard.style.pointerEvents = "auto";
    playerSign = "X";
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

function gameEnded(text) {
  if (text === "Game Over, You lose!") {
    setTimeout(() => {
      resultBox.classList.add("show");
      playBoard.classList.remove("show");
    }, 700);
    wonText.innerHTML = `AI won the game!`;
  } else if (text === "Game Over, You win!") {
    setTimeout(() => {
      resultBox.classList.add("show");
      playBoard.classList.remove("show");
    }, 700);
    wonText.innerHTML = `You won the game!`;
  } else {
    setTimeout(() => {
      resultBox.classList.add("show");
      playBoard.classList.remove("show");
    }, 700);
    wonText.textContent = "Match has been drawn!";
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

replayBtn.onclick = () => {
  console.log("Game is Reseting");
  window.location.reload();
  resetGame();
};
