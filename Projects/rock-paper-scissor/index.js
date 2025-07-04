const buttons = document.querySelectorAll("button");
const res = document.getElementById("result1");
const usc = document.getElementById("ysco"); // User score
const csc = document.getElementById("csco"); // Computer score

let cscor = 0; // Computer score
let pscor = 0; // Player score

buttons.forEach((button) => {
    button.addEventListener("click", () => {
        const result1 = playRound(button.id, computerPlay());
        res.textContent = result1;
    });
});

function computerPlay() {
    const choices = ["rock", "scissor", "paper"];
    const randchoice = Math.floor(Math.random() * choices.length);
    return choices[randchoice];
}

function playRound(PlayerSelection, ComputerSelection) {
    if (
        PlayerSelection === ComputerSelection
    ) {
        return "It's a tie!";
    } 
    else if (
        (PlayerSelection === "rock" && ComputerSelection === "scissor") ||
        (PlayerSelection === "scissor" && ComputerSelection === "paper") ||
        (PlayerSelection === "paper" && ComputerSelection === "rock")
    ) {
        pscor++;
        usc.textContent = pscor;
        return `You Win! ${PlayerSelection} beats ${ComputerSelection}`;
    } 
    else {
        cscor++;
        csc.textContent = cscor;
        return `Computer Wins! ${ComputerSelection} beats ${PlayerSelection}`;
    }
}
