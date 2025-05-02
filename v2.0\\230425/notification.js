const NTC_TRESHOLD = 5.0;

var dhtTemp;
var ntcTemp;
var dhtText;
var ntcText;
var dhtLen;
var ntcLen;

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function sendNotification() {
    const notification = new Notification("Your drink is ready to enjoy!");
}

if (Notification.permission !== "granted")
    Notification.requestPermission();

while (true) {
    sleep(5000);
    dhtTemp = document.getElementById("dhtTemp").innerText.match(/[0-9.]+/);
    ntcTemp = document.getElementById("ntcTemp").innerText.match(/[0-9.]+/);
    dhtTemp = parseFloat(dhtTemp);
    ntcTemp = parseFloat(ntcTemp);

    if (ntcTemp <= NTC_TRESHOLD) {
        sendNotification();
        sleep(15000);
    }
}
