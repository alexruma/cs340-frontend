

function createValues(id) {
    // returns an array of tuples to easily add tracks for albums 
    const trackList = document.querySelector(".tracklist");
    const tBody = trackList.children[1];
    const tracks = tBody.children;
    let values = [];
    console.log(tracks);
    for (let i = 1; i < tracks.length - 1; i++) {
        if (tracks[i].children[4]) {
             const time = tracks[i].children[4].innerText;
            const timeSplit = time.split(":");
            const timeToSeconds = parseInt(timeSplit[0]) * 60 + parseInt(timeSplit[1]);
            let entry =`(${tracks[i].children[1].textContent.split("(")[0]}, ${timeToSeconds}, ${id})`
            values.push(entry);   
        }
    }
    
    return values.join(",");
 }