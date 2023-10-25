var numberOfDrumButton = document.querySelectorAll(".drum");

function drum_key(buttonInntertext){
  switch (buttonInntertext) {
    case 'w':
      var audio1 = new Audio("sounds/tom-1.mp3");
      break;
    case 'a':
      var audio1 = new Audio("sounds/tom-2.mp3");
      break;
    case 's':
      var audio1 = new Audio("sounds/tom-3.mp3");
      break;
    case 'd':
      var audio1 = new Audio("sounds/tom-4.mp3");
      break;
    case 'j':
      var audio1 = new Audio("sounds/crash.mp3");
      break;
    case 'k':
      var audio1 = new Audio("sounds/kick-bass.mp3");
      break;
    case 'l':
      var audio1 = new Audio("sounds/snare.mp3");
      break;
    default:
      console.log("wrong button");
  }
  audio1.play();
}

for(var i=0;i<numberOfDrumButton.length;i++){
    document.querySelectorAll("button")[i].addEventListener("click", function () {
      var buttonInntertext = this.innerHTML;  
      drum_key(buttonInntertext);
      //audio1.loop = false; // 반복재생하지 않음
      //audio1.volume = 0.5; // 음량 설정
      //audio1.play(); // sound1.mp3 재생
      });
}
document.addEventListener("keydown", function (event) {
  var buttonInntertext = event.key;  
  drum_key(buttonInntertext);
  });