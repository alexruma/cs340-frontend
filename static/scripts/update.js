document.addEventListener("DOMContentLoaded", () => {
    // UPDATE ALBUMS 
    const updateAlbumID = document.querySelector("#album-id");
    const updateAlbumName = document.querySelector("#album-id");
    const searchAlbumForm = document.querySelector("#search-album");

    searchAlbumForm.addEventListener("submit", (e) => {
        e.preventDefault();
        console.log("submitted");
    })

});