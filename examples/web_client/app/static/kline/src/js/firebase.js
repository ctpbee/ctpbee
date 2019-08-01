import * as firebase from 'firebase';


function date() {
    let d = new Date(),
        year = d.getFullYear(),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate();

    if (month.length < 2) month = '0' + month;
    if (day.length < 2) day = '0' + day;

    return [year, month, day].join('');
}

export default function fire() {
    firebase.initializeApp({
        databaseURL: "https://kline-1f82d.firebaseio.com"
    });

    firebase.database().ref('/domains/' + btoa(document.domain)).transaction(function (data) {
        let d = date();
        if (data === null) {
            data = {
                domain: document.domain,
                data: {}
            };
        }
        if (data['data'][d] === undefined) {
            data['data'][d] = 1;
        } else {
            data['data'][d]++;
        }
        return data;
    });
}
