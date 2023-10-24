var numberOfDrumButton = document.querySelectorAll(".drum");

var audios = ["sounds/tom-1.mp3","sounds/tom-2.mp3","sounds/tom-3.mp3","sounds/tom-4.mp3","sounds/crash.mp3","sounds/kick.mp3","sounds/snare.mp3"]
for(var i=0;i<numberOfDrumButton.length;i++){
    document.querySelectorAll("button")[i].addEventListener("click", function () {
        this.classList.toggle("white");
        var audio1 = new Audio(audios[i]);
        audio1.loop = false; // 반복재생하지 않음
        audio1.volume = 0.5; // 음량 설정
        audio1.play(); // sound1.mp3 재생
      });

}
// document.querySelectorAll("button")[0].addEventListener("click", function () {
//     var audio1 = new Audio("sounds/tom-1.mp3");
//     audio1.loop = false; // 반복재생하지 않음
//     audio1.volume = 0.25; // 음량 설정
//     audio1.play(); // sound1.mp3 재생
// });
