document.addEventListener('DOMContentLoaded', () => {

    // Get all "navbar-burger" elements
    const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);
  
    // Check if there are any navbar burgers
    if ($navbarBurgers.length > 0) {
  
      // Add a click event on each of them
      $navbarBurgers.forEach( el => {
        el.addEventListener('click', () => {
  
          // Get the target from the "data-target" attribute
          const target = el.dataset.target;
          const $target = document.getElementById(target);
  
          // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
          el.classList.toggle('is-active');
          $target.classList.toggle('is-active');
  
        });
      });
    }
  
    // CHANGE ALBUMS BY GENRE 

    const genreLinks = document.querySelectorAll(".genre-link");
    const albumsContainer = document.querySelector("#albums");

    const createAlbumImage = (albumName, albumID) => {
      // return a node <div><img><p></div>
      // put album img src into image and title into p

      const link = document.createElement("a");
      link.href = `/album/${albumID}`
      const div = document.createElement("div");
      link.appendChild(div)
      div.id = "album-thumbnail";
      div.className = "column is-one-fifth has-text-centered is-vcentered";
      const img = document.createElement("img");
      img.className = "mt-1";
      img.setAttribute("src", `static/images/${albumName}.jpg`)
      const p = document.createElement("p");
      p.textContent = albumName;
      div.appendChild(img);
      div.appendChild(p);
      return link
    }

    const updateAlbums = async (search, api) => {
      try {
        const body = JSON.stringify({ search });
        const headers = new Headers();
        headers.append("Content-Type", "application/json");
        const response = await fetch(api, { method: "POST", body, headers })
        const data = await response.json();
        
        const nodes = data.map(album => createAlbumImage(album[1], album[0]));
        
        // remove old albums 
        while (albumsContainer.firstChild) {
          albumsContainer.removeChild(albumsContainer.firstChild);
        }
        
        // add new albums 
        nodes.forEach(album => {
          albumsContainer.appendChild(album)
        });

      } catch (err) {
        console.error("an error occurred ", err);
      }
    }
  
    // add click handlers to each link 
    for (let link of genreLinks) {
        const id = link.getAttribute("data-id");
        link.addEventListener("click", () => updateAlbums(id, "/api/albumsByGenre"));
    }

    // SEARCH ALBUMS 

    const searchBar = document.querySelector("#search");
    const searchText = document.querySelector("#searchText");

    searchBar.addEventListener("submit", (e) => {
      const apiURL = "/api/albumsSearch";
      e.preventDefault();
      updateAlbums(searchText.value, apiURL);
    });


  });

