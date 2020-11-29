document.addEventListener("DOMContentLoaded", () => {
    // UPDATE ALBUMS 
    const updateAlbumID = document.querySelector("#album-id");
    const updateAlbumName = document.querySelector("#album-name");
    const searchAlbumForm = document.querySelector("#search-album");
    const albumName = document.querySelector("#update-album-name");
    const artistName = document.querySelector("#update-artist-name")
    const albumID = document.querySelector("#album-id");
    const albumPrice = document.querySelector("#price");
    const albumError = document.querySelector("#album-error");
    const albumGenre = document.querySelector("#update-album-genre");
    const albumYear = document.querySelector("#year");
    const CopiesInStock = document.querySelector("#copies");

    searchAlbumForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const headers = new Headers();
        headers.append("Content-Type", "application/json");
        const body = JSON.stringify({ albumID: updateAlbumID.value, albumName: updateAlbumName.value });
        console.log(body);
        const request = await fetch("/api/getAlbumDetails", {method: "POST", headers, body });
        const data = await request.json();
        if (data.length > 0) {
            const albumData = data[0]
            albumError.textContent = "";
            albumName.value = albumData[1];
            artistName.value = albumData[4];
            albumPrice.value = albumData[2];
            albumGenre.value = albumData[3];
            albumID.value = albumData[0];
            albumYear.value = albumData[5];
            CopiesInStock.value = albumData[6];
        } else {
            albumError.textContent = "album not found!"
        }
    });

    // update album 
    const updateAlbumForm = document.querySelector("#update-album");
    updateAlbumForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const body = JSON.stringify({
            albumID: albumID.value, 
            albumName: albumName.value,
            price: albumPrice.value,
            artistID: artistName.value,
            genreID: albumGenre.value,
            CopiesInStock: CopiesInStock.value, 
            ReleasedYear: albumYear.value
        })
        const headers = new Headers();
        headers.append("Content-Type", "application/json");
        const request = await fetch("/api/updateAlbum", { body, headers, method: "POST" });
        const data = await request.json();
        if (data.status === "fail") {
            alert("there was an error updating your form!");
        } else {
            alert("album updated!");
            updateAlbumForm.reset();
        }
    });

});