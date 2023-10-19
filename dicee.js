var number1 = Math.floor(Math.random()*5)+1;
var number2 = Math.floor(Math.random()*5)+1;

var dices = document.querySelectorAll("img");

var dice1 = dices[0];
// dice1.src= "./images/dice"+number1+".png";
dice1.setAttribute("src","./images/dice"+number1+".png");

var dice2 = dices[1]
dice2.src = "./images/dice"+number2+".png";
// dice2.setAttribute("src","./images/dice"+number2+".png");

// var h1 = document.getElementsByTagName("h1")[0];
var h1 = document.querySelector("h1");
if (number1>number2){
    h1.innerText = "Player1 Win!"
}else if(number1<number2){
    h1.innerText = "Player2 Win!"
}else{
    h1.innerText = "Draw"
}
