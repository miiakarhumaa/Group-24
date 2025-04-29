// var jsonTemps;
// var ntcTemp;
// var dhtTemp;

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}


function fetchJsonData() {
    return fetch('./temps.json')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            return data;
        })
        .catch(error => console.error('Failed to fetch data:', error));
}


function refreshTemps() {
    var jsonTemps;
    var ntcTemp;
    var dhtTemp;
    fetchJsonData().then((data) => {
        jsonTemps = data;
        ntcTemp = jsonTemps.ntc_temp;
        dhtTemp = jsonTemps.dht_temp;
        console.log(jsonTemps);
        console.log(ntcTemp);
        console.log(dhtTemp);
        document.getElementById("tempDiv").innerHTML = `NTC temp: ${ntcTemp}, DHT temp: ${dhtTemp}`;
    })
}

refreshTemps();
