document.addEventListener("DOMContentLoaded", () => {
    const button = document.querySelector("#surprise");
    const msg = document.querySelector("#message");

    if (button) {
        button.addEventListener("click", () => {
            msg.textContent = "Thanks for visiting my homepage!";
        });
    }
});
