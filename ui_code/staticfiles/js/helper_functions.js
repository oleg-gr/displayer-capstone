function convertSecondsToWords(seconds) {

    if (seconds <= 60*2) {
        return "1 minute";
    } else if (seconds <= 60*60) {
        return Math.round(seconds/60) + " minutes";
    } else if (seconds <= 60*60*2) {
        return "1 hour";
    } else if (seconds <= 60*60*24) {
        return Math.round(seconds/(60*60)) + " hours";
    } else if (seconds <= 60*60*24*2) {
        return "1 day";
    } else {
        return Math.round(seconds/(60*60*24)) + " days";
    }

}