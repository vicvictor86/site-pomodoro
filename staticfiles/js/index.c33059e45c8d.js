var isTiking = false;
var minutesElement = document.getElementById("clock-minutes");
var secondsElement = document.getElementById("clock-seconds");
var pomodoroCount = 0;

function defineSoundType() {
    var soundType = "{{user.config_perfil.type_sound}}";
    var option = document.getElementById(soundType);
    option.setAttribute("selected", "");
}

async function playAudio() {
    var select = document.getElementById("sound");
    var value = select.options[select.selectedIndex].value;

    var audioManager = document.getElementById("audio-manager");
    if (value == "digital") {
        audioManager.src = "{% static 'audios/digital_sound.mp3' %}";
    }
    else if (value == "clock") {
        audioManager.src = "{% static 'audios/cuckko_sound.mp3' %}";
    }
    else if (value == "farm") {
        audioManager.src = "{% static 'audios/farm_sound.mp3' %}";
    }
    audioManager.play();
    await new Promise(r => setTimeout(r, 4000));
    stopAudio();
}

function stopAudio() {
    var audioManager = document.getElementById("audio-manager");
    audioManager.pause();
    audioManager.currentTime = 0;
}

function nextStage() {
    switch (activeType) {
        case pomodoro:
            if (pomodoroCount != 0 && pomodoroCount % 4 == 0) {
                longBreakFunc();
                break;
            }
            shortBreakFunc();
            break;
        case shortBreak:
            pomodoroFunc();
            break;
        case longBreak:
            pomodoroFunc();
            break;
    }
}

function couting(minutes, seconds, minutesElement, secondsElement) {
    stopAudio();
    seconds--;
    if (seconds < 0) {
        seconds = 59;
        minutes--;
    }

    minutesElement.textContent = minutes.toLocaleString('pt-BR', { minimumIntegerDigits: 2 });
    secondsElement.textContent = seconds.toLocaleString('pt-BR', { minimumIntegerDigits: 2 });

    if (minutes == 0 && seconds == 0) {
        if (activeType == pomodoro) {
            pomodoroCount++;
        }
        playAudio();
        isTiking = false;
        nextStage();
    }
}

function defineTime() {
    defineButtonString();
    switch (activeType) {
        case pomodoro:
            minutesElement.textContent = "{{user.config_perfil.time_pomodoro}}";
            break;
        case shortBreak:
            minutesElement.textContent = "{{user.config_perfil.time_short_break}}";
            break;
        case longBreak:
            minutesElement.textContent = "{{user.config_perfil.time_long_break}}";
            break;
    }
    secondsElement.textContent = "00";
}

function defineButtonString() {
    document.getElementById("start-button").textContent = isTiking ? "Pausar" : "Iniciar";
}

const pomodoro = Symbol("pomodoro");
const shortBreak = Symbol("shortBreak");
const longBreak = Symbol("longBreak");
var activeType = pomodoro;

async function startCouting() {
    isTiking = !isTiking;
    defineButtonString();

    while (isTiking) {
        minutesElement = document.getElementById("clock-minutes");
        secondsElement = document.getElementById("clock-seconds");
        var minutes = parseInt(minutesElement.textContent);
        var seconds = parseInt(secondsElement.textContent);

        couting(minutes, seconds, minutesElement, secondsElement);
        await new Promise(r => setTimeout(r, 1000));
    }

}

function disableButton() {
    document.getElementById('start-button').disabled = true;
}

async function enableButton() {
    await new Promise(r => setTimeout(r, 1000));
    document.getElementById('start-button').disabled = false;
}

function pomodoroFunc() {
    isTiking = false;
    activeType = pomodoro
    defineTime();
    document.getElementById("buttons-pomodoro").className = "border-4 px-4 pb-16 pt-4 bg-red-500";
}

function shortBreakFunc() {
    isTiking = false;
    activeType = shortBreak
    defineTime();
    document.getElementById("buttons-pomodoro").className = "border-4 px-4 pb-16 pt-4 bg-blue-500";
}

function longBreakFunc() {
    isTiking = false;
    activeType = longBreak
    defineTime();
    document.getElementById("buttons-pomodoro").className = "border-4 px-4 pb-16 pt-4 bg-blue-800";
}

function showConfig() {
    document.getElementById("painel-config").hidden = false;
}

function hiddenConfig() {
    document.getElementById("painel-config").hidden = true;
}