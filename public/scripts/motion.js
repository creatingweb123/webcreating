let currentPlayer = 'X';
let gameBoard = Array.from(Array(15), () => Array(15).fill(''));
let gameOver = false;
let minValue = -1;
let maxValue = 15;

$(".board").on('click',function(event){
    if (event.target.classList.contains('cell') && !gameOver) {
        console.log(event.target.dataset);
        var row = parseInt(event.target.dataset.row);
        var col = parseInt(event.target.dataset.col);

        if (gameBoard[row][col] === '') {
            gameBoard[row][col] = currentPlayer;
            event.target.textContent = currentPlayer;
            

            if (checkWinner(row, col,currentPlayer)) {
                $("#message").textContent = `${currentPlayer} wins!`;
                gameOver = true;
                setTimeout(function(){
                    reStart();
                },3000);

            } else {
                currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
                $("#message").textContent = `${currentPlayer}'s turn`;
            }
        }
    }
});


function checkWinner(row, col,currentPlayer) {
    if(horizonCheck(row, col,currentPlayer)||verticalCheck(row, col,currentPlayer)||plusGradient(row, col,currentPlayer)||minusGradient(row, col,currentPlayer)){
        return true
    }else{
        return false;
    }
}

function horizonCheck(row, col, currentPlayer){
    var count = 1;
    var lr = row-1;
    var rr = row+1;
    while(lr>minValue && gameBoard[lr][col]==currentPlayer){
        count += 1;
        lr    -= 1;
    }
    while(rr<maxValue && gameBoard[rr][col]==currentPlayer){
        count += 1;
        rr    += 1;
    }
    if(count>4){
        console.log("horizon");
        return true;
    }else{
        return false;
    }
}
function verticalCheck(row, col, currentPlayer){
    var count = 1;
    var uc = col-1;
    var dc = col+1;
    while(uc>minValue && gameBoard[row][uc]==currentPlayer){
        count += 1;
        uc    -= 1;
    }
    while(dc<maxValue && gameBoard[row][dc]==currentPlayer){
        count += 1;
        dc    += 1;
    }
    if(count>4){
        return true;
    }else{
        return false;
    }
}
function plusGradient(row, col, currentPlayer){
    var count = 1;
    var lr = row-1;
    var dc = col+1;

    var rr = row+1;
    var uc = col-1;
    
    while(lr>minValue && dc<maxValue && gameBoard[lr][dc]==currentPlayer){
        count += 1;
        lr    -= 1;
        dc    += 1;
    }
    while(rr<maxValue && uc>minValue && gameBoard[rr][uc]==currentPlayer){
        count += 1;
        rr    += 1;
        uc    -= 1;
    }
    if(count>4){
        return true;
    }else{
        return false;
    }
}
function minusGradient(row, col, currentPlayer){
    var count = 1;
    var lr = row-1;
    var uc = col-1;
    
    var rr = row+1;
    var dc = col+1;

    while(lr>minValue && uc>minValue && gameBoard[lr][uc]==currentPlayer){
        count += 1;
        lr    -= 1;
        uc    -= 1;
    }
    while(rr<maxValue && dc<maxValue && gameBoard[rr][dc]==currentPlayer){
        count += 1;
        rr    += 1;
        uc    += 1;
    }
    if(count>4){
        return true;
    }else{
        return false;
    }
}

function reStart(){

    currentPlayer = 'X';
    gameBoard = Array.from(Array(15), () => Array(15).fill(''));
    $(".board>.cell").each(function(index,item){
        item.textContent = "";
    });   
    $("#message").textContent = "Start";
    gameOver = false;
}