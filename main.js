var synth = window.speechSynthesis;

function speak(word) {
    if (synth.speaking)
        return;

    if (word == '')
        return;

    var spellingWord = new SpeechSynthesisUtterance(word);

    var voices = synth.getVoices();
    voices.forEach(function (voice) {
        if (voice.default) {
            spellingWord.voice = voice;
            return;
        }
    });

    spellingWord.pitch = 1;
    spellingWord.rate = 1;

    synth.speak(spellingWord);
}

$('.play-button').click(function (e) {
    speak($(e.target).data('speech'));
});