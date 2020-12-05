document.addEventListener("DOMContentLoaded", () => {
    const addToCart = document.querySelector("button");
    addToCart.addEventListener("click", () => {
        // get album data from button 
        const { albumName, albumPrice, albumId } = addToCart.dataset;
        // get current cart info from local storage or create cart if necessary 
        const cartData = localStorage.getItem("cart")
        const cart = cartData ? JSON.parse(cartData) : [];

        // add new item to the cart 
        cart.push({albumName, albumPrice, albumId})
        localStorage.setItem("cart", JSON.stringify(cart));

        // navigate to cart page after 
        window.location.href = "/cart";

    });
});