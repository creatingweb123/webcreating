let currentPlayer = 'X';
let gameBoard = Array.from({ length: 15 }, () => Array(15).fill(''));
let gameOver = false;
const minValue = -1;
const maxValue = 15;

$(".board").on('click', function (event) {
    if (event.target.classList.contains('cell') && !gameOver) {
        const { row, col } = event.target.dataset;
        const [i, j] = [parseInt(row), parseInt(col)];

        if (gameBoard[i][j] === '') {
            gameBoard[i][j] = currentPlayer;
            event.target.textContent = currentPlayer;

            if (checkWinner(i, j, currentPlayer)) {
                $("#message").text(`${currentPlayer} wins!`);
                gameOver = true;
                setTimeout(reStart, 3000);
            } else {
                currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
                $("#message").text(`${currentPlayer}'s turn`);
            }
        }
    }
});

function checkWinner(row, col, currentPlayer) {
    return (
        horizonCheck(row, col, currentPlayer) ||
        verticalCheck(row, col, currentPlayer) ||
        plusGradient(row, col, currentPlayer) ||
        minusGradient(row, col, currentPlayer)
    );
}

function directionCheck(row, col, currentPlayer, rowIncrement, colIncrement) {
    let count = 1;
    let r = row + rowIncrement;
    let c = col + colIncrement;

    while (r >= minValue && r < maxValue && c >= minValue && c < maxValue && gameBoard[r][c] === currentPlayer) {
        count += 1;
        r += rowIncrement;
        c += colIncrement;
    }

    return count;
}

function horizonCheck(row, col, currentPlayer) {
    return directionCheck(row, col, currentPlayer, 0, 1) + directionCheck(row, col, currentPlayer, 0, -1) -1 >5;
}

function verticalCheck(row, col, currentPlayer) {
    return directionCheck(row, col, currentPlayer, 1, 0) + directionCheck(row, col, currentPlayer, -1, 0) -1 >5;
}

function plusGradient(row, col, currentPlayer) {
    return directionCheck(row, col, currentPlayer, 1, 1) + directionCheck(row, col, currentPlayer, -1, -1) -1 >5;
}

function minusGradient(row, col, currentPlayer) {
    return directionCheck(row, col, currentPlayer, 1, -1) + directionCheck(row, col, currentPlayer, -1, 1) -1 >5;
}

function reStart() {
    currentPlayer = 'X';
    gameBoard = Array.from({ length: 15 }, () => Array(15).fill(''));
    $(".board > .cell").each(function (index, item) {
        item.textContent = '';
    });
    $("#message").text('Start');
    gameOver = false;
}
