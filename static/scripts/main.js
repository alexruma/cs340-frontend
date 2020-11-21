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

    const createAlbumImage = (albumName) => {
      const div = document.createElement("div");
      div.setAttribute("style", "height: 250px");
      div.classList = ["column", "is-one-fifth", "has-text-centered", "is-vcentered"]
      const img = document.createElement("img");
      img.className = "mt-6";
      img.setAttribute("src", `static/images/${albumName}.jpg`)
      const p = document.createElement("p");
      p.textContent = albumName;
      div.appendChild(img);
      div.appendChild(p);
      return div 
    }

    const updateAlbums = async (id) => {
      try {
        const body = JSON.stringify({ id });
        const headers = new Headers();
        headers.append("Content-Type", "application/json");
        const response = await fetch("/api/albumsByGenre", { method: "POST", body, headers })
        const data = await response.json();
        
        const nodes = data.map(album => createAlbumImage(album[1]));
        
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
    
    for (let link of genreLinks) {
        const id = link.getAttribute("data-id");
        link.addEventListener("click", () => updateAlbums(id));
    }


  });

