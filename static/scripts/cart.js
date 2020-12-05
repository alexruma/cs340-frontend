document.addEventListener('DOMContentLoaded', () => {
    const cart = localStorage.getItem("cart");
    const emptyCart = document.querySelector("h2");
    const container = document.querySelector("#container");
    let total = 0;
    const remove = id => {
        const newCart = JSON.parse(cart).filter(item => item.albumId != id);
        localStorage.setItem("cart", JSON.stringify(newCart));
        window.location.reload();
    }

    if (!cart) {
        emptyCart.className = "";
    } else {
        const cartContents = JSON.parse(cart);
        const ul = document.querySelector("#albums-container");
        for (let item of cartContents) {
            const li = document.createElement("div");
            li.style = "width: 250px;";
            li.className = "is-flex is-flex-direction-row";
            
            const name = document.createElement("span")
            name.className = "cart-item is-one third is-capitalized"
            name.textContent = item.albumName;
            li.appendChild(name);

            const price = document.createElement("span");
            price.className = "cart-item is-one third"
            price.textContent = item.albumPrice;
            total += parseInt(item.albumPrice);
            li.appendChild(name);

            const removeButton = document.createElement("button");
            removeButton.className = "button remove-button is-one third";
            removeButton.innerText = "delete"
            removeButton.style = "margin-left: auto;"
            removeButton.addEventListener("click", () => {
                remove(item.albumId);
            });
            li.appendChild(removeButton);

            ul.appendChild(li);
        }
        if (cartContents.length > 0) {
            // convert total to currency 
            total /= 100
            total.toFixed(2);

            const totalPrice = document.createElement("p");
            totalPrice.textContent = "$" + total; 
            container.appendChild(totalPrice);
    
            const buyButton = document.createElement("button");
            buyButton.textContent = "Buy";
            buyButton.className = "button buy-btn";
            container.appendChild(buyButton);

            buyButton.addEventListener("click", async () => {
                const albums = JSON.parse(cart).map(album => album.albumId)
                try {
                    // send request to api 
                    const body = JSON.stringify({albums});
                    const headers = new Headers();
                    headers.append("Content-Type", "application/json");
                    const request = await fetch("/api/createOrder", { method: "POST", headers, body });
                    const data = await request.json();

                    // if the user isnt logged in send them to login
                    if (data.status === "fail") {
                        window.location.href = "/login";
                    
                    // if the order is placed, clear the cart, let the user know the order was placed, refresh page 
                    } else {
                        alert("order placed!");
                        localStorage.setItem("cart", JSON.stringify([]));
                        window.location.reload();
                    }
                } catch (e) {
                    console.error("error occurred!", e);
                }
            });
        }
    }
})