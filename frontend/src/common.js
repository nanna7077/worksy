export function secondsToTime(secs){
    let hours = Math.floor(secs / (60 * 60));

    let minutes = Math.floor((secs % (60 * 60)) / 60);

    let seconds = Math.floor(secs % 60);

    // Return component only when non zero
    if (hours > 0) {
        return `${hours} hours ${minutes} minutes ${seconds} seconds`;
    } else if (minutes > 0) {
        return `${minutes} minutes ${seconds} seconds`;
    } else {
        return `${seconds} seconds`;
    }
}