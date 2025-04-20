document.addEventListener("DOMContentLoaded", function() {
    const voiceButton = document.getElementById("voiceBotButton");

    function setListening() {
        voiceBotButton.classList.remove("speaking");
        voiceBotButton.classList.add("listening");
    }

        function setSpeaking() {
        voiceBotButton.classList.remove("listening");
        voiceBotButton.classList.add("speaking");
    }

        function setIdle() {
        voiceBotButton.classList.remove("speaking", "listening");
    }

    setTimeout(setListening, 2000);
    setTimeout(setSpeaking, 5000);
    setTimeout(setIdle, 8000);
});